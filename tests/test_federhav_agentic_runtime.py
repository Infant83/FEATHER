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
