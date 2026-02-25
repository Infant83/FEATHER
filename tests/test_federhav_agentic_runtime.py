from __future__ import annotations

from pathlib import Path

import federhav.agentic_runtime as runtime_mod


def test_build_action_preflight_marks_missing_instruction(tmp_path: Path) -> None:
    run_dir = tmp_path / "runs" / "demo"
    run_dir.mkdir(parents=True, exist_ok=True)
    preflight = runtime_mod._build_action_preflight(
        {"type": "run_feather", "run_hint": "demo", "create_if_missing": False},
        root=tmp_path,
        run_rel="runs/demo",
    )
    assert preflight["status"] == "missing_instruction"
    assert preflight["ready_for_execute"] is False
    assert preflight["instruction"]["required"] is True
    assert preflight["instruction"]["available"] is False


def test_normalize_action_planner_payload_enriches_handoff(tmp_path: Path) -> None:
    run_dir = tmp_path / "runs" / "demo" / "instruction"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "demo.txt").write_text("instruction\n", encoding="utf-8")

    payload = runtime_mod._normalize_action_planner_payload(
        {
            "type": "run_feather",
            "run_hint": "runs/demo/archive/youtube/videos.jsonl",
            "confidence": 82,
            "intent_rationale": "사용자 요청은 명시 실행 의도입니다.",
            "execution_handoff": {
                "planner": "DEEPAGENT",
                "preflight": {"status": "needs_confirmation", "ready_for_execute": False},
            },
        },
        root=tmp_path,
        run_rel="runs/demo",
    )
    assert isinstance(payload, dict)
    assert payload["type"] == "run_feather"
    assert payload["run_hint"] == "demo"
    assert payload["planner"] == "deepagent"
    assert payload["confidence"] == 0.82
    handoff = payload["execution_handoff"]
    assert isinstance(handoff, dict)
    assert handoff["planner"] == "deepagent"
    preflight = handoff["preflight"]
    assert preflight["status"] == "needs_confirmation"
    assert preflight["ready_for_execute"] is False
    assert preflight["resolved_run_rel"] == "runs/demo"


def test_try_deepagent_action_plan_returns_none_when_runtime_off(tmp_path: Path) -> None:
    result = runtime_mod.try_deepagent_action_plan(
        question="run feather 실행해줘",
        run_rel="runs/demo",
        history=[],
        state_memory={},
        capabilities={},
        execution_mode="plan",
        allow_artifacts=False,
        model=None,
        llm_backend="openai_api",
        reasoning_effort="off",
        runtime_mode="off",
        root=tmp_path,
    )
    assert result is None


def test_try_deepagent_action_plan_uses_action_object(monkeypatch, tmp_path: Path) -> None:
    class _FakeAgent:
        def invoke(self, _payload):
            return {
                "action": {
                    "type": "run_federlicht",
                    "run_hint": "demo",
                    "confidence": 0.91,
                }
            }

    class _FakeReportMod:
        @staticmethod
        def create_agent_with_fallback(*_args, **_kwargs):
            return _FakeAgent()

    monkeypatch.setattr(runtime_mod, "_load_agent_factory", lambda: (_FakeReportMod(), object()))

    run_dir = tmp_path / "runs" / "demo" / "instruction"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "demo.txt").write_text("instruction\n", encoding="utf-8")

    result = runtime_mod.try_deepagent_action_plan(
        question="federlicht 실행",
        run_rel="runs/demo",
        history=[],
        state_memory={"scope": {"run_rel": "runs/demo"}},
        capabilities={},
        execution_mode="act",
        allow_artifacts=False,
        model="gpt-4o-mini",
        llm_backend="openai_api",
        reasoning_effort="off",
        runtime_mode="auto",
        root=tmp_path,
    )
    assert isinstance(result, dict)
    assert result["type"] == "run_federlicht"
    assert result["planner"] == "deepagent"
    assert result["execution_handoff"]["preflight"]["resolved_run_rel"] == "runs/demo"


def test_try_deepagent_action_plan_parses_json_from_assistant_text(monkeypatch, tmp_path: Path) -> None:
    class _FakeAgent:
        def invoke(self, _payload):
            return {
                "messages": [
                    {
                        "role": "assistant",
                        "content": '{"type":"focus_editor","target":"feather_instruction","confidence":65}',
                    }
                ]
            }

    class _FakeReportMod:
        @staticmethod
        def create_agent_with_fallback(*_args, **_kwargs):
            return _FakeAgent()

    monkeypatch.setattr(runtime_mod, "_load_agent_factory", lambda: (_FakeReportMod(), object()))

    result = runtime_mod.try_deepagent_action_plan(
        question="instruction 열어줘",
        run_rel="runs/demo",
        history=[],
        state_memory={},
        capabilities={},
        execution_mode="plan",
        allow_artifacts=False,
        model=None,
        llm_backend="openai_api",
        reasoning_effort="off",
        runtime_mode="auto",
        root=tmp_path,
    )
    assert isinstance(result, dict)
    assert result["type"] == "focus_editor"
    assert result["planner"] == "deepagent"
    assert result["confidence"] == 0.65


