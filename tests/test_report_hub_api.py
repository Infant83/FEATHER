from __future__ import annotations

import json
from pathlib import Path

import pytest

from federnett import report_hub as hub_mod


def _make_hub(tmp_path: Path) -> Path:
    hub_root = tmp_path / "site" / "report_hub"
    hub_root.mkdir(parents=True, exist_ok=True)
    manifest = {
        "revision": "r1",
        "items": [
            {
                "id": "post_001",
                "run": "demo_run",
                "title": "Demo Report",
                "summary": "summary",
                "author": "tester",
                "paths": {"report": "../runs/demo_run/report_full.html"},
            }
        ],
    }
    (hub_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return hub_root


def test_list_posts_reads_manifest(tmp_path: Path) -> None:
    hub_root = _make_hub(tmp_path)
    payload = hub_mod.list_posts(hub_root, query="demo", limit=10)
    assert payload.get("total") == 1
    rows = payload.get("items")
    assert isinstance(rows, list)
    assert rows[0]["id"] == "post_001"


def test_add_comment_and_followup_and_link(tmp_path: Path) -> None:
    hub_root = _make_hub(tmp_path)
    comment = hub_mod.add_comment(
        hub_root,
        post_id="post_001",
        text="코멘트",
        author="alice",
        run_rel="site/runs/demo_run",
        profile_id="team_a",
    )
    assert comment["post_id"] == "post_001"
    comments = hub_mod.list_comments(hub_root, "post_001")
    assert comments[-1]["text"] == "코멘트"

    follow = hub_mod.add_followup(
        hub_root,
        post_id="post_001",
        prompt="다음 리비전에서는 표를 추가해줘",
        author="alice",
        run_rel="site/runs/demo_run",
        status="proposed",
    )
    assert follow["post_id"] == "post_001"
    followups = hub_mod.list_followups(hub_root, "post_001")
    assert followups[-1]["prompt"].startswith("다음 리비전")

    link = hub_mod.link_post(
        hub_root,
        post_id="post_001",
        run_rel="site/runs/demo_run",
        linked_by="federnett",
    )
    assert link["post_id"] == "post_001"
    assert hub_mod.get_post_link(hub_root, "post_001")["link"]["run_rel"] == "site/runs/demo_run"


def test_post_approval_roundtrip(tmp_path: Path) -> None:
    hub_root = _make_hub(tmp_path)
    baseline = hub_mod.get_post_approval(hub_root, "post_001")
    assert baseline["status"] == "published"
    assert "review" in (baseline.get("allowed_next") or [])
    updated = hub_mod.set_post_approval(
        hub_root,
        post_id="post_001",
        status="review",
        updated_by="alice",
        note="Needs methodology clarification.",
    )
    assert updated["status"] == "review"
    assert "approved" in (updated.get("allowed_next") or [])
    assert updated["updated_by"] == "alice"
    assert "history" in updated
    loaded = hub_mod.get_post_approval(hub_root, "post_001")
    assert loaded["status"] == "review"
    assert "approved" in (loaded.get("allowed_next") or [])
    assert loaded["history"][-1]["status"] == "review"


def test_post_approval_rejects_invalid_transition(tmp_path: Path) -> None:
    hub_root = _make_hub(tmp_path)
    baseline = hub_mod.get_post_approval(hub_root, "post_001")
    assert baseline["status"] == "published"
    with pytest.raises(ValueError, match="invalid approval transition"):
        hub_mod.set_post_approval(
            hub_root,
            post_id="post_001",
            status="draft",
            updated_by="alice",
            note="Rewind to draft should be blocked from published.",
        )
