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


def test_plan_prompt_high_structure_includes_full_axes() -> None:
    prompt = prompts.build_plan_prompt(
        "Korean",
        depth="deep",
        template_rigidity="balanced",
        free_form=False,
    )
    assert "방법론/소스 선정 기준" in prompt
    assert "핵심 결과/비교 분석" in prompt
    assert "리스크/불확실성" in prompt


def test_plan_prompt_brief_allows_selective_axes() -> None:
    prompt = prompts.build_plan_prompt(
        "Korean",
        depth="brief",
        template_rigidity="balanced",
        free_form=False,
    )
    assert "요청 목적에 따라 필요한 축만 선택하세요." in prompt


def test_evidence_prompt_high_structure_requests_evidence_ledger() -> None:
    prompt = prompts.build_evidence_prompt(
        "Korean",
        depth="deep",
        template_rigidity="balanced",
        free_form=False,
    )
    assert "Evidence Ledger" in prompt
    assert "Claim | Evidence summary | Source URL/path" in prompt
    assert "Strength(high/medium/low)" in prompt


def test_evidence_prompt_brief_makes_ledger_optional() -> None:
    prompt = prompts.build_evidence_prompt(
        "Korean",
        depth="brief",
        template_rigidity="balanced",
        free_form=False,
    )
    assert "필요한 경우에만" in prompt


def test_writer_prompt_high_structure_requests_method_and_traceability() -> None:
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
        free_form=False,
    )
    assert "방법론 투명성: Method 계열 섹션" in prompt
    assert "evidence matrix" in prompt
    assert "확정 사실과 불확실/추정 항목을 분리" in prompt
    assert "서술 연결성" in prompt


def test_writer_prompt_free_form_relaxes_structure_requirements() -> None:
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
        free_form=True,
    )
    assert "요청 목적에 맞는 최소 수준으로만 공개하세요." in prompt
    assert "evidence matrix를 강제하지 않습니다." in prompt


def test_evaluate_prompt_switches_quality_axis_by_mode() -> None:
    deep_prompt = prompts.build_evaluate_prompt(
        "coverage, structure",
        depth="deep",
        template_rigidity="strict",
        free_form=False,
    )
    brief_prompt = prompts.build_evaluate_prompt(
        "coverage, structure",
        depth="brief",
        template_rigidity="balanced",
        free_form=False,
    )
    assert "강하게 평가하세요." in deep_prompt
    assert "간결성, 목적 적합성" in brief_prompt


def test_prompt_intent_guidance_adapts_to_decision_mode() -> None:
    plan_prompt = prompts.build_plan_prompt(
        "Korean",
        depth="normal",
        template_rigidity="balanced",
        free_form=False,
        report_intent="decision_brief",
    )
    evidence_prompt = prompts.build_evidence_prompt(
        "Korean",
        depth="normal",
        template_rigidity="balanced",
        free_form=False,
        report_intent="decision",
    )
    evaluate_prompt = prompts.build_evaluate_prompt(
        "coverage, structure",
        depth="normal",
        template_rigidity="balanced",
        free_form=False,
        report_intent="decision",
    )
    assert "의도=decision" in plan_prompt
    assert "옵션별 근거" in evidence_prompt
    assert "실행 가능성" in evaluate_prompt


def test_data_scientist_prompt_enforces_grounded_narrative_provenance() -> None:
    prompt = prompts.build_data_scientist_prompt(
        "Korean",
        depth="deep",
        report_intent="research",
    )
    assert "환각을 피하기 위해" in prompt
    assert "근거가 없는 수치/비교를 만들지 말 것" in prompt
    assert "원출처 URL 또는 파일 경로" in prompt
    assert "딱딱한 라벨형 문구 금지" in prompt


def test_writer_prompt_deep_adds_density_and_visual_integration_guidance() -> None:
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
        artwork_enabled=True,
        free_form=False,
        report_intent="research",
    )
    assert "심층 모드에서는 핵심 섹션" in prompt
    assert "figure 후보가 없거나 부족하면 artwork 도구" in prompt
    assert "문장 품질: '주장/근거/인사이트'" in prompt
    assert "시각물 문맥 규칙" in prompt


def test_writer_finalizer_prompt_enforces_narrative_cleanup_and_citation_integrity() -> None:
    prompt = prompts.build_writer_finalizer_prompt(
        _format_instructions(),
        "",
        _template_spec(),
        ["Executive Summary", "Key Findings"],
        "html",
        "Korean",
        depth="deep",
        template_rigidity="balanced",
        figures_enabled=False,
        figures_mode="auto",
        artwork_enabled=True,
        free_form=False,
        report_intent="research",
    )
    assert "라벨형 단답 나열" in prompt
    assert "깨진 인용 문법" in prompt
