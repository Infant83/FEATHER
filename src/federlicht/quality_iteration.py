from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .quality_profiles import QUALITY_PROFILE_NONE, normalize_quality_profile


@dataclass(frozen=True)
class QualityIterationPolicy:
    min_iterations: int
    max_iterations: int
    plateau_delta: float
    plateau_patience: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "min_iterations": int(self.min_iterations),
            "max_iterations": int(self.max_iterations),
            "plateau_delta": float(self.plateau_delta),
            "plateau_patience": int(self.plateau_patience),
        }


_POLICIES: dict[str, QualityIterationPolicy] = {
    QUALITY_PROFILE_NONE: QualityIterationPolicy(
        min_iterations=0,
        max_iterations=3,
        plateau_delta=1.2,
        plateau_patience=1,
    ),
    "smoke": QualityIterationPolicy(
        min_iterations=1,
        max_iterations=2,
        plateau_delta=1.0,
        plateau_patience=1,
    ),
    "baseline": QualityIterationPolicy(
        min_iterations=1,
        max_iterations=4,
        plateau_delta=0.9,
        plateau_patience=1,
    ),
    "professional": QualityIterationPolicy(
        min_iterations=2,
        max_iterations=5,
        plateau_delta=0.8,
        plateau_patience=2,
    ),
    "world_class": QualityIterationPolicy(
        min_iterations=3,
        max_iterations=7,
        plateau_delta=0.7,
        plateau_patience=2,
    ),
}


def policy_for_profile(profile: object) -> QualityIterationPolicy:
    key = normalize_quality_profile(profile)
    return _POLICIES.get(key, _POLICIES[QUALITY_PROFILE_NONE])


def resolve_iteration_plan(
    *,
    profile: object,
    gate_enabled: bool,
    requested_iterations: int,
    auto_extra_iterations: int,
) -> dict[str, Any]:
    policy = policy_for_profile(profile)
    requested = max(0, int(requested_iterations or 0))
    auto_extra = max(0, int(auto_extra_iterations or 0))

    if gate_enabled:
        base = max(requested, policy.min_iterations)
        effective = min(policy.max_iterations, base + auto_extra)
    else:
        base = requested
        effective = min(policy.max_iterations, base)
    if gate_enabled and effective < policy.min_iterations:
        effective = policy.min_iterations
    return {
        "policy": policy.as_dict(),
        "requested_iterations": requested,
        "base_iterations": base,
        "effective_iterations": max(0, effective),
        "auto_extra_iterations": auto_extra,
    }


def compute_delta(previous: dict[str, Any], current: dict[str, Any]) -> dict[str, float]:
    def _to_float(value: Any) -> float:
        try:
            return float(value)
        except Exception:
            return 0.0

    return {
        "overall": round(_to_float(current.get("overall")) - _to_float(previous.get("overall")), 4),
        "claim_support_ratio": round(
            _to_float(current.get("claim_support_ratio")) - _to_float(previous.get("claim_support_ratio")), 4
        ),
        "unsupported_claim_count": round(
            _to_float(current.get("unsupported_claim_count")) - _to_float(previous.get("unsupported_claim_count")), 4
        ),
        "section_coherence_score": round(
            _to_float(current.get("section_coherence_score")) - _to_float(previous.get("section_coherence_score")), 4
        ),
    }


def is_plateau_delta(delta: dict[str, Any], *, plateau_delta: float) -> bool:
    threshold = max(0.1, float(plateau_delta))
    def _abs(name: str) -> float:
        try:
            return abs(float(delta.get(name, 0.0)))
        except Exception:
            return 0.0

    return bool(
        _abs("overall") < threshold
        and _abs("claim_support_ratio") < max(1.0, threshold * 2.0)
        and _abs("section_coherence_score") < max(1.0, threshold * 2.0)
        and _abs("unsupported_claim_count") <= 1.0
    )


