from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module():
    path = Path("tools/run_report_quality_gate.py")
    spec = importlib.util.spec_from_file_location("run_report_quality_gate", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = _load_module()


def test_build_gate_report_markdown_contains_key_sections() -> None:
    payload = {
        "rows_count": 1,
        "summary": {
            "overall": 72.0,
            "claim_support_ratio": 58.0,
            "unsupported_claim_count": 14.0,
            "evidence_density_score": 66.0,
            "section_coherence_score": 70.0,
        },
        "baseline_summary": {
            "overall": 70.0,
            "claim_support_ratio": 55.0,
            "unsupported_claim_count": 18.0,
            "evidence_density_score": 60.0,
            "section_coherence_score": 66.0,
        },
        "delta_summary": {
            "overall": 2.0,
            "claim_support_ratio": 3.0,
            "unsupported_claim_count": -4.0,
            "evidence_density_score": 6.0,
            "section_coherence_score": 4.0,
        },
        "suite": {"suite_id": "report_quality_v1"},
        "compare_markdown": "| metric | current | baseline | delta |\n| --- | ---: | ---: | ---: |",
    }
    text = runner.build_gate_report_markdown(payload, "gate-result | PASS", 0)
    assert "gate_result: PASS" in text
    assert "## Summary" in text
    assert "## Delta (current - baseline)" in text
    assert "## Compare Table" in text
