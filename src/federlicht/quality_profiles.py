from __future__ import annotations

from dataclasses import dataclass
from typing import Any


QUALITY_PROFILE_NONE = "none"
QUALITY_PROFILE_DEEP_RESEARCH = "deep_research"


@dataclass(frozen=True)
class QualityGateThresholds:
    min_overall: float
    min_claim_support: float
    max_unsupported: float
    min_section_coherence: float

    def as_dict(self) -> dict[str, float]:
        return {
            "min_overall": float(self.min_overall),
            "min_claim_support": float(self.min_claim_support),
            "max_unsupported": float(self.max_unsupported),
            "min_section_coherence": float(self.min_section_coherence),
        }


@dataclass(frozen=True)
class QualityProfileSpec:
    name: str
    label: str
    purpose: str
    thresholds: QualityGateThresholds


QUALITY_PROFILES: dict[str, QualityProfileSpec] = {
    "smoke": QualityProfileSpec(
        name="smoke",
        label="Smoke / Pipeline Health",
        purpose="Checks basic generation stability only. Not a publication-quality bar.",
        thresholds=QualityGateThresholds(
            min_overall=65.0,
            min_claim_support=2.0,
            max_unsupported=70.0,
            min_section_coherence=55.0,
        ),
    ),
    "baseline": QualityProfileSpec(
        name="baseline",
        label="Baseline Research",
        purpose="Minimum practical report quality for routine regression checks.",
        thresholds=QualityGateThresholds(
            min_overall=70.0,
            min_claim_support=40.0,
            max_unsupported=25.0,
            min_section_coherence=60.0,
        ),
    ),
    "professional": QualityProfileSpec(
        name="professional",
        label="Professional Research",
        purpose="Production-quality research report bar for stakeholder review.",
        thresholds=QualityGateThresholds(
            min_overall=76.0,
            min_claim_support=50.0,
            max_unsupported=18.0,
            min_section_coherence=68.0,
        ),
    ),
    QUALITY_PROFILE_DEEP_RESEARCH: QualityProfileSpec(
        name=QUALITY_PROFILE_DEEP_RESEARCH,
        label="Deep Research",
        purpose="High-rigor deep research quality gate for publication-ready deliverables.",
        thresholds=QualityGateThresholds(
            min_overall=82.0,
            min_claim_support=60.0,
            max_unsupported=12.0,
            min_section_coherence=75.0,
        ),
    ),
}


def quality_profile_choices() -> tuple[str, ...]:
    # Canonical choices are exposed to CLI/help; legacy aliases are normalized.
    return (QUALITY_PROFILE_NONE, "smoke", "baseline", "professional", QUALITY_PROFILE_DEEP_RESEARCH)


def normalize_quality_profile(value: object) -> str:
    token = str(value or "").strip().lower()
    if not token or token in {"off", "false", "0", QUALITY_PROFILE_NONE}:
        return QUALITY_PROFILE_NONE
    if token in {
        "deepresearch",
        "deep-research",
        QUALITY_PROFILE_DEEP_RESEARCH,
        "world",
        "worldclass",
        "world-class",
        "world_class",
        "wc",
    }:
        return QUALITY_PROFILE_DEEP_RESEARCH
    if token in QUALITY_PROFILES:
        return token
    return QUALITY_PROFILE_NONE


def get_quality_profile(profile: object) -> QualityProfileSpec | None:
    normalized = normalize_quality_profile(profile)
    return QUALITY_PROFILES.get(normalized)


def _override_threshold(
    current: float,
    override: object,
    *,
    disabled_value: float,
    mode: str,
) -> float:
    try:
        value = float(override)  # type: ignore[arg-type]
    except Exception:
        return float(current)
    if mode == "min":
        if value <= 0:
            return float(current)
        return float(value)
    if mode == "max":
        if value < 0:
            return float(current)
        return float(value)
    if value == disabled_value:
        return float(current)
    return float(value)


def resolve_quality_gate_targets(
    *,
    profile: object = QUALITY_PROFILE_NONE,
    min_overall: object = 0.0,
    min_claim_support: object = 0.0,
    max_unsupported: object = -1.0,
    min_section_coherence: object = 0.0,
) -> dict[str, Any]:
    selected_profile = get_quality_profile(profile)
    if selected_profile:
        thresholds = selected_profile.thresholds.as_dict()
        source = f"profile:{selected_profile.name}"
    else:
        thresholds = QualityGateThresholds(
            min_overall=0.0,
            min_claim_support=0.0,
            max_unsupported=-1.0,
            min_section_coherence=0.0,
        ).as_dict()
        source = "custom"

    thresholds["min_overall"] = _override_threshold(
        thresholds["min_overall"],
        min_overall,
        disabled_value=0.0,
        mode="min",
    )
    thresholds["min_claim_support"] = _override_threshold(
        thresholds["min_claim_support"],
        min_claim_support,
        disabled_value=0.0,
        mode="min",
    )
    thresholds["max_unsupported"] = _override_threshold(
        thresholds["max_unsupported"],
        max_unsupported,
        disabled_value=-1.0,
        mode="max",
    )
    thresholds["min_section_coherence"] = _override_threshold(
        thresholds["min_section_coherence"],
        min_section_coherence,
        disabled_value=0.0,
        mode="min",
    )

    enabled = any(
        (
            float(thresholds["min_overall"]) > 0.0,
            float(thresholds["min_claim_support"]) > 0.0,
            float(thresholds["max_unsupported"]) >= 0.0,
            float(thresholds["min_section_coherence"]) > 0.0,
        )
    )
    strict_mode = bool(
        float(thresholds["min_overall"]) >= 78.0
        or float(thresholds["min_claim_support"]) >= 50.0
        or float(thresholds["min_section_coherence"]) >= 70.0
    )
    effective_band = classify_quality_band(thresholds)
    return {
        "profile": normalize_quality_profile(profile),
        "profile_label": selected_profile.label if selected_profile else "Custom",
        "profile_purpose": selected_profile.purpose if selected_profile else "Custom threshold set.",
        "thresholds": thresholds,
        "enabled": enabled,
        "strict_mode": strict_mode,
        "source": source,
        "effective_band": effective_band,
    }


def classify_quality_band(thresholds: dict[str, float]) -> str:
    min_overall = float(thresholds.get("min_overall", 0.0))
    min_support = float(thresholds.get("min_claim_support", 0.0))
    max_unsupported = float(thresholds.get("max_unsupported", -1.0))
    min_coherence = float(thresholds.get("min_section_coherence", 0.0))

    def _meets(spec: QualityProfileSpec) -> bool:
        target = spec.thresholds
        return (
            min_overall >= target.min_overall
            and min_support >= target.min_claim_support
            and max_unsupported >= 0.0
            and max_unsupported <= target.max_unsupported
            and min_coherence >= target.min_section_coherence
        )

    if _meets(QUALITY_PROFILES[QUALITY_PROFILE_DEEP_RESEARCH]):
        return QUALITY_PROFILE_DEEP_RESEARCH
    if _meets(QUALITY_PROFILES["professional"]):
        return "professional"
    if _meets(QUALITY_PROFILES["baseline"]):
        return "baseline"
    if _meets(QUALITY_PROFILES["smoke"]):
        return "smoke"
    if (
        min_overall <= 0.0
        and min_support <= 0.0
        and max_unsupported < 0.0
        and min_coherence <= 0.0
    ):
        return "disabled"
    return "custom"
