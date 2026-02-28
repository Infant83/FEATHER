from __future__ import annotations

from federlicht.quality_profiles import (
    QUALITY_PROFILE_NONE,
    classify_quality_band,
    normalize_quality_profile,
    resolve_quality_gate_targets,
)


def test_normalize_quality_profile_aliases() -> None:
    assert normalize_quality_profile("worldclass") == "deep_research"
    assert normalize_quality_profile("world-class") == "deep_research"
    assert normalize_quality_profile("world_class") == "deep_research"
    assert normalize_quality_profile("deep_research") == "deep_research"
    assert normalize_quality_profile("off") == QUALITY_PROFILE_NONE


def test_resolve_quality_gate_targets_baseline_defaults() -> None:
    policy = resolve_quality_gate_targets(profile="baseline")
    targets = policy["thresholds"]
    assert policy["enabled"] is True
    assert targets["min_overall"] == 70.0
    assert targets["min_claim_support"] == 40.0
    assert targets["max_unsupported"] == 25.0
    assert targets["min_section_coherence"] == 60.0
    assert policy["effective_band"] == "baseline"


def test_resolve_quality_gate_targets_override_to_deep_research() -> None:
    policy = resolve_quality_gate_targets(
        profile="professional",
        min_overall=84.0,
        min_claim_support=62.0,
        max_unsupported=10.0,
        min_section_coherence=77.0,
    )
    targets = policy["thresholds"]
    assert policy["strict_mode"] is True
    assert targets["min_overall"] == 84.0
    assert targets["min_claim_support"] == 62.0
    assert targets["max_unsupported"] == 10.0
    assert targets["min_section_coherence"] == 77.0
    assert classify_quality_band(targets) == "deep_research"


def test_resolve_quality_gate_targets_none_and_disabled() -> None:
    policy = resolve_quality_gate_targets(profile="none")
    targets = policy["thresholds"]
    assert policy["enabled"] is False
    assert targets["min_overall"] == 0.0
    assert targets["min_claim_support"] == 0.0
    assert targets["max_unsupported"] == -1.0
    assert targets["min_section_coherence"] == 0.0
    assert policy["effective_band"] == "disabled"
