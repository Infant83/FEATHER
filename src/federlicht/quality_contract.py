from __future__ import annotations

QUALITY_CONTRACT_METRIC_VERSION = "qc-metrics.v2"
QUALITY_CONTRACT_PRIMARY_SOURCE = "final_signals"


def detect_quality_contract_staleness(
    payload: dict | None,
    *,
    expected_metric_version: str = QUALITY_CONTRACT_METRIC_VERSION,
) -> tuple[bool, str]:
    if not isinstance(payload, dict):
        return True, "invalid_payload"
    metric_version = str(payload.get("metric_version") or "").strip().lower()
    expected = str(expected_metric_version or "").strip().lower()
    metric_source = str(payload.get("metric_source") or "").strip().lower()

    if metric_source and metric_source != QUALITY_CONTRACT_PRIMARY_SOURCE:
        return True, f"legacy_metric_source:{metric_source}"
    if not metric_version:
        return True, "missing_metric_version"
    if expected and metric_version != expected:
        return True, f"metric_version_mismatch:{metric_version}!={expected}"
    return False, ""

