from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def _load_gate_module():
    path = Path("tools/report_quality_regression_gate.py")
    spec = importlib.util.spec_from_file_location("report_quality_regression_gate", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gate = _load_gate_module()


def test_run_gate_passes_with_good_averages() -> None:
    rows = [
        {
            "overall": 78.0,
            "claim_support_ratio": 68.0,
            "unsupported_claim_count": 10.0,
            "section_coherence_score": 72.0,
        },
        {
            "overall": 74.0,
            "claim_support_ratio": 54.0,
            "unsupported_claim_count": 16.0,
            "section_coherence_score": 66.0,
        },
    ]
    ok, errors = gate.run_gate(
        rows,
        min_overall=70.0,
        min_claim_support=40.0,
        max_unsupported=25.0,
        min_section_coherence=60.0,
    )
    assert ok is True
    assert errors == []


def test_run_gate_fails_with_bad_averages() -> None:
    rows = [
        {
            "overall": 50.0,
            "claim_support_ratio": 10.0,
            "unsupported_claim_count": 80.0,
            "section_coherence_score": 30.0,
        }
    ]
    ok, errors = gate.run_gate(
        rows,
        min_overall=70.0,
        min_claim_support=40.0,
        max_unsupported=25.0,
        min_section_coherence=60.0,
    )
    assert ok is False
    assert len(errors) >= 3


def test_main_like_file_roundtrip(tmp_path: Path) -> None:
    rows = [
        {
            "overall": 75.0,
            "claim_support_ratio": 60.0,
            "unsupported_claim_count": 12.0,
            "section_coherence_score": 65.0,
        }
    ]
    path = tmp_path / "bench.json"
    path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    loaded = json.loads(path.read_text(encoding="utf-8"))
    ok, _ = gate.run_gate(
        loaded,
        min_overall=70.0,
        min_claim_support=40.0,
        max_unsupported=25.0,
        min_section_coherence=60.0,
    )
    assert ok is True


def test_load_rows_supports_bundle_shape() -> None:
    payload = {"rows": [{"overall": 72.0, "claim_support_ratio": 45.0, "unsupported_claim_count": 12.0, "section_coherence_score": 63.0}]}
    rows = gate._load_rows(payload)
    assert len(rows) == 1


def test_profile_policy_deep_research_makes_gate_stricter() -> None:
    rows = [
        {
            "overall": 79.0,
            "claim_support_ratio": 55.0,
            "unsupported_claim_count": 14.0,
            "section_coherence_score": 70.0,
        }
    ]
    baseline_policy = gate.resolve_quality_gate_targets(profile="baseline")
    baseline_targets = baseline_policy["thresholds"]
    ok_baseline, _ = gate.run_gate(
        rows,
        min_overall=baseline_targets["min_overall"],
        min_claim_support=baseline_targets["min_claim_support"],
        max_unsupported=baseline_targets["max_unsupported"],
        min_section_coherence=baseline_targets["min_section_coherence"],
    )
    assert ok_baseline is True

    world_policy = gate.resolve_quality_gate_targets(profile="deep_research")
    world_targets = world_policy["thresholds"]
    ok_world, errors_world = gate.run_gate(
        rows,
        min_overall=world_targets["min_overall"],
        min_claim_support=world_targets["min_claim_support"],
        max_unsupported=world_targets["max_unsupported"],
        min_section_coherence=world_targets["min_section_coherence"],
    )
    assert ok_world is False
    assert errors_world
