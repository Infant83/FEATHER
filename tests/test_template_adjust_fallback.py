from __future__ import annotations

from federlicht import report


class _FailingAgent:
    def __init__(self, message: str) -> None:
        self._message = message

    def invoke(self, _payload: dict) -> dict:
        raise RuntimeError(self._message)


def _build_template() -> report.TemplateSpec:
    return report.TemplateSpec(
        name="default",
        sections=["Executive Summary", "Key Findings", "Appendix"],
        section_guidance={},
        writer_guidance=[],
    )


def test_adjust_template_spec_recovers_on_quota_error(monkeypatch) -> None:
    monkeypatch.setenv("FEDERLICHT_LLM_BACKEND", "openai_api")

    def _create_deep_agent(**_kwargs):
        return _FailingAgent("Error code: 429 insufficient_quota")

    template = _build_template()
    adjusted, adjustment = report.adjust_template_spec(
        template_spec=template,
        report_prompt="research report for D-Wave",
        scout_notes="scout notes",
        align_scout=None,
        clarification_answers=None,
        language="en",
        output_format="md",
        model_name="gpt-4o-mini",
        create_deep_agent=_create_deep_agent,
        backend=object(),
        adjust_mode="extend",
    )
    assert adjusted.sections == template.sections
    assert adjustment is not None
    assert "fallback" in str(adjustment.get("rationale") or "").lower()
    assert "fallback_reason=recoverable_agent_error" in str(adjustment.get("rationale") or "")


def test_adjust_template_spec_recovers_on_timeout_error(monkeypatch) -> None:
    monkeypatch.setenv("FEDERLICHT_LLM_BACKEND", "openai_api")

    def _create_deep_agent(**_kwargs):
        return _FailingAgent("gateway timeout while calling model")

    template = _build_template()
    adjusted, adjustment = report.adjust_template_spec(
        template_spec=template,
        report_prompt="deep review",
        scout_notes="scout notes",
        align_scout=None,
        clarification_answers=None,
        language="en",
        output_format="md",
        model_name="gpt-4o-mini",
        create_deep_agent=_create_deep_agent,
        backend=object(),
        adjust_mode="extend",
    )
    assert adjusted.sections == template.sections
    assert adjustment is not None
    assert "recoverable_agent_error" in str(adjustment.get("rationale") or "")


def test_adjust_template_spec_raises_on_non_recoverable_error(monkeypatch) -> None:
    monkeypatch.setenv("FEDERLICHT_LLM_BACKEND", "openai_api")

    def _create_deep_agent(**_kwargs):
        return _FailingAgent("unexpected parser panic")

    template = _build_template()
    raised = False
    try:
        report.adjust_template_spec(
            template_spec=template,
            report_prompt="research report for D-Wave",
            scout_notes="scout notes",
            align_scout=None,
            clarification_answers=None,
            language="en",
            output_format="md",
            model_name="gpt-4o-mini",
            create_deep_agent=_create_deep_agent,
            backend=object(),
            adjust_mode="extend",
        )
    except RuntimeError as exc:
        raised = True
        assert "unexpected parser panic" in str(exc)
    assert raised
