from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator
from urllib.parse import urlparse

_OFF_TOKENS = {"", "0", "false", "off", "none", "disable", "disabled"}
_DEFAULT_MODEL_FALLBACK = "gpt-4o-mini"
_ONPREM_FEDERHAV_MODEL_FALLBACK = "Qwen3-235B-A22B-Thinking-2507"
_STATE_MEMORY_MAX_CHARS = 5200
_RUN_FILE_MAX_CHARS = 3200
_RUN_FILE_MAX_BYTES = 180_000
_ACTION_ALLOWED_TYPES = (
    "none",
    "run_feather",
    "run_federlicht",
    "run_feather_then_federlicht",
    "create_run_folder",
    "switch_run",
    "preset_resume_stage",
    "focus_editor",
    "set_action_mode",
    "run_capability",
)
_ACTION_ALLOWED_SET = set(_ACTION_ALLOWED_TYPES)
_GOVERNOR_MAX_ITER_DEFAULT = 2
_GOVERNOR_MAX_ITER_MAX = 4
_GOVERNOR_DELTA_DEFAULT = 0.12
_GOVERNOR_BUDGET_CHARS_DEFAULT = 20_000
_GOVERNOR_BUDGET_CHARS_MIN = 4_000
_GOVERNOR_BUDGET_CHARS_MAX = 60_000


def normalize_runtime_mode(value: Any) -> str:
    token = str(value or "").strip().lower()
    if token in _OFF_TOKENS:
        return "off"
    if token in {"deepagent", "agentic", "on", "1", "true"}:
        return "deepagent"
    return "auto"


def federhav_runtime_mode() -> str:
    return normalize_runtime_mode(
        os.getenv("FEDERHAV_AGENTIC_RUNTIME")
        or os.getenv("FEDERHAV_RUNTIME_MODE")
        or "auto"
    )


def runtime_enabled(mode: str | None = None) -> bool:
    return normalize_runtime_mode(mode or federhav_runtime_mode()) != "off"


def _resolve_backend(value: str | None) -> str:
    token = str(value or "").strip().lower()
    if token in {"codex_cli", "codex-cli", "codex", "cli"}:
        return "codex_cli"
    return "openai_api"


