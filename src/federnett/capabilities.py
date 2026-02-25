from __future__ import annotations

import difflib
import datetime as dt
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
    "edit_text_file",
    "rewrite_section",
    "run_feather",
    "run_federlicht",
    "run_feather_then_federlicht",
    "mcp_ping",
}

_EDIT_ALLOWED_PREFIXES = (
    "site/runs/",
    "site/report_hub/",
    "docs/",
    "site/agent_profiles/",
)
_RUN_RELATIVE_EDIT_PREFIXES = (
    "archive/",
    "instruction/",
    "report/",
    "report_notes/",
    "output/",
    "supporting/",
    "tmp/",
    "final_report/",
    "large_tool_results/",
)
_EDIT_DIFF_MAX_LINES = 180
_EDIT_DIFF_MAX_CHARS = 8000


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


def _to_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _read_text_utf8(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"edit_text_file supports utf-8 text files only: {path.name}") from exc


def _parse_edit_target_spec(target: str) -> dict[str, Any]:
    token = str(target or "").strip()
    if not token:
        return {}
    if token.startswith("{"):
        try:
            parsed = json.loads(token)
        except Exception as exc:
            raise ValueError(f"edit_text_file target JSON parse failed: {exc}") from exc
        if not isinstance(parsed, dict):
            raise ValueError("edit_text_file target JSON must be an object")
        return parsed
    return {"path": token}


