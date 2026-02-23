from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .utils import resolve_under_root, safe_rel

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover - optional runtime dependency
    requests = None  # type: ignore


ALLOWED_ACTION_KINDS = {
    "none",
    "open_path",
    "open_url",
    "set_inline_prompt",
    "run_feather",
    "run_federlicht",
    "run_feather_then_federlicht",
    "mcp_ping",
}


def _registry_path(root: Path) -> Path:
    return root / "site" / "agent_profiles" / "capability_registry.json"


def _slug_id(raw: object, fallback: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9_.-]+", "_", str(raw or "").strip()).strip("_.-").lower()
    return text or fallback


def _normalize_keywords(raw: Any) -> list[str]:
    source = raw if isinstance(raw, list) else [raw]
    out: list[str] = []
    seen: set[str] = set()
    for item in source:
        for token in re.split(r"[,/\n]+", str(item or "").strip().lower()):
            cleaned = re.sub(r"\s+", " ", token).strip()
            if not cleaned:
                continue
            cleaned = cleaned[:48]
            if cleaned in seen:
                continue
            seen.add(cleaned)
            out.append(cleaned)
    return out[:16]


def _normalize_action(payload: Any, *, default_kind: str = "none", fallback_target: str = "") -> dict[str, Any]:
    source = payload if isinstance(payload, dict) else {}
    kind_raw = str(source.get("kind") or source.get("type") or default_kind or "none").strip().lower()
    kind = kind_raw if kind_raw in ALLOWED_ACTION_KINDS else "none"
    target = str(source.get("target") or fallback_target or "").strip()[:1200]
    confirm = source.get("confirm")
    return {
        "kind": kind,
        "target": target,
        "confirm": False if confirm is False else True,
    }


def _normalize_basic_entry(entry: Any, *, fallback_id: str) -> dict[str, Any]:
    payload = entry if isinstance(entry, dict) else {}
    token = _slug_id(payload.get("id"), fallback_id)
    label = str(payload.get("label") or token).strip()[:80] or token
    description = str(payload.get("description") or "").strip()[:400]
    enabled = payload.get("enabled")
    keywords = _normalize_keywords(payload.get("keywords") or payload.get("trigger_keywords") or [])
    action = _normalize_action(payload.get("action"), default_kind="none")
    return {
        "id": token,
        "label": label,
        "description": description,
        "enabled": False if enabled is False else True,
        "keywords": keywords,
        "action": action,
    }


def _normalize_mcp_entry(entry: Any, *, fallback_id: str) -> dict[str, Any]:
    payload = entry if isinstance(entry, dict) else {}
    base = _normalize_basic_entry(payload, fallback_id=fallback_id)
    endpoint = str(payload.get("endpoint") or payload.get("url") or "").strip()[:300]
    transport = str(payload.get("transport") or "http").strip().lower()
    if transport not in {"http", "sse", "stdio", "ws"}:
        transport = "http"
    base["endpoint"] = endpoint
    base["transport"] = transport
    base["action"] = _normalize_action(
        payload.get("action"),
        default_kind="mcp_ping",
        fallback_target=endpoint,
    )
    return base


def _normalize_registry(payload: Any) -> dict[str, Any]:
    raw = payload if isinstance(payload, dict) else {}
    tools_raw = raw.get("tools")
    skills_raw = raw.get("skills")
    mcp_raw = raw.get("mcp_servers")
    tools = []
    if isinstance(tools_raw, list):
        for idx, item in enumerate(tools_raw, start=1):
            tools.append(_normalize_basic_entry(item, fallback_id=f"tool_{idx}"))
    skills = []
    if isinstance(skills_raw, list):
        for idx, item in enumerate(skills_raw, start=1):
            skills.append(_normalize_basic_entry(item, fallback_id=f"skill_{idx}"))
    mcp_servers = []
    if isinstance(mcp_raw, list):
        for idx, item in enumerate(mcp_raw, start=1):
            mcp_servers.append(_normalize_mcp_entry(item, fallback_id=f"mcp_{idx}"))
    return {
        "tools": tools[:64],
        "skills": skills[:64],
        "mcp_servers": mcp_servers[:32],
    }


def load_capability_registry(root: Path) -> dict[str, Any]:
    path = _registry_path(root)
    if not path.exists():
        return {"tools": [], "skills": [], "mcp_servers": []}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"tools": [], "skills": [], "mcp_servers": []}
    return _normalize_registry(payload)


def save_capability_registry(root: Path, payload: Any) -> dict[str, Any]:
    normalized = _normalize_registry(payload)
    path = _registry_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return normalized