def build_focus_directives(
    *,
    profile_label: str,
    targets: dict[str, float],
    current_signals: dict[str, Any],
    unsupported_examples: list[str] | None = None,
) -> str:
    def _to_float(value: Any, default: float = 0.0) -> float:
        try:
            return float(value)
        except Exception:
            return default

    lines: list[str] = [
        f"Quality profile: {profile_label}",
        "Current score snapshot vs gate target:",
        (
            f"- overall: {_to_float(current_signals.get('overall')):.2f} "
            f"(target >= {_to_float(targets.get('min_overall')):.2f})"
        ),
        (
            f"- claim_support_ratio: {_to_float(current_signals.get('claim_support_ratio')):.2f} "
            f"(target >= {_to_float(targets.get('min_claim_support')):.2f})"
        ),
        (
            f"- unsupported_claim_count: {_to_float(current_signals.get('unsupported_claim_count')):.2f} "
            f"(target <= {_to_float(targets.get('max_unsupported')):.2f})"
        ),
        (
            f"- section_coherence_score: {_to_float(current_signals.get('section_coherence_score')):.2f} "
            f"(target >= {_to_float(targets.get('min_section_coherence')):.2f})"
        ),
        "",
        "Improvement priorities:",
    ]
    if _to_float(current_signals.get("claim_support_ratio")) < _to_float(targets.get("min_claim_support")):
        lines.append(
            "- Increase claim grounding: attach direct citations to high-impact claims, and avoid claim-only prose."
        )
    if _to_float(current_signals.get("unsupported_claim_count")) > _to_float(targets.get("max_unsupported"), 1e9):
        lines.append(
            "- Reduce unsupported claims: convert weak assertions to bounded statements or add verifiable sources."
        )
    if _to_float(current_signals.get("section_coherence_score")) < _to_float(targets.get("min_section_coherence")):
        lines.append(
            "- Improve section coherence: add section opening claim, evidence synthesis, and transition sentence."
        )
    if _to_float(current_signals.get("overall")) < _to_float(targets.get("min_overall")):
        lines.append(
            "- Raise overall rigor: strengthen method transparency and results traceability without adding fluff."
        )
    samples = [item.strip() for item in (unsupported_examples or []) if str(item or "").strip()]
    if samples:
        lines.extend(["", "Unsupported claim examples (prioritize fixes):"])
        for item in samples[:5]:
            lines.append(f"- {item[:220]}")
    return "\n".join(lines).strip()


def quality_gate_distance(signals: dict[str, Any], targets: dict[str, float]) -> dict[str, float]:
    def _to_float(value: Any, default: float = 0.0) -> float:
        try:
            return float(value)
        except Exception:
            return default

    overall = _to_float(signals.get("overall"))
    support = _to_float(signals.get("claim_support_ratio"))
    unsupported = _to_float(signals.get("unsupported_claim_count"))
    coherence = _to_float(signals.get("section_coherence_score"))
    min_overall = _to_float(targets.get("min_overall"))
    min_support = _to_float(targets.get("min_claim_support"))
    max_unsupported = _to_float(targets.get("max_unsupported"), -1.0)
    min_coherence = _to_float(targets.get("min_section_coherence"))
    deficits = {
        "overall": max(0.0, min_overall - overall) if min_overall > 0 else 0.0,
        "claim_support_ratio": max(0.0, min_support - support) if min_support > 0 else 0.0,
        "unsupported_claim_count": (
            max(0.0, unsupported - max_unsupported) if max_unsupported >= 0 else 0.0
        ),
        "section_coherence_score": max(0.0, min_coherence - coherence) if min_coherence > 0 else 0.0,
    }
    weighted = (
        deficits["overall"] * 1.0
        + deficits["claim_support_ratio"] * 0.7
        + deficits["unsupported_claim_count"] * 1.1
        + deficits["section_coherence_score"] * 0.9
    )
    failure_count = sum(1 for _, value in deficits.items() if value > 0.0)
    deficits["distance"] = round(weighted, 4)
    deficits["failure_count"] = float(failure_count)
    return deficits


def candidate_rank_tuple(evaluation: dict[str, Any], targets: dict[str, float]) -> tuple[float, float, float, float]:
    gate_pass = bool(evaluation.get("quality_gate_pass"))
    deficits = quality_gate_distance(evaluation, targets)
    distance = float(deficits.get("distance", 0.0))
    failure_count = float(deficits.get("failure_count", 0.0))
    overall = float(evaluation.get("overall", 0.0) or 0.0)
    return (
        1.0 if gate_pass else 0.0,
        -failure_count,
        -distance,
        overall,
    )