def _normalize_edit_override(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return {}
    out: dict[str, Any] = {}
    nested = raw.get("edit")
    if isinstance(nested, dict):
        out.update(nested)
    for key in (
        "path",
        "mode",
        "find",
        "replace",
        "title",
        "author",
        "request_text",
        "max_replacements",
    ):
        if key in raw and raw.get(key) is not None:
            out[key] = raw.get(key)
    alias = {
        "edit_path": "path",
        "target_path": "path",
        "file_path": "path",
        "edit_mode": "mode",
        "edit_find": "find",
        "edit_replace": "replace",
        "title_text": "title",
        "author_name": "author",
        "max_replace": "max_replacements",
        "request": "request_text",
    }
    for src, dst in alias.items():
        if src in raw and raw.get(src) is not None:
            out[dst] = raw.get(src)
    return out


def _merge_edit_spec(
    target_spec: dict[str, Any],
    action_override: dict[str, Any] | None,
    request_text: str | None,
) -> dict[str, Any]:
    spec = dict(target_spec)
    override = _normalize_edit_override(action_override)
    spec.update({k: v for k, v in override.items() if v is not None})
    request = str(request_text or spec.get("request_text") or "").strip()
    if request:
        spec["request_text"] = request[:1200]
    return spec


def _is_allowed_edit_path(rel_path: str, *, run_rel: str | None = None) -> bool:
    rel = str(rel_path or "").replace("\\", "/").strip().lstrip("./")
    if not rel:
        return False
    run_token = str(run_rel or "").replace("\\", "/").strip().strip("/")
    if run_token:
        run_prefix = f"{run_token}/"
        if rel == run_token or rel.startswith(run_prefix):
            return True
    return any(rel == prefix.rstrip("/") or rel.startswith(prefix) for prefix in _EDIT_ALLOWED_PREFIXES)


def _resolve_edit_path(root: Path, raw_path: str, *, run_rel: str | None = None) -> tuple[Path, str]:
    token = str(raw_path or "").replace("\\", "/").strip()
    if not token:
        raise ValueError("edit_text_file path is required")
    run_token = str(run_rel or "").replace("\\", "/").strip().strip("/")
    # Allow concise run-relative path declarations like "report/report_full.html".
    lowered = token.lower().lstrip("./")
    if run_token and any(lowered.startswith(prefix) for prefix in _RUN_RELATIVE_EDIT_PREFIXES):
        token = f"{run_token}/{token.lstrip('./')}"
    resolved = resolve_under_root(root, token)
    if not resolved:
        raise ValueError("edit_text_file path is required")
    rel = safe_rel(resolved, root).replace("\\", "/")
    if not _is_allowed_edit_path(rel, run_rel=run_rel):
        raise ValueError(f"edit_text_file path is outside allowed scope: {rel}")
    return resolved, rel


def _infer_edit_from_request(request_text: str, source_text: str) -> dict[str, Any]:
    text = str(request_text or "").strip()
    if not text:
        return {}
    replace_pat = re.compile(
        r"""replace\s+["'“”‘’`](?P<find>.+?)["'“”‘’`]\s*(?:with|to|->|=>)\s*["'“”‘’`](?P<replace>.+?)["'“”‘’`]""",
        re.IGNORECASE | re.DOTALL,
    )
    match = replace_pat.search(text)
    if match:
        return {
            "mode": "replace_first",
            "find": match.group("find"),
            "replace": match.group("replace"),
        }
    kor_replace_pat = re.compile(
        r"""["'“”‘’`](?P<find>.+?)["'“”‘’`]\s*(?:을|를)?\s*["'“”‘’`](?P<replace>.+?)["'“”‘’`]\s*로\s*(?:바꿔|변경|수정)""",
        re.IGNORECASE | re.DOTALL,
    )
    match = kor_replace_pat.search(text)
    if match:
        return {
            "mode": "replace_first",
            "find": match.group("find"),
            "replace": match.group("replace"),
        }
    title_pat = re.compile(r"""(?:title|제목)\s*(?:을|를)?\s*["'“”‘’`](?P<title>.+?)["'“”‘’`]""", re.IGNORECASE)
    match = title_pat.search(text)
    if match and "<title" in source_text.lower():
        return {
            "mode": "replace_title_html",
            "title": match.group("title"),
        }
    author_pat = re.compile(r"""(?:author|저자|작성자)(?:\s*이름)?\s*(?:을|를)?\s*["'“”‘’`](?P<author>.+?)["'“”‘’`]""", re.IGNORECASE)
    match = author_pat.search(text)
    if match:
        return {
            "mode": "replace_author_html",
            "author": match.group("author"),
        }
    return {}


def _replace_html_title(content: str, title: str) -> tuple[str, int]:
    pattern = re.compile(r"(<title[^>]*>)(.*?)(</title>)", re.IGNORECASE | re.DOTALL)
    return pattern.subn(lambda m: f"{m.group(1)}{title}{m.group(3)}", content, count=1)


def _replace_html_author(content: str, author: str) -> tuple[str, int]:
    meta_pat = re.compile(
        r"""(<meta[^>]+(?:name|property)=["'](?:author|article:author)["'][^>]*content=["'])([^"']*)(["'][^>]*>)""",
        re.IGNORECASE | re.DOTALL,
    )
    updated, replaced = meta_pat.subn(lambda m: f"{m.group(1)}{author}{m.group(3)}", content, count=1)
    if replaced > 0:
        return updated, replaced
    byline_pat = re.compile(
        r"""(<(?:span|p|div)[^>]*class=["'][^"']*(?:author|byline)[^"']*["'][^>]*>)(.*?)(</(?:span|p|div)>)""",
        re.IGNORECASE | re.DOTALL,
    )
    return byline_pat.subn(lambda m: f"{m.group(1)}{author}{m.group(3)}", content, count=1)


def _apply_text_edit(content: str, spec: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    mode_raw = str(spec.get("mode") or "").strip().lower()
    mode = {
        "replace": "replace_first",
        "replace_one": "replace_first",
        "replace_first": "replace_first",
        "replace_all": "replace_all",
        "append": "append",
        "prepend": "prepend",
        "overwrite": "overwrite",
        "replace_title_html": "replace_title_html",
        "replace_author_html": "replace_author_html",
    }.get(mode_raw, mode_raw)
    find = str(spec.get("find") or "")
    replace = str(spec.get("replace") or "")
    if not mode:
        mode = "replace_first" if find else "overwrite"
    if not find and not replace:
        inferred = _infer_edit_from_request(str(spec.get("request_text") or ""), content)
        if inferred:
            mode = str(inferred.get("mode") or mode).strip().lower()
            find = str(inferred.get("find") or find)
            replace = str(inferred.get("replace") or replace)
            if inferred.get("title") is not None:
                spec["title"] = str(inferred.get("title"))
            if inferred.get("author") is not None:
                spec["author"] = str(inferred.get("author"))
    max_replacements = max(0, _to_int(spec.get("max_replacements"), 0))
    if mode == "replace_first":
        if not find:
            raise ValueError("edit_text_file replace_first mode requires 'find'")
        replaced = 1 if find in content else 0
        updated = content.replace(find, replace, 1)
        return updated, {"mode": mode, "replacements": replaced}
    if mode == "replace_all":
        if not find:
            raise ValueError("edit_text_file replace_all mode requires 'find'")
        total = content.count(find)
        limit = max_replacements if max_replacements > 0 else total
        updated = content.replace(find, replace, limit)
        return updated, {"mode": mode, "replacements": min(total, limit)}
    if mode == "append":
        text = replace or str(spec.get("append_text") or "")
        updated = content + text
        return updated, {"mode": mode, "replacements": 1 if text else 0}
    if mode == "prepend":
        text = replace or str(spec.get("prepend_text") or "")
        updated = text + content
        return updated, {"mode": mode, "replacements": 1 if text else 0}
    if mode == "overwrite":
        text = replace or str(spec.get("content") or "")
        updated = text
        return updated, {"mode": mode, "replacements": 1}
    if mode == "replace_title_html":
        title = str(spec.get("title") or replace).strip()
        if not title:
            raise ValueError("edit_text_file replace_title_html mode requires 'title'")
        updated, replaced = _replace_html_title(content, title)
        return updated, {"mode": mode, "replacements": replaced}
    if mode == "replace_author_html":
        author = str(spec.get("author") or replace).strip()
        if not author:
            raise ValueError("edit_text_file replace_author_html mode requires 'author'")
        updated, replaced = _replace_html_author(content, author)
        return updated, {"mode": mode, "replacements": replaced}
    raise ValueError(f"unsupported edit_text_file mode: {mode}")


def _build_diff_preview(before: str, after: str, rel_path: str) -> str:
    diff_lines = list(
        difflib.unified_diff(
            before.splitlines(),
            after.splitlines(),
            fromfile=f"a/{rel_path}",
            tofile=f"b/{rel_path}",
            n=2,
            lineterm="",
        )
    )
    if len(diff_lines) > _EDIT_DIFF_MAX_LINES:
        diff_lines = diff_lines[:_EDIT_DIFF_MAX_LINES] + ["... (diff truncated)"]
    diff_text = "\n".join(diff_lines)
    if len(diff_text) > _EDIT_DIFF_MAX_CHARS:
        diff_text = diff_text[:_EDIT_DIFF_MAX_CHARS] + "\n... (diff truncated)"
    return diff_text


def _parse_rewrite_target_spec(target: str) -> dict[str, Any]:
    token = str(target or "").strip()
    if not token:
        return {}
    if token.startswith("{"):
        try:
            parsed = json.loads(token)
        except Exception as exc:
            raise ValueError(f"rewrite_section target JSON parse failed: {exc}") from exc
        if not isinstance(parsed, dict):
            raise ValueError("rewrite_section target JSON must be an object")
        return parsed
    if "#" in token:
        path, section = token.split("#", 1)
        return {"path": path.strip(), "section": section.strip()}
    return {"path": token}


def _normalize_rewrite_override(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return {}
    out: dict[str, Any] = {}
    nested = raw.get("rewrite")
    if isinstance(nested, dict):
        out.update(nested)
    for key in (
        "path",
        "section",
        "section_title",
        "replacement",
        "content",
        "tone",
        "style",
        "length",
        "request_text",
    ):
        if key in raw and raw.get(key) is not None:
            out[key] = raw.get(key)
    alias = {
        "edit_path": "path",
        "target_path": "path",
        "file_path": "path",
        "section_name": "section",
        "section_id": "section",
        "rewrite_text": "replacement",
        "tone_hint": "tone",
        "style_hint": "style",
        "length_hint": "length",
        "request": "request_text",
    }
    for src, dst in alias.items():
        if src in raw and raw.get(src) is not None:
            out[dst] = raw.get(src)
    return out


def _merge_rewrite_spec(
    target_spec: dict[str, Any],
    action_override: dict[str, Any] | None,
    request_text: str | None,
) -> dict[str, Any]:
    spec = dict(target_spec)
    override = _normalize_rewrite_override(action_override)
    spec.update({k: v for k, v in override.items() if v is not None})
    section = str(spec.get("section") or spec.get("section_title") or "").strip()
    if section:
        spec["section"] = section[:160]
    request = str(request_text or spec.get("request_text") or "").strip()
    if request:
        spec["request_text"] = request[:1200]
    return spec


def _infer_run_rel_from_path(rel_path: str) -> str:
    token = str(rel_path or "").replace("\\", "/").strip().strip("/")
    if not token.startswith("site/runs/"):
        return ""
    parts = token.split("/")
    if len(parts) < 3:
        return ""
    return "/".join(parts[:3])


def _infer_output_format_from_path(rel_path: str) -> str:
    suffix = Path(str(rel_path or "")).suffix.lower()
    if suffix in {".html", ".htm"}:
        return "html"
    if suffix in {".tex", ".latex"}:
        return "tex"
    return "md"


def _extract_section_from_request(request_text: str) -> str:
    text = str(request_text or "").strip()
    if not text:
        return ""
    patterns = (
        r"""(?:section|섹션|단락)\s*["'“”‘’`](?P<section>.+?)["'“”‘’`]""",
        r"""["'“”‘’`](?P<section>.+?)["'“”‘’`]\s*(?:section|섹션|단락)""",
        r"""(?:section|섹션)\s+(?P<section>[A-Za-z0-9가-힣][^,\n]{1,80})""",
    )
    for pat in patterns:
        match = re.search(pat, text, flags=re.IGNORECASE | re.DOTALL)
        if not match:
            continue
        token = re.sub(r"\s+", " ", str(match.group("section") or "")).strip(" .,:;")
        if token:
            return token[:160]
    return ""


def _extract_rewrite_block_from_request(request_text: str) -> str:
    text = str(request_text or "")
    if not text:
        return ""
    triple = re.search(r"(?s)```(?:md|markdown|text|html)?\n(?P<body>.+?)\n```", text, flags=re.IGNORECASE)
    if triple:
        body = str(triple.group("body") or "").strip()
        if body:
            return body
    quoted = re.search(r'(?s)"""(?P<body>.+?)"""', text)
    if quoted:
        body = str(quoted.group("body") or "").strip()
        if body:
            return body
    return ""


def _extract_tone_hint(request_text: str) -> str:
    text = str(request_text or "").lower()
    if not text:
        return ""
    tone_tokens = {
        "냉철": "냉철하고 분석적인 톤",
        "차분": "차분하고 균형 잡힌 톤",
        "전문": "전문적이고 검증 중심의 톤",
        "공격적": "강한 주장 중심의 톤",
        "friendly": "friendly and reader-friendly tone",
        "formal": "formal and objective tone",
    }
    for token, desc in tone_tokens.items():
        if token in text:
            return desc
    match = re.search(r'(["\'“”‘’`][^"\'“”‘’`\n]{1,64}["\'“”‘’`])\s*톤', str(request_text or ""), flags=re.IGNORECASE)
    if match:
        raw = str(match.group(1) or "").strip().strip('"\'“”‘’`')
        if raw:
            return f"{raw} tone"
    return ""


def _extract_length_hint(request_text: str) -> str:
    text = str(request_text or "").lower()
    if not text:
        return ""
    if any(token in text for token in ("길게", "더 길", "expand", "longer")):
        return "expand length by roughly 30-70% while keeping substance concise."
    if any(token in text for token in ("짧게", "요약", "shorter", "condense")):
        return "condense to a shorter, sharper section."
    return ""


def _extract_style_hint(request_text: str) -> str:
    text = str(request_text or "").lower()
    if not text:
        return ""
    if any(token in text for token in ("서술형", "narrative")):
        return "narrative prose format (avoid bullet-only output)."
    if any(token in text for token in ("불릿", "bullet")):
        return "use concise bullets where appropriate."
    return ""


def _render_section_rewrite_prompt(
    *,
    report_rel: str,
    section_title: str,
    existing_section: str,
    tone_hint: str,
    style_hint: str,
    length_hint: str,
) -> str:
    excerpt = existing_section.strip()
    if len(excerpt) > 5000:
        excerpt = excerpt[:5000].rstrip() + "\n...(truncated)"
    lines = [
        "Update request:",
        f"- Base report: {report_rel}",
        f"- Target section: {section_title}",
        "- Task: rewrite the target section only, preserving factual claims and citation traceability.",
    ]
    if tone_hint:
        lines.append(f"- Tone: {tone_hint}")
    if style_hint:
        lines.append(f"- Writing style: {style_hint}")
    if length_hint:
        lines.append(f"- Length: {length_hint}")
    lines.extend(
        [
            "",
            "Constraints:",
            "- Keep the section heading unchanged.",
            "- Do not rewrite unrelated sections unless required for consistency.",
            "- Maintain claim-evidence-source alignment; preserve citations or refresh them if the claim changes.",
            "",
            "Current section excerpt:",
            "<<<",
            excerpt or "(section currently empty)",
            ">>>",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def _next_section_update_request_path(root: Path, run_rel: str, section_title: str) -> tuple[Path, str]:
    run_dir = resolve_under_root(root, run_rel)
    if not run_dir:
        raise ValueError(f"invalid run path for rewrite_section: {run_rel}")
    report_notes_dir = run_dir / "report_notes"
    stamp = dt.datetime.now().strftime("%Y%m%d")
    slug = _slug_id(section_title, "section")
    base = f"update_request_section_{slug}_{stamp}"
    candidate = report_notes_dir / f"{base}.txt"
    idx = 1
    while candidate.exists():
        candidate = report_notes_dir / f"{base}_{idx}.txt"
        idx += 1
    rel = safe_rel(candidate, root).replace("\\", "/")
    return candidate, rel


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
    query_raw = str(question or "").strip()
    query = query_raw.lower()
    if not query:
        return None
    run_like = any(token in query for token in ("실행", "run", "start", "시작", "테스트", "ping"))
    open_like = any(token in query for token in ("열어", "open", "보기", "preview", "확인"))
    prompt_like = any(token in query for token in ("prompt", "프롬프트", "inline"))
    edit_like = any(
        token in query
        for token in ("수정", "편집", "바꿔", "변경", "replace", "edit", "rewrite", "제목", "저자", "author", "title")
    )
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
        if action_kind in {"edit_text_file", "rewrite_section"} and edit_like:
            score += 2.5
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
        if action_kind in {"edit_text_file", "rewrite_section"} and not (edit_like or run_like):
            if score < 10.0:
                continue
        if best is None or score > best[0]:
            best = (score, entry)
    if best is None:
        return None
    picked = best[1]
    action = picked.get("action") if isinstance(picked.get("action"), dict) else {}
    action_payload = {
        "type": "run_capability",
        "label": f"{picked.get('label') or picked.get('id')} 실행",
        "summary": picked.get("description") or "등록된 커스텀 capability 실행",
        "safety": "Capability allowlist action",
        "capability_id": picked.get("id"),
        "capability_kind": picked.get("kind"),
        "action_kind": action.get("kind") or "none",
        "run_rel": run_rel or "",
    }
    if query_raw:
        action_payload["request_text"] = query_raw[:1200]
    return action_payload


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
    action_override: dict[str, Any] | None = None,
    request_text: str | None = None,
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
    if action_kind == "edit_text_file":
        target_spec = _parse_edit_target_spec(target)
        merged_spec = _merge_edit_spec(target_spec, action_override, request_text)
        path_token = str(merged_spec.get("path") or "").strip()
        if not path_token:
            raise ValueError("edit_text_file action requires path (target or action_override.path)")
        resolved_path, rel_path = _resolve_edit_path(root, path_token, run_rel=run_rel)
        if not resolved_path.exists():
            raise ValueError(f"edit_text_file target does not exist: {rel_path}")
        before = _read_text_utf8(resolved_path)
        after, edit_meta = _apply_text_edit(before, merged_spec)
        changed = before != after
        replacements = int(edit_meta.get("replacements") or 0)
        mode = str(edit_meta.get("mode") or merged_spec.get("mode") or "").strip().lower()
        diff_preview = _build_diff_preview(before, after, rel_path) if changed else ""
        preview_payload = {
            "effect": "edit_text_file",
            "path": rel_path,
            "mode": mode or "-",
            "changed": changed,
            "replacements": replacements,
            "chars_before": len(before),
            "chars_after": len(after),
            "diff": diff_preview,
        }
        result.update(
            {
                "effect": "edit_text_file",
                "path": rel_path,
                "mode": mode or "-",
                "changed": changed,
                "replacements": replacements,
                "chars_before": len(before),
                "chars_after": len(after),
                "diff": diff_preview,
                "preview": json.dumps(preview_payload, ensure_ascii=False, indent=2),
            }
        )
        if dry_run:
            return result
        if changed:
            resolved_path.write_text(after, encoding="utf-8")
            stat = resolved_path.stat()
            result["size"] = stat.st_size
        else:
            result["message"] = "no changes applied"
        return result
    if action_kind == "rewrite_section":
        target_spec = _parse_rewrite_target_spec(target)
        merged_spec = _merge_rewrite_spec(target_spec, action_override, request_text)
        path_token = str(merged_spec.get("path") or "").strip()
        if not path_token:
            raise ValueError("rewrite_section action requires path (target or action_override.path)")
        resolved_path, rel_path = _resolve_edit_path(root, path_token, run_rel=run_rel)
        if not resolved_path.exists():
            raise ValueError(f"rewrite_section target does not exist: {rel_path}")
        before = _read_text_utf8(resolved_path)
        section_title = str(merged_spec.get("section") or "").strip()
        if not section_title:
            section_title = _extract_section_from_request(str(merged_spec.get("request_text") or ""))
        if not section_title:
            raise ValueError("rewrite_section requires section title (target#section, action_override.section, or request text)")
        output_format = str(merged_spec.get("output_format") or "").strip().lower() or _infer_output_format_from_path(rel_path)
        if output_format not in {"md", "html", "tex"}:
            output_format = _infer_output_format_from_path(rel_path)
        from federlicht import report as feder_report  # local import avoids heavy startup for non-rewrite actions

        existing_section = feder_report.extract_named_section(before, output_format, section_title) or ""
        replacement_text = str(merged_spec.get("replacement") or merged_spec.get("content") or "").strip()
        if not replacement_text:
            replacement_text = _extract_rewrite_block_from_request(str(merged_spec.get("request_text") or ""))

        tone_hint = str(merged_spec.get("tone") or "").strip() or _extract_tone_hint(str(merged_spec.get("request_text") or ""))
        style_hint = str(merged_spec.get("style") or "").strip() or _extract_style_hint(str(merged_spec.get("request_text") or ""))
        length_hint = str(merged_spec.get("length") or "").strip() or _extract_length_hint(str(merged_spec.get("request_text") or ""))

        if replacement_text:
            after = feder_report.upsert_named_section(before, output_format, section_title, replacement_text)
            changed = before != after
            diff_preview = _build_diff_preview(before, after, rel_path) if changed else ""
            preview_payload = {
                "effect": "rewrite_section",
                "rewrite_mode": "direct_upsert",
                "path": rel_path,
                "section": section_title,
                "changed": changed,
                "chars_before": len(before),
                "chars_after": len(after),
                "diff": diff_preview,
            }
            result.update(
                {
                    "effect": "rewrite_section",
                    "rewrite_mode": "direct_upsert",
                    "path": rel_path,
                    "section": section_title,
                    "found_section": bool(existing_section),
                    "changed": changed,
                    "chars_before": len(before),
                    "chars_after": len(after),
                    "diff": diff_preview,
                    "preview": json.dumps(preview_payload, ensure_ascii=False, indent=2),
                }
            )
            if dry_run:
                return result
            if changed:
                resolved_path.write_text(after, encoding="utf-8")
                result["size"] = resolved_path.stat().st_size
            else:
                result["message"] = "no changes applied"
            return result

        run_rel_effective = str(run_rel or "").strip() or _infer_run_rel_from_path(rel_path)
        prompt_text = _render_section_rewrite_prompt(
            report_rel=rel_path,
            section_title=section_title,
            existing_section=existing_section,
            tone_hint=tone_hint,
            style_hint=style_hint,
            length_hint=length_hint,
        )
        prompt_file_rel = ""
        if run_rel_effective:
            prompt_path, prompt_file_rel = _next_section_update_request_path(root, run_rel_effective, section_title)
            if not dry_run:
                prompt_path.parent.mkdir(parents=True, exist_ok=True)
                prompt_path.write_text(prompt_text, encoding="utf-8")
        preview_payload = {
            "effect": "rewrite_section",
            "rewrite_mode": "prompt_prep",
            "path": rel_path,
            "section": section_title,
            "found_section": bool(existing_section),
            "prompt_file": prompt_file_rel,
            "prompt_preview": prompt_text[:1200],
            "suggested_action_type": "run_federlicht" if run_rel_effective else "",
        }
        result.update(
            {
                "effect": "rewrite_section",
                "rewrite_mode": "prompt_prep",
                "path": rel_path,
                "section": section_title,
                "found_section": bool(existing_section),
                "existing_chars": len(existing_section),
                "tone_hint": tone_hint,
                "style_hint": style_hint,
                "length_hint": length_hint,
                "prompt_text": prompt_text,
                "prompt_file": prompt_file_rel,
                "suggested_action_type": "run_federlicht" if run_rel_effective else "",
                "preview": json.dumps(preview_payload, ensure_ascii=False, indent=2),
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
            "id": "artwork.artwork_infographic_spec_builder",
            "label": "artwork_infographic_spec_builder",
            "description": "표 기반 claim/data를 infographic_spec JSON으로 자동 변환",
            "enabled": True,
            "group": "federlicht",
        },
        {
            "id": "artwork.artwork_infographic_claim_packet_builder",
            "label": "artwork_infographic_claim_packet_builder",
            "description": "claim_evidence_map/evidence_packet JSON에서 infographic_spec 자동 생성",
            "enabled": True,
            "group": "federlicht",
        },
        {
            "id": "artwork.artwork_infographic_html",
            "label": "artwork_infographic_html",
            "description": "Chart.js/Plotly 기반 데이터 인포그래픽 HTML 렌더링",
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
                "artwork.artwork_infographic_spec_builder",
                "artwork.artwork_infographic_claim_packet_builder",
                "artwork.artwork_infographic_html",
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
