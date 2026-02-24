from __future__ import annotations

from federlicht.quality_contract import (
    QUALITY_CONTRACT_METRIC_VERSION,
    detect_quality_contract_staleness,
)


def test_detect_quality_contract_staleness_accepts_current_contract() -> None:
    stale, reason = detect_quality_contract_staleness(
        {
            "metric_version": QUALITY_CONTRACT_METRIC_VERSION,
            "metric_source": "final_signals",
        }
    )
    assert stale is False
    assert reason == ""


def test_detect_quality_contract_staleness_flags_legacy_source() -> None:
    stale, reason = detect_quality_contract_staleness(
        {
            "metric_version": QUALITY_CONTRACT_METRIC_VERSION,
            "metric_source": "selected_eval",
        }
    )
    assert stale is True
    assert "legacy_metric_source" in reason


def test_detect_quality_contract_staleness_flags_missing_version() -> None:
    stale, reason = detect_quality_contract_staleness({"metric_source": "final_signals"})
    assert stale is True
    assert reason == "missing_metric_version"

