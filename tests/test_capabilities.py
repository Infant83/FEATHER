from __future__ import annotations

from pathlib import Path

from federnett.capabilities import (
    execute_capability_action,
    infer_capability_action,
    load_capability_registry,
    runtime_capabilities,
    save_capability_registry,
)


def _make_root(tmp_path: Path) -> Path:
    root = tmp_path
    (root / "site" / "agent_profiles").mkdir(parents=True, exist_ok=True)
    return root


def test_capability_registry_roundtrip(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    payload = {
        "tools": [{"id": " custom.lookup ", "label": "Lookup"}],
        "skills": [{"id": "triage_skill", "label": "Triage Skill"}],
        "mcp_servers": [{"id": "local_mcp", "endpoint": "http://localhost:8787/sse"}],
    }
    saved = save_capability_registry(root, payload)
    loaded = load_capability_registry(root)
    assert loaded == saved
    assert loaded["tools"][0]["id"] == "custom.lookup"
    assert loaded["mcp_servers"][0]["endpoint"] == "http://localhost:8787/sse"


def test_runtime_capabilities_reflect_web_search_flag(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    runtime_off = runtime_capabilities(root, web_search_enabled=False)
    runtime_on = runtime_capabilities(root, web_search_enabled=True)
    tools_off = runtime_off.get("tools") if isinstance(runtime_off, dict) else []
    tools_on = runtime_on.get("tools") if isinstance(runtime_on, dict) else []
    off_entry = next((item for item in tools_off if item.get("id") == "web_research"), None)
    on_entry = next((item for item in tools_on if item.get("id") == "web_research"), None)
    assert isinstance(off_entry, dict)
    assert isinstance(on_entry, dict)
    assert off_entry.get("enabled") is False
    assert on_entry.get("enabled") is True


def test_infer_capability_action_from_keywords(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    save_capability_registry(
        root,
        {
            "tools": [
                {
                    "id": "open_probe_notes",
                    "label": "Open Probe Notes",
                    "keywords": ["probe notes", "프로브 노트"],
                    "action": {"kind": "open_path", "target": "README.md"},
                }
            ],
            "skills": [],
            "mcp_servers": [],
        },
    )
    action = infer_capability_action(root, "프로브 노트 열어줘", run_rel="site/runs/demo")
    assert isinstance(action, dict)
    assert action.get("type") == "run_capability"
    assert action.get("capability_id") == "open_probe_notes"


def test_execute_capability_action_open_path(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    (root / "README.md").write_text("hello\n", encoding="utf-8")
    save_capability_registry(
        root,
        {
            "tools": [
                {
                    "id": "open_readme",
                    "label": "Open README",
                    "action": {"kind": "open_path", "target": "README.md"},
                }
            ],
            "skills": [],
            "mcp_servers": [],
        },
    )
    result = execute_capability_action(root, "open_readme", dry_run=False)
    assert result.get("ok") is True
    assert result.get("effect") == "open_path"
    assert result.get("path") == "README.md"


def test_execute_capability_action_delegate(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    save_capability_registry(
        root,
        {
            "tools": [
                {
                    "id": "run_feather_fast",
                    "label": "Run Feather Fast",
                    "action": {"kind": "run_feather"},
                }
            ],
            "skills": [],
            "mcp_servers": [],
        },
    )
    result = execute_capability_action(root, "run_feather_fast", dry_run=True)
    assert result.get("effect") == "delegate"
    assert result.get("action_type") == "run_feather"
