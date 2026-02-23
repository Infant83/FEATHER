from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_post_id(value: Any) -> str:
    token = str(value or "").strip()
    if not token:
        raise ValueError("post_id is required")
    return token[:200]


def _normalize_author(value: Any) -> str:
    token = str(value or "").strip()
    if not token:
        return "anonymous"
    return token[:120]


def _normalize_text(value: Any, *, field: str, limit: int = 10000) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text[:limit]


def _safe_slug(value: str) -> str:
    token = re.sub(r"[^a-zA-Z0-9_.-]+", "_", str(value or "").strip()).strip("._-").lower()
    return token[:180] or "post"


def _manifest_path(hub_root: Path) -> Path:
    return hub_root / "manifest.json"


def _api_data_root(hub_root: Path) -> Path:
    return hub_root / "api_data"


def _comments_path(hub_root: Path, post_id: str) -> Path:
    return _api_data_root(hub_root) / "comments" / f"{_safe_slug(post_id)}.jsonl"


def _followups_path(hub_root: Path, post_id: str) -> Path:
    return _api_data_root(hub_root) / "followups" / f"{_safe_slug(post_id)}.jsonl"


def _links_path(hub_root: Path) -> Path:
    return _api_data_root(hub_root) / "links.json"


def _approval_path(hub_root: Path, post_id: str) -> Path:
    return _api_data_root(hub_root) / "approval" / f"{_safe_slug(post_id)}.json"


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except Exception:
            continue
        if isinstance(payload, dict):
            rows.append(payload)
    return rows


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    _ensure_parent(path)
    with path.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _manifest_items(hub_root: Path) -> list[dict[str, Any]]:
    manifest = _read_json(_manifest_path(hub_root), {"items": []})
    if not isinstance(manifest, dict):
        return []
    items = manifest.get("items")
    if not isinstance(items, list):
        return []
    out: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        if not str(item.get("id") or "").strip():
            continue
        out.append(item)
    return out


