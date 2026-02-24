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


def test_build_quality_contract_consistency_pass() -> None:
    summary_payload = {
        "summary": {
            "overall": 74.0,
            "claim_support_ratio": 58.0,
            "unsupported_claim_count": 12.0,
            "evidence_density_score": 66.0,
            "section_coherence_score": 69.0,
        }
    }
    contract_payload = {
        "metric_version": runner.QUALITY_CONTRACT_METRIC_VERSION,
        "metric_source": "final_signals",
        "final_signals": {
            "overall": 73.0,
            "claim_support_ratio": 55.0,
            "unsupported_claim_count": 10.0,
            "evidence_density_score": 64.0,
            "section_coherence_score": 66.0,
        },
        "selected_eval": {
            "overall": 73.0,
            "claim_support_ratio": 55.0,
            "unsupported_claim_count": 10.0,
            "evidence_density_score": 64.0,
            "section_coherence_score": 66.0,
        }
    }
    result = runner.build_quality_contract_consistency(
        summary_payload,
        contract_payload,
        max_overall_delta=3.0,
        max_claim_support_delta=8.0,
        max_unsupported_delta=8.0,
        max_evidence_density_delta=8.0,
        max_section_coherence_delta=8.0,
    )
    assert result["pass"] is True
    assert result["skipped"] is False
    assert result["stale"] is False
    assert result["failed_checks"] == []
    assert result["metric_source"] == "final_signals"


def test_build_quality_contract_consistency_fail() -> None:
    summary_payload = {
        "summary": {
            "overall": 82.0,
            "claim_support_ratio": 62.0,
            "unsupported_claim_count": 11.0,
            "evidence_density_score": 68.0,
            "section_coherence_score": 73.0,
        }
    }
    contract_payload = {
        "metric_version": runner.QUALITY_CONTRACT_METRIC_VERSION,
        "metric_source": "final_signals",
        "final_signals": {
            "overall": 72.0,
            "claim_support_ratio": 38.0,
            "unsupported_claim_count": 25.0,
            "evidence_density_score": 45.0,
            "section_coherence_score": 52.0,
        }
    }
    result = runner.build_quality_contract_consistency(
        summary_payload,
        contract_payload,
        max_overall_delta=2.5,
        max_claim_support_delta=8.0,
        max_unsupported_delta=8.0,
        max_evidence_density_delta=8.0,
        max_section_coherence_delta=8.0,
    )
    assert result["pass"] is False
    assert result["skipped"] is False
    assert result["stale"] is False
    assert result["metric_source"] == "final_signals"
    assert len(result["failed_checks"]) >= 3


def test_build_quality_contract_consistency_skips_stale_contract() -> None:
    summary_payload = {
        "summary": {
            "overall": 82.0,
            "claim_support_ratio": 62.0,
            "unsupported_claim_count": 11.0,
            "evidence_density_score": 68.0,
            "section_coherence_score": 73.0,
        }
    }
    contract_payload = {
        "metric_source": "selected_eval",
        "selected_eval": {
            "overall": 70.0,
            "claim_support_ratio": 30.0,
            "unsupported_claim_count": 30.0,
            "evidence_density_score": 40.0,
            "section_coherence_score": 45.0,
        },
    }
    result = runner.build_quality_contract_consistency(summary_payload, contract_payload)
    assert result["pass"] is True
    assert result["skipped"] is True
    assert result["stale"] is True
    assert "legacy_metric_source" in str(result["stale_reason"])
    assert result["failed_checks"] == []


def test_build_gate_report_markdown_includes_contract_consistency() -> None:
    summary_payload = {
        "rows_count": 1,
        "summary": {
            "overall": 72.0,
            "claim_support_ratio": 56.0,
            "unsupported_claim_count": 13.0,
            "evidence_density_score": 64.0,
            "section_coherence_score": 68.0,
        },
    }
    consistency = {
        "pass": True,
        "skipped": False,
        "stale": False,
        "stale_reason": "",
        "metric_version": runner.QUALITY_CONTRACT_METRIC_VERSION,
        "expected_metric_version": runner.QUALITY_CONTRACT_METRIC_VERSION,
        "metric_source": "selected_eval",
        "benchmark_summary": summary_payload["summary"],
        "quality_contract_metrics": {
            "overall": 71.0,
            "claim_support_ratio": 55.0,
            "unsupported_claim_count": 12.0,
            "evidence_density_score": 63.0,
            "section_coherence_score": 67.0,
        },
        "delta": {
            "overall": 1.0,
            "claim_support_ratio": 1.0,
            "unsupported_claim_count": 1.0,
            "evidence_density_score": 1.0,
            "section_coherence_score": 1.0,
        },
        "abs_delta": {
            "overall": 1.0,
            "claim_support_ratio": 1.0,
            "unsupported_claim_count": 1.0,
            "evidence_density_score": 1.0,
            "section_coherence_score": 1.0,
        },
        "thresholds": {
            "overall": 2.5,
            "claim_support_ratio": 8.0,
            "unsupported_claim_count": 8.0,
            "evidence_density_score": 8.0,
            "section_coherence_score": 8.0,
        },
        "failed_checks": [],
    }
    text = runner.build_gate_report_markdown(
        summary_payload,
        "gate-result | PASS",
        0,
        contract_consistency=consistency,
    )
    assert "## Quality Contract Consistency" in text
    assert "Metric Delta (benchmark - quality_contract)" in text
    assert "| overall |" in text
    assert "metric_version" in text


def test_extract_quality_contract_metrics_respects_metric_source_final_signals() -> None:
    payload = {
        "metric_source": "final_signals",
        "selected_eval": {
            "overall": 88.0,
            "claim_support_ratio": 80.0,
            "unsupported_claim_count": 2.0,
            "evidence_density_score": 85.0,
            "section_coherence_score": 84.0,
        },
        "final_signals": {
            "overall": 72.0,
            "claim_support_ratio": 54.0,
            "unsupported_claim_count": 16.0,
            "evidence_density_score": 66.0,
            "section_coherence_score": 68.0,
        },
    }
    metrics = runner.extract_quality_contract_metrics(payload)
    assert metrics["overall"] == 72.0
    assert metrics["claim_support_ratio"] == 54.0
    assert metrics["unsupported_claim_count"] == 16.0
