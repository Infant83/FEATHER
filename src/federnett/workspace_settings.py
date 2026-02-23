from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import FedernettConfig
from .constants import DEFAULT_REPORT_HUB_ROOT, DEFAULT_RUN_ROOTS, DEFAULT_SITE_ROOT
from .utils import safe_rel

WORKSPACE_SETTINGS_REL = "site/federnett/workspace_settings.json"


def workspace_settings_path(root: Path) -> Path:
    return (root / WORKSPACE_SETTINGS_REL).resolve()


def _iso_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _normalize_rel_token(value: str) -> str:
    token = str(value or "").strip().replace("\\", "/")
    token = token.replace("//", "/").strip("/")
    return token


def _resolve_rel_path(root: Path, value: str, *, field: str) -> Path:
    token = _normalize_rel_token(value)
    if not token:
        raise ValueError(f"{field} is required")
    candidate = (root / token).resolve()
    try:
        candidate.relative_to(root)
    except Exception as exc:
        raise ValueError(f"{field} escapes workspace root: {value}") from exc
    return candidate


def _normalize_run_roots(root: Path, raw: Any) -> list[Path]:
    tokens: list[str] = []
    if isinstance(raw, str):
        tokens = [part.strip() for part in raw.split(",")]
    elif isinstance(raw, list):
        for item in raw:
            token = str(item or "").strip()
            if token:
                tokens.append(token)
    elif raw is None:
        tokens = []
    else:
        raise ValueError("run_roots must be a list or comma-separated string")
    if not tokens:
        tokens = list(DEFAULT_RUN_ROOTS)

    seen: set[str] = set()
    resolved: list[Path] = []
    for token in tokens:
        path = _resolve_rel_path(root, token, field="run_roots")
        key = str(path.resolve()).lower()
        if key in seen:
            continue
        seen.add(key)
        resolved.append(path)
    if not resolved:
        raise ValueError("run_roots must include at least one path")
    return resolved


def current_workspace_settings(cfg: FedernettConfig) -> dict[str, Any]:
    run_roots = [safe_rel(path, cfg.root) for path in cfg.run_roots]
    site_root = safe_rel(cfg.site_root, cfg.root)
    report_hub = safe_rel(cfg.report_hub_root or cfg.site_root, cfg.root)
    return {
        "run_roots": run_roots,
        "site_root": site_root,
        "report_hub_root": report_hub,
    }


def _workspace_payload(cfg: FedernettConfig, *, source: str) -> dict[str, Any]:
    base = current_workspace_settings(cfg)
    run_root_abs: list[str] = [str(path.resolve()) for path in cfg.run_roots]
    site_root_abs = str(cfg.site_root.resolve())
    hub_root_abs = str((cfg.report_hub_root or cfg.site_root).resolve())
    return {
        **base,
        "run_roots_abs": run_root_abs,
        "site_root_abs": site_root_abs,
        "report_hub_root_abs": hub_root_abs,
        "source": source,
    }


def apply_workspace_settings(cfg: FedernettConfig, payload: dict[str, Any]) -> dict[str, Any]:
    incoming = payload if isinstance(payload, dict) else {}
    run_roots = _normalize_run_roots(cfg.root, incoming.get("run_roots"))
    site_root = _resolve_rel_path(
        cfg.root,
        str(incoming.get("site_root") or DEFAULT_SITE_ROOT),
        field="site_root",
    )
    report_hub_root = _resolve_rel_path(
        cfg.root,
        str(incoming.get("report_hub_root") or DEFAULT_REPORT_HUB_ROOT),
        field="report_hub_root",
    )

    for path in run_roots:
        path.mkdir(parents=True, exist_ok=True)
    site_root.mkdir(parents=True, exist_ok=True)
    report_hub_root.mkdir(parents=True, exist_ok=True)

    cfg.run_roots = run_roots
    cfg.site_root = site_root
    cfg.report_hub_root = report_hub_root
    return _workspace_payload(cfg, source="runtime")


def load_workspace_settings(root: Path) -> dict[str, Any]:
    path = workspace_settings_path(root)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def save_workspace_settings(root: Path, payload: dict[str, Any]) -> Path:
    path = workspace_settings_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    llm_policy = payload.get("llm_policy")
    data = {
        "run_roots": payload.get("run_roots") or list(DEFAULT_RUN_ROOTS),
        "site_root": payload.get("site_root") or DEFAULT_SITE_ROOT,
        "report_hub_root": payload.get("report_hub_root") or DEFAULT_REPORT_HUB_ROOT,
        "updated_at": _iso_now(),
    }
    if isinstance(llm_policy, dict):
        data["llm_policy"] = llm_policy
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def load_and_apply_workspace_settings(cfg: FedernettConfig) -> dict[str, Any]:
    stored = load_workspace_settings(cfg.root)
    if not stored:
        return _workspace_payload(cfg, source="cli")
    merged = {
        "run_roots": stored.get("run_roots"),
        "site_root": stored.get("site_root"),
        "report_hub_root": stored.get("report_hub_root"),
    }
    try:
        return apply_workspace_settings(cfg, merged)
    except Exception:
        return _workspace_payload(cfg, source="cli")
