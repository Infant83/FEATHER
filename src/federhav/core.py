from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from federnett.filesystem import read_help_history, write_help_history
from federnett.help_agent import answer_help_question, stream_help_question
from federnett.utils import resolve_under_root, safe_rel

_HISTORY_SUMMARY_PREFIX = "[context-compress]"
_HISTORY_MAX_ITEM_CHARS = 1400
_HISTORY_SUMMARY_SAMPLE_TURNS = 24
_HISTORY_SUMMARY_MAX_CHARS = 2000


@dataclass(frozen=True)
class FederHavChatConfig:
    root: Path
    run_rel: str | None = None
    profile_id: str = "default"
    agent: str = "federhav"
    execution_mode: str = "plan"
    allow_artifacts: bool = False
    model: str | None = None
    llm_backend: str | None = None
    reasoning_effort: str | None = None
    runtime_mode: str | None = "auto"
    strict_model: bool = False
    max_sources: int = 8
    web_search: bool = False
    live_log_tail: str | None = None
    history_turns: int = 14


def normalize_run_relpath(root: Path, run: str | None, *, run_roots: list[str] | None = None) -> str | None:
    token = str(run or "").strip()
    if not token:
        return None
    resolved = resolve_under_root(root, token)
    if resolved and resolved.exists() and resolved.is_dir():
        return safe_rel(resolved, root)
    if "/" in token or "\\" in token:
        return token.replace("\\", "/")
    roots = run_roots or ["site/runs", "runs", "examples/runs"]
    for rel_root in roots:
        candidate = (root / rel_root / token).resolve()
        if candidate.exists() and candidate.is_dir():
            return safe_rel(candidate, root)
    return token


def _normalize_profile_id(value: str | None) -> str:
    raw = str(value or "").strip()
    if not raw:
        return "default"
    cleaned = "".join(ch for ch in raw if ch.isalnum() or ch in {"_", "-"})
    return cleaned[:80] or "default"


def _normalize_agent_id(value: str | None) -> str:
    raw = str(value or "").strip()
    if not raw:
        return "federhav"
    cleaned = "".join(ch for ch in raw if ch.isalnum() or ch in {"_", "-", "."})
    return cleaned[:80] or "federhav"


def _normalize_execution_mode(value: str | None) -> str:
    token = str(value or "").strip().lower()
    if token in {"act", "execute", "run"}:
        return "act"
    return "plan"


def _compact_history_snippet(text: str, limit: int = 180) -> str:
    normalized = " ".join(str(text or "").replace("\r", "\n").split()).strip()
    if not normalized:
        return ""
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[: max(1, limit - 1)].rstrip()}…"


def _compact_history(items: list[dict[str, Any]], turns: int) -> list[dict[str, str]]:
    max_items = max(2, turns * 2)
    window = max(max_items * 4, 80)
    compacted: list[dict[str, str]] = []
    for row in items[-window:]:
        role = str(row.get("role") or "").strip().lower()
        if role not in {"user", "assistant"}:
            continue
        content = str(row.get("content") or "").strip()
        if not content:
            continue
        compacted.append({"role": role, "content": content[:_HISTORY_MAX_ITEM_CHARS]})
    if not compacted:
        return []
    compacted = [
        row
        for row in compacted
        if not (
            row.get("role") == "assistant"
            and str(row.get("content") or "").strip().lower().startswith(_HISTORY_SUMMARY_PREFIX)
        )
    ]
    if not compacted:
        return []
    recent = compacted[-max_items:]
    older = compacted[:-max_items]
    if not older:
        return recent
    sampled = older[-_HISTORY_SUMMARY_SAMPLE_TURNS:]
    lines = []
    for row in sampled:
        role_label = "FederHav" if row.get("role") == "assistant" else "User"
        snippet = _compact_history_snippet(str(row.get("content") or ""))
        if not snippet:
            continue
        lines.append(f"- {role_label}: {snippet}")
    if not lines:
        return recent
    summary = "\n".join(
        [
            f"{_HISTORY_SUMMARY_PREFIX} 이전 대화 {len(older)}개를 요약했습니다.",
            *lines,
        ],
    )
    if len(summary) > _HISTORY_SUMMARY_MAX_CHARS:
        summary = f"{summary[: max(1, _HISTORY_SUMMARY_MAX_CHARS - 1)].rstrip()}…"
    return [{"role": "assistant", "content": summary}, *recent]


