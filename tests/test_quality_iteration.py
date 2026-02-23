from __future__ import annotations

from federlicht.quality_iteration import (
    build_focus_directives,
    compute_delta,
    is_plateau_delta,
    policy_for_profile,
    resolve_iteration_plan,
)


def test_policy_for_profile_world_class_has_higher_min_iterations() -> None:
    world = policy_for_profile("world_class")
    baseline = policy_for_profile("baseline")
    assert world.min_iterations >= baseline.min_iterations
    assert world.max_iterations >= baseline.max_iterations


def test_resolve_iteration_plan_respects_profile_min_when_gate_enabled() -> None:
    plan = resolve_iteration_plan(
        profile="world_class",
        gate_enabled=True,
        requested_iterations=1,
        auto_extra_iterations=1,
    )
    assert plan["base_iterations"] >= 3
    assert plan["effective_iterations"] >= 3


def test_resolve_iteration_plan_no_gate_keeps_requested() -> None:
    plan = resolve_iteration_plan(
        profile="world_class",
        gate_enabled=False,
        requested_iterations=2,
        auto_extra_iterations=4,
    )
    assert plan["base_iterations"] == 2
    assert plan["effective_iterations"] == 2


def test_compute_delta_and_plateau() -> None:
    prev = {
        "overall": 70.0,
        "claim_support_ratio": 50.0,
        "unsupported_claim_count": 18.0,
        "section_coherence_score": 62.0,
    }
    cur_small = {
        "overall": 70.3,
        "claim_support_ratio": 50.5,
        "unsupported_claim_count": 18.0,
        "section_coherence_score": 62.4,
    }
    cur_large = {
        "overall": 73.0,
        "claim_support_ratio": 54.0,
        "unsupported_claim_count": 16.0,
        "section_coherence_score": 65.0,
    }
    d_small = compute_delta(prev, cur_small)
    d_large = compute_delta(prev, cur_large)
    assert is_plateau_delta(d_small, plateau_delta=0.8) is True
    assert is_plateau_delta(d_large, plateau_delta=0.8) is False


def test_build_focus_directives_includes_priority_hints() -> None:
    text = build_focus_directives(
        profile_label="world_class",
        targets={
            "min_overall": 82.0,
            "min_claim_support": 60.0,
            "max_unsupported": 12.0,
            "min_section_coherence": 75.0,
        },
        current_signals={
            "overall": 70.0,
            "claim_support_ratio": 45.0,
            "unsupported_claim_count": 22.0,
            "section_coherence_score": 60.0,
        },
        unsupported_examples=[
            "This claim has no citation and should be grounded.",
        ],
    )
    assert "Quality profile: world_class" in text
    assert "Increase claim grounding" in text
    assert "Reduce unsupported claims" in text
    assert "Improve section coherence" in text
    assert "Unsupported claim examples" in text

