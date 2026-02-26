from __future__ import annotations

import federlicht.slide_pipeline as slide_pipeline


def _sample_claim_packet() -> dict:
    return {
        "schema_version": "v1",
        "claims": [
            {
                "claim_id": "C001",
                "claim_text": "Method A reduces latency under constrained routing workloads.",
                "section_hint": "scope_methodology",
                "evidence_ids": ["E001", "E002"],
                "source_kind": "doi",
                "score": 0.91,
            },
            {
                "claim_id": "C002",
                "claim_text": "Benchmark variance remains high in edge traffic bursts.",
                "section_hint": "risks_gaps",
                "evidence_ids": ["E003"],
                "source_kind": "web",
                "score": 0.82,
            },
            {
                "claim_id": "C003",
                "claim_text": "Pilot deployment shows improvement in mean response time.",
                "section_hint": "key_findings",
                "evidence_ids": ["E004"],
                "source_kind": "arxiv",
                "score": 0.87,
            },
        ],
        "evidence_registry": [
            {"evidence_id": "E001", "ref": "https://doi.org/10.1000/demo"},
            {"evidence_id": "E002", "ref": "./archive/openalex/text/a1.txt"},
            {"evidence_id": "E003", "ref": "https://example.com/risk-note"},
            {"evidence_id": "E004", "ref": "./archive/arxiv/text/2401.01234.txt"},
        ],
    }


def test_build_slide_outline_from_claim_packet_and_validate() -> None:
    outline = slide_pipeline.build_slide_outline(
        report_prompt="Build a decision briefing for rollout readiness.",
        depth="deep",
        audience="operator board",
        time_budget_minutes=25,
        target_slide_count=6,
        claim_packet=_sample_claim_packet(),
    )
    assert outline["schema_version"] == slide_pipeline.SLIDE_OUTLINE_SCHEMA_VERSION
    slides = list(outline.get("slides") or [])
    assert len(slides) == 5
    assert slides[0]["intent"] == "intro"
    assert slides[-1]["intent"] == "summary"
    errors = slide_pipeline.validate_slide_outline(outline)
    assert errors == []


def test_validate_slide_outline_reports_errors() -> None:
    bad = {
        "schema_version": "broken",
        "created_at": "now",
        "meta": {"depth": "x", "audience": "", "time_budget_minutes": 0, "target_slide_count": 0},
        "slides": [{"slide_id": "SLIDE-01"}],
    }
    errors = slide_pipeline.validate_slide_outline(bad)
    assert errors
    assert any("schema_version" in err for err in errors)
    assert any("meta.depth" in err for err in errors)
    assert any("missing key" in err for err in errors)


def test_build_slide_ast_and_validate() -> None:
    outline = {
        "schema_version": slide_pipeline.SLIDE_OUTLINE_SCHEMA_VERSION,
        "created_at": "2026-02-26T10:00:00",
        "meta": {
            "depth": "normal",
            "audience": "general",
            "time_budget_minutes": 15,
            "target_slide_count": 4,
            "source": "prompt_only",
        },
        "slides": [
            {
                "slide_id": "SLIDE-01",
                "intent": "methodology",
                "title": "Method Scope",
                "key_claim": "Method steps and assumptions.",
                "evidence_refs": ["./archive/local/text/method.txt"],
                "visual_type": "diagram",
            },
            {
                "slide_id": "SLIDE-02",
                "intent": "evidence",
                "title": "Evidence Table",
                "key_claim": "Evidence coverage by source category.",
                "evidence_refs": ["./archive/openalex/text/a.txt"],
                "visual_type": "table",
            },
            {
                "slide_id": "SLIDE-03",
                "intent": "analysis",
                "title": "Trend Chart",
                "key_claim": "Trend shows sustained improvement over baseline.",
                "evidence_refs": ["./archive/arxiv/text/x.txt"],
                "visual_type": "chart",
            },
            {
                "slide_id": "SLIDE-04",
                "intent": "summary",
                "title": "Summary",
                "key_claim": "Recommended next action and validation gate.",
                "evidence_refs": [],
                "visual_type": "bullets",
            },
        ],
    }
    slide_ast = slide_pipeline.build_slide_ast(outline, style_pack="executive_light")
    assert slide_ast["schema_version"] == slide_pipeline.SLIDE_AST_SCHEMA_VERSION
    errors = slide_pipeline.validate_slide_ast(slide_ast)
    assert errors == []
    blocks = {
        entry["slide_id"]: [item.get("type") for item in (entry.get("body_blocks") or [])]
        for entry in slide_ast.get("slides", [])
    }
    assert "diagram" in blocks["SLIDE-01"]
    assert "table" in blocks["SLIDE-02"]
    assert "chart" in blocks["SLIDE-03"]
    assert "bullets" in blocks["SLIDE-04"]


def test_formatters_render_human_readable_summary() -> None:
    outline = slide_pipeline.build_slide_outline(
        report_prompt="Short briefing prompt",
        target_slide_count=4,
        claim_packet=None,
    )
    outline_text = slide_pipeline.format_slide_outline(outline)
    assert "Slide Outline (v1)" in outline_text
    slide_ast = slide_pipeline.build_slide_ast(outline)
    ast_text = slide_pipeline.format_slide_ast(slide_ast)
    assert "Slide AST (v1)" in ast_text
    assert "style pack" in ast_text
