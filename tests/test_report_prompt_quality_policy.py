from __future__ import annotations

from types import SimpleNamespace

from federlicht import prompts


def _format_instructions():
    return SimpleNamespace(
        section_heading_instruction="",
        report_skeleton="",
        format_instruction="",
        citation_instruction="",
        latex_safety_instruction="",
    )


def _template_spec():
    return SimpleNamespace(name="default", source="builtin/default")


def test_plan_prompt_includes_method_and_result_tracks() -> None:
    prompt = prompts.build_plan_prompt("Korean")
    assert "방법론/소스 선정 기준" in prompt
    assert "핵심 결과/비교 분석" in prompt
    assert "리스크/불확실성" in prompt


def test_evidence_prompt_requests_evidence_ledger() -> None:
    prompt = prompts.build_evidence_prompt("Korean")
    assert "Evidence Ledger" in prompt
    assert "Claim | Evidence summary | Source URL/path" in prompt
    assert "Strength(high/medium/low)" in prompt


def test_writer_prompt_requires_method_transparency_and_traceability() -> None:
    prompt = prompts.build_writer_prompt(
        _format_instructions(),
        "",
        _template_spec(),
        ["Executive Summary", "Methods & Evidence", "Results & Benchmarks", "Risks & Gaps"],
        "md",
        "Korean",
        depth="deep",
        template_rigidity="balanced",
        figures_enabled=False,
        figures_mode="auto",
        artwork_enabled=False,
    )
    assert "방법론 투명성" in prompt
    assert "evidence matrix" in prompt
    assert "확정 사실과 불확실/추정 항목을 분리" in prompt
    assert "섹션 시작 문장과 끝 문장" in prompt

