from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Callable, Protocol
from urllib.parse import parse_qs, unquote, urlparse

from federlicht.hub_publish import publish_report_to_hub as _publish_report_to_hub

from .auth import RootAuthManager, SessionAuthManager
from .agent_profiles import delete_agent_profile, get_agent_profile, list_agent_profiles, save_agent_profile
from .capabilities import (
    execute_capability_action,
    load_capability_registry,
    runtime_capabilities,
    save_capability_registry,
)
from .commands import (
    _build_feather_cmd,
    _build_federlicht_cmd,
    _build_generate_prompt_cmd,
    _build_generate_template_cmd,
)
from .filesystem import (
    create_run_folder as _create_run_folder,
    clear_help_history,
    delete_run_file as _delete_run_file,
    list_dir as _list_dir,
    list_instruction_files as _list_instruction_files,
    list_run_dirs,
    list_run_logs,
    move_run_to_trash,
    read_binary_file as _read_binary_file,
    read_help_history,
    read_text_file as _read_text_file,
    resolve_run_dir as _resolve_run_dir,
    summarize_run,
    write_help_history,
    write_text_file as _write_text_file,
)
from .help_agent import answer_help_question, stream_help_question
from .jobs import Job
from .report_hub import (
    add_comment as _add_report_hub_comment,
    add_followup as _add_report_hub_followup,
    get_post_approval as _get_report_hub_approval,
    get_post as _get_report_hub_post,
    get_post_link as _get_report_hub_link,
    link_post as _link_report_hub_post,
    list_comments as _list_report_hub_comments,
    list_followups as _list_report_hub_followups,
    list_posts as _list_report_hub_posts,
    set_post_approval as _set_report_hub_approval,
)
from .templates import list_template_styles, list_templates, read_template_style, template_details
from .utils import parse_bool as _parse_bool, resolve_under_root as _resolve_under_root, safe_rel as _safe_rel
from .workspace_settings import (
    apply_workspace_settings,
    current_workspace_settings,
    load_workspace_settings,
    save_workspace_settings,
    workspace_settings_path,
)


class HandlerLike(Protocol):
    path: str
    headers: Any
    rfile: Any

    def _cfg(self): ...

    def _jobs(self): ...

    def _send_json(self, payload: Any, status: int = 200) -> None: ...

    def _send_bytes(self, data: bytes, content_type: str, status: int = 200) -> None: ...

    def _read_json(self) -> dict[str, Any]: ...

    def _stream_job(self, job: Job) -> None: ...

    def _session_auth(self): ...

    def send_response(self, code: int, message: str | None = None) -> None: ...

    def send_header(self, keyword: str, value: str) -> None: ...

    def end_headers(self) -> None: ...

    @property
    def wfile(self): ...


def _send_running_conflict(handler: HandlerLike, exc: RuntimeError) -> None:
    running = handler._jobs().find_running()
    handler._send_json(
        {
            "error": str(exc),
            "running_job_id": getattr(running, "job_id", None),
            "running_kind": getattr(running, "kind", None),
        },
        status=409,
    )


def _resolve_unique_output_path(root: Path, raw_output: str) -> dict[str, Any]:
    requested = _resolve_under_root(root, raw_output)
    if not requested:
        raise ValueError("output path is required")
    companion_suffixes = [".pdf"] if requested.suffix.lower() == ".tex" else []

    def has_companion_conflict(path: Path) -> bool:
        for suffix in companion_suffixes:
            if path.with_suffix(suffix).exists():
                return True
        return False

    suggested = requested
    if suggested.exists() or has_companion_conflict(suggested):
        parent = suggested.parent
        stem = suggested.stem
        suffix = suggested.suffix
        counter = 1
        while True:
            candidate = parent / f"{stem}_{counter}{suffix}"
            if candidate.exists() or has_companion_conflict(candidate):
                counter += 1
                continue
            suggested = candidate
            break

    return {
        "requested_output": _safe_rel(requested, root),
        "suggested_output": _safe_rel(suggested, root),
        "changed": requested != suggested,
        "requested_exists": requested.exists(),
    }


def _normalize_run_rel(cfg: Any, raw_run_rel: str | None) -> str | None:
    token = str(raw_run_rel or "").strip()
    if not token:
        return None
    resolved = _resolve_under_root(cfg.root, token)
    if resolved and resolved.exists() and resolved.is_dir():
        return _safe_rel(resolved, cfg.root)
    if "/" in token or "\\" in token:
        return token
    for run_root in cfg.run_roots:
        candidate = run_root / token
        if candidate.exists() and candidate.is_dir():
            return _safe_rel(candidate, cfg.root)
    return token


def _latest_report_path(run_dir: Path) -> Path | None:
    candidates = list(run_dir.glob("report_full*.html"))
    report_subdir = run_dir / "report"
    if report_subdir.exists():
        candidates.extend(report_subdir.glob("report_full*.html"))
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def _resolve_publish_run_dir(cfg: Any, payload: dict[str, Any]) -> Path | None:
    run_value = str(payload.get("run") or "").strip()
    if not run_value:
        return None
    run_dir = _resolve_under_root(cfg.root, run_value)
    if not run_dir or not run_dir.exists() or not run_dir.is_dir():
        raise ValueError(f"Run folder not found: {run_value}")
    return run_dir


def _resolve_publish_report_path(cfg: Any, payload: dict[str, Any], run_dir: Path | None) -> Path:
    report_value = str(payload.get("report") or "").strip()
    if report_value:
        report_path = _resolve_under_root(cfg.root, report_value)
        if not report_path or not report_path.exists() or not report_path.is_file():
            raise ValueError(f"Report file not found: {report_value}")
        return report_path
    if run_dir is None:
        raise ValueError("run or report is required for publish")
    latest = _latest_report_path(run_dir)
    if latest is None:
        raise ValueError(f"No report_full*.html found in run: {_safe_rel(run_dir, cfg.root)}")
    return latest


def _root_auth_manager(handler: HandlerLike) -> RootAuthManager | None:
    getter = getattr(handler, "_root_auth", None)
    if callable(getter):
        try:
            mgr = getter()
        except Exception:
            return None
        if isinstance(mgr, RootAuthManager):
            return mgr
    return None


def _session_auth_manager(handler: HandlerLike) -> SessionAuthManager | None:
    getter = getattr(handler, "_session_auth", None)
    if callable(getter):
        try:
            mgr = getter()
        except Exception:
            return None
        if isinstance(mgr, SessionAuthManager):
            return mgr
    return None


def _extract_session_token(handler: HandlerLike, payload: dict[str, Any] | None = None) -> str:
    if isinstance(payload, dict):
        token = payload.get("session_token")
        if isinstance(token, str) and token.strip():
            return token.strip()
    try:
        header_value = str(handler.headers.get("X-Federnett-Session-Token") or "").strip()
    except Exception:
        header_value = ""
    return header_value


