from __future__ import annotations

import argparse
import sys
import types

from federlicht import report


def _runtime_args(*, model: str, check_model: str = "", reasoning_effort: str = "high") -> argparse.Namespace:
    return argparse.Namespace(
        model=model,
        check_model=check_model,
        llm_backend="openai_api",
        reasoning_effort=reasoning_effort,
    )


def test_resolve_effective_reasoning_effort_disables_for_non_reasoning_model(monkeypatch) -> None:
    monkeypatch.delenv("FEDERLICHT_FORCE_REASONING_EFFORT", raising=False)
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    args = _runtime_args(model="gpt-4o-mini", reasoning_effort="medium")
    effort = report.resolve_effective_reasoning_effort(args)
    assert effort == ""
    assert args.reasoning_effort == ""


def test_resolve_effective_reasoning_effort_disables_for_compat_gateway(monkeypatch) -> None:
    monkeypatch.delenv("FEDERLICHT_FORCE_REASONING_EFFORT", raising=False)
    monkeypatch.setenv("OPENAI_BASE_URL", "http://127.0.0.1:11434/v1")
    args = _runtime_args(model="gpt-5-mini", reasoning_effort="high")
    effort = report.resolve_effective_reasoning_effort(args)
    assert effort == ""
    assert args.reasoning_effort == ""


def test_resolve_effective_reasoning_effort_keeps_for_reasoning_model(monkeypatch) -> None:
    monkeypatch.delenv("FEDERLICHT_FORCE_REASONING_EFFORT", raising=False)
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    args = _runtime_args(model="gpt-5-mini", reasoning_effort="high")
    effort = report.resolve_effective_reasoning_effort(args)
    assert effort == "high"
    assert args.reasoning_effort == "high"


def test_build_openai_compat_model_omits_reasoning_for_non_reasoning_model(monkeypatch) -> None:
    monkeypatch.delenv("FEDERLICHT_FORCE_REASONING_EFFORT", raising=False)
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    captured: list[dict] = []

    class DummyChatOpenAI:
        def __init__(self, **kwargs):
            captured.append(dict(kwargs))

    monkeypatch.setitem(sys.modules, "langchain_openai", types.SimpleNamespace(ChatOpenAI=DummyChatOpenAI))
    model = report.build_openai_compat_model("gpt-4o-mini", reasoning_effort="high")
    assert model is not None
    assert captured
    assert "reasoning_effort" not in captured[-1]


def test_build_openai_compat_model_keeps_reasoning_for_reasoning_model(monkeypatch) -> None:
    monkeypatch.delenv("FEDERLICHT_FORCE_REASONING_EFFORT", raising=False)
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    captured: list[dict] = []

    class DummyChatOpenAI:
        def __init__(self, **kwargs):
            captured.append(dict(kwargs))

    monkeypatch.setitem(sys.modules, "langchain_openai", types.SimpleNamespace(ChatOpenAI=DummyChatOpenAI))
    model = report.build_openai_compat_model("gpt-5-mini", reasoning_effort="high")
    assert model is not None
    assert captured
    assert captured[-1].get("reasoning_effort") == "high"
