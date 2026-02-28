from __future__ import annotations

import importlib.util
import json
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
    text = runner.build_gate_report_markdown(
        payload,
        "gate-result | PASS",
        0,
        gate_policy={
            "profile": "deep_research",
            "effective_band": "deep_research",
            "source": "profile:deep_research",
            "thresholds": {
                "min_overall": 82.0,
                "min_claim_support": 60.0,
                "max_unsupported": 12.0,
                "min_section_coherence": 75.0,
            },
        },
    )
    assert "gate_result: PASS" in text
    assert "gate_profile: deep_research" in text
    assert "gate_effective_band: deep_research" in text
    assert "## Summary" in text
    assert "## Delta (current - baseline)" in text
    assert "## Compare Table" in text


def test_evaluate_infographic_lint_detects_missing_source(tmp_path: Path) -> None:
    spec_path = tmp_path / "infographic_spec.json"
    spec_path.write_text(
        json.dumps(
            {
                "title": "demo",
                "charts": [{"id": "a", "type": "bar", "labels": ["A"], "datasets": [{"label": "x", "data": [1]}]}],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    lint = runner.evaluate_infographic_lint([spec_path])
    assert lint.get("pass") is False
    assert int(lint.get("failed_count", 0) or 0) >= 1
    assert int(lint.get("chart_count", 0) or 0) == 1
    assert float(lint.get("caption_meta_coverage_ratio", 0.0) or 0.0) < 100.0
    rows = lint.get("rows")
    assert isinstance(rows, list)
    assert rows
    issues = rows[0].get("issues")
    assert isinstance(issues, list)
    assert any("source is missing" in str(item) for item in issues)


def test_build_gate_report_markdown_includes_infographic_lint_block() -> None:
    payload = {
        "rows_count": 1,
        "summary": {
            "overall": 82.0,
            "claim_support_ratio": 70.0,
            "unsupported_claim_count": 5.0,
            "evidence_density_score": 90.0,
            "section_coherence_score": 80.0,
        },
    }
    text = runner.build_gate_report_markdown(
        payload,
        "gate-result | PASS",
        0,
        infographic_lint={
            "checked_count": 1,
            "failed_count": 1,
            "pass": False,
            "chart_count": 2,
            "caption_meta_complete_chart_count": 1,
            "caption_meta_coverage_ratio": 80.0,
            "caption_meta_complete_chart_ratio": 50.0,
            "rows": [
                {
                    "path": "demo.json",
                    "chart_count": 2,
                    "caption_meta_coverage_ratio": 80.0,
                    "caption_meta_complete_chart_count": 1,
                    "issues": ["charts[1] source is missing."],
                }
            ],
        },
    )
    assert "## Infographic Lint" in text
    assert "failed_specs: 1" in text
    assert "caption_meta_coverage_ratio: 80.00%" in text
    assert "caption_meta_complete_charts: 1/2 (50.00%)" in text
    assert "demo.json" in text


def test_should_enforce_strict_infographic_lint_deep_research_default() -> None:
    strict = runner.should_enforce_strict_infographic_lint(
        quality_profile="deep_research",
        explicit_strict=False,
        has_infographic_spec=True,
    )
    assert strict is True


def test_should_enforce_strict_infographic_lint_respects_profile_and_flag() -> None:
    strict_baseline = runner.should_enforce_strict_infographic_lint(
        quality_profile="baseline",
        explicit_strict=False,
        has_infographic_spec=True,
    )
    strict_explicit = runner.should_enforce_strict_infographic_lint(
        quality_profile="baseline",
        explicit_strict=True,
        has_infographic_spec=False,
    )
    assert strict_baseline is False
    assert strict_explicit is True
