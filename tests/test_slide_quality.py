from __future__ import annotations

import federlicht.slide_quality as slide_quality


def _good_slide_ast() -> dict:
    return {
        "schema_version": "slide_ast.v1",
        "slides": [
            {
                "slide_id": "SLIDE-01",
                "layout": "title_body",
                "title_block": {"headline": "Executive Framing", "subheadline": "Intro"},
                "body_blocks": [
                    {"type": "text", "text": "Decision objective and scope for this briefing."},
                    {"type": "bullets", "items": ["Goal", "Constraints", "Expected outcome"]},
                ],
                "citation_footer": {"refs": ["./archive/local/text/a.txt"], "source_policy": "claim-evidence-source"},
            },
            {
                "slide_id": "SLIDE-02",
                "layout": "title_two_column",
                "title_block": {"headline": "Evidence Snapshot", "subheadline": "Evidence"},
                "body_blocks": [
                    {"type": "text", "text": "Benchmark and evidence mapping."},
                    {
                        "type": "table",
                        "columns": ["Claim", "Evidence"],
                        "rows": [["Latency improves", "https://doi.org/10.1000/demo"]],
                    },
                ],
                "citation_footer": {"refs": ["https://doi.org/10.1000/demo"], "source_policy": "claim-evidence-source"},
            },
            {
                "slide_id": "SLIDE-03",
                "layout": "title_two_column",
                "title_block": {"headline": "Risks", "subheadline": "Risk"},
                "body_blocks": [
                    {"type": "text", "text": "Uncertainty and mitigation plan."},
                    {"type": "diagram", "engine": "mermaid", "spec": "flowchart LR\nA-->B"},
                ],
                "citation_footer": {"refs": ["https://example.com/risk"], "source_policy": "claim-evidence-source"},
            },
            {
                "slide_id": "SLIDE-04",
                "layout": "title_body",
                "title_block": {"headline": "Decision Summary", "subheadline": "Summary"},
                "body_blocks": [
                    {"type": "text", "text": "Recommended next action and validation gate."},
                    {"type": "bullets", "items": ["Run pilot", "Track KPI", "Review in 2 weeks"]},
                ],
                "citation_footer": {"refs": ["./archive/local/text/b.txt"], "source_policy": "claim-evidence-source"},
            },
        ],
    }


def _bad_slide_ast() -> dict:
    return {
        "schema_version": "slide_ast.v1",
        "slides": [
            {
                "slide_id": "SLIDE-01",
                "layout": "title_body",
                "title_block": {"headline": "Slide 1", "subheadline": "Analysis"},
                "body_blocks": [{"type": "bullets", "items": []}],
                "citation_footer": {"refs": [], "source_policy": ""},
            },
            {
                "slide_id": "SLIDE-02",
                "layout": "title_body",
                "title_block": {"headline": "Slide 2", "subheadline": "Analysis"},
                "body_blocks": [{"type": "text", "text": "x" * 1200}],
                "citation_footer": {"refs": [], "source_policy": ""},
            },
        ],
    }


def test_evaluate_slide_ast_quality_passes_for_balanced_deck() -> None:
    summary = slide_quality.evaluate_slide_ast_quality(_good_slide_ast())
    assert summary["quality_gate_pass"] is True
    assert summary["overall_score"] >= 78.0
    report_text = slide_quality.build_slide_quality_report(summary)
    assert "PASS" in report_text


def test_evaluate_slide_ast_quality_flags_unbalanced_deck() -> None:
    summary = slide_quality.evaluate_slide_ast_quality(_bad_slide_ast())
    assert summary["quality_gate_pass"] is False
    assert summary["overall_score"] < 78.0
    assert "traceability" in set(summary["gate_failures"]) or "density" in set(summary["gate_failures"])
    report_text = slide_quality.build_slide_quality_report(summary)
    assert "FAIL" in report_text


def test_revise_slide_ast_for_quality_improves_bad_case() -> None:
    bad = _bad_slide_ast()
    before = slide_quality.evaluate_slide_ast_quality(bad)
    revised, actions = slide_quality.revise_slide_ast_for_quality(bad, baseline_summary=before)
    after = slide_quality.evaluate_slide_ast_quality(revised)
    assert actions
    assert after["overall_score"] >= before["overall_score"]