def _session_status_payload(handler: HandlerLike, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    manager = _session_auth_manager(handler)
    if manager is None:
        return {
            "enabled": False,
            "authenticated": False,
            "username": None,
            "display_name": None,
            "role": None,
            "expires_at": None,
        }
    token = _extract_session_token(handler, payload)
    status = manager.status(token)
    return {
        "enabled": status.enabled,
        "authenticated": status.authenticated,
        "username": status.username,
        "display_name": status.display_name,
        "role": status.role,
        "expires_at": status.expires_at,
    }


def _session_principal(handler: HandlerLike, payload: dict[str, Any] | None = None) -> dict[str, str] | None:
    manager = _session_auth_manager(handler)
    if manager is None:
        return None
    token = _extract_session_token(handler, payload)
    return manager.principal(token)


def _session_has_root_role(handler: HandlerLike, payload: dict[str, Any] | None = None) -> bool:
    principal = _session_principal(handler, payload)
    if not isinstance(principal, dict):
        return False
    role = str(principal.get("role") or "").strip().lower()
    return role in {"root", "admin", "owner", "superuser"}


def _extract_root_token(handler: HandlerLike, payload: dict[str, Any] | None = None) -> str:
    if isinstance(payload, dict):
        token = payload.get("root_token")
        if isinstance(token, str) and token.strip():
            return token.strip()
    try:
        header_value = str(handler.headers.get("X-Federnett-Root-Token") or "").strip()
    except Exception:
        header_value = ""
    if header_value:
        return header_value
    try:
        auth_value = str(handler.headers.get("Authorization") or "").strip()
    except Exception:
        auth_value = ""
    if auth_value.lower().startswith("bearer "):
        return auth_value[7:].strip()
    return ""


def _root_auth_status_payload(handler: HandlerLike, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    manager = _root_auth_manager(handler)
    session_root = _session_has_root_role(handler, payload)
    if manager is None:
        return {
            "enabled": False,
            "unlocked": bool(session_root),
            "expires_at": None,
            "session_root": bool(session_root),
        }
    token = _extract_root_token(handler, payload)
    status = manager.status(token)
    unlocked = bool(status.unlocked or session_root)
    return {
        "enabled": status.enabled,
        "unlocked": unlocked,
        "expires_at": status.expires_at if status.unlocked else None,
        "session_root": bool(session_root),
    }


def _is_root_unlocked(handler: HandlerLike, payload: dict[str, Any] | None = None) -> bool:
    if _session_has_root_role(handler, payload):
        return True
    manager = _root_auth_manager(handler)
    if manager is None:
        return False
    token = _extract_root_token(handler, payload)
    return manager.is_unlocked(token)


def _can_edit_workspace_settings(handler: HandlerLike, payload: dict[str, Any] | None = None) -> bool:
    manager = _root_auth_manager(handler)
    if manager is None or not manager.enabled:
        return True
    return _is_root_unlocked(handler, payload)


def _can_edit_report_hub_approval(handler: HandlerLike, payload: dict[str, Any] | None = None) -> bool:
    manager = _root_auth_manager(handler)
    if manager is None or not manager.enabled:
        return True
    return _is_root_unlocked(handler, payload)


def _stream_help_events(handler: HandlerLike, events: Any) -> None:
    handler.send_response(200)
    handler.send_header("Content-Type", "text/event-stream; charset=utf-8")
    handler.send_header("Cache-Control", "no-cache")
    handler.send_header("Connection", "keep-alive")
    handler.end_headers()
    try:
        for event in events:
            payload = dict(event or {})
            event_name = str(payload.pop("event", "message") or "message")
            data = json.dumps(payload, ensure_ascii=False)
            chunk = f"event: {event_name}\ndata: {data}\n\n".encode("utf-8")
            try:
                handler.wfile.write(chunk)
                handler.wfile.flush()
            except BrokenPipeError:
                return
    except Exception as exc:
        payload = json.dumps({"error": str(exc)}, ensure_ascii=False)
        chunk = f"event: error\ndata: {payload}\n\n".encode("utf-8")
        try:
            handler.wfile.write(chunk)
            handler.wfile.flush()
        except BrokenPipeError:
            return


def _normalize_llm_backend(value: Any) -> str:
    token = str(value or "").strip().lower()
    if token in {"codex", "codex_cli", "codex-cli", "cli"}:
        return "codex_cli"
    return "openai_api"


def _normalize_reasoning_effort(value: Any) -> str:
    token = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    if token in {"low", "medium", "high", "extra_high"}:
        return token
    return "off"


def _normalize_runtime_mode(value: Any) -> str:
    token = str(value or "").strip().lower()
    if token in {"auto", "deepagent", "off"}:
        return token
    return "auto"


def _normalize_override_mode(value: Any) -> str:
    token = str(value or "").strip().lower()
    return "custom" if token == "custom" else "inherit"


def _normalize_log_chars(value: Any, default: int = 2200) -> int:
    try:
        parsed = int(value)
    except Exception:
        parsed = default
    return max(400, min(parsed, 12000))


def _normalize_model_for_backend(token: Any, backend: str) -> str:
    raw = _model_token(token)
    if not raw:
        return ""
    if backend == "codex_cli":
        return _canonicalize_codex_model_token(raw)
    return raw


def _normalize_llm_policy_payload(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return {}
    legacy_global_hint = {
        "backend",
        "model",
        "checkModel",
        "check_model",
        "visionModel",
        "vision_model",
        "reasoningEffort",
        "reasoning_effort",
    }
    global_raw = raw.get("global") if isinstance(raw.get("global"), dict) else None
    if global_raw is None and any(key in raw for key in legacy_global_hint):
        global_raw = raw
    global_raw = global_raw or {}

    global_backend = _normalize_llm_backend(global_raw.get("backend"))
    global_policy = {
        "lock": bool(global_raw.get("lock", True)),
        "backend": global_backend,
        "model": _normalize_model_for_backend(global_raw.get("model"), global_backend),
        "checkModel": _normalize_model_for_backend(
            global_raw.get("checkModel", global_raw.get("check_model")),
            global_backend,
        ),
        "visionModel": _normalize_model_for_backend(
            global_raw.get("visionModel", global_raw.get("vision_model")),
            global_backend,
        ),
        "reasoningEffort": _normalize_reasoning_effort(
            global_raw.get("reasoningEffort", global_raw.get("reasoning_effort")),
        ),
        "federhavRuntimeMode": _normalize_runtime_mode(
            global_raw.get("federhavRuntimeMode", global_raw.get("federhav_runtime_mode")),
        ),
        "liveAutoLogContext": bool(global_raw.get("liveAutoLogContext", global_raw.get("live_auto_log_context", True))),
        "liveAutoLogChars": _normalize_log_chars(
            global_raw.get("liveAutoLogChars", global_raw.get("live_auto_log_chars", 2200)),
            default=2200,
        ),
    }

    overrides_raw = raw.get("overrides") if isinstance(raw.get("overrides"), dict) else {}
    feather_raw = overrides_raw.get("feather") if isinstance(overrides_raw.get("feather"), dict) else {}
    federlicht_raw = overrides_raw.get("federlicht") if isinstance(overrides_raw.get("federlicht"), dict) else {}
    federhav_raw = overrides_raw.get("federhav") if isinstance(overrides_raw.get("federhav"), dict) else {}

    feather_backend = _normalize_llm_backend(feather_raw.get("backend", global_backend))
    federlicht_backend = _normalize_llm_backend(federlicht_raw.get("backend", global_backend))
    federhav_backend = _normalize_llm_backend(federhav_raw.get("backend", global_backend))

    overrides = {
        "feather": {
            "mode": _normalize_override_mode(feather_raw.get("mode")),
            "backend": feather_backend,
            "model": _normalize_model_for_backend(feather_raw.get("model"), feather_backend),
        },
        "federlicht": {
            "mode": _normalize_override_mode(federlicht_raw.get("mode")),
            "backend": federlicht_backend,
            "model": _normalize_model_for_backend(federlicht_raw.get("model"), federlicht_backend),
            "checkModel": _normalize_model_for_backend(
                federlicht_raw.get("checkModel", federlicht_raw.get("check_model")),
                federlicht_backend,
            ),
            "visionModel": _normalize_model_for_backend(
                federlicht_raw.get("visionModel", federlicht_raw.get("vision_model")),
                federlicht_backend,
            ),
            "reasoningEffort": _normalize_reasoning_effort(
                federlicht_raw.get("reasoningEffort", federlicht_raw.get("reasoning_effort")),
            ),
        },
        "federhav": {
            "mode": _normalize_override_mode(federhav_raw.get("mode")),
            "backend": federhav_backend,
            "model": _normalize_model_for_backend(federhav_raw.get("model"), federhav_backend),
            "reasoningEffort": _normalize_reasoning_effort(
                federhav_raw.get("reasoningEffort", federhav_raw.get("reasoning_effort")),
            ),
            "runtimeMode": _normalize_runtime_mode(
                federhav_raw.get("runtimeMode", federhav_raw.get("runtime_mode")),
            ),
            "liveAutoLogContext": bool(
                federhav_raw.get("liveAutoLogContext", federhav_raw.get("live_auto_log_context", True))
            ),
            "liveAutoLogChars": _normalize_log_chars(
                federhav_raw.get("liveAutoLogChars", federhav_raw.get("live_auto_log_chars", 2200)),
                default=2200,
            ),
        },
    }

    return {
        "global": global_policy,
        "overrides": overrides,
    }


def _job_env_overrides(kind: str, payload: dict[str, Any]) -> dict[str, str]:
    backend = _normalize_llm_backend(payload.get("llm_backend"))
    env: dict[str, str] = {}
    if kind == "feather":
        env["FEATHER_AGENTIC_LLM_BACKEND"] = backend
    elif kind in {"federlicht", "generate_prompt"}:
        env["FEDERLICHT_LLM_BACKEND"] = backend
    return env


_REASONING_MODEL_RE = re.compile(r"^(gpt-5|o1|o3|o4)", re.IGNORECASE)
_TRUE_LIKE = {"1", "true", "yes", "on"}
_OPENAI_MODEL_TOKENS = {"$openai_model", "${openai_model}", "%openai_model%"}
_OPENAI_MODEL_VISION_TOKENS = {"$openai_model_vision", "${openai_model_vision}"}
_CODEX_BACKENDS = {"codex_cli", "codex-cli", "codex", "cli"}
_CODEX_MODEL_OPTIONS = [
    "gpt-5.3-codex",
    "gpt-5.3-codex-spark",
    "gpt-5.2-codex",
    "gpt-5.1-codex-max",
    "gpt-5.2",
    "gpt-5.1-codex-mini",
]


def _model_token(raw: Any) -> str:
    return str(raw).strip() if isinstance(raw, str) else ""


def _canonicalize_codex_model_token(token: str) -> str:
    raw = str(token or "").strip()
    if not raw:
        return ""
    lowered = raw.lower()
    if lowered in _OPENAI_MODEL_TOKENS or lowered in _OPENAI_MODEL_VISION_TOKENS:
        return raw
    if raw.startswith("$") or (raw.startswith("${") and raw.endswith("}")):
        return raw
    if raw.startswith("%") and raw.endswith("%"):
        return raw
    return lowered


def _reasoning_disabled(token: str) -> bool:
    normalized = str(token or "").strip().lower().replace("-", "_").replace(" ", "_")
    return normalized in {"", "off", "none", "false", "0", "disabled", "disable"}


def _looks_like_codex_model(token: str) -> bool:
    lowered = token.strip().lower()
    return bool(lowered) and "codex" in lowered


def _preferred_openai_model(default: str = "gpt-4o-mini") -> str:
    model = str(os.getenv("OPENAI_MODEL") or "").strip()
    if not model or _looks_like_codex_model(model):
        return default
    return model


def _preferred_openai_vision_model(default: str = "gpt-4o-mini") -> str:
    model = str(os.getenv("OPENAI_MODEL_VISION") or "").strip()
    if not model:
        model = str(os.getenv("OPENAI_MODEL") or "").strip()
    if not model or _looks_like_codex_model(model):
        return default
    return model


def _openai_reasoning_api_supported() -> bool:
    force = str(os.getenv("FEDERNETT_FORCE_REASONING_EFFORT") or "").strip().lower() in _TRUE_LIKE
    if force:
        return True
    base_url = str(
        os.getenv("OPENAI_BASE_URL")
        or os.getenv("OPENAI_API_BASE")
        or "https://api.openai.com"
    ).strip()
    if not base_url:
        return False
    host = urlparse(base_url).netloc.lower()
    if not host:
        return False
    if host.endswith("openai.com"):
        return True
    if host.endswith("openai.azure.com"):
        return True
    return False


def _supports_reasoning_effort(model_token: str, backend: str) -> bool:
    if str(backend or "").strip().lower() in _CODEX_BACKENDS:
        return True
    if backend == "openai_api" and not _openai_reasoning_api_supported():
        return False
    token = model_token.strip()
    if not token:
        return False
    lowered = token.lower()
    if lowered in _OPENAI_MODEL_TOKENS:
        lowered = str(os.getenv("OPENAI_MODEL") or "").strip().lower()
    if lowered in _OPENAI_MODEL_VISION_TOKENS:
        lowered = str(os.getenv("OPENAI_MODEL_VISION") or "").strip().lower()
    if _looks_like_codex_model(lowered):
        return backend == "codex_cli"
    if not lowered:
        return False
    if _REASONING_MODEL_RE.match(lowered):
        return True
    return "reason" in lowered


def _prepare_federlicht_payload(raw_payload: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    payload = dict(raw_payload or {})
    notes: list[str] = []
    backend = _normalize_llm_backend(payload.get("llm_backend"))
    payload["llm_backend"] = backend

    model = _model_token(payload.get("model"))
    check_model = _model_token(payload.get("check_model"))
    model_vision = _model_token(payload.get("model_vision"))
    reasoning_effort = _model_token(payload.get("reasoning_effort"))

    if backend == "openai_api":
        openai_model = _preferred_openai_model()
        model_lower = model.lower()
        check_lower = check_model.lower()
        vision_lower = model_vision.lower()
        if not model or model_lower in _OPENAI_MODEL_TOKENS:
            payload["model"] = openai_model
            model = openai_model
            notes.append(f"OpenAI backend selected: model resolved -> {openai_model}")
        elif _looks_like_codex_model(model):
            payload["model"] = openai_model
            model = openai_model
            notes.append(f"OpenAI backend selected: model fallback applied -> {openai_model}")
        if not check_model or check_lower in _OPENAI_MODEL_TOKENS:
            fallback_check = model or openai_model
            payload["check_model"] = fallback_check
            check_model = fallback_check
            notes.append(f"OpenAI backend selected: check_model resolved -> {fallback_check}")
        elif _looks_like_codex_model(check_model):
            fallback_check = model or openai_model
            payload["check_model"] = fallback_check
            check_model = fallback_check
            notes.append(f"OpenAI backend selected: check_model fallback applied -> {fallback_check}")
        if vision_lower in _OPENAI_MODEL_VISION_TOKENS:
            fallback_vision = _preferred_openai_vision_model(default=openai_model)
            payload["model_vision"] = fallback_vision
            model_vision = fallback_vision
            notes.append(f"OpenAI backend selected: vision model resolved -> {fallback_vision}")
        elif model_vision and _looks_like_codex_model(model_vision):
            fallback_vision = _preferred_openai_vision_model(default=openai_model)
            payload["model_vision"] = fallback_vision
            model_vision = fallback_vision
            notes.append(f"OpenAI backend selected: vision model fallback applied -> {fallback_vision}")
    else:
        codex_model = _canonicalize_codex_model_token(str(os.getenv("CODEX_MODEL") or "").strip())
        if model in {"$OPENAI_MODEL", "${OPENAI_MODEL}", "%OPENAI_MODEL%"} and codex_model:
            payload["model"] = codex_model
            model = codex_model
            notes.append(f"Codex backend selected: model override applied -> {codex_model}")
        for key in ("model", "check_model", "model_vision"):
            current = _model_token(payload.get(key))
            if not current:
                continue
            normalized = _canonicalize_codex_model_token(current)
            if normalized and normalized != current:
                payload[key] = normalized
                notes.append(f"Codex backend selected: {key} normalized -> {normalized}")
        model = _model_token(payload.get("model"))
        check_model = _model_token(payload.get("check_model"))
        model_vision = _model_token(payload.get("model_vision"))

    gateway_reasoning_supported = backend == "codex_cli" or _openai_reasoning_api_supported()
    if _reasoning_disabled(reasoning_effort):
        payload.pop("reasoning_effort", None)
        reasoning_effort = ""

    reasoning_target = check_model or model
    if reasoning_effort and backend == "openai_api" and not gateway_reasoning_supported:
        payload.pop("reasoning_effort", None)
        notes.append(
            "reasoning_effort was removed because OPENAI_BASE_URL is not the official OpenAI endpoint."
        )
    elif reasoning_effort and not _supports_reasoning_effort(reasoning_target, backend):
        payload.pop("reasoning_effort", None)
        notes.append(
            "reasoning_effort was removed because the selected model/backend pair is not reasoning-compatible."
        )

    return payload, notes


def _federlicht_runtime_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    backend = _normalize_llm_backend(payload.get("llm_backend"))
    model = _model_token(payload.get("model"))
    check_model = _model_token(payload.get("check_model"))
    model_vision = _model_token(payload.get("model_vision"))
    reasoning_effort = _model_token(payload.get("reasoning_effort")) or "off"
    progress_chars = payload.get("progress_chars")
    return {
        "llm_backend": backend,
        "model": model,
        "check_model": check_model,
        "model_vision": model_vision,
        "reasoning_effort": reasoning_effort,
        "progress_chars": progress_chars,
    }


def handle_api_get(
    handler: HandlerLike,
    *,
    list_models: Callable[[], list[str]],
) -> None:
    cfg = handler._cfg()
    parsed = urlparse(handler.path)
    path = parsed.path
    qs = parse_qs(parsed.query)
    if path == "/api/health":
        handler._send_json({"status": "ok"})
        return
    if path == "/api/info":
        default_openai_model = _preferred_openai_model()
        default_openai_vision = _preferred_openai_vision_model(default=default_openai_model)
        default_codex_model = _canonicalize_codex_model_token(str(os.getenv("CODEX_MODEL") or "").strip())
        federlicht_default_model = str(os.getenv("OPENAI_MODEL") or "").strip() or default_openai_model
        federlicht_default_vision = (
            str(os.getenv("OPENAI_MODEL_VISION") or "").strip()
            or str(os.getenv("OPENAI_MODEL") or "").strip()
            or default_openai_vision
        )
        payload = {
            "root": _safe_rel(cfg.root, cfg.root),
            "root_abs": str(cfg.root.resolve()),
            "run_roots": [_safe_rel(p, cfg.root) for p in cfg.run_roots],
            "run_roots_abs": [str(p.resolve()) for p in cfg.run_roots],
            "site_root": _safe_rel(cfg.site_root, cfg.root),
            "site_root_abs": str(cfg.site_root.resolve()),
            "report_hub_root": _safe_rel(cfg.report_hub_root or cfg.site_root, cfg.root),
            "report_hub_root_abs": str((cfg.report_hub_root or cfg.site_root).resolve()),
            "templates": list_templates(cfg.root),
            "llm_defaults": {
                "openai_model": default_openai_model,
                "openai_model_vision": default_openai_vision,
                "codex_model": default_codex_model,
                "codex_model_options": list(_CODEX_MODEL_OPTIONS),
                "openai_reasoning_api": _openai_reasoning_api_supported(),
                "openai_reasoning_model": _supports_reasoning_effort(default_openai_model, "openai_api"),
                "federlicht_default_backend": "openai_api",
                "federlicht_default_model": federlicht_default_model,
                "federlicht_default_model_vision": federlicht_default_vision,
                "federhav_default_backend": "openai_api",
                "federhav_default_model": "gpt-4o-mini",
                "federhav_runtime_mode": str(
                    os.getenv("FEDERHAV_AGENTIC_RUNTIME")
                    or os.getenv("FEDERHAV_RUNTIME_MODE")
                    or "auto"
                ).strip().lower(),
            },
            "root_auth": _root_auth_status_payload(handler),
            "session_auth": _session_status_payload(handler),
        }
        handler._send_json(payload)
        return
    if path == "/api/workspace/settings":
        effective = current_workspace_settings(cfg)
        stored = load_workspace_settings(cfg.root)
        raw_llm_policy = (
            stored.get("llm_policy")
            if isinstance(stored, dict) and isinstance(stored.get("llm_policy"), dict)
            else {}
        )
        llm_policy = _normalize_llm_policy_payload(raw_llm_policy)
        effective_with_policy = {
            **effective,
            "llm_policy": llm_policy,
        }
        handler._send_json(
            {
                "effective": effective_with_policy,
                "stored": {
                    "run_roots": stored.get("run_roots"),
                    "site_root": stored.get("site_root"),
                    "report_hub_root": stored.get("report_hub_root"),
                    "llm_policy": llm_policy,
                    "updated_at": stored.get("updated_at"),
                }
                if isinstance(stored, dict) and stored
                else {},
                "path": _safe_rel(workspace_settings_path(cfg.root), cfg.root),
                "can_edit": _can_edit_workspace_settings(handler),
                "root_auth": _root_auth_status_payload(handler),
            }
        )
        return
    if path == "/api/auth/root/status":
        handler._send_json(_root_auth_status_payload(handler))
        return
    if path == "/api/auth/session/status":
        handler._send_json(_session_status_payload(handler))
        return
    if path == "/api/runs":
        runs = list_run_dirs(cfg.root, cfg.run_roots)
        handler._send_json(runs)
        return
    if path == "/api/templates":
        run_rel = (qs.get("run") or [None])[0]
        handler._send_json(list_templates(cfg.root, run=run_rel))
        return
    if path == "/api/template-styles":
        run_rel = (qs.get("run") or [None])[0]
        handler._send_json(list_template_styles(cfg.root, run=run_rel))
        return
    if path.startswith("/api/template-styles/"):
        name = unquote(path.split("/", 3)[3])
        try:
            payload = read_template_style(cfg.root, name)
        except ValueError as exc:
            handler._send_json({"error": str(exc)}, status=404)
            return
        handler._send_json(payload)
        return
    if path.startswith("/api/templates/"):
        name = unquote(path.split("/", 3)[3])
        try:
            payload = template_details(cfg.root, name)
        except ValueError as exc:
            handler._send_json({"error": str(exc)}, status=404)
            return
        handler._send_json(payload)
        return
    if path == "/api/template-preview":
        name = (qs.get("name") or [None])[0]
        if not name:
            handler._send_json({"error": "name is required"}, status=400)
            return
        try:
            detail = template_details(cfg.root, unquote(name))
        except ValueError as exc:
            handler._send_json({"error": str(exc)}, status=404)
            return
        css_name = detail.get("meta", {}).get("css")
        css_content = None
        extra_body_class = None
        if css_name:
            try:
                css_content = read_template_style(cfg.root, css_name).get("content")
                css_base = Path(css_name).stem
                if css_base:
                    extra_body_class = f"template-{css_base.lower()}"
            except Exception:
                css_content = None
        lines = [f"# Template Preview: {detail.get('name', name)}", ""]
        if detail.get("meta", {}).get("description"):
            lines.append(detail["meta"]["description"])
            lines.append("")
        if detail.get("writer_guidance"):
            lines.append("## Writer Notes")
            lines.extend([f"- {note}" for note in detail["writer_guidance"]])
            lines.append("")
        for section in detail.get("sections", []):
            lines.append(f"## {section}")
            guide = detail.get("guides", {}).get(section)
            if guide:
                lines.append(f"*Guidance:* {guide}")
            lines.append(
                "Sample paragraph to preview layout, spacing, and typography. "
                "Replace with real content when generating the report."
            )
            lines.append("")
        markdown = "\n".join(lines).strip() + "\n"
        try:
            from federlicht.render.html import markdown_to_html, wrap_html  # type: ignore
        except Exception:
            handler._send_json({"error": "preview renderer unavailable"}, status=500)
            return
        body_html = markdown_to_html(markdown)
        rendered = wrap_html(
            detail.get("name", name),
            body_html,
            template_name=detail.get("name", name),
            theme_css=css_content,
            extra_body_class=extra_body_class,
        )
        handler._send_json({"html": rendered})
        return
    if path == "/api/agent-profiles":
        root_status = _root_auth_status_payload(handler)
        can_edit_builtin = bool(root_status.get("unlocked"))
        profiles = list_agent_profiles(cfg.root)
        if can_edit_builtin:
            for item in profiles:
                if str(item.get("source") or "") == "builtin":
                    item["read_only"] = False
        handler._send_json({"profiles": profiles, "root_auth": root_status})
        return
    if path.startswith("/api/agent-profiles/"):
        profile_id = unquote(path.split("/", 3)[3])
        source = (qs.get("source") or [None])[0]
        try:
            payload = get_agent_profile(cfg.root, profile_id, source=source)
        except ValueError as exc:
            handler._send_json({"error": str(exc)}, status=404)
            return
        root_status = _root_auth_status_payload(handler)
        if bool(root_status.get("unlocked")) and str(payload.get("source") or "") == "builtin":
            payload["read_only"] = False
        payload["root_auth"] = root_status
        handler._send_json(payload)
        return
    if path == "/api/models":
        handler._send_json(list_models())
        return
    if path == "/api/report-hub/posts":
        query = (qs.get("q") or [""])[0]
        run = (qs.get("run") or [""])[0]
        try:
            limit = int((qs.get("limit") or ["40"])[0])
        except Exception:
            limit = 40
        try:
            offset = int((qs.get("offset") or ["0"])[0])
        except Exception:
            offset = 0
        hub_root = (cfg.report_hub_root or cfg.site_root).resolve()
        payload = _list_report_hub_posts(
            hub_root,
            query=str(query or ""),
            run=str(run or ""),
            limit=limit,
            offset=offset,
        )
        handler._send_json(payload)
        return
    if path.startswith("/api/report-hub/posts/"):
        parts = path.split("/")
        if len(parts) < 5:
            handler._send_json({"error": "post_id is required"}, status=400)
            return
        post_id = unquote(parts[4])
        tail = parts[5:] if len(parts) > 5 else []
        hub_root = (cfg.report_hub_root or cfg.site_root).resolve()
        try:
            if not tail:
                handler._send_json(_get_report_hub_post(hub_root, post_id))
                return
            if tail[0] == "comments":
                try:
                    limit = int((qs.get("limit") or ["80"])[0])
                except Exception:
                    limit = 80
                handler._send_json(
                    {
                        "post_id": post_id,
                        "items": _list_report_hub_comments(hub_root, post_id, limit=limit),
                    }
                )
                return
            if tail[0] == "followups":
                try:
                    limit = int((qs.get("limit") or ["80"])[0])
                except Exception:
                    limit = 80
                handler._send_json(
                    {
                        "post_id": post_id,
                        "items": _list_report_hub_followups(hub_root, post_id, limit=limit),
                    }
                )
                return
            if tail[0] == "link":
                handler._send_json(_get_report_hub_link(hub_root, post_id))
                return
            if tail[0] == "approval":
                handler._send_json(_get_report_hub_approval(hub_root, post_id))
                return
        except ValueError as exc:
            handler._send_json({"error": str(exc)}, status=404)
            return
        handler._send_json({"error": "unknown report_hub endpoint"}, status=404)
        return
    if path == "/api/capabilities":
        web_search_raw = (qs.get("web_search") or ["0"])[0]
        web_search_enabled = str(web_search_raw).strip().lower() in {"1", "true", "yes", "on"}
        handler._send_json(
            {
                "registry": load_capability_registry(cfg.root),
                "runtime": runtime_capabilities(cfg.root, web_search_enabled=web_search_enabled),
            }
        )
        return
    if path == "/api/federlicht/output-suggestion":
        raw_output = (qs.get("output") or [None])[0]
        run_rel = (qs.get("run") or [None])[0]
        output_value = str(raw_output or "").strip()
        if not output_value:
            handler._send_json({"error": "output is required"}, status=400)
            return
        if run_rel and "/" not in output_value and "\\" not in output_value:
            output_value = f"{str(run_rel).strip().strip('/').strip()}/{output_value}"
        try:
            payload = _resolve_unique_output_path(cfg.root, output_value)
        except ValueError as exc:
            handler._send_json({"error": str(exc)}, status=400)
            return
        handler._send_json(payload)
        return
    if path == "/api/run-summary":
        run_rel = _normalize_run_rel(cfg, (qs.get("run") or [None])[0])
        try:
            payload = summarize_run(cfg.root, run_rel)
        except ValueError as exc:
            handler._send_json({"error": str(exc)}, status=400)
            return
        handler._send_json(payload)
        return
    if path == "/api/run-logs":
        run_rel = _normalize_run_rel(cfg, (qs.get("run") or [None])[0])
        try:
            payload = list_run_logs(cfg.root, run_rel)
        except ValueError as exc:
            handler._send_json({"error": str(exc)}, status=400)
            return
        handler._send_json(payload)
        return
    if path == "/api/help/history":
        run_rel = _normalize_run_rel(cfg, (qs.get("run") or [None])[0])
        profile_id = (qs.get("profile_id") or [None])[0]
        try:
            payload = read_help_history(cfg.root, run_rel, profile_id=profile_id)
        except ValueError as exc:
            handler._send_json({"error": str(exc)}, status=400)
            return
        handler._send_json(payload)
        return
    if path == "/api/run-instructions":
        run_rel = _normalize_run_rel(cfg, (qs.get("run") or [None])[0])
        try:
            run_dir = _resolve_run_dir(cfg.root, run_rel)
            payload = _list_instruction_files(cfg.root, run_dir)
        except ValueError as exc:
            handler._send_json({"error": str(exc)}, status=400)
            return
        handler._send_json(payload)
        return
    if path == "/api/fs":
        raw_path = (qs.get("path") or [None])[0]
        try:
            payload = _list_dir(cfg.root, raw_path)
        except ValueError as exc:
            handler._send_json({"error": str(exc)}, status=404)
            return
        handler._send_json(payload)
        return
    if path == "/api/files":
        raw_path = (qs.get("path") or [None])[0]
        try:
            payload = _read_text_file(cfg.root, raw_path)
        except ValueError as exc:
            handler._send_json({"error": str(exc)}, status=404)
            return
        handler._send_json(payload)
        return
    if path == "/api/raw":
        raw_path = (qs.get("path") or [None])[0]
        try:
            _file_path, data, content_type = _read_binary_file(cfg.root, raw_path)
        except ValueError as exc:
            handler._send_json({"error": str(exc)}, status=404)
            return
        handler._send_bytes(data, content_type)
        return
    if path.startswith("/raw/"):
        raw_path = unquote(path[len("/raw/") :])
        try:
            _file_path, data, content_type = _read_binary_file(cfg.root, raw_path)
        except ValueError as exc:
            handler._send_json({"error": str(exc)}, status=404)
            return
        handler._send_bytes(data, content_type)
        return
    if path.startswith("/api/jobs/") and path.endswith("/status"):
        job_id = path.split("/")[3]
        job = handler._jobs().get(job_id)
        if not job:
            handler._send_json({"error": "job_not_found"}, status=404)
            return
        payload = {
            "job_id": job.job_id,
            "kind": job.kind,
            "status": job.status,
            "returncode": job.returncode,
            "command": job.command,
            "cwd": _safe_rel(job.cwd, cfg.root),
            "log_count": len(job.logs),
        }
        handler._send_json(payload)
        return
    if path.startswith("/api/jobs/") and path.endswith("/events"):
        job_id = path.split("/")[3]
        job = handler._jobs().get(job_id)
        if not job:
            handler._send_json({"error": "job_not_found"}, status=404)
            return
        handler._stream_job(job)
        return
    handler._send_json({"error": "unknown_endpoint"}, status=404)


def handle_api_post(
    handler: HandlerLike,
    *,
    render_template_preview: Callable[[Path, dict[str, Any]], str],
) -> None:
    cfg = handler._cfg()
    parsed = urlparse(handler.path)
    path = parsed.path
    qs = parse_qs(parsed.query)
    payload = handler._read_json()
    try:
        if path == "/api/feather/start":
            cmd = _build_feather_cmd(cfg, payload)
            env_overrides = _job_env_overrides("feather", payload)
            try:
                job = handler._jobs().start("feather", cmd, cfg.root, env_overrides=env_overrides)
            except RuntimeError as exc:
                _send_running_conflict(handler, exc)
                return
            handler._send_json({"job_id": job.job_id})
            return
        if path == "/api/templates/generate":
            cmd = _build_generate_template_cmd(cfg, payload)
            try:
                job = handler._jobs().start("template", cmd, cfg.root)
            except RuntimeError as exc:
                _send_running_conflict(handler, exc)
                return
            handler._send_json({"job_id": job.job_id})
            return
        if path == "/api/federlicht/start":
            prepared_payload, notes = _prepare_federlicht_payload(payload)
            cmd = _build_federlicht_cmd(cfg, prepared_payload)
            env_overrides = _job_env_overrides("federlicht", prepared_payload)
            runtime = _federlicht_runtime_snapshot(prepared_payload)
            try:
                job = handler._jobs().start("federlicht", cmd, cfg.root, env_overrides=env_overrides)
            except RuntimeError as exc:
                _send_running_conflict(handler, exc)
                return
            for note in notes:
                job.append_log(f"[federlicht:config] {note}", stream="meta")
            handler._send_json({"job_id": job.job_id, "warnings": notes, "runtime": runtime})
            return
        if path == "/api/federlicht/generate_prompt":
            prepared_payload, notes = _prepare_federlicht_payload(payload)
            cmd = _build_generate_prompt_cmd(cfg, prepared_payload)
            env_overrides = _job_env_overrides("generate_prompt", prepared_payload)
            runtime = _federlicht_runtime_snapshot(prepared_payload)
            try:
                job = handler._jobs().start("generate_prompt", cmd, cfg.root, env_overrides=env_overrides)
            except RuntimeError as exc:
                _send_running_conflict(handler, exc)
                return
            for note in notes:
                job.append_log(f"[federlicht:config] {note}", stream="meta")
            handler._send_json({"job_id": job.job_id, "warnings": notes, "runtime": runtime})
            return
        if path == "/api/files":
            raw_path = payload.get("path")
            content = payload.get("content")
            if not isinstance(content, str):
                raise ValueError("content must be a string")
            result = _write_text_file(cfg.root, raw_path, content)
            handler._send_json(result)
            return
        if path == "/api/files/delete":
            raw_path = payload.get("path")
            result = _delete_run_file(cfg.root, raw_path, cfg.run_roots)
            handler._send_json(result)
            return
        if path == "/api/runs/trash":
            run_rel = payload.get("run")
            result = move_run_to_trash(cfg.root, run_rel, cfg.run_roots)
            handler._send_json(result)
            return
        if path == "/api/runs/create":
            run_name_raw = payload.get("run_name")
            topic_raw = payload.get("topic")
            run_name = str(run_name_raw).strip() if isinstance(run_name_raw, str) else ""
            topic = str(topic_raw).strip() if isinstance(topic_raw, str) else ""
            run_root_raw = payload.get("run_root")
            selected_run_root = str(run_root_raw).strip() if isinstance(run_root_raw, str) else ""
            run_roots_for_create = list(cfg.run_roots)
            if selected_run_root:
                normalized_root = selected_run_root.replace("\\", "/").strip("/")
                preferred_root = None
                for root_path in cfg.run_roots:
                    root_rel = _safe_rel(root_path, cfg.root).replace("\\", "/").strip("/")
                    if root_rel == normalized_root:
                        preferred_root = root_path
                        break
                if preferred_root is None:
                    raise ValueError(f"Unknown run_root: {selected_run_root}")
                run_roots_for_create = [preferred_root] + [
                    root_path for root_path in cfg.run_roots if root_path != preferred_root
                ]
            result = _create_run_folder(
                cfg.root,
                run_roots_for_create,
                run_name=run_name or None,
                topic=topic or None,
            )
            handler._send_json(result)
            return
        if path == "/api/template-preview":
            html = render_template_preview(cfg.root, payload)
            handler._send_json({"html": html})
            return
        if path == "/api/workspace/settings":
            if not _can_edit_workspace_settings(handler, payload):
                handler._send_json(
                    {"error": "Root unlock is required to update workspace settings."},
                    status=403,
                )
                return
            current = current_workspace_settings(cfg)
            stored = load_workspace_settings(cfg.root)
            requested = {
                "run_roots": payload.get("run_roots", current.get("run_roots")),
                "site_root": payload.get("site_root", current.get("site_root")),
                "report_hub_root": payload.get("report_hub_root", current.get("report_hub_root")),
            }
            incoming_llm_policy = payload.get("llm_policy")
            if isinstance(incoming_llm_policy, dict):
                llm_policy = _normalize_llm_policy_payload(incoming_llm_policy)
            else:
                llm_policy = _normalize_llm_policy_payload(
                    stored.get("llm_policy")
                    if isinstance(stored, dict) and isinstance(stored.get("llm_policy"), dict)
                    else {}
                )
            effective = apply_workspace_settings(cfg, requested)
            effective_with_policy = {
                **effective,
                "llm_policy": llm_policy,
            }
            settings_path = save_workspace_settings(cfg.root, effective_with_policy)
            handler._send_json(
                {
                    "saved": True,
                    "effective": effective_with_policy,
                    "path": _safe_rel(settings_path, cfg.root),
                }
            )
            return
        if path == "/api/auth/root/unlock":
            manager = _root_auth_manager(handler)
            if manager is None or not manager.enabled:
                handler._send_json(
                    {"error": "Root auth is disabled. Set FEDERNETT_ROOT_PASSWORD first."},
                    status=400,
                )
                return
            password = payload.get("password")
            if not isinstance(password, str):
                raise ValueError("password must be a string")
            status = manager.unlock(password)
            handler._send_json(
                {
                    "enabled": status.enabled,
                    "unlocked": status.unlocked,
                    "expires_at": status.expires_at,
                    "token": status.token,
                }
            )
            return
        if path == "/api/auth/root/lock":
            manager = _root_auth_manager(handler)
            if manager is None:
                handler._send_json({"enabled": False, "unlocked": False, "expires_at": None})
                return
            token = _extract_root_token(handler, payload)
            status = manager.lock(token)
            handler._send_json(
                {
                    "enabled": status.enabled,
                    "unlocked": status.unlocked,
                    "expires_at": status.expires_at,
                }
            )
            return
        if path == "/api/auth/session/login":
            manager = _session_auth_manager(handler)
            if manager is None or not manager.enabled:
                handler._send_json(
                    {
                        "error": (
                            "Session auth is disabled. "
                            "Set FEDERNETT_AUTH_ACCOUNTS_JSON first."
                        )
                    },
                    status=400,
                )
                return
            username = payload.get("username")
            password = payload.get("password")
            if not isinstance(username, str) or not isinstance(password, str):
                raise ValueError("username and password must be strings")
            status = manager.login(username, password)
            handler._send_json(
                {
                    "enabled": status.enabled,
                    "authenticated": status.authenticated,
                    "username": status.username,
                    "display_name": status.display_name,
                    "role": status.role,
                    "expires_at": status.expires_at,
                    "token": status.token,
                }
            )
            return
        if path == "/api/auth/session/logout":
            manager = _session_auth_manager(handler)
            if manager is None:
                handler._send_json(
                    {
                        "enabled": False,
                        "authenticated": False,
                        "username": None,
                        "display_name": None,
                        "role": None,
                        "expires_at": None,
                    }
                )
                return
            token = _extract_session_token(handler, payload)
            status = manager.logout(token)
            handler._send_json(
                {
                    "enabled": status.enabled,
                    "authenticated": status.authenticated,
                    "username": status.username,
                    "display_name": status.display_name,
                    "role": status.role,
                    "expires_at": status.expires_at,
                }
            )
            return
        if path == "/api/agent-profiles/save":
            profile = payload.get("profile")
            if not isinstance(profile, dict):
                raise ValueError("profile must be an object")
            memory_text = payload.get("memory_text")
            store = payload.get("store") or "site"
            store_value = str(store).strip().lower()
            if store_value == "builtin" and not _is_root_unlocked(handler, payload):
                handler._send_json(
                    {"error": "Root unlock is required to edit built-in profiles."},
                    status=403,
                )
                return
            result = save_agent_profile(cfg.root, profile, memory_text=memory_text, store=store_value)
            handler._send_json(result)
            return
        if path == "/api/agent-profiles/delete":
            profile_id = payload.get("id")
            result = delete_agent_profile(cfg.root, profile_id)
            handler._send_json(result)
            return
        if path == "/api/capabilities/save":
            registry_payload = payload.get("registry")
            saved = save_capability_registry(cfg.root, registry_payload)
            web_search_raw = _parse_bool(payload, "web_search")
            web_search_enabled = bool(web_search_raw) if web_search_raw is not None else False
            handler._send_json(
                {
                    "saved": True,
                    "registry": saved,
                    "runtime": runtime_capabilities(cfg.root, web_search_enabled=web_search_enabled),
                }
            )
            return
        if path == "/api/capabilities/execute":
            cap_id_raw = payload.get("id")
            cap_id = str(cap_id_raw or "").strip()
            if not cap_id:
                raise ValueError("id is required")
            dry_run_raw = _parse_bool(payload, "dry_run")
            dry_run = True if dry_run_raw is None else bool(dry_run_raw)
            run_rel_raw = payload.get("run")
            run_rel = _normalize_run_rel(cfg, str(run_rel_raw).strip() if isinstance(run_rel_raw, str) else None)
            timeout_raw = payload.get("timeout_sec")
            try:
                timeout_sec = int(timeout_raw) if timeout_raw is not None else 6
            except Exception:
                timeout_sec = 6
            result = execute_capability_action(
                cfg.root,
                cap_id,
                dry_run=dry_run,
                run_rel=run_rel,
                timeout_sec=max(2, min(timeout_sec, 30)),
            )
            handler._send_json(result)
            return
        if path == "/api/report-hub/publish":
            run_dir = _resolve_publish_run_dir(cfg, payload)
            report_path = _resolve_publish_report_path(cfg, payload, run_dir)
            hub_root = (cfg.report_hub_root or cfg.site_root).resolve()
            title_raw = payload.get("title")
            author_raw = payload.get("author")
            summary_raw = payload.get("summary")
            title = str(title_raw).strip() if isinstance(title_raw, str) else ""
            author = str(author_raw).strip() if isinstance(author_raw, str) else ""
            summary = str(summary_raw).strip() if isinstance(summary_raw, str) else ""
            copy_overview_raw = _parse_bool(payload, "copy_overview")
            copy_workflow_raw = _parse_bool(payload, "copy_workflow")
            include_linked_raw = _parse_bool(payload, "include_linked_assets")
            overwrite_raw = _parse_bool(payload, "overwrite")
            refresh_raw = payload.get("refresh_minutes")
            try:
                refresh_minutes = int(refresh_raw) if refresh_raw is not None else 10
            except Exception:
                refresh_minutes = 10
            try:
                result = _publish_report_to_hub(
                    report_path=report_path,
                    hub_root=hub_root,
                    run_dir=run_dir,
                    title=title or None,
                    author=author or None,
                    summary=summary or None,
                    copy_overview=True if copy_overview_raw is None else bool(copy_overview_raw),
                    copy_workflow=True if copy_workflow_raw is None else bool(copy_workflow_raw),
                    include_linked_assets=True if include_linked_raw is None else bool(include_linked_raw),
                    refresh_minutes=max(1, refresh_minutes),
                    overwrite=True if overwrite_raw is None else bool(overwrite_raw),
                )
            except (FileNotFoundError, FileExistsError, RuntimeError) as exc:
                raise ValueError(str(exc)) from exc
            handler._send_json(
                {
                    "entry_id": result.entry_id,
                    "run_rel": _safe_rel(result.run_dir, cfg.root),
                    "report_rel": _safe_rel(result.report_path, cfg.root),
                    "hub_root_rel": _safe_rel(result.hub_root, cfg.root),
                    "published_report_rel": _safe_rel(result.published_report_path, cfg.root),
                    "published_overview_rel": (
                        _safe_rel(result.published_overview_path, cfg.root)
                        if result.published_overview_path
                        else ""
                    ),
                    "published_workflow_rel": (
                        _safe_rel(result.published_workflow_path, cfg.root)
                        if result.published_workflow_path
                        else ""
                    ),
                    "published_asset_rels": [
                        _safe_rel(path, cfg.root) for path in result.published_asset_paths
                    ],
                    "skipped_asset_refs": list(result.skipped_asset_refs),
                    "manifest_rel": _safe_rel(result.manifest_path, cfg.root),
                    "index_rel": _safe_rel(result.index_path, cfg.root),
                }
            )
            return
        if path == "/api/report-hub/comments":
            hub_root = (cfg.report_hub_root or cfg.site_root).resolve()
            post_id = payload.get("post_id")
            text = payload.get("text")
            principal = _session_principal(handler, payload)
            author = payload.get("author") or (principal or {}).get("display_name") or (principal or {}).get("username")
            run_rel = payload.get("run_rel")
            profile_id = payload.get("profile_id")
            metadata = payload.get("metadata")
            if not isinstance(metadata, dict):
                metadata = {}
            if principal:
                metadata = {
                    **metadata,
                    "signed_by": principal.get("display_name") or principal.get("username"),
                    "signed_role": principal.get("role") or "user",
                }
            result = _add_report_hub_comment(
                hub_root,
                post_id=post_id,
                text=text,
                author=author,
                run_rel=run_rel,
                profile_id=profile_id,
                metadata=metadata,
            )
            handler._send_json(result)
            return
        if path == "/api/report-hub/followups":
            hub_root = (cfg.report_hub_root or cfg.site_root).resolve()
            post_id = payload.get("post_id")
            prompt = payload.get("prompt")
            principal = _session_principal(handler, payload)
            author = payload.get("author") or (principal or {}).get("display_name") or (principal or {}).get("username")
            run_rel = payload.get("run_rel")
            profile_id = payload.get("profile_id")
            status = payload.get("status")
            metadata = payload.get("metadata")
            if not isinstance(metadata, dict):
                metadata = {}
            if principal:
                metadata = {
                    **metadata,
                    "signed_by": principal.get("display_name") or principal.get("username"),
                    "signed_role": principal.get("role") or "user",
                }
            result = _add_report_hub_followup(
                hub_root,
                post_id=post_id,
                prompt=prompt,
                author=author,
                run_rel=run_rel,
                profile_id=profile_id,
                status=status,
                metadata=metadata,
            )
            handler._send_json(result)
            return
        if path == "/api/report-hub/approval":
            if not _can_edit_report_hub_approval(handler, payload):
                handler._send_json(
                    {"error": "Root unlock is required to update report approval."},
                    status=403,
                )
                return
            hub_root = (cfg.report_hub_root or cfg.site_root).resolve()
            post_id = payload.get("post_id")
            status = payload.get("status")
            note = payload.get("note")
            principal = _session_principal(handler, payload)
            updated_by = (
                payload.get("updated_by")
                or (principal or {}).get("display_name")
                or (principal or {}).get("username")
            )
            metadata = payload.get("metadata")
            if not isinstance(metadata, dict):
                metadata = {}
            if principal:
                metadata = {
                    **metadata,
                    "signed_by": principal.get("display_name") or principal.get("username"),
                    "signed_role": principal.get("role") or "user",
                }
            result = _set_report_hub_approval(
                hub_root,
                post_id=post_id,
                status=status,
                updated_by=updated_by,
                note=note,
                metadata=metadata,
            )
            handler._send_json(result)
            return
        if path == "/api/report-hub/link":
            hub_root = (cfg.report_hub_root or cfg.site_root).resolve()
            post_id = payload.get("post_id")
            run_rel = payload.get("run_rel")
            principal = _session_principal(handler, payload)
            linked_by = payload.get("linked_by") or (principal or {}).get("display_name") or (principal or {}).get("username")
            metadata = payload.get("metadata")
            if not isinstance(metadata, dict):
                metadata = {}
            if principal:
                metadata = {
                    **metadata,
                    "signed_by": principal.get("display_name") or principal.get("username"),
                    "signed_role": principal.get("role") or "user",
                }
            result = _link_report_hub_post(
                hub_root,
                post_id=post_id,
                run_rel=run_rel,
                linked_by=linked_by,
                metadata=metadata,
            )
            handler._send_json(result)
            return
        if path == "/api/upload":
            name = (qs.get("name") or ["upload.bin"])[0]
            safe_name = Path(name).name or "upload.bin"
            target_dir = cfg.root / "site" / "uploads"
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / safe_name
            length = int(handler.headers.get("Content-Length", "0") or "0")
            if length <= 0:
                raise ValueError("empty upload")
            data = handler.rfile.read(length)
            target_path.write_bytes(data)
            handler._send_json(
                {
                    "name": safe_name,
                    "path": _safe_rel(target_path, cfg.root),
                    "abs_path": str(target_path.resolve()),
                    "size": target_path.stat().st_size,
                }
            )
            return
        if path == "/api/help/ask":
            question = payload.get("question")
            if not isinstance(question, str) or not question.strip():
                raise ValueError("question must be a non-empty string")
            agent_raw = payload.get("agent")
            agent_value = str(agent_raw).strip() if isinstance(agent_raw, str) else None
            execution_mode_raw = payload.get("execution_mode")
            execution_mode_value = (
                str(execution_mode_raw).strip() if isinstance(execution_mode_raw, str) else "plan"
            )
            model = payload.get("model")
            model_value = str(model).strip() if isinstance(model, str) else None
            llm_backend = payload.get("llm_backend")
            llm_backend_value = str(llm_backend).strip() if isinstance(llm_backend, str) else None
            reasoning_effort = payload.get("reasoning_effort")
            reasoning_effort_value = (
                str(reasoning_effort).strip() if isinstance(reasoning_effort, str) else None
            )
            runtime_mode = payload.get("runtime_mode")
            runtime_mode_value = (
                str(runtime_mode).strip() if isinstance(runtime_mode, str) else None
            )
            strict_model_raw = payload.get("strict_model")
            strict_model_value = bool(strict_model_raw) if isinstance(strict_model_raw, bool) else False
            run_rel = payload.get("run")
            run_value = _normalize_run_rel(cfg, str(run_rel).strip() if isinstance(run_rel, str) else None)
            history_raw = payload.get("history")
            history_value = history_raw if isinstance(history_raw, list) else None
            state_memory_raw = payload.get("state_memory")
            state_memory_value = state_memory_raw if isinstance(state_memory_raw, dict) else None
            live_log_tail_raw = payload.get("live_log_tail")
            live_log_tail_value = (
                str(live_log_tail_raw).strip() if isinstance(live_log_tail_raw, str) else None
            )
            max_sources_raw = payload.get("max_sources")
            try:
                max_sources = int(max_sources_raw) if max_sources_raw is not None else 8
            except Exception:
                max_sources = 8
            web_search_raw = _parse_bool(payload, "web_search")
            web_search_value = bool(web_search_raw) if web_search_raw is not None else False
            allow_artifacts_raw = _parse_bool(payload, "allow_artifacts")
            allow_artifacts_value = bool(allow_artifacts_raw) if allow_artifacts_raw is not None else False
            result = answer_help_question(
                cfg.root,
                question,
                agent=agent_value,
                execution_mode=execution_mode_value,
                allow_artifacts=allow_artifacts_value,
                model=model_value,
                llm_backend=llm_backend_value,
                reasoning_effort=reasoning_effort_value,
                runtime_mode=runtime_mode_value,
                strict_model=strict_model_value,
                max_sources=max_sources,
                history=history_value,
                state_memory=state_memory_value,
                run_rel=run_value,
                web_search=web_search_value,
                live_log_tail=live_log_tail_value,
            )
            handler._send_json(result)
            return
        if path == "/api/help/ask/stream":
            question = payload.get("question")
            if not isinstance(question, str) or not question.strip():
                raise ValueError("question must be a non-empty string")
            agent_raw = payload.get("agent")
            agent_value = str(agent_raw).strip() if isinstance(agent_raw, str) else None
            execution_mode_raw = payload.get("execution_mode")
            execution_mode_value = (
                str(execution_mode_raw).strip() if isinstance(execution_mode_raw, str) else "plan"
            )
            model = payload.get("model")
            model_value = str(model).strip() if isinstance(model, str) else None
            llm_backend = payload.get("llm_backend")
            llm_backend_value = str(llm_backend).strip() if isinstance(llm_backend, str) else None
            reasoning_effort = payload.get("reasoning_effort")
            reasoning_effort_value = (
                str(reasoning_effort).strip() if isinstance(reasoning_effort, str) else None
            )
            runtime_mode = payload.get("runtime_mode")
            runtime_mode_value = (
                str(runtime_mode).strip() if isinstance(runtime_mode, str) else None
            )
            strict_model_raw = payload.get("strict_model")
            strict_model_value = bool(strict_model_raw) if isinstance(strict_model_raw, bool) else False
            run_rel = payload.get("run")
            run_value = _normalize_run_rel(cfg, str(run_rel).strip() if isinstance(run_rel, str) else None)
            history_raw = payload.get("history")
            history_value = history_raw if isinstance(history_raw, list) else None
            state_memory_raw = payload.get("state_memory")
            state_memory_value = state_memory_raw if isinstance(state_memory_raw, dict) else None
            live_log_tail_raw = payload.get("live_log_tail")
            live_log_tail_value = (
                str(live_log_tail_raw).strip() if isinstance(live_log_tail_raw, str) else None
            )
            max_sources_raw = payload.get("max_sources")
            try:
                max_sources = int(max_sources_raw) if max_sources_raw is not None else 8
            except Exception:
                max_sources = 8
            web_search_raw = _parse_bool(payload, "web_search")
            web_search_value = bool(web_search_raw) if web_search_raw is not None else False
            allow_artifacts_raw = _parse_bool(payload, "allow_artifacts")
            allow_artifacts_value = bool(allow_artifacts_raw) if allow_artifacts_raw is not None else False
            events = stream_help_question(
                cfg.root,
                question,
                agent=agent_value,
                execution_mode=execution_mode_value,
                allow_artifacts=allow_artifacts_value,
                model=model_value,
                llm_backend=llm_backend_value,
                reasoning_effort=reasoning_effort_value,
                runtime_mode=runtime_mode_value,
                strict_model=strict_model_value,
                max_sources=max_sources,
                history=history_value,
                state_memory=state_memory_value,
                run_rel=run_value,
                web_search=web_search_value,
                live_log_tail=live_log_tail_value,
            )
            _stream_help_events(handler, events)
            return
        if path == "/api/help/history":
            run_rel = payload.get("run")
            run_value = _normalize_run_rel(cfg, str(run_rel).strip() if isinstance(run_rel, str) else None)
            profile_raw = payload.get("profile_id")
            profile_value = str(profile_raw).strip() if isinstance(profile_raw, str) else None
            items = payload.get("items")
            if not isinstance(items, list):
                raise ValueError("items must be an array")
            result = write_help_history(cfg.root, run_value, items, profile_id=profile_value)
            handler._send_json(result)
            return
        if path == "/api/help/history/clear":
            run_rel = payload.get("run")
            run_value = _normalize_run_rel(cfg, str(run_rel).strip() if isinstance(run_rel, str) else None)
            profile_raw = payload.get("profile_id")
            profile_value = str(profile_raw).strip() if isinstance(profile_raw, str) else None
            result = clear_help_history(cfg.root, run_value, profile_id=profile_value)
            handler._send_json(result)
            return
        if path.startswith("/api/jobs/") and path.endswith("/kill"):
            job_id = path.split("/")[3]
            job = handler._jobs().get(job_id)
            if not job:
                handler._send_json({"error": "job_not_found"}, status=404)
                return
            killed = job.kill()
            handler._send_json({"job_id": job_id, "killed": killed})
            return
    except ValueError as exc:
        handler._send_json({"error": str(exc)}, status=400)
        return
    handler._send_json({"error": "unknown_endpoint"}, status=404)