def test_governor_loop_policy_clamps_env_values(monkeypatch) -> None:
    monkeypatch.setenv("FEDERHAV_GOVERNOR_MAX_ITER", "999")
    monkeypatch.setenv("FEDERHAV_GOVERNOR_DELTA_THRESHOLD", "-1")
    monkeypatch.setenv("FEDERHAV_GOVERNOR_BUDGET_CHARS", "10")

    policy = runtime_mod._governor_loop_policy()

    assert policy["max_iter"] == 4
    assert policy["delta_threshold"] == 0.01
    assert policy["budget_chars"] == 4000


def test_try_deepagent_action_plan_records_governor_loop_and_selects_best_candidate(
    monkeypatch, tmp_path: Path
) -> None:
    class _FakeAgent:
        def __init__(self) -> None:
            self.calls = 0

        def invoke(self, _payload):
            self.calls += 1
            if self.calls == 1:
                return {
                    "action": {
                        "type": "run_feather",
                        "run_hint": "demo",
                        "confidence": 0.61,
                        "execution_handoff": {
                            "preflight": {"status": "needs_confirmation", "ready_for_execute": False}
                        },
                    }
                }
            return {
                "action": {
                    "type": "run_federlicht",
                    "run_hint": "demo",
                    "confidence": 0.94,
                    "execution_handoff": {"preflight": {"status": "ok", "ready_for_execute": True}},
                }
            }

    fake_agent = _FakeAgent()

    class _FakeReportMod:
        @staticmethod
        def create_agent_with_fallback(*_args, **_kwargs):
            return fake_agent

    monkeypatch.setenv("FEDERHAV_GOVERNOR_MAX_ITER", "3")
    monkeypatch.setattr(runtime_mod, "_load_agent_factory", lambda: (_FakeReportMod(), object()))

    run_dir = tmp_path / "runs" / "demo" / "instruction"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "demo.txt").write_text("instruction\n", encoding="utf-8")

    result = runtime_mod.try_deepagent_action_plan(
        question="federlicht 실행",
        run_rel="runs/demo",
        history=[],
        state_memory={},
        capabilities={},
        execution_mode="act",
        allow_artifacts=False,
        model="gpt-4o-mini",
        llm_backend="openai_api",
        reasoning_effort="off",
        runtime_mode="auto",
        root=tmp_path,
    )
    assert isinstance(result, dict)
    assert result["type"] == "run_federlicht"
    assert result["planner"] == "deepagent"
    assert fake_agent.calls == 2

    handoff = result.get("execution_handoff")
    assert isinstance(handoff, dict)
    loop = handoff.get("governor_loop")
    assert isinstance(loop, dict)
    assert loop.get("attempts") == 2
    assert loop.get("converged") is True
    assert loop.get("selected_candidate_index") == 1


def test_resolve_model_hint_prefers_onprem_default_when_openai_base_is_custom(monkeypatch) -> None:
    monkeypatch.delenv("FEDERHAV_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.setenv("OPENAI_BASE_URL", "http://127.0.0.1:8000/v1")

    model = runtime_mod._resolve_model_hint(None, "openai_api")
    assert model == "Qwen3-235B-A22B-Thinking-2507"


def test_resolve_model_hint_keeps_openai_default_for_public_api(monkeypatch) -> None:
    monkeypatch.delenv("FEDERHAV_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    model = runtime_mod._resolve_model_hint(None, "openai_api")
    assert model == "gpt-4o-mini"


def test_try_deepagent_answer_tools_expose_callable_name(monkeypatch, tmp_path: Path) -> None:
    captured_tools: list[object] = []

    class _FakeAgent:
        def invoke(self, _payload):
            return {"messages": [{"role": "assistant", "content": "ok"}]}

    class _FakeReportMod:
        @staticmethod
        def create_agent_with_fallback(*args, **_kwargs):
            if len(args) >= 3 and isinstance(args[2], list):
                captured_tools.extend(args[2])
            return _FakeAgent()

    monkeypatch.setattr(runtime_mod, "_load_agent_factory", lambda: (_FakeReportMod(), object()))

    out = runtime_mod.try_deepagent_answer(
        question="요약해줘",
        messages=[{"role": "user", "content": "hello"}],
        sources=[],
        state_memory={"run": {"run_rel": "runs/demo"}},
        model="gpt-4o-mini",
        llm_backend="openai_api",
        reasoning_effort="off",
        runtime_mode="auto",
        root=tmp_path,
    )
    assert out is not None
    assert captured_tools
    assert all(callable(tool) for tool in captured_tools)
    assert all(hasattr(tool, "__name__") and str(getattr(tool, "__name__", "")).strip() for tool in captured_tools)
    assert all(hasattr(tool, "__qualname__") and str(getattr(tool, "__qualname__", "")).strip() for tool in captured_tools)