def _iter_custom_entries(registry: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for kind, key in (("tool", "tools"), ("skill", "skills"), ("mcp", "mcp_servers")):
        for item in registry.get(key) or []:
            if not isinstance(item, dict):
                continue
            entry = dict(item)
            entry["kind"] = kind
            out.append(entry)
    return out


def resolve_capability_entry(root: Path, capability_id: str) -> dict[str, Any] | None:
    token = _slug_id(capability_id, "")
    if not token:
        return None
    registry = load_capability_registry(root)
    for item in _iter_custom_entries(registry):
        if str(item.get("id") or "").strip().lower() == token:
            return item
    return None


def _contains_token(text: str, token: str) -> bool:
    token = token.strip().lower()
    if not token:
        return False
    if len(token) <= 2:
        return token in text.split()
    return token in text


def infer_capability_action(root: Path, question: str, *, run_rel: str | None = None) -> dict[str, Any] | None:
    query = str(question or "").strip().lower()
    if not query:
        return None
    run_like = any(token in query for token in ("실행", "run", "start", "시작", "테스트", "ping"))
    open_like = any(token in query for token in ("열어", "open", "보기", "preview", "확인"))
    prompt_like = any(token in query for token in ("prompt", "프롬프트", "inline"))
    best: tuple[float, dict[str, Any]] | None = None
    registry = load_capability_registry(root)
    for entry in _iter_custom_entries(registry):
        if entry.get("enabled") is False:
            continue
        cap_id = str(entry.get("id") or "").strip().lower()
        label = str(entry.get("label") or cap_id).strip().lower()
        action = entry.get("action") if isinstance(entry.get("action"), dict) else {}
        action_kind = str(action.get("kind") or "none").strip().lower()
        score = 0.0
        if cap_id and _contains_token(query, cap_id):
            score += 8.0
        if label and _contains_token(query, label):
            score += 4.0
        for kw in entry.get("keywords") or []:
            if _contains_token(query, str(kw)):
                score += 3.0
        if action_kind in {"mcp_ping"} and any(token in query for token in ("mcp", "연결", "connection", "health")):
            score += 3.0
        if score <= 0:
            continue
        if action_kind in {"run_feather", "run_federlicht", "run_feather_then_federlicht", "mcp_ping"} and not run_like:
            if score < 10.0:
                continue
        if action_kind == "open_path" and not (open_like or run_like):
            if score < 10.0:
                continue
        if action_kind == "set_inline_prompt" and not (prompt_like or run_like):
            if score < 10.0:
                continue
        if best is None or score > best[0]:
            best = (score, entry)
    if best is None:
        return None
    picked = best[1]
    action = picked.get("action") if isinstance(picked.get("action"), dict) else {}
    return {
        "type": "run_capability",
        "label": f"{picked.get('label') or picked.get('id')} 실행",
        "summary": picked.get("description") or "등록된 커스텀 capability 실행",
        "safety": "Capability allowlist action",
        "capability_id": picked.get("id"),
        "capability_kind": picked.get("kind"),
        "action_kind": action.get("kind") or "none",
        "run_rel": run_rel or "",
    }


def _validate_url(value: str) -> str:
    url = str(value or "").strip()
    if not re.match(r"^https?://", url, re.IGNORECASE):
        raise ValueError("URL action target must start with http:// or https://")
    return url


def execute_capability_action(
    root: Path,
    capability_id: str,
    *,
    dry_run: bool = True,
    run_rel: str | None = None,
    timeout_sec: int = 6,
) -> dict[str, Any]:
    entry = resolve_capability_entry(root, capability_id)
    if not entry:
        raise ValueError(f"capability not found: {capability_id}")
    if entry.get("enabled") is False:
        raise ValueError(f"capability disabled: {capability_id}")
    action = entry.get("action") if isinstance(entry.get("action"), dict) else {}
    action_kind = str(action.get("kind") or "none").strip().lower()
    target = str(action.get("target") or "").strip()
    result: dict[str, Any] = {
        "ok": True,
        "id": entry.get("id"),
        "label": entry.get("label"),
        "kind": entry.get("kind"),
        "action_kind": action_kind,
        "run_rel": run_rel or "",
        "dry_run": bool(dry_run),
        "description": entry.get("description") or "",
    }
    if action_kind == "none":
        result.update(
            {
                "effect": "noop",
                "message": "등록된 실행 동작이 없습니다.",
                "preview": f"Capability {entry.get('id')} has no executable action.",
            }
        )
        return result
    if action_kind == "open_path":
        resolved = resolve_under_root(root, target)
        if not resolved:
            raise ValueError("open_path target is required")
        rel = safe_rel(resolved, root)
        result.update(
            {
                "effect": "open_path",
                "path": rel,
                "preview": json.dumps({"effect": "open_path", "path": rel}, ensure_ascii=False, indent=2),
            }
        )
        return result
    if action_kind == "open_url":
        url = _validate_url(target)
        result.update(
            {
                "effect": "open_url",
                "url": url,
                "preview": json.dumps({"effect": "open_url", "url": url}, ensure_ascii=False, indent=2),
            }
        )
        return result
    if action_kind == "set_inline_prompt":
        text = target.strip()
        if not text:
            text = str(entry.get("description") or "").strip()
        text = text[:6000]
        if not text:
            raise ValueError("set_inline_prompt target is empty")
        result.update(
            {
                "effect": "set_inline_prompt",
                "prompt_text": text,
                "preview": json.dumps({"effect": "set_inline_prompt", "chars": len(text)}, ensure_ascii=False, indent=2),
            }
        )
        return result
    if action_kind in {"run_feather", "run_federlicht", "run_feather_then_federlicht"}:
        result.update(
            {
                "effect": "delegate",
                "action_type": action_kind,
                "preview": json.dumps({"effect": "delegate", "action_type": action_kind}, ensure_ascii=False, indent=2),
            }
        )
        return result
    if action_kind == "mcp_ping":
        endpoint = str(entry.get("endpoint") or target).strip()
        if not endpoint:
            raise ValueError("mcp_ping endpoint is required")
        transport = str(entry.get("transport") or "http").strip().lower()
        if transport in {"http", "sse", "ws"}:
            _validate_url(endpoint)
        if dry_run:
            result.update(
                {
                    "effect": "mcp_ping",
                    "endpoint": endpoint,
                    "transport": transport,
                    "preview": json.dumps(
                        {
                            "effect": "mcp_ping",
                            "endpoint": endpoint,
                            "transport": transport,
                        },
                        ensure_ascii=False,
                        indent=2,
                    ),
                }
            )
            return result
        if requests is None:
            raise RuntimeError("requests package is required for mcp_ping")
        try:
            resp = requests.get(endpoint, timeout=max(2, int(timeout_sec)))
            status_code = int(resp.status_code)
            ok = 200 <= status_code < 500
            result.update(
                {
                    "ok": ok,
                    "effect": "mcp_ping",
                    "endpoint": endpoint,
                    "transport": transport,
                    "http_status": status_code,
                    "message": "reachable" if ok else "unreachable",
                    "preview": json.dumps(
                        {
                            "effect": "mcp_ping",
                            "endpoint": endpoint,
                            "http_status": status_code,
                        },
                        ensure_ascii=False,
                        indent=2,
                    ),
                }
            )
            return result
        except Exception as exc:
            result.update(
                {
                    "ok": False,
                    "effect": "mcp_ping",
                    "endpoint": endpoint,
                    "transport": transport,
                    "message": str(exc),
                    "preview": json.dumps(
                        {
                            "effect": "mcp_ping",
                            "endpoint": endpoint,
                            "error": str(exc),
                        },
                        ensure_ascii=False,
                        indent=2,
                    ),
                }
            )
            return result
    raise ValueError(f"unsupported action kind: {action_kind}")


def runtime_capabilities(root: Path, *, web_search_enabled: bool) -> dict[str, Any]:
    registry = load_capability_registry(root)
    tools: list[dict[str, Any]] = [
        {
            "id": "source_index",
            "label": "Source Index",
            "description": "코드/문서/런 인덱스를 검색해 근거 후보를 선택합니다.",
            "enabled": True,
            "group": "ask",
        },
        {
            "id": "web_research",
            "label": "Web Search",
            "description": "Tavily 기반 웹 보강 검색으로 최신 근거를 보완합니다.",
            "enabled": bool(web_search_enabled),
            "group": "ask",
        },
        {
            "id": "llm_generate",
            "label": "LLM Generate",
            "description": "선별 근거를 기반으로 최종 답변을 생성합니다.",
            "enabled": True,
            "group": "ask",
        },
        {
            "id": "filesystem.list_archive_files",
            "label": "list_archive_files",
            "description": "아카이브 파일 목록 조회",
            "enabled": True,
            "group": "federlicht",
        },
        {
            "id": "filesystem.list_supporting_files",
            "label": "list_supporting_files",
            "description": "supporting 파일 목록 조회",
            "enabled": True,
            "group": "federlicht",
        },
        {
            "id": "filesystem.read_document",
            "label": "read_document",
            "description": "텍스트/PDF/PPTX/문서 청크 읽기",
            "enabled": True,
            "group": "federlicht",
        },
        {
            "id": "artwork.artwork_capabilities",
            "label": "artwork_capabilities",
            "description": "아트웍 생성 가능 항목 조회",
            "enabled": True,
            "group": "federlicht",
        },
        {
            "id": "artwork.artwork_mermaid_flowchart",
            "label": "artwork_mermaid_flowchart",
            "description": "Mermaid flowchart 생성",
            "enabled": True,
            "group": "federlicht",
        },
        {
            "id": "artwork.artwork_mermaid_timeline",
            "label": "artwork_mermaid_timeline",
            "description": "Mermaid timeline 생성",
            "enabled": True,
            "group": "federlicht",
        },
        {
            "id": "artwork.artwork_mermaid_render",
            "label": "artwork_mermaid_render",
            "description": "Mermaid 소스를 SVG/PNG/PDF 파일로 렌더링",
            "enabled": True,
            "group": "federlicht",
        },
        {
            "id": "artwork.artwork_d2_render",
            "label": "artwork_d2_render",
            "description": "D2 소스에서 SVG 렌더링",
            "enabled": True,
            "group": "federlicht",
        },
        {
            "id": "artwork.artwork_diagrams_render",
            "label": "artwork_diagrams_render",
            "description": "Python diagrams 노드/엣지로 SVG 아키텍처 다이어그램 렌더링",
            "enabled": True,
            "group": "federlicht",
        },
        {
            "id": "deepagents.subagent_router",
            "label": "Subagent Router",
            "description": "create_deep_agent의 subagent 라우팅 경로",
            "enabled": True,
            "group": "deepagents",
        },
        {
            "id": "deepagents.tool_executor",
            "label": "Tool Executor",
            "description": "deepagents 도구 호출 실행기",
            "enabled": True,
            "group": "deepagents",
        },
    ]
    skills: list[dict[str, Any]] = [
        {
            "id": "action_runner",
            "label": "Action Runner",
            "description": "질문 문맥 기반 실행 제안/미리보기",
            "enabled": True,
            "group": "ask",
        },
        {
            "id": "citation_guard",
            "label": "Citation Guard",
            "description": "인용 형식/검증 규칙 준수 점검",
            "enabled": True,
            "group": "federlicht",
        },
        {
            "id": "context_budget_guard",
            "label": "Context Budget Guard",
            "description": "컨텍스트 길이 초과 방지/축약 경로",
            "enabled": True,
            "group": "federlicht",
        },
    ]
    mcp = []
    for idx, item in enumerate(registry.get("mcp_servers") or [], start=1):
        normalized = _normalize_mcp_entry(item, fallback_id=f"mcp_{idx}")
        normalized["group"] = "custom"
        mcp.append(normalized)
    for idx, item in enumerate(registry.get("tools") or [], start=1):
        normalized = _normalize_basic_entry(item, fallback_id=f"custom_tool_{idx}")
        normalized["group"] = "custom"
        tools.append(normalized)
    for idx, item in enumerate(registry.get("skills") or [], start=1):
        normalized = _normalize_basic_entry(item, fallback_id=f"custom_skill_{idx}")
        normalized["group"] = "custom"
        skills.append(normalized)
    packs = [
        {
            "id": "ask_core_pack",
            "label": "Ask Core Pack",
            "description": "질문/근거/답변 기본 경로",
            "items": ["source_index", "web_research", "llm_generate", "action_runner"],
        },
        {
            "id": "federlicht_runtime_pack",
            "label": "Federlicht Runtime Pack",
            "description": "Writer/Evidence/Quality 단계 내부 도구",
            "items": [
                "filesystem.list_archive_files",
                "filesystem.list_supporting_files",
                "filesystem.read_document",
                "artwork.artwork_capabilities",
                "artwork.artwork_mermaid_flowchart",
                "artwork.artwork_mermaid_timeline",
                "artwork.artwork_mermaid_render",
                "artwork.artwork_d2_render",
                "artwork.artwork_diagrams_render",
                "citation_guard",
                "context_budget_guard",
            ],
        },
        {
            "id": "deepagents_pack",
            "label": "DeepAgents Pack",
            "description": "create_deep_agent 기반 라우팅/도구 실행",
            "items": ["deepagents.subagent_router", "deepagents.tool_executor"],
        },
    ]
    return {
        "term": "Capability Packs",
        "tools": tools,
        "skills": skills,
        "mcp": mcp,
        "packs": packs,
    }
