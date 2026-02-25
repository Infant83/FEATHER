from __future__ import annotations

from federlicht import report


def test_create_agent_with_fallback_drops_subagents_on_typeerror(monkeypatch) -> None:
    monkeypatch.delenv("FEDERLICHT_LLM_BACKEND", raising=False)
    calls: list[dict] = []

    def fake_create_deep_agent(**kwargs):
        calls.append(dict(kwargs))
        if "subagents" in kwargs:
            raise TypeError("create_deep_agent() got an unexpected keyword argument 'subagents'")
        return {"ok": True, "kwargs": kwargs}

    out = report.create_agent_with_fallback(
        fake_create_deep_agent,
        "",
        [],
        "system",
        backend=object(),
        subagents=[{"name": "artwork_agent"}],
    )

    assert out["ok"] is True
    assert len(calls) >= 2
    assert "subagents" in calls[0]
    assert "subagents" not in calls[-1]


def test_create_agent_with_fallback_uses_codex_bridge_when_backend_enabled(monkeypatch) -> None:
    monkeypatch.setenv("FEDERLICHT_LLM_BACKEND", "codex_cli")

    class DummyBridge:
        def __init__(self, model_name: str, system_prompt: str, tools=None) -> None:
            self.model_name = model_name
            self.system_prompt = system_prompt
            self.tools = tools

    monkeypatch.setattr(report, "_CodexCliBridgeAgent", DummyBridge)

    called = {"value": False}

    def fake_create_deep_agent(**kwargs):
        called["value"] = True
        return {"unexpected": True}

    out = report.create_agent_with_fallback(
        fake_create_deep_agent,
        "gpt-5.3-codex",
        [],
        "system prompt",
        backend=object(),
    )

    assert isinstance(out, DummyBridge)
    assert out.model_name == "gpt-5.3-codex"
    assert out.system_prompt == "system prompt"
    assert out.tools == []
    assert called["value"] is False


def test_create_agent_with_fallback_uses_codex_bridge_from_backend_argument(monkeypatch) -> None:
    monkeypatch.delenv("FEDERLICHT_LLM_BACKEND", raising=False)

    class DummyBridge:
        def __init__(self, model_name: str, system_prompt: str, tools=None) -> None:
            self.model_name = model_name
            self.system_prompt = system_prompt
            self.tools = tools

    monkeypatch.setattr(report, "_CodexCliBridgeAgent", DummyBridge)

    called = {"value": False}

    def fake_create_deep_agent(**kwargs):
        called["value"] = True
        return {"unexpected": True}

    out = report.create_agent_with_fallback(
        fake_create_deep_agent,
        "gpt-5.3-codex",
        [],
        "system prompt",
        backend="codex_cli",
    )

    assert isinstance(out, DummyBridge)
    assert out.model_name == "gpt-5.3-codex"
    assert out.system_prompt == "system prompt"
    assert out.tools == []
    assert called["value"] is False


def test_create_agent_with_fallback_prefers_explicit_backend_over_env(monkeypatch) -> None:
    monkeypatch.setenv("FEDERLICHT_LLM_BACKEND", "codex_cli")

    called = {"value": False}

    def fake_create_deep_agent(**kwargs):
        called["value"] = True
        return {"ok": True, "kwargs": kwargs}

    out = report.create_agent_with_fallback(
        fake_create_deep_agent,
        "",
        [],
        "system prompt",
        backend="openai_api",
    )

    assert isinstance(out, dict)
    assert out.get("ok") is True
    assert called["value"] is True
