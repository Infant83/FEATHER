from __future__ import annotations

from federlicht import section_ast


def test_build_section_ast_generates_sections_and_claim_bindings() -> None:
    claim_packet = {
        "claims": [
            {"claim_id": "C001", "claim_text": "A", "evidence_ids": ["E001"]},
            {"claim_id": "C002", "claim_text": "B", "evidence_ids": ["E002"]},
        ]
    }
    ast = section_ast.build_section_ast(
        required_sections=["Executive Summary", "Key Findings", "Risks & Gaps"],
        claim_packet=claim_packet,
        report_intent="research",
        depth="deep",
    )
    assert ast["schema_version"] == "section_ast.v1"
    assert len(ast["sections"]) == 3
    assert ast["sections"][0]["section_id"] == "S01"
    assert "objective" in ast["sections"][0]


def test_format_section_ast_outline_contains_claim_registry_text() -> None:
    ast = {
        "schema_version": "section_ast.v1",
        "report_intent": "research",
        "depth": "deep",
        "sections": [
            {"section_id": "S01", "title": "Executive Summary", "objective": "obj", "claim_ids": ["C001"]},
        ],
        "claim_registry": {"C001": "pilot benchmark improved throughput"},
    }
    text = section_ast.format_section_ast_outline(ast)
    assert "Section AST (v1)" in text
    assert "C001" in text
    assert "pilot benchmark" in text


def test_apply_section_rewrite_updates_target_section() -> None:
    ast = {
        "sections": [
            {"section_id": "S01", "title": "Executive Summary", "revision": ""},
            {"section_id": "S02", "title": "Key Findings", "revision": ""},
        ]
    }
    updated = section_ast.apply_section_rewrite(ast, section_id="S02", revised_text="revised text")
    assert updated["sections"][1]["revision"] == "revised text"
    assert updated["sections"][0]["revision"] == ""


def test_build_rewrite_tasks_returns_only_missing_sections() -> None:
    ast = {
        "sections": [
            {"section_id": "S01", "title": "Executive Summary", "objective": "obj1", "claim_ids": ["C001"]},
            {"section_id": "S02", "title": "Key Findings", "objective": "obj2", "claim_ids": ["C002"]},
        ],
        "claim_registry": {"C001": "a", "C002": "b"},
    }
    tasks = section_ast.build_rewrite_tasks(ast, missing_sections=["Key Findings"])
    assert len(tasks) == 1
    assert tasks[0]["section_id"] == "S02"
    assert tasks[0]["claims"][0]["claim_id"] == "C002"