def _sort_posts(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def _stamp(row: dict[str, Any]) -> str:
        return str(row.get("timestamp") or row.get("date") or "")

    return sorted(items, key=_stamp, reverse=True)


def list_posts(
    hub_root: Path,
    *,
    query: str = "",
    run: str = "",
    limit: int = 40,
    offset: int = 0,
) -> dict[str, Any]:
    q = str(query or "").strip().lower()
    run_token = str(run or "").strip().lower()
    rows = _sort_posts(_manifest_items(hub_root))
    if q:
        rows = [
            row
            for row in rows
            if q in str(row.get("id") or "").lower()
            or q in str(row.get("title") or "").lower()
            or q in str(row.get("summary") or "").lower()
            or q in str(row.get("author") or "").lower()
        ]
    if run_token:
        rows = [row for row in rows if run_token in str(row.get("run") or "").lower()]
    safe_offset = max(0, int(offset))
    safe_limit = max(1, min(int(limit), 200))
    paged = rows[safe_offset : safe_offset + safe_limit]
    return {
        "items": paged,
        "total": len(rows),
        "offset": safe_offset,
        "limit": safe_limit,
    }


def get_post(hub_root: Path, post_id: Any) -> dict[str, Any]:
    target = _normalize_post_id(post_id)
    for row in _manifest_items(hub_root):
        if str(row.get("id") or "") == target:
            return row
    raise ValueError(f"post not found: {target}")


def list_comments(hub_root: Path, post_id: Any, *, limit: int = 80) -> list[dict[str, Any]]:
    _ = get_post(hub_root, post_id)
    path = _comments_path(hub_root, _normalize_post_id(post_id))
    rows = _read_jsonl(path)
    safe_limit = max(1, min(int(limit), 400))
    return rows[-safe_limit:]


def add_comment(
    hub_root: Path,
    *,
    post_id: Any,
    text: Any,
    author: Any = "",
    run_rel: Any = "",
    profile_id: Any = "",
    metadata: Any = None,
) -> dict[str, Any]:
    pid = _normalize_post_id(post_id)
    _ = get_post(hub_root, pid)
    payload = {
        "id": f"c_{_safe_slug(pid)}_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
        "post_id": pid,
        "text": _normalize_text(text, field="text"),
        "author": _normalize_author(author),
        "run_rel": str(run_rel or "").strip()[:240],
        "profile_id": str(profile_id or "").strip()[:120],
        "metadata": metadata if isinstance(metadata, dict) else {},
        "created_at": _now_iso(),
    }
    _append_jsonl(_comments_path(hub_root, pid), payload)
    return payload


def list_followups(hub_root: Path, post_id: Any, *, limit: int = 80) -> list[dict[str, Any]]:
    _ = get_post(hub_root, post_id)
    path = _followups_path(hub_root, _normalize_post_id(post_id))
    rows = _read_jsonl(path)
    safe_limit = max(1, min(int(limit), 400))
    return rows[-safe_limit:]


def add_followup(
    hub_root: Path,
    *,
    post_id: Any,
    prompt: Any,
    author: Any = "",
    run_rel: Any = "",
    profile_id: Any = "",
    status: Any = "proposed",
    metadata: Any = None,
) -> dict[str, Any]:
    pid = _normalize_post_id(post_id)
    _ = get_post(hub_root, pid)
    status_token = str(status or "proposed").strip().lower()
    if status_token not in {"proposed", "accepted", "rejected", "applied"}:
        status_token = "proposed"
    payload = {
        "id": f"f_{_safe_slug(pid)}_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
        "post_id": pid,
        "prompt": _normalize_text(prompt, field="prompt"),
        "author": _normalize_author(author),
        "run_rel": str(run_rel or "").strip()[:240],
        "profile_id": str(profile_id or "").strip()[:120],
        "status": status_token,
        "metadata": metadata if isinstance(metadata, dict) else {},
        "created_at": _now_iso(),
    }
    _append_jsonl(_followups_path(hub_root, pid), payload)
    return payload


def get_post_link(hub_root: Path, post_id: Any) -> dict[str, Any]:
    pid = _normalize_post_id(post_id)
    links = _read_json(_links_path(hub_root), {})
    if not isinstance(links, dict):
        links = {}
    linked = links.get(pid)
    if not isinstance(linked, dict):
        linked = {}
    return {"post_id": pid, "link": linked}


def _normalize_approval_status(value: Any) -> str:
    token = str(value or "").strip().lower()
    if token in {"draft", "review", "approved", "published", "rejected", "archived"}:
        return token
    return "draft"


_APPROVAL_TRANSITIONS: dict[str, set[str]] = {
    "draft": {"draft", "review", "rejected", "archived"},
    "review": {"review", "draft", "approved", "rejected", "archived"},
    "approved": {"approved", "review", "rejected", "published", "archived"},
    "published": {"published", "review", "archived"},
    "rejected": {"rejected", "review", "archived"},
    "archived": {"archived", "draft", "review"},
}


def _is_valid_approval_transition(current: str, next_status: str) -> bool:
    current_token = _normalize_approval_status(current)
    next_token = _normalize_approval_status(next_status)
    allowed = _APPROVAL_TRANSITIONS.get(current_token)
    if not isinstance(allowed, set):
        return current_token == next_token
    return next_token in allowed


def _allowed_next_approval_states(current: str) -> list[str]:
    current_token = _normalize_approval_status(current)
    allowed = _APPROVAL_TRANSITIONS.get(current_token)
    if not isinstance(allowed, set):
        return [current_token]
    return sorted(allowed)


def get_post_approval(hub_root: Path, post_id: Any) -> dict[str, Any]:
    pid = _normalize_post_id(post_id)
    _ = get_post(hub_root, pid)
    path = _approval_path(hub_root, pid)
    payload = _read_json(path, {})
    if isinstance(payload, dict) and str(payload.get("post_id") or "").strip() == pid:
        history = payload.get("history")
        payload["history"] = history if isinstance(history, list) else []
        status_token = _normalize_approval_status(payload.get("status"))
        payload["status"] = status_token
        payload["allowed_next"] = _allowed_next_approval_states(status_token)
        payload["updated_at"] = str(payload.get("updated_at") or "") or _now_iso()
        payload["updated_by"] = _normalize_author(payload.get("updated_by"))
        payload["note"] = str(payload.get("note") or "").strip()[:1000]
        return payload
    # Existing report_hub entries are already published artifacts by definition.
    return {
        "post_id": pid,
        "status": "published",
        "allowed_next": _allowed_next_approval_states("published"),
        "updated_at": _now_iso(),
        "updated_by": "system",
        "note": "",
        "history": [],
    }


def set_post_approval(
    hub_root: Path,
    *,
    post_id: Any,
    status: Any,
    updated_by: Any = "",
    note: Any = "",
    metadata: Any = None,
) -> dict[str, Any]:
    pid = _normalize_post_id(post_id)
    _ = get_post(hub_root, pid)
    next_status = _normalize_approval_status(status)
    actor = _normalize_author(updated_by)
    note_text = str(note or "").strip()[:1000]
    current = get_post_approval(hub_root, pid)
    current_status = _normalize_approval_status(current.get("status"))
    if not _is_valid_approval_transition(current_status, next_status):
        raise ValueError(f"invalid approval transition: {current_status} -> {next_status}")
    history = current.get("history")
    if not isinstance(history, list):
        history = []
    stamp = _now_iso()
    history.append(
        {
            "status": next_status,
            "updated_at": stamp,
            "updated_by": actor,
            "note": note_text,
            "metadata": metadata if isinstance(metadata, dict) else {},
        }
    )
    payload = {
        "post_id": pid,
        "status": next_status,
        "allowed_next": _allowed_next_approval_states(next_status),
        "updated_at": stamp,
        "updated_by": actor,
        "note": note_text,
        "metadata": metadata if isinstance(metadata, dict) else {},
        "history": history[-120:],
    }
    path = _approval_path(hub_root, pid)
    _ensure_parent(path)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def link_post(
    hub_root: Path,
    *,
    post_id: Any,
    run_rel: Any,
    linked_by: Any = "federnett",
    metadata: Any = None,
) -> dict[str, Any]:
    pid = _normalize_post_id(post_id)
    _ = get_post(hub_root, pid)
    run_token = str(run_rel or "").strip()
    if not run_token:
        raise ValueError("run_rel is required")
    path = _links_path(hub_root)
    links = _read_json(path, {})
    if not isinstance(links, dict):
        links = {}
    payload = {
        "post_id": pid,
        "run_rel": run_token[:240],
        "linked_by": _normalize_author(linked_by),
        "linked_at": _now_iso(),
        "metadata": metadata if isinstance(metadata, dict) else {},
    }
    links[pid] = payload
    _ensure_parent(path)
    path.write_text(json.dumps(links, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload
