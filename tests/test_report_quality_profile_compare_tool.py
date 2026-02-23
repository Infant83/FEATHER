from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def _load_module():
    path = Path("tools/report_quality_profile_compare.py")
    spec = importlib.util.spec_from_file_location("report_quality_profile_compare", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tool = _load_module()


def test_evaluate_profiles_has_world_class_fail_for_mid_summary() -> None:
    summary = {
        "overall": 74.0,
        "claim_support_ratio": 52.0,
        "unsupported_claim_count": 18.0,
        "section_coherence_score": 66.0,
    }
    rows = tool.evaluate_profiles(summary)
    by_profile = {row["profile"]: row for row in rows}
    assert by_profile["baseline"]["pass"] is True
    assert by_profile["professional"]["pass"] is False
    assert by_profile["world_class"]["pass"] is False


def test_load_summary_supports_bundle_and_render_markdown(tmp_path: Path) -> None:
    payload = {
        "summary": {
            "overall": 80.0,
            "claim_support_ratio": 62.0,
            "unsupported_claim_count": 11.0,
            "section_coherence_score": 76.0,
        }
    }
    path = tmp_path / "summary.json"
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    summary = tool._load_summary(path)
    rows = tool.evaluate_profiles(summary)
    md = tool.render_markdown(summary, rows)
    assert "Quality Profile Compare" in md
    assert "| world_class |" in md

