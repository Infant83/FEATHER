from __future__ import annotations

from federlicht import report


def test_heuristic_quality_signals_reward_traceable_reports() -> None:
    required = ["Executive Summary", "Scope & Methodology", "Key Findings"]
    good_report = """
## Executive Summary
Industrial QC adoption remains early but measurable in optimization pilots [https://example.com/pilot].

## Scope & Methodology
We used explicit selection criteria and exclusion criteria across vendor case studies [https://example.com/method].

## Key Findings
Claim | Evidence summary | Source URL/path | Confidence | Limits
--- | --- | --- | --- | ---
Speedup in routing | Pilot benchmark vs baseline | https://example.com/benchmark | medium | small sample
"""
    weak_report = """
Quick summary without clear structure.
There might be improvements but no grounded references.
"""
    good = report.compute_heuristic_quality_signals(
        good_report,
        required,
        "md",
        depth="deep",
        report_intent="research",
    )
    weak = report.compute_heuristic_quality_signals(
        weak_report,
        required,
        "md",
        depth="deep",
        report_intent="research",
    )
    assert good["overall"] > weak["overall"]
    assert good["traceability"] >= weak["traceability"]
    assert good["claim_support_ratio"] >= weak["claim_support_ratio"]
    assert good["unsupported_claim_count"] <= weak["unsupported_claim_count"]


def test_heuristic_brief_mode_keeps_method_weight_lighter() -> None:
    required = ["Executive Summary", "Key Findings"]
    concise = """
## Executive Summary
Top recommendation: run a 12-week pilot with explicit stop/go criteria [https://example.com/policy].

## Key Findings
- Option A: lower risk, slower ROI [https://example.com/a]
- Option B: higher upside, integration risk [https://example.com/b]
"""
    signals = report.compute_heuristic_quality_signals(
        concise,
        required,
        "md",
        depth="brief",
        report_intent="briefing",
    )
    assert signals["overall"] >= 55.0
    assert "section_coherence_score" in signals
    assert "evidence_density_score" in signals


def test_heuristic_handles_html_headings_and_links() -> None:
    html_report = """
<html><body>
<h2>Executive Summary</h2>
<p>OpenClaw pilot outcome shows moderate automation gain <a href="https://example.com/pilot">[1]</a>.</p>
<h2>Key Findings</h2>
<p>Risk remains around IAM and audit trail <a href="https://example.com/risk">[2]</a>.</p>
</body></html>
"""
    signals = report.compute_heuristic_quality_signals(
        html_report,
        ["Executive Summary", "Key Findings"],
        "html",
        depth="brief",
        report_intent="briefing",
    )
    assert signals["section_coverage"] >= 99.0
    assert signals["citation_density"] > 0.0
    assert signals["claim_support_ratio"] > 0.0


def test_unsupported_claim_examples_detects_missing_citations() -> None:
    report_text = """
## Executive Summary
This line is grounded with citation [https://example.com/a].
This line states a strong claim without any source and should be flagged by detector.
"""
    examples = report._unsupported_claim_examples(report_text, "md", max_items=4)
    assert examples
    assert any("strong claim without any source" in item for item in examples)


def test_quality_gate_failures_supports_threshold_checks() -> None:
    signals = {
        "overall": 68.0,
        "claim_support_ratio": 38.0,
        "unsupported_claim_count": 29.0,
        "section_coherence_score": 52.0,
    }
    failures = report.quality_gate_failures(
        signals,
        min_overall=70.0,
        min_claim_support=45.0,
        max_unsupported=25.0,
        min_section_coherence=60.0,
    )
    assert len(failures) == 4