def _history_items(root: Path, run_rel: str | None, profile_id: str) -> list[dict[str, Any]]:
    payload = read_help_history(root, run_rel, profile_id=profile_id)
    rows = payload.get("items")
    if not isinstance(rows, list):
        return []
    out: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        role = str(row.get("role") or "").strip().lower()
        content = str(row.get("content") or "").strip()
        if role not in {"user", "assistant"} or not content:
            continue
        ts = str(row.get("ts") or "")
        out.append({"role": role, "content": content, "ts": ts})
    return out


def load_chat_history(
    root: Path,
    run_rel: str | None,
    *,
    profile_id: str | None = None,
    turns: int = 14,
) -> list[dict[str, str]]:
    pid = _normalize_profile_id(profile_id)
    items = _history_items(root, run_rel, pid)
    return _compact_history(items, turns)


def append_chat_history(
    root: Path,
    run_rel: str | None,
    *,
    profile_id: str | None,
    question: str,
    answer: str,
) -> dict[str, Any]:
    pid = _normalize_profile_id(profile_id)
    existing = _history_items(root, run_rel, pid)
    now = datetime.now(timezone.utc).isoformat()
    q = str(question or "").strip()
    a = str(answer or "").strip()
    if q:
        existing.append({"role": "user", "content": q, "ts": now})
    if a:
        existing.append({"role": "assistant", "content": a, "ts": now})
    return write_help_history(root, run_rel, existing, profile_id=pid)


def ask_question(config: FederHavChatConfig, question: str) -> dict[str, Any]:
    q = str(question or "").strip()
    if not q:
        raise ValueError("question is required")
    root = config.root.resolve()
    run_rel = normalize_run_relpath(root, config.run_rel)
    pid = _normalize_profile_id(config.profile_id)
    agent_id = _normalize_agent_id(config.agent)
    execution_mode = _normalize_execution_mode(config.execution_mode)
    history = load_chat_history(root, run_rel, profile_id=pid, turns=config.history_turns)
    result = answer_help_question(
        root,
        q,
        agent=agent_id,
        execution_mode=execution_mode,
        allow_artifacts=bool(config.allow_artifacts),
        model=config.model,
        llm_backend=config.llm_backend,
        reasoning_effort=config.reasoning_effort,
        runtime_mode=config.runtime_mode,
        strict_model=bool(config.strict_model),
        max_sources=max(3, min(int(config.max_sources), 16)),
        history=history,
        run_rel=run_rel,
        web_search=bool(config.web_search),
        live_log_tail=config.live_log_tail,
    )
    answer = str(result.get("answer") or "").strip()
    if answer:
        append_chat_history(root, run_rel, profile_id=pid, question=q, answer=answer)
    return {
        **result,
        "run_rel": run_rel or "",
        "profile_id": pid,
        "agent": agent_id,
        "execution_mode": execution_mode,
    }


def stream_question(config: FederHavChatConfig, question: str) -> Iterator[dict[str, Any]]:
    q = str(question or "").strip()
    if not q:
        raise ValueError("question is required")
    root = config.root.resolve()
    run_rel = normalize_run_relpath(root, config.run_rel)
    pid = _normalize_profile_id(config.profile_id)
    agent_id = _normalize_agent_id(config.agent)
    execution_mode = _normalize_execution_mode(config.execution_mode)
    history = load_chat_history(root, run_rel, profile_id=pid, turns=config.history_turns)
    answer_parts: list[str] = []
    for event in stream_help_question(
        root,
        q,
        agent=agent_id,
        execution_mode=execution_mode,
        allow_artifacts=bool(config.allow_artifacts),
        model=config.model,
        llm_backend=config.llm_backend,
        reasoning_effort=config.reasoning_effort,
        runtime_mode=config.runtime_mode,
        strict_model=bool(config.strict_model),
        max_sources=max(3, min(int(config.max_sources), 16)),
        history=history,
        run_rel=run_rel,
        web_search=bool(config.web_search),
        live_log_tail=config.live_log_tail,
    ):
        name = str(event.get("event") or "").strip().lower()
        if name == "delta":
            chunk = str(event.get("text") or "")
            if chunk:
                answer_parts.append(chunk)
        if name == "done":
            answer = "".join(answer_parts).strip() or str(event.get("answer") or "").strip()
            if answer:
                append_chat_history(root, run_rel, profile_id=pid, question=q, answer=answer)
            yield {
                **event,
                "run_rel": run_rel or "",
                "profile_id": pid,
                "agent": agent_id,
                "execution_mode": execution_mode,
            }
            continue
        yield event
