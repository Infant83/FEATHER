from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator

_OFF_TOKENS = {"", "0", "false", "off", "none", "disable", "disabled"}
_DEFAULT_MODEL_FALLBACK = "gpt-4o-mini"
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


def _resolve_model_hint(model: str | None, backend: str) -> str:
    explicit = str(model or "").strip()
    if explicit:
        return explicit
    if backend == "codex_cli":
        return str(os.getenv("CODEX_MODEL") or "").strip()
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


@dataclass
class _MemorySnapshotTool:
    name: str
    description: str
    snapshot: dict[str, Any]

    def invoke(self, payload: Any = None) -> dict[str, Any]:
        _ = payload
        return dict(self.snapshot)

    def __call__(self, payload: Any = None) -> dict[str, Any]:
        return self.invoke(payload)


@dataclass
class _RunArtifactIndexTool:
    name: str
    description: str
    snapshot: dict[str, Any]

    def invoke(self, payload: Any = None) -> dict[str, Any]:
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

    def __call__(self, payload: Any = None) -> dict[str, Any]:
        return self.invoke(payload)


@dataclass
class _RunFileReadTool:
    name: str
    description: str
    root: Path | None
    run_rel: str

    def _resolve_candidate(self, payload: Any) -> Path | None:
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

    def invoke(self, payload: Any = None) -> dict[str, Any]:
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

    def __call__(self, payload: Any = None) -> dict[str, Any]:
        return self.invoke(payload)


@dataclass
class _SourceDigestTool:
    name: str
    description: str
    sources: list[dict[str, Any]]

    def invoke(self, payload: Any = None) -> dict[str, Any]:
        _ = payload
        rows: list[dict[str, Any]] = []
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

    def __call__(self, payload: Any = None) -> dict[str, Any]:
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
        "instruction_confirm_reason,run_name_hint,topic_hint,stage,target,mode,allow_artifacts,capability_id}\n"
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
        result = agent.invoke({"messages": messages, "question": question})
        if isinstance(result, dict):
            action_obj = result.get("action")
            if isinstance(action_obj, dict):
                return action_obj
        answer_text = _extract_assistant_text(result)
        return _extract_first_json_object(answer_text)
    except Exception:
        if mode == "deepagent":
            raise
        return None