def _is_onprem_openai_compatible() -> bool:
    raw = str(os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE") or "").strip()
    if not raw:
        return False
    parsed = urlparse(raw if "://" in raw else f"https://{raw}")
    host = parsed.netloc.lower()
    if not host:
        return False
    return host != "api.openai.com"


def _resolve_model_hint(model: str | None, backend: str) -> str:
    explicit = str(model or "").strip()
    if explicit:
        return explicit
    if backend == "codex_cli":
        return str(os.getenv("CODEX_MODEL") or "").strip()
    federhav_model = str(os.getenv("FEDERHAV_MODEL") or "").strip()
    if federhav_model:
        return federhav_model
    if _is_onprem_openai_compatible():
        return _ONPREM_FEDERHAV_MODEL_FALLBACK
    return str(os.getenv("OPENAI_MODEL") or _DEFAULT_MODEL_FALLBACK).strip()


def _extract_assistant_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload.strip()
    if not isinstance(payload, dict):
        return str(payload or "").strip()
    messages = payload.get("messages")
    if isinstance(messages, list):
        for row in reversed(messages):
            if not isinstance(row, dict):
                continue
            role = str(row.get("role") or row.get("type") or "").strip().lower()
            if role not in {"assistant", "ai"}:
                continue
            content = row.get("content")
            if isinstance(content, list):
                parts: list[str] = []
                for part in content:
                    if isinstance(part, str):
                        parts.append(part)
                    elif isinstance(part, dict):
                        token = str(
                            part.get("text")
                            or part.get("content")
                            or part.get("output_text")
                            or ""
                        ).strip()
                        if token:
                            parts.append(token)
                merged = "\n".join(p for p in parts if p).strip()
                if merged:
                    return merged
            token = str(content or "").strip()
            if token:
                return token
    for key in ("answer", "output_text", "text", "content"):
        token = str(payload.get(key) or "").strip()
        if token:
            return token
    return ""


def _iter_chunks(text: str, target_chars: int = 42) -> Iterator[str]:
    cleaned = str(text or "")
    if not cleaned:
        return
    carry = ""
    for raw_line in cleaned.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = f"{carry}{raw_line}" if carry else raw_line
        carry = ""
        while len(line) > target_chars:
            cut = line.rfind(" ", 0, target_chars)
            if cut <= 0:
                cut = target_chars
            chunk = line[:cut]
            if chunk:
                yield chunk
            line = line[cut:].lstrip()
        if line:
            yield f"{line}\n"
    if carry:
        yield carry


def _extract_first_json_object(raw: str) -> dict[str, Any] | None:
    text = str(raw or "")
    if not text:
        return None
    start = text.find("{")
    while start >= 0:
        depth = 0
        in_string = False
        escaped = False
        for idx in range(start, len(text)):
            ch = text[idx]
            if in_string:
                if escaped:
                    escaped = False
                    continue
                if ch == "\\":
                    escaped = True
                    continue
                if ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
                continue
            if ch == "{":
                depth += 1
                continue
            if ch == "}":
                depth -= 1
                if depth == 0:
                    snippet = text[start : idx + 1]
                    try:
                        payload = json.loads(snippet)
                    except Exception:
                        break
                    if isinstance(payload, dict):
                        return payload
                    break
        start = text.find("{", start + 1)
    return None


def _safe_int(value: object, default: int, minimum: int, maximum: int) -> int:
    try:
        parsed = int(str(value).strip())
    except Exception:
        parsed = int(default)
    return max(minimum, min(maximum, parsed))


def _safe_float(value: object, default: float, minimum: float, maximum: float) -> float:
    try:
        parsed = float(str(value).strip())
    except Exception:
        parsed = float(default)
    return max(minimum, min(maximum, parsed))


def _governor_loop_policy() -> dict[str, float | int]:
    max_iter = _safe_int(
        os.getenv("FEDERHAV_GOVERNOR_MAX_ITER"),
        _GOVERNOR_MAX_ITER_DEFAULT,
        1,
        _GOVERNOR_MAX_ITER_MAX,
    )
    delta_threshold = _safe_float(
        os.getenv("FEDERHAV_GOVERNOR_DELTA_THRESHOLD"),
        _GOVERNOR_DELTA_DEFAULT,
        0.01,
        0.5,
    )
    budget_chars = _safe_int(
        os.getenv("FEDERHAV_GOVERNOR_BUDGET_CHARS"),
        _GOVERNOR_BUDGET_CHARS_DEFAULT,
        _GOVERNOR_BUDGET_CHARS_MIN,
        _GOVERNOR_BUDGET_CHARS_MAX,
    )
    return {
        "max_iter": int(max_iter),
        "delta_threshold": float(delta_threshold),
        "budget_chars": int(budget_chars),
    }


def _attempt_budget_chars(
    *,
    base_budget_chars: int,
    attempt: int,
    max_iter: int,
    execution_mode: str,
    allow_artifacts: bool,
) -> int:
    safe_base = max(_GOVERNOR_BUDGET_CHARS_MIN, int(base_budget_chars))
    mode = str(execution_mode or "plan").strip().lower()
    mode_factor = 1.0 if mode == "plan" else (0.88 if allow_artifacts else 0.94)
    decay_step = 0.16
    decay = 1.0 - (max(1, int(attempt)) - 1) * decay_step
    if max_iter <= 1:
        decay = 1.0
    decay = max(0.55, min(1.0, decay))
    budget = int(round(safe_base * mode_factor * decay))
    budget = max(_GOVERNOR_BUDGET_CHARS_MIN, min(safe_base, budget))
    return budget


def _action_signature(payload: dict[str, Any]) -> tuple[str, str, str, str, str, str]:
    return (
        str(payload.get("type") or "").strip().lower(),
        str(payload.get("stage") or "").strip().lower(),
        str(payload.get("target") or "").strip().lower(),
        str(payload.get("run_hint") or "").strip().lower(),
        str(payload.get("mode") or "").strip().lower(),
        str(payload.get("capability_id") or "").strip().lower(),
    )


def _action_score(payload: dict[str, Any]) -> float:
    confidence = _normalize_confidence(payload.get("confidence")) or 0.0
    score = confidence * 100.0
    action_type = str(payload.get("type") or "").strip().lower()
    if action_type and action_type != "none":
        score += 3.0
    handoff = payload.get("execution_handoff")
    if isinstance(handoff, dict):
        preflight = handoff.get("preflight")
        if isinstance(preflight, dict):
            if bool(preflight.get("ready_for_execute")):
                score += 14.0
            status = str(preflight.get("status") or "").strip().lower()
            if status == "ok":
                score += 8.0
            elif status == "needs_confirmation":
                score -= 2.0
            elif status in {"missing_instruction", "missing_run"}:
                score -= 6.0
    return round(score, 3)


def _trim_messages_to_budget(messages: list[dict[str, str]], budget_chars: int) -> list[dict[str, str]]:
    if budget_chars <= 0:
        return messages
    total_chars = sum(len(str(item.get("content") or "")) for item in messages if isinstance(item, dict))
    if total_chars <= budget_chars or len(messages) <= 3:
        return messages
    head = messages[:2]
    tail = messages[-4:]
    merged: list[dict[str, str]] = []
    for row in [*head, *tail]:
        if not isinstance(row, dict):
            continue
        if row not in merged:
            merged.append(row)
    trimmed_chars = sum(len(str(item.get("content") or "")) for item in merged)
    if trimmed_chars <= budget_chars:
        return merged
    if merged:
        first = dict(merged[0])
        first_content = str(first.get("content") or "")
        reserve = max(1000, budget_chars - sum(len(str(item.get("content") or "")) for item in merged[1:]))
        if len(first_content) > reserve:
            first["content"] = first_content[:reserve].rstrip() + "…"
        merged[0] = first
    return merged


def _extract_normalized_action_from_result(
    result: Any,
    *,
    root: Path | None,
    run_rel: str,
) -> dict[str, Any] | None:
    if isinstance(result, dict):
        action_obj = result.get("action")
        if isinstance(action_obj, dict):
            normalized = _normalize_action_planner_payload(action_obj, root=root, run_rel=run_rel)
            if normalized is not None:
                return normalized
        normalized = _normalize_action_planner_payload(result, root=root, run_rel=run_rel)
        if normalized is not None:
            return normalized
    answer_text = _extract_assistant_text(result)
    parsed = _extract_first_json_object(answer_text)
    return _normalize_action_planner_payload(parsed, root=root, run_rel=run_rel)


def _safe_rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


def _compact_json_payload(payload: dict[str, Any], max_chars: int = _STATE_MEMORY_MAX_CHARS) -> dict[str, Any]:
    draft = payload if isinstance(payload, dict) else {}
    try:
        if len(json.dumps(draft, ensure_ascii=False, default=str)) <= max_chars:
            return draft
    except Exception:
        pass
    compact: dict[str, Any] = {
        "schema": draft.get("schema"),
        "scope": draft.get("scope"),
        "workflow": draft.get("workflow"),
        "run": {},
        "recent_sources": [],
        "dialogue_state": [],
    }
    run = draft.get("run")
    if isinstance(run, dict):
        compact["run"] = {
            "run_rel": run.get("run_rel") or "",
            "latest_report": run.get("latest_report") or "",
            "counts": run.get("counts") or {},
            "recent_reports": list(run.get("recent_reports") or [])[:4],
            "recent_instructions": list(run.get("recent_instructions") or [])[:4],
            "recent_indexes": list(run.get("recent_indexes") or [])[:4],
        }
    recent_sources = draft.get("recent_sources")
    if isinstance(recent_sources, list):
        compact["recent_sources"] = recent_sources[:6]
    dialogue_state = draft.get("dialogue_state")
    if isinstance(dialogue_state, list):
        compact["dialogue_state"] = dialogue_state[-8:]
    return compact


def _extract_run_rel(memory: dict[str, Any]) -> str:
    if not isinstance(memory, dict):
        return ""
    scope = memory.get("scope")
    if isinstance(scope, dict):
        token = str(scope.get("run_rel") or "").strip()
        if token:
            return token.replace("\\", "/").strip("/")
    run = memory.get("run")
    if isinstance(run, dict):
        token = str(run.get("run_rel") or "").strip()
        if token:
            return token.replace("\\", "/").strip("/")
    return ""


def _normalize_action_type(value: Any) -> str:
    token = str(value or "").strip().lower()
    if token in _ACTION_ALLOWED_SET:
        return token
    return ""


def _normalize_run_hint(value: Any) -> str:
    token = str(value or "").strip().replace("\\", "/").strip("/")
    if not token:
        return ""
    lowered = token.lower()
    if lowered.startswith("site/runs/"):
        token = token[len("site/runs/") :]
    elif lowered.startswith("runs/"):
        token = token[len("runs/") :]
    token = token.strip("/").split("/", 1)[0].strip()
    if not token:
        return ""
    return token[:160]


def _run_root_prefix_from_run_rel(run_rel: str) -> str:
    token = str(run_rel or "").strip().replace("\\", "/").strip("/")
    lowered = token.lower()
    if lowered.startswith("site/runs/"):
        return "site/runs"
    if lowered.startswith("runs/"):
        return "runs"
    if "/" in token:
        return token.rsplit("/", 1)[0]
    return ""


def _candidate_run_rel_paths(run_hint: str, run_rel: str) -> list[str]:
    out: list[str] = []

    def _push(raw: str) -> None:
        token = str(raw or "").strip().replace("\\", "/").strip("/")
        if not token:
            return
        if token not in out:
            out.append(token)

    normalized_run = str(run_rel or "").strip().replace("\\", "/").strip("/")
    _push(normalized_run)
    hint = _normalize_run_hint(run_hint)
    if hint:
        _push(hint)
        _push(f"runs/{hint}")
        _push(f"site/runs/{hint}")
        prefix = _run_root_prefix_from_run_rel(normalized_run)
        if prefix:
            _push(f"{prefix}/{hint}")
    return out


def _resolve_existing_run_rel(root: Path | None, run_hint: str, run_rel: str) -> tuple[str, bool]:
    if root is None:
        return "", False
    root_resolved = root.resolve()
    for candidate in _candidate_run_rel_paths(run_hint, run_rel):
        target = (root_resolved / candidate).resolve()
        try:
            target.relative_to(root_resolved)
        except Exception:
            continue
        if target.exists() and target.is_dir():
            return _safe_rel(target, root_resolved), True
    return "", False


def _collect_instruction_candidates(root: Path | None, resolved_run_rel: str) -> list[str]:
    if root is None:
        return []
    run_token = str(resolved_run_rel or "").strip().replace("\\", "/").strip("/")
    if not run_token:
        return []
    root_resolved = root.resolve()
    run_dir = (root_resolved / run_token).resolve()
    try:
        run_dir.relative_to(root_resolved)
    except Exception:
        return []
    instruction_dir = run_dir / "instruction"
    if not instruction_dir.exists() or not instruction_dir.is_dir():
        return []
    rows: list[tuple[float, str]] = []
    for pattern in ("*.txt", "*.md", "*.markdown"):
        for path in instruction_dir.glob(pattern):
            if not path.is_file():
                continue
            try:
                mtime = float(path.stat().st_mtime)
            except Exception:
                mtime = 0.0
            rows.append((mtime, _safe_rel(path, root_resolved)))
    rows.sort(key=lambda item: (-item[0], item[1]))
    out: list[str] = []
    seen: set[str] = set()
    for _mtime, rel in rows:
        if rel and rel not in seen:
            seen.add(rel)
            out.append(rel)
    return out[:8]


def _build_action_preflight(action: dict[str, Any], *, root: Path | None, run_rel: str) -> dict[str, Any]:
    action_type = _normalize_action_type(action.get("type"))
    base_run_rel = str(run_rel or action.get("run_rel") or "").strip().replace("\\", "/").strip("/")
    run_hint = _normalize_run_hint(action.get("run_hint") or action.get("run_name_hint") or "")
    create_if_missing = bool(action.get("create_if_missing"))
    auto_instruction = bool(action.get("auto_instruction"))
    require_instruction_confirm = bool(action.get("require_instruction_confirm"))

    resolved_run_rel, run_exists = _resolve_existing_run_rel(root, run_hint, base_run_rel)
    if not resolved_run_rel and base_run_rel:
        resolved_run_rel = base_run_rel
        if root is not None:
            target = (root.resolve() / resolved_run_rel).resolve()
            try:
                target.relative_to(root.resolve())
                run_exists = target.exists() and target.is_dir()
            except Exception:
                run_exists = False

    if not resolved_run_rel and run_hint:
        prefix = _run_root_prefix_from_run_rel(base_run_rel) or "runs"
        resolved_run_rel = f"{prefix}/{run_hint}".replace("//", "/").strip("/")

    run_actions = {
        "run_feather",
        "run_federlicht",
        "run_feather_then_federlicht",
        "switch_run",
        "focus_editor",
    }
    instruction_required = action_type in {"run_feather", "run_feather_then_federlicht", "focus_editor"}
    instruction_candidates = _collect_instruction_candidates(root, resolved_run_rel)
    selected_instruction = instruction_candidates[0] if instruction_candidates else ""
    instruction_available = bool(selected_instruction)

    requires_run_confirmation = bool(
        run_hint and resolved_run_rel and base_run_rel and resolved_run_rel != base_run_rel
    )
    notes: list[str] = []
    status = "ok"
    ready_for_execute = True

    if action_type in run_actions:
        if not resolved_run_rel:
            status = "missing_run"
            ready_for_execute = False
            notes.append("run target could not be resolved from run_hint/run_rel.")
        elif not run_exists and not create_if_missing:
            status = "missing_run"
            ready_for_execute = False
            notes.append("target run does not exist and create_if_missing is false.")

    if instruction_required:
        if not instruction_available and not auto_instruction:
            if status == "ok":
                status = "missing_instruction"
            ready_for_execute = False
            notes.append("no instruction file found under run/instruction.")
        if require_instruction_confirm:
            if status == "ok":
                status = "needs_confirmation"
            ready_for_execute = False
            notes.append("instruction confirmation is required before execution.")

    if action_type in {"create_run_folder", "set_action_mode", "run_capability"} and status == "ok":
        ready_for_execute = True

    return {
        "status": status,
        "ready_for_execute": bool(ready_for_execute),
        "run_rel": base_run_rel,
        "run_hint": run_hint,
        "resolved_run_rel": resolved_run_rel,
        "run_exists": bool(run_exists),
        "create_if_missing": bool(create_if_missing),
        "requires_run_confirmation": bool(requires_run_confirmation),
        "requires_instruction_confirm": bool(require_instruction_confirm),
        "instruction": {
            "required": bool(instruction_required),
            "available": bool(instruction_available),
            "selected": selected_instruction,
            "candidates": instruction_candidates,
        },
        "notes": notes[:6],
    }


def _normalize_confidence(value: Any) -> float | None:
    try:
        token = float(value)
    except Exception:
        return None
    if not math.isfinite(token):
        return None
    if token > 1.0 and token <= 100.0:
        token = token / 100.0
    token = max(0.0, min(token, 1.0))
    return round(token, 3)


def _sanitize_execution_handoff(
    raw: Any,
    *,
    action: dict[str, Any],
    root: Path | None,
    run_rel: str,
) -> dict[str, Any]:
    handoff = dict(raw) if isinstance(raw, dict) else {}
    preflight = _build_action_preflight(action, root=root, run_rel=run_rel)
    provided_preflight = handoff.get("preflight")
    if isinstance(provided_preflight, dict):
        status = str(provided_preflight.get("status") or "").strip().lower()
        if status in {"ok", "missing_run", "missing_instruction", "needs_confirmation"}:
            preflight["status"] = status
        if isinstance(provided_preflight.get("ready_for_execute"), bool):
            preflight["ready_for_execute"] = bool(provided_preflight.get("ready_for_execute"))
        provided_notes = provided_preflight.get("notes")
        if isinstance(provided_notes, list):
            notes = [str(item or "").strip() for item in provided_notes if str(item or "").strip()]
            if notes:
                preflight["notes"] = notes[:6]
    rationale = str(
        handoff.get("intent_rationale")
        or handoff.get("rationale")
        or action.get("intent_rationale")
        or action.get("rationale")
        or ""
    ).strip()
    confidence = _normalize_confidence(
        handoff.get("confidence")
        if isinstance(handoff, dict) and "confidence" in handoff
        else action.get("confidence")
    )
    intent = str(handoff.get("intent") or "").strip().lower()[:80]
    planner = str(handoff.get("planner") or "deepagent").strip().lower()[:40] or "deepagent"
    out: dict[str, Any] = {
        "planner": planner,
        "preflight": preflight,
    }
    if intent:
        out["intent"] = intent
    if rationale:
        out["intent_rationale"] = rationale[:320]
    if confidence is not None:
        out["confidence"] = confidence
    return out


def _normalize_action_planner_payload(
    raw: Any,
    *,
    root: Path | None,
    run_rel: str,
) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        return None
    action_type = _normalize_action_type(raw.get("type") or raw.get("action_type"))
    if not action_type:
        return None
    payload = dict(raw)
    payload["type"] = action_type
    run_hint = _normalize_run_hint(payload.get("run_hint") or payload.get("run_name_hint") or "")
    if run_hint:
        payload["run_hint"] = run_hint
    confidence = _normalize_confidence(payload.get("confidence"))
    if confidence is not None:
        payload["confidence"] = confidence
    else:
        payload.pop("confidence", None)
    rationale = str(payload.get("intent_rationale") or payload.get("rationale") or "").strip()
    if rationale:
        payload["intent_rationale"] = rationale[:320]
    payload["execution_handoff"] = _sanitize_execution_handoff(
        payload.get("execution_handoff"),
        action=payload,
        root=root,
        run_rel=run_rel,
    )
    payload["planner"] = "deepagent"
    return payload


def _prime_tool_metadata(tool_obj: object, fallback_name: str, description: str = "") -> None:
    raw_name = str(getattr(tool_obj, "name", "") or fallback_name).strip() or fallback_name
    safe_name = "".join(ch if (ch.isalnum() or ch == "_") else "_" for ch in raw_name) or fallback_name
    safe_desc = str(description or "").strip()
    for key, value in (
        ("__name__", safe_name),
        ("__qualname__", safe_name),
        ("__annotations__", {}),
    ):
        try:
            setattr(tool_obj, key, value)
        except Exception:
            pass
    if safe_desc:
        try:
            setattr(tool_obj, "__doc__", safe_desc)
        except Exception:
            pass


@dataclass
class _MemorySnapshotTool:
    name: str
    description: str
    snapshot: dict[str, object]

    def __post_init__(self) -> None:
        _prime_tool_metadata(self, "memory_snapshot", self.description)

    def invoke(self, payload=None):
        _ = payload
        return dict(self.snapshot)

    def __call__(self, payload=None):
        return self.invoke(payload)


@dataclass
class _RunArtifactIndexTool:
    name: str
    description: str
    snapshot: dict[str, object]

    def __post_init__(self) -> None:
        _prime_tool_metadata(self, "run_artifacts", self.description)

    def invoke(self, payload=None):
        _ = payload
        run = self.snapshot.get("run") if isinstance(self.snapshot, dict) else {}
        if not isinstance(run, dict):
            run = {}
        artifacts: list[str] = []
        for key in ("recent_reports", "recent_instructions", "recent_indexes"):
            values = run.get(key)
            if not isinstance(values, list):
                continue
            for item in values:
                token = str(item or "").strip()
                if token and token not in artifacts:
                    artifacts.append(token)
        return {
            "run_rel": str(run.get("run_rel") or ""),
            "latest_report": str(run.get("latest_report") or ""),
            "counts": run.get("counts") if isinstance(run.get("counts"), dict) else {},
            "artifacts": artifacts[:24],
        }

    def __call__(self, payload=None):
        return self.invoke(payload)


@dataclass
class _RunFileReadTool:
    name: str
    description: str
    root: Path | None
    run_rel: str

    def __post_init__(self) -> None:
        _prime_tool_metadata(self, "read_run_file", self.description)

    def _resolve_candidate(self, payload) -> Path | None:
        if self.root is None:
            return None
        root = self.root.resolve()
        raw = ""
        if isinstance(payload, dict):
            raw = str(
                payload.get("path")
                or payload.get("file")
                or payload.get("target")
                or ""
            ).strip()
        else:
            raw = str(payload or "").strip()
        raw = raw.replace("\\", "/").strip()
        if not raw:
            return None
        candidate_rel = raw
        lowered = candidate_rel.lower()
        if lowered.startswith("site/runs/"):
            candidate_rel = candidate_rel[len("site/runs/") :]
        if self.run_rel and not candidate_rel.startswith(f"{self.run_rel}/") and candidate_rel != self.run_rel:
            if candidate_rel.startswith(("report/", "report_notes/", "instruction/", "archive/", "output/", "supporting/")):
                candidate_rel = f"{self.run_rel}/{candidate_rel}"
        candidate = (root / candidate_rel).resolve()
        try:
            candidate.relative_to(root)
        except Exception:
            return None
        if self.run_rel:
            run_root = (root / self.run_rel).resolve()
            try:
                candidate.relative_to(run_root)
            except Exception:
                return None
        return candidate

    def invoke(self, payload=None):
        target = self._resolve_candidate(payload)
        if target is None:
            return {"ok": False, "error": "path must be run-scoped and under workspace root"}
        if not target.exists() or not target.is_file():
            return {
                "ok": False,
                "error": "file not found",
                "path": str(target).replace("\\", "/"),
            }
        size = 0
        try:
            size = int(target.stat().st_size)
        except Exception:
            size = 0
        try:
            data = target.read_bytes()
        except Exception as exc:
            return {
                "ok": False,
                "error": f"read failed: {exc}",
                "path": str(target).replace("\\", "/"),
            }
        if len(data) > _RUN_FILE_MAX_BYTES:
            data = data[:_RUN_FILE_MAX_BYTES]
        text = data.decode("utf-8", errors="replace")
        truncated = len(text) > _RUN_FILE_MAX_CHARS
        if truncated:
            text = text[:_RUN_FILE_MAX_CHARS].rstrip() + "…"
        root = self.root.resolve() if self.root else Path(".")
        return {
            "ok": True,
            "path": _safe_rel(target, root),
            "bytes": size,
            "truncated": truncated,
            "content": text,
        }

    def __call__(self, payload=None):
        return self.invoke(payload)


@dataclass
class _SourceDigestTool:
    name: str
    description: str
    sources: list[dict[str, object]]

    def __post_init__(self) -> None:
        _prime_tool_metadata(self, "source_digest", self.description)

    def invoke(self, payload=None):
        _ = payload
        rows: list[dict[str, object]] = []
        for item in self.sources[:10]:
            if not isinstance(item, dict):
                continue
            rows.append(
                {
                    "id": str(item.get("id") or ""),
                    "path": str(item.get("path") or ""),
                    "start_line": int(item.get("start_line") or 0),
                    "end_line": int(item.get("end_line") or 0),
                    "excerpt": str(item.get("excerpt") or "")[:280],
                }
            )
        return {"sources": rows}

    def __call__(self, payload=None):
        return self.invoke(payload)


@dataclass
class _ActionPreflightTool:
    name: str
    description: str
    root: Path | None
    run_rel: str

    def __post_init__(self) -> None:
        _prime_tool_metadata(self, "execution_preflight", self.description)

    def invoke(self, payload=None):
        action = payload if isinstance(payload, dict) else {"type": str(payload or "")}
        if "run_rel" not in action and self.run_rel:
            action = {**action, "run_rel": self.run_rel}
        return _build_action_preflight(action, root=self.root, run_rel=self.run_rel)

    def __call__(self, payload=None):
        return self.invoke(payload)


def _governor_prompt() -> str:
    return (
        "You are FederHav, the governing agent for Federnett.\n"
        "Mission:\n"
        "- Operate as an agentic governor for the network: user -> federhav -> federnett(feather/federlicht/orchestrator/tools/subagents).\n"
        "- Coordinate intent across Feather/Federlicht/Workflow controls and run artifacts.\n"
        "- Prefer state_memory and source-grounded tool outputs before generic advice.\n"
        "- When execution is requested, provide an executable next step and why.\n"
        "- Validate instruction quality before run actions (auto-draft/refine if needed).\n"
        "- Keep answers concise, operational, and UI-driven unless CLI was explicitly requested.\n"
        "- Avoid policy drift: execution_mode plan/act only controls suggested actions.\n"
        "- If the question references a concrete file/folder/path, use run-scoped tools (especially read_run_file) "
        "to inspect artifacts and answer with actual findings before proposing execution.\n"
        "- Avoid placeholder replies that only promise future work.\n"
        "- If context is insufficient, ask one concrete follow-up question."
    )


def _memory_tool_payload(state_memory: Any, sources: list[dict[str, Any]]) -> dict[str, Any]:
    normalized_sources = []
    for src in sources[:8]:
        normalized_sources.append(
            {
                "id": str(src.get("id") or ""),
                "path": str(src.get("path") or ""),
                "start_line": int(src.get("start_line") or 0),
                "end_line": int(src.get("end_line") or 0),
                "excerpt": str(src.get("excerpt") or "")[:220],
            }
        )
    if isinstance(state_memory, dict):
        memory = dict(state_memory)
    elif isinstance(state_memory, str):
        try:
            parsed = json.loads(state_memory)
        except Exception:
            parsed = {}
        memory = dict(parsed) if isinstance(parsed, dict) else {}
    else:
        memory = {}
    memory["sources_hint"] = normalized_sources
    return _compact_json_payload(memory, _STATE_MEMORY_MAX_CHARS)


def _normalize_history(history: list[dict[str, str]] | None) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in history or []:
        if not isinstance(row, dict):
            continue
        role = str(row.get("role") or "").strip().lower()
        if role not in {"user", "assistant", "system"}:
            continue
        content = str(row.get("content") or "").strip()
        if not content:
            continue
        rows.append({"role": role, "content": content[:1200]})
    return rows


def _capability_digest(capabilities: dict[str, Any] | None) -> str:
    if not isinstance(capabilities, dict):
        return "-"
    out: list[str] = []
    for key in ("tools", "skills", "packs"):
        rows = capabilities.get(key)
        if not isinstance(rows, list):
            out.append(f"{key}=-")
            continue
        ids: list[str] = []
        for item in rows:
            if not isinstance(item, dict):
                continue
            token = str(item.get("id") or "").strip()
            if token:
                ids.append(token)
        out.append(f"{key}={','.join(ids[:12]) if ids else '-'}")
    return "; ".join(out)


def _build_action_planner_messages(
    *,
    question: str,
    run_rel: str,
    history: list[dict[str, str]] | None,
    state_memory: dict[str, Any],
    capabilities: dict[str, Any] | None,
    execution_mode: str,
    allow_artifacts: bool,
) -> list[dict[str, str]]:
    history_rows = _normalize_history(history)
    history_brief = "\n".join(
        f"- {row['role']}: {row['content'][:220]}"
        for row in history_rows[-8:]
    ) or "- (none)"
    system = (
        "You are FederHav governor+executor action planner.\n"
        "Return exactly one JSON object and nothing else.\n"
        "Only choose from allowed action types.\n"
        "Prefer no-action when intent is unclear.\n"
        "Never propose destructive/unbounded actions.\n"
        f"allowed_types=[{','.join(_ACTION_ALLOWED_TYPES)}]\n"
        "schema={type,label,summary,safety,run_hint,create_if_missing,auto_instruction,require_instruction_confirm,"
        "instruction_confirm_reason,run_name_hint,topic_hint,stage,target,mode,allow_artifacts,capability_id,"
        "confidence,intent_rationale,execution_handoff}\n"
        "For run/switch actions, call execution_preflight tool first and copy result into execution_handoff.preflight.\n"
        "Set confidence in [0,1] and add intent_rationale in 1-2 concise sentences.\n"
    )
    user = (
        f"question={question}\n"
        f"run_rel={run_rel}\n"
        f"execution_mode={execution_mode}\n"
        f"allow_artifacts={str(bool(allow_artifacts)).lower()}\n"
        f"capabilities={_capability_digest(capabilities)}\n"
        f"recent_history:\n{history_brief}\n"
        "state_memory_json:\n"
        f"{json.dumps(state_memory, ensure_ascii=False)}\n"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def _load_agent_factory():
    from federlicht import report as report_mod

    create_deep_agent = report_mod.resolve_create_deep_agent(None)
    return report_mod, create_deep_agent


def try_deepagent_answer(
    *,
    question: str,
    messages: list[dict[str, str]],
    sources: list[dict[str, Any]],
    state_memory: Any,
    model: str | None,
    llm_backend: str | None,
    reasoning_effort: str | None,
    runtime_mode: str | None = None,
    root: Path | None = None,
) -> tuple[str, str] | None:
    mode = normalize_runtime_mode(runtime_mode or federhav_runtime_mode())
    if mode == "off":
        return None
    backend = _resolve_backend(llm_backend)
    model_hint = _resolve_model_hint(model, backend)
    try:
        report_mod, create_deep_agent = _load_agent_factory()
        memory_snapshot = _memory_tool_payload(state_memory, sources)
        run_rel = _extract_run_rel(memory_snapshot)
        tools: Iterable[Any] = [
            _MemorySnapshotTool(
                name="memory_snapshot",
                description="Read compact state memory and recent source hints.",
                snapshot=memory_snapshot,
            ),
            _RunArtifactIndexTool(
                name="run_artifacts",
                description="Return run-scoped artifact index (reports/instructions/index files).",
                snapshot=memory_snapshot,
            ),
            _RunFileReadTool(
                name="read_run_file",
                description="Read a run-scoped file excerpt by relative path.",
                root=root,
                run_rel=run_rel,
            ),
            _SourceDigestTool(
                name="source_digest",
                description="Return compact digest of currently indexed evidence sources.",
                sources=sources,
            ),
        ]
        agent = report_mod.create_agent_with_fallback(
            create_deep_agent,
            model_hint,
            list(tools),
            _governor_prompt(),
            backend,
            reasoning_effort=reasoning_effort,
            subagents=[
                {
                    "name": "orchestrator",
                    "description": "Govern end-to-end routing from user intent to execution.",
                },
                {
                    "name": "planner",
                    "description": "Decompose objectives into scout/plan/evidence/writer/quality steps.",
                },
                {
                    "name": "executor",
                    "description": "Map plan steps to Feather/Federlicht/UI actions with guardrails.",
                },
                {
                    "name": "scout",
                    "description": "Discover candidate sources and run scope.",
                },
                {
                    "name": "plan",
                    "description": "Draft instruction and execution plan before action.",
                },
                {
                    "name": "evidence",
                    "description": "Verify statements against source paths and run artifacts.",
                },
                {
                    "name": "writer",
                    "description": "Compose concise operator-facing summaries and output guidance.",
                },
                {
                    "name": "quality",
                    "description": "Run quality/consistency checks and identify risks before execution.",
                },
                {
                    "name": "artwork",
                    "description": "Handle figure/artwork-related tasks and report visual assets when requested.",
                },
                {
                    "name": "doc_reader",
                    "description": "Read files/artifacts and ground decisions in run-scoped documents.",
                },
            ],
        )
        payload: dict[str, Any] = {"messages": messages}
        if question:
            payload["question"] = question
        result = agent.invoke(payload)
        answer = _extract_assistant_text(result)
        if not answer:
            return None
        return answer, model_hint or _DEFAULT_MODEL_FALLBACK
    except Exception:
        if mode == "deepagent":
            raise
        return None


def try_deepagent_stream(
    *,
    question: str,
    messages: list[dict[str, str]],
    sources: list[dict[str, Any]],
    state_memory: Any,
    model: str | None,
    llm_backend: str | None,
    reasoning_effort: str | None,
    runtime_mode: str | None = None,
    root: Path | None = None,
) -> tuple[Iterator[str], str] | None:
    out = try_deepagent_answer(
        question=question,
        messages=messages,
        sources=sources,
        state_memory=state_memory,
        model=model,
        llm_backend=llm_backend,
        reasoning_effort=reasoning_effort,
        runtime_mode=runtime_mode,
        root=root,
    )
    if not out:
        return None
    answer, used_model = out

    def _iter() -> Iterator[str]:
        yield from _iter_chunks(answer, target_chars=48)

    return _iter(), used_model


def try_deepagent_action_plan(
    *,
    question: str,
    run_rel: str | None,
    history: list[dict[str, str]] | None,
    state_memory: Any,
    capabilities: dict[str, Any] | None,
    execution_mode: str,
    allow_artifacts: bool,
    model: str | None,
    llm_backend: str | None,
    reasoning_effort: str | None,
    runtime_mode: str | None = None,
    root: Path | None = None,
) -> dict[str, Any] | None:
    mode = normalize_runtime_mode(runtime_mode or federhav_runtime_mode())
    if mode == "off":
        return None
    backend = _resolve_backend(llm_backend)
    model_hint = _resolve_model_hint(model, backend)
    try:
        report_mod, create_deep_agent = _load_agent_factory()
        memory_snapshot = _memory_tool_payload(state_memory, [])
        effective_run_rel = str(run_rel or "").strip().replace("\\", "/").strip("/")
        if not effective_run_rel:
            effective_run_rel = _extract_run_rel(memory_snapshot)
        tools: Iterable[Any] = [
            _MemorySnapshotTool(
                name="memory_snapshot",
                description="Read compact state memory and scope state.",
                snapshot=memory_snapshot,
            ),
            _RunArtifactIndexTool(
                name="run_artifacts",
                description="Return run-scoped artifact index summary.",
                snapshot=memory_snapshot,
            ),
            _RunFileReadTool(
                name="read_run_file",
                description="Read run-scoped file excerpt by relative path.",
                root=root,
                run_rel=effective_run_rel,
            ),
            _ActionPreflightTool(
                name="execution_preflight",
                description="Validate action run target and instruction readiness before execution.",
                root=root,
                run_rel=effective_run_rel,
            ),
        ]
        agent = report_mod.create_agent_with_fallback(
            create_deep_agent,
            model_hint,
            list(tools),
            _governor_prompt(),
            backend,
            reasoning_effort=reasoning_effort,
            subagents=[
                {
                    "name": "orchestrator",
                    "description": "Govern action routing from user intent to safe execution intent.",
                },
                {
                    "name": "executor",
                    "description": "Validate run/workflow actions with policy guardrails and return executable action JSON.",
                },
            ],
        )
        messages = _build_action_planner_messages(
            question=question,
            run_rel=effective_run_rel,
            history=history,
            state_memory=memory_snapshot,
            capabilities=capabilities,
            execution_mode=execution_mode,
            allow_artifacts=allow_artifacts,
        )
        policy = _governor_loop_policy()
        max_iter = int(policy["max_iter"])
        delta_threshold = float(policy["delta_threshold"])
        budget_chars = int(policy["budget_chars"])
        attempts: list[dict[str, Any]] = []
        candidates: list[dict[str, Any]] = []
        converged = False
        previous_candidate: dict[str, Any] | None = None
        previous_signature: tuple[str, str, str, str, str, str] | None = None
        previous_conf = 0.0
        active_messages = list(messages)

        for attempt in range(1, max_iter + 1):
            attempt_budget_chars = _attempt_budget_chars(
                base_budget_chars=budget_chars,
                attempt=attempt,
                max_iter=max_iter,
                execution_mode=execution_mode,
                allow_artifacts=bool(allow_artifacts),
            )
            invoke_messages = _trim_messages_to_budget(active_messages, attempt_budget_chars)
            result = agent.invoke({"messages": invoke_messages, "question": question})
            candidate = _extract_normalized_action_from_result(
                result,
                root=root,
                run_rel=effective_run_rel,
            )
            attempt_row: dict[str, Any] = {
                "attempt": attempt,
                "budget_chars": attempt_budget_chars,
                "message_chars": sum(len(str(item.get("content") or "")) for item in invoke_messages),
                "candidate": False,
            }
            if candidate:
                signature = _action_signature(candidate)
                confidence = _normalize_confidence(candidate.get("confidence")) or 0.0
                score = _action_score(candidate)
                attempt_row.update(
                    {
                        "candidate": True,
                        "type": candidate.get("type"),
                        "confidence": confidence,
                        "score": score,
                    }
                )
                candidates.append(candidate)
                same_signature = previous_signature is not None and signature == previous_signature
                confidence_delta = abs(confidence - previous_conf) if previous_candidate else 1.0
                preflight = candidate.get("execution_handoff", {}).get("preflight", {}) if isinstance(
                    candidate.get("execution_handoff"), dict
                ) else {}
                ready_for_execute = bool(preflight.get("ready_for_execute")) if isinstance(preflight, dict) else False
                if same_signature and confidence_delta <= delta_threshold:
                    converged = True
                    attempts.append(attempt_row)
                    break
                if ready_for_execute and confidence >= 0.92:
                    converged = True
                    attempts.append(attempt_row)
                    break
                previous_candidate = candidate
                previous_signature = signature
                previous_conf = confidence
                feedback = {
                    "attempt": attempt,
                    "candidate": {
                        "type": candidate.get("type"),
                        "run_hint": candidate.get("run_hint", ""),
                        "target": candidate.get("target", ""),
                        "stage": candidate.get("stage", ""),
                        "confidence": confidence,
                        "score": score,
                    },
                    "instruction": (
                        "Refine the action JSON. Keep schema strict, improve execution safety/preflight clarity, "
                        "and avoid changing action type unless evidence demands."
                    ),
                }
                active_messages = [
                    *invoke_messages,
                    {"role": "user", "content": json.dumps(feedback, ensure_ascii=False)},
                ]
            attempts.append(attempt_row)

        if not candidates:
            return None
        selected_index = max(range(len(candidates)), key=lambda idx: _action_score(candidates[idx]))
        selected = dict(candidates[selected_index])
        handoff = dict(selected.get("execution_handoff") or {})
        handoff["governor_loop"] = {
            "max_iter": max_iter,
            "attempts": len(attempts),
            "converged": bool(converged),
            "delta_threshold": delta_threshold,
            "budget_chars": budget_chars,
            "stage_budget_mode": "adaptive_decay",
            "attempt_budget_chars": [int(item.get("budget_chars") or 0) for item in attempts],
            "selected_candidate_index": selected_index,
            "candidates": [
                {
                    "type": str(item.get("type") or ""),
                    "confidence": _normalize_confidence(item.get("confidence")) or 0.0,
                    "score": _action_score(item),
                }
                for item in candidates
            ],
            "attempt_trace": attempts,
        }
        selected["execution_handoff"] = handoff
        selected["planner"] = "deepagent"
        return selected
    except Exception:
        if mode == "deepagent":
            raise
        return None
