from __future__ import annotations

import json
from pathlib import Path

import pytest

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


def test_runtime_capabilities_include_infographic_tool(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    runtime = runtime_capabilities(root, web_search_enabled=True)
    tools = runtime.get("tools") if isinstance(runtime, dict) else []
    packs = runtime.get("packs") if isinstance(runtime, dict) else []
    infographic_builder = next(
        (
            item
            for item in tools
            if isinstance(item, dict) and item.get("id") == "artwork.artwork_infographic_spec_builder"
        ),
        None,
    )
    infographic_html = next(
        (item for item in tools if isinstance(item, dict) and item.get("id") == "artwork.artwork_infographic_html"),
        None,
    )
    infographic_claim_packet = next(
        (
            item
            for item in tools
            if isinstance(item, dict) and item.get("id") == "artwork.artwork_infographic_claim_packet_builder"
        ),
        None,
    )
    federlicht_pack = next(
        (item for item in packs if isinstance(item, dict) and item.get("id") == "federlicht_runtime_pack"),
        None,
    )
    assert isinstance(infographic_builder, dict)
    assert infographic_builder.get("enabled") is True
    assert isinstance(infographic_claim_packet, dict)
    assert infographic_claim_packet.get("enabled") is True
    assert isinstance(infographic_html, dict)
    assert infographic_html.get("enabled") is True
    assert isinstance(federlicht_pack, dict)
    pack_items = federlicht_pack.get("items")
    assert isinstance(pack_items, list)
    assert "artwork.artwork_infographic_spec_builder" in pack_items
    assert "artwork.artwork_infographic_claim_packet_builder" in pack_items
    assert "artwork.artwork_infographic_html" in pack_items


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


def test_execute_capability_action_edit_text_file_dry_run_and_apply(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    doc = root / "docs" / "note.md"
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("title: Old\nbody\n", encoding="utf-8")
    save_capability_registry(
        root,
        {
            "tools": [
                {
                    "id": "edit_note",
                    "label": "Edit Note",
                    "action": {
                        "kind": "edit_text_file",
                        "target": json.dumps(
                            {
                                "path": "docs/note.md",
                                "mode": "replace_first",
                                "find": "Old",
                                "replace": "New",
                            },
                            ensure_ascii=False,
                        ),
                    },
                }
            ],
            "skills": [],
            "mcp_servers": [],
        },
    )
    dry = execute_capability_action(root, "edit_note", dry_run=True)
    assert dry.get("effect") == "edit_text_file"
    assert dry.get("changed") is True
    assert doc.read_text(encoding="utf-8") == "title: Old\nbody\n"
    applied = execute_capability_action(root, "edit_note", dry_run=False)
    assert applied.get("effect") == "edit_text_file"
    assert applied.get("changed") is True
    assert doc.read_text(encoding="utf-8") == "title: New\nbody\n"


def test_execute_capability_action_edit_text_file_uses_request_title_hint(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    html = root / "site" / "runs" / "demo" / "report" / "report_full.html"
    html.parent.mkdir(parents=True, exist_ok=True)
    html.write_text("<html><head><title>Before</title></head><body>ok</body></html>", encoding="utf-8")
    save_capability_registry(
        root,
        {
            "tools": [
                {
                    "id": "edit_report_title",
                    "label": "Edit Report Title",
                    "action": {"kind": "edit_text_file", "target": "report/report_full.html"},
                }
            ],
            "skills": [],
            "mcp_servers": [],
        },
    )
    result = execute_capability_action(
        root,
        "edit_report_title",
        dry_run=False,
        run_rel="site/runs/demo",
        request_text='제목을 "After"로 바꿔줘',
    )
    assert result.get("effect") == "edit_text_file"
    assert result.get("changed") is True
    assert "<title>After</title>" in html.read_text(encoding="utf-8")


def test_execute_capability_action_edit_text_file_rejects_unsafe_path(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    target = root / "src" / "unsafe.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("unsafe", encoding="utf-8")
    save_capability_registry(
        root,
        {
            "tools": [
                {
                    "id": "edit_src",
                    "label": "Edit Src",
                    "action": {"kind": "edit_text_file", "target": "src/unsafe.txt"},
                }
            ],
            "skills": [],
            "mcp_servers": [],
        },
    )
    with pytest.raises(ValueError):
        execute_capability_action(root, "edit_src", dry_run=False)


def test_execute_capability_action_rewrite_section_direct_upsert(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    report_path = root / "site" / "runs" / "demo" / "report" / "report_full.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "## Executive Summary\nold summary\n\n## Key Findings\nold findings\n",
        encoding="utf-8",
    )
    save_capability_registry(
        root,
        {
            "tools": [
                {
                    "id": "rewrite_key_findings",
                    "label": "Rewrite Key Findings",
                    "action": {"kind": "rewrite_section", "target": "report/report_full.md#Key Findings"},
                }
            ],
            "skills": [],
            "mcp_servers": [],
        },
    )
    result = execute_capability_action(
        root,
        "rewrite_key_findings",
        dry_run=False,
        run_rel="site/runs/demo",
        action_override={"replacement": "new findings in narrative form"},
    )
    assert result.get("effect") == "rewrite_section"
    assert result.get("rewrite_mode") == "direct_upsert"
    assert result.get("changed") is True
    updated = report_path.read_text(encoding="utf-8")
    assert "new findings in narrative form" in updated
    assert "old findings" not in updated


def test_execute_capability_action_rewrite_section_prompt_prep(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    report_path = root / "site" / "runs" / "demo" / "report" / "report_full.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "## Key Findings\n"
        "baseline section text with enough words to be treated as an existing section body for prompt preparation.\n",
        encoding="utf-8",
    )
    save_capability_registry(
        root,
        {
            "tools": [
                {
                    "id": "rewrite_section_prompt",
                    "label": "Rewrite Section Prompt",
                    "action": {"kind": "rewrite_section", "target": "report/report_full.md#Key Findings"},
                }
            ],
            "skills": [],
            "mcp_servers": [],
        },
    )
    result = execute_capability_action(
        root,
        "rewrite_section_prompt",
        dry_run=False,
        run_rel="site/runs/demo",
        request_text="section 'Key Findings' tone: formal style: bullet flow: context continuity length: 3 paragraphs",
    )
    assert result.get("effect") == "rewrite_section"
    assert result.get("rewrite_mode") == "prompt_prep"
    assert result.get("section_insert_policy") == "upsert_missing_append_end"
    assert "formal" in str(result.get("tone_hint") or "").lower()
    assert "bullet" in str(result.get("style_hint") or "").lower()
    assert "context continuity" in str(result.get("flow_hint") or "").lower()
    assert "3" in str(result.get("length_hint") or "")
    prompt_file = str(result.get("prompt_file") or "")
    assert prompt_file.startswith("site/runs/demo/report_notes/update_request_section_")
    prompt_abs = root / prompt_file
    assert prompt_abs.exists()
    prompt_text = prompt_abs.read_text(encoding="utf-8")
    assert "Target section: Key Findings" in prompt_text
    assert "Tone:" in prompt_text
    assert "Narrative flow:" in prompt_text
    assert "Target section status: found in current report" in prompt_text
    assert "opening claim sentence -> evidence interpretation" in prompt_text


def test_execute_capability_action_rewrite_section_prompt_prep_missing_section(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    report_path = root / "site" / "runs" / "demo" / "report" / "report_full.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("## Executive Summary\nbaseline text\n", encoding="utf-8")
    save_capability_registry(
        root,
        {
            "tools": [
                {
                    "id": "rewrite_missing_section_prompt",
                    "label": "Rewrite Missing Section Prompt",
                    "action": {"kind": "rewrite_section", "target": "report/report_full.md#Key Findings"},
                }
            ],
            "skills": [],
            "mcp_servers": [],
        },
    )
    result = execute_capability_action(
        root,
        "rewrite_missing_section_prompt",
        dry_run=False,
        run_rel="site/runs/demo",
        request_text="section 'Key Findings' style: narrative",
    )
    assert result.get("effect") == "rewrite_section"
    assert result.get("rewrite_mode") == "prompt_prep"
    assert result.get("found_section") is False
    prompt_file = str(result.get("prompt_file") or "")
    prompt_abs = root / prompt_file
    prompt_text = prompt_abs.read_text(encoding="utf-8")
    assert "Target section status: missing in current report" in prompt_text


def test_execute_capability_action_rewrite_section_prompt_prep_flow_hint_from_override(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    report_path = root / "site" / "runs" / "demo" / "report" / "report_full.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("## Key Findings\nbaseline text\n", encoding="utf-8")
    save_capability_registry(
        root,
        {
            "tools": [
                {
                    "id": "rewrite_section_prompt_flow",
                    "label": "Rewrite Section Prompt Flow",
                    "action": {"kind": "rewrite_section", "target": "report/report_full.md#Key Findings"},
                }
            ],
            "skills": [],
            "mcp_servers": [],
        },
    )
    result = execute_capability_action(
        root,
        "rewrite_section_prompt_flow",
        dry_run=False,
        run_rel="site/runs/demo",
        action_override={"flow_hint": "setup -> evidence -> implication"},
    )
    assert result.get("effect") == "rewrite_section"
    assert result.get("rewrite_mode") == "prompt_prep"
    assert str(result.get("flow_hint") or "") == "setup -> evidence -> implication"
    prompt_file = str(result.get("prompt_file") or "")
    prompt_abs = root / prompt_file
    prompt_text = prompt_abs.read_text(encoding="utf-8")
    assert "Narrative flow: setup -> evidence -> implication" in prompt_text


def test_infer_capability_action_rewrite_section_from_keywords(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    save_capability_registry(
        root,
        {
            "tools": [
                {
                    "id": "rewrite_report_section",
                    "label": "Section Rewrite",
                    "keywords": ["섹션 수정", "section rewrite"],
                    "action": {"kind": "rewrite_section", "target": "report/report_full.md#Executive Summary"},
                }
            ],
            "skills": [],
            "mcp_servers": [],
        },
    )
    action = infer_capability_action(root, "section 'Executive Summary'를 서술형으로 수정해줘", run_rel="site/runs/demo")
    assert isinstance(action, dict)
    assert action.get("type") == "run_capability"
    assert action.get("capability_id") == "rewrite_report_section"
    assert action.get("action_kind") == "rewrite_section"
