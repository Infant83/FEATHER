from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Any

import pytest

from federnett import help_agent


@dataclass
class _FakeResponse:
    status_code: int
    text: str = ""
    payload: dict[str, Any] | None = None

    def json(self) -> dict[str, Any]:
        return self.payload or {}


class _RequestsStub:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def post(self, url: str, *, headers: dict[str, str], json: dict[str, Any], timeout: int) -> _FakeResponse:
        self.calls.append({"url": url, "headers": headers, "json": json, "timeout": timeout})
        if "max_completion_tokens" in json:
            return _FakeResponse(
                400,
                text=(
                    '{"error":{"message":"Unsupported parameter: \'max_completion_tokens\'"}}'
                ),
            )
        return _FakeResponse(
            200,
            payload={
                "choices": [
                    {
                        "message": {
                            "content": "요약 답변",
                        }
                    }
                ]
            },
        )


class _EndpointFallbackStub:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def post(self, url: str, *, headers: dict[str, str], json: dict[str, Any], timeout: int) -> _FakeResponse:
        self.calls.append({"url": url, "headers": headers, "json": json, "timeout": timeout})
        if url.endswith("/v1/chat/completions"):
            return _FakeResponse(404, text='{"error":{"message":"Not Found"}}')
        return _FakeResponse(
            200,
            payload={
                "choices": [
                    {
                        "message": {
                            "content": "fallback endpoint answer",
                        }
                    }
                ]
            },
        )


class _ResponsesOnlyStub:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def post(self, url: str, *, headers: dict[str, str], json: dict[str, Any], timeout: int) -> _FakeResponse:
        self.calls.append({"url": url, "headers": headers, "json": json, "timeout": timeout})
        if url.endswith("/responses"):
            return _FakeResponse(
                200,
                payload={
                    "output_text": "responses endpoint answer",
                },
            )
        return _FakeResponse(404, text='{"error":{"message":"Not Found"}}')


class _ModelFallbackStub:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def post(self, url: str, *, headers: dict[str, str], json: dict[str, Any], timeout: int) -> _FakeResponse:
        self.calls.append({"url": url, "headers": headers, "json": json, "timeout": timeout})
        model = str(json.get("model") or "")
        if model == "gpt-5-nano":
            return _FakeResponse(404, text='{"error":{"message":"Model gpt-5-nano does not exist"}}')
        return _FakeResponse(
            200,
            payload={
                "choices": [
                    {
                        "message": {
                            "content": "fallback model answer",
                        }
                    }
                ]
            },
        )


def _sample_sources() -> list[dict[str, Any]]:
    return [
        {
            "id": "S1",
            "path": "README.md",
            "start_line": 1,
            "end_line": 3,
            "excerpt": "Federnett guide",
        }
    ]


def test_help_system_prompt_enforces_ui_first_cli_guardrails() -> None:
    prompt = help_agent._help_system_prompt()
    assert "Prioritize Federnett UI workflow first" in prompt
    assert "If CLI is not explicitly requested, do not output shell command lines." in prompt
    assert "do not suggest changing execution_mode" in prompt


def test_help_user_prompt_contains_ui_first_operating_rules() -> None:
    prompt = help_agent._help_user_prompt("옵션 알려줘", "[S1] README.md:1-3")
    assert "질문자가 CLI를 명시하지 않았다면 Federnett UI 단계로 안내." in prompt
    assert "CLI를 요청받지 않은 상태에서는 명령어를 출력하지 말고" in prompt
    assert "execution_mode(plan/act) 전환을 기본 제안하지 말 것." in prompt


def test_help_user_prompt_includes_path_first_analysis_rule() -> None:
    prompt = help_agent._help_user_prompt(
        "archive/youtube 의 videos.jsonl 을 정리해줘",
        "[S1] runs/QC_ppt/archive/youtube/videos.jsonl:1-40",
    )
    assert "특정 파일/폴더/경로" in prompt
    assert "해당 경로를 우선 분석" in prompt


def test_is_file_context_question_detects_path_queries() -> None:
    assert help_agent._is_file_context_question("archive/youtube 의 내용을 정리해줘") is True
    assert help_agent._is_file_context_question("Feather 실행해줘") is False


def test_is_file_context_question_detects_folder_query_without_slash() -> None:
    assert help_agent._is_file_context_question("archive 폴더에 있는 파일을 정리해줘") is True


def test_is_run_content_summary_request_detects_archive_summary() -> None:
    assert help_agent._is_run_content_summary_request("archive/youtube 의 videos.jsonl 을 정리해줘") is True
    assert help_agent._is_run_content_summary_request("archive 폴더 내용을 요약해줘") is True
    assert help_agent._is_run_content_summary_request("archive/youtube 기반으로 feather 실행해줘") is False


def test_needs_agentic_action_planning_skips_archive_summary_questions() -> None:
    assert help_agent._needs_agentic_action_planning("archive/youtube 의 videos.jsonl 을 정리해줘") is False
    assert help_agent._needs_agentic_action_planning("run feather 실행해줘") is True


def test_chat_completion_urls_with_v1_base() -> None:
    urls = help_agent._chat_completion_urls("http://localhost:8080/v1")
    assert "http://localhost:8080/v1/chat/completions" in urls
    assert "http://localhost:8080/chat/completions" in urls


def test_iter_run_context_files_includes_archive_jsonl_for_archive_question(tmp_path) -> None:
    run_dir = tmp_path / "runs" / "QC_ppt"
    (run_dir / "instruction").mkdir(parents=True, exist_ok=True)
    (run_dir / "archive" / "youtube").mkdir(parents=True, exist_ok=True)
    (run_dir / "instruction" / "QC_ppt.txt").write_text("instruction", encoding="utf-8")
    (run_dir / "archive" / "youtube" / "videos.jsonl").write_text(
        '{"title":"A"}\n{"title":"B"}\n',
        encoding="utf-8",
    )

    files = help_agent._iter_run_context_files(
        tmp_path,
        "runs/QC_ppt",
        question="archive/youtube 의 videos.jsonl 을 정리해줘",
    )
    rels = {help_agent.safe_rel(path, tmp_path).replace("\\", "/") for path in files}
    assert "runs/QC_ppt/archive/youtube/videos.jsonl" in rels


def test_select_sources_prioritizes_explicit_archive_path_hint(tmp_path) -> None:
    run_dir = tmp_path / "runs" / "QC_ppt"
    (run_dir / "instruction").mkdir(parents=True, exist_ok=True)
    (run_dir / "archive" / "youtube").mkdir(parents=True, exist_ok=True)
    (tmp_path / "src" / "feather").mkdir(parents=True, exist_ok=True)
    (run_dir / "instruction" / "QC_ppt.txt").write_text("archive 요약 요청", encoding="utf-8")
    (run_dir / "archive" / "youtube" / "videos.jsonl").write_text(
        '{"title":"D-Wave case","summary":"industrial use"}\n{"title":"pilot","summary":"manufacturing"}\n',
        encoding="utf-8",
    )
    (tmp_path / "src" / "feather" / "review.py").write_text(
        "def summarize():\n    return '정리 정리 정리 정리 정리'\n",
        encoding="utf-8",
    )
    sources, _indexed = help_agent._select_sources(
        tmp_path,
        "archive/youtube 의 videos.jsonl 을 정리해줘",
        max_sources=5,
        run_rel="runs/QC_ppt",
    )
    assert sources
    assert sources[0]["path"].replace("\\", "/") == "runs/QC_ppt/archive/youtube/videos.jsonl"


def test_answer_help_question_uses_archive_sources_for_archive_summary(tmp_path, monkeypatch) -> None:
    run_dir = tmp_path / "runs" / "QC_ppt"
    (run_dir / "archive" / "youtube").mkdir(parents=True, exist_ok=True)
    (run_dir / "archive" / "youtube" / "videos.jsonl").write_text(
        '{"title":"demo","summary":"line"}\n',
        encoding="utf-8",
    )
    captured: dict[str, Any] = {}

    def _fake_call_llm(question, sources, **kwargs):
        captured["question"] = question
        captured["sources"] = list(sources or [])
        return "요약 완료", "gpt-4o-mini"

    monkeypatch.setattr(help_agent, "_call_llm", _fake_call_llm)
    result = help_agent.answer_help_question(
        tmp_path,
        "archive/youtube 의 videos.jsonl 을 정리해줘",
        run_rel="runs/QC_ppt",
    )
    assert result["answer"] == "요약 완료"
    source_paths = [str(item.get("path") or "").replace("\\", "/") for item in captured.get("sources", [])]
    assert "runs/QC_ppt/archive/youtube/videos.jsonl" in source_paths


def test_answer_help_question_uses_run_rel_from_state_memory_when_run_missing(tmp_path, monkeypatch) -> None:
    run_dir = tmp_path / "runs" / "QC_ppt"
    (run_dir / "archive" / "youtube").mkdir(parents=True, exist_ok=True)
    (run_dir / "archive" / "youtube" / "videos.jsonl").write_text(
        '{"title":"demo","summary":"line"}\n',
        encoding="utf-8",
    )
    captured: dict[str, Any] = {}

    def _fake_call_llm(question, sources, **kwargs):
        captured["question"] = question
        captured["sources"] = list(sources or [])
        return "요약 완료", "gpt-4o-mini"

    monkeypatch.setattr(help_agent, "_call_llm", _fake_call_llm)
    result = help_agent.answer_help_question(
        tmp_path,
        "archive/youtube 의 videos.jsonl 을 정리해줘",
        run_rel=None,
        state_memory={"scope": {"run_rel": "runs/QC_ppt"}},
    )
    assert result["answer"] == "요약 완료"
    source_paths = [str(item.get("path") or "").replace("\\", "/") for item in captured.get("sources", [])]
    assert "runs/QC_ppt/archive/youtube/videos.jsonl" in source_paths


def test_call_llm_retries_token_budget_parameter(monkeypatch) -> None:
    stub = _RequestsStub()
    monkeypatch.setattr(help_agent, "requests", stub)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o-mini")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://llm.example")

    answer, model = help_agent._call_llm("테스트 질문", _sample_sources(), model=None, history=None)

    assert answer == "요약 답변"
    assert model == "gpt-4o-mini"
    assert len(stub.calls) >= 2
    assert "max_completion_tokens" in stub.calls[0]["json"]
    assert "max_tokens" in stub.calls[1]["json"]


def test_call_llm_falls_back_to_secondary_endpoint(monkeypatch) -> None:
    stub = _EndpointFallbackStub()
    monkeypatch.setattr(help_agent, "requests", stub)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o-mini")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://gw.example")

    answer, model = help_agent._call_llm("endpoint fallback", _sample_sources(), model=None, history=None)

    assert answer == "fallback endpoint answer"
    assert model == "gpt-4o-mini"
    assert len(stub.calls) >= 2
    assert stub.calls[0]["url"].endswith("/v1/chat/completions")
    assert any(call["url"].endswith("/chat/completions") for call in stub.calls[1:])


def test_call_llm_uses_responses_endpoint_when_chat_missing(monkeypatch) -> None:
    stub = _ResponsesOnlyStub()
    monkeypatch.setattr(help_agent, "requests", stub)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o-mini")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://gw.example")

    answer, model = help_agent._call_llm("responses fallback", _sample_sources(), model=None, history=None)

    assert answer == "responses endpoint answer"
    assert model == "gpt-4o-mini"
    assert any(call["url"].endswith("/responses") for call in stub.calls)


def test_call_llm_falls_back_when_model_unavailable(monkeypatch) -> None:
    stub = _ModelFallbackStub()
    monkeypatch.setattr(help_agent, "requests", stub)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o-mini")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://gw.example")
    with pytest.raises(RuntimeError):
        help_agent._call_llm("model fallback", _sample_sources(), model="gpt-5-nano", history=None)
    models_seen = [str(call["json"].get("model") or "") for call in stub.calls]
    assert "gpt-5-nano" in models_seen
    assert "gpt-4o-mini" not in models_seen


def test_call_llm_falls_back_when_explicit_model_unavailable_and_allowed(monkeypatch) -> None:
    stub = _ModelFallbackStub()
    monkeypatch.setattr(help_agent, "requests", stub)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o-mini")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://gw.example")
    monkeypatch.setenv("FEDERNETT_HELP_ALLOW_MODEL_FALLBACK", "true")

    answer, model = help_agent._call_llm("model fallback", _sample_sources(), model="gpt-5-nano", history=None)

    assert answer == "fallback model answer"
    assert model == "gpt-4o-mini"
    models_seen = [str(call["json"].get("model") or "") for call in stub.calls]
    assert "gpt-5-nano" in models_seen
    assert "gpt-4o-mini" in models_seen


def test_call_llm_strict_model_blocks_fallback(monkeypatch) -> None:
    stub = _ModelFallbackStub()
    monkeypatch.setattr(help_agent, "requests", stub)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o-mini")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://gw.example")
    monkeypatch.setenv("FEDERNETT_HELP_ALLOW_MODEL_FALLBACK", "true")

    with pytest.raises(RuntimeError):
        help_agent._call_llm(
            "model fallback",
            _sample_sources(),
            model="gpt-5-nano",
            history=None,
            strict_model=True,
        )

    models_seen = [str(call["json"].get("model") or "") for call in stub.calls]
    assert "gpt-5-nano" in models_seen
    assert "gpt-4o-mini" not in models_seen


def test_resolve_requested_model_supports_openai_model_reference(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_MODEL", "gpt-5-mini")
    chosen, explicit = help_agent._resolve_requested_model("$OPENAI_MODEL")
    assert chosen == "gpt-5-mini"
    assert explicit is False


def test_stream_help_question_emits_delta_and_done(monkeypatch, tmp_path) -> None:
    root = tmp_path
    monkeypatch.setattr(help_agent, "_select_sources", lambda *_args, **_kwargs: (_sample_sources(), 3))

    def _fake_call_llm_stream(_q, _sources, **_kwargs):
        def _iter():
            yield "부분 "
            yield "응답"
        return _iter(), "gpt-4o-mini"

    monkeypatch.setattr(help_agent, "_call_llm_stream", _fake_call_llm_stream)
    events = list(
        help_agent.stream_help_question(
            root,
            "질문",
            model="gpt-4o-mini",
            history=[{"role": "user", "content": "prev"}],
        )
    )
    event_types = [evt.get("event") for evt in events]
    assert "activity" in event_types
    assert "meta" in event_types
    assert "delta" in event_types
    assert event_types[-1] == "done"
    done_payload = events[-1]
    assert done_payload.get("answer") == "부분 응답"
    assert isinstance(done_payload.get("capabilities"), dict)


def test_infer_safe_action_detects_create_run_folder(tmp_path) -> None:
    action = help_agent._infer_safe_action(
        tmp_path,
        "새로운 run folder 를 하나 만들어줘. 주제는 양자컴퓨터 최신 기술소개",
        run_rel="site/runs/demo",
    )
    assert isinstance(action, dict)
    assert action.get("type") == "create_run_folder"
    assert "양자컴퓨터" in str(action.get("topic_hint") or "")


def test_infer_safe_action_skips_non_workspace_analysis_prompt(tmp_path) -> None:
    action = help_agent._infer_safe_action(
        tmp_path,
        "양자컴퓨터 관련된 최신 기술동향을 파악해보자.",
        run_rel="site/runs/demo",
    )
    assert action is None


def test_infer_safe_action_skips_run_action_for_run_content_summary(tmp_path) -> None:
    action = help_agent._infer_safe_action(
        tmp_path,
        "archive/youtube 의 videos.jsonl 을 정리해줘",
        run_rel="runs/QC_ppt",
    )
    assert action is None


def test_infer_safe_action_binds_run_hint_for_run_execution(tmp_path) -> None:
    action = help_agent._infer_safe_action(
        tmp_path,
        "feather run folder를 test_my_run으로 설정하고 실행해줘",
        run_rel="site/runs/demo",
    )
    assert isinstance(action, dict)
    assert action.get("type") == "run_feather"
    assert action.get("run_hint") == "test_my_run"
    assert action.get("create_if_missing") is True


def test_extract_run_hint_trims_nested_artifact_path_to_run_name() -> None:
    hint = help_agent._extract_run_hint("runs/QC_ppt/archive/youtube/videos.jsonl 파일을 정리해줘")
    assert hint == "QC_ppt"


def test_infer_safe_action_detects_switch_run(tmp_path) -> None:
    action = help_agent._infer_safe_action(
        tmp_path,
        "run을 mytest_01으로 전환해줘",
        run_rel="site/runs/demo",
    )
    assert isinstance(action, dict)
    assert action.get("type") == "switch_run"
    assert str(action.get("run_hint") or "").lower().startswith("mytest_01")
    assert action.get("create_if_missing") is not True


def test_infer_safe_action_prefers_switch_when_run_hint_is_explicit(tmp_path) -> None:
    action = help_agent._infer_safe_action(
        tmp_path,
        "run 폴더를 test_my_run 으로 하고 예제를 만들어보자",
        run_rel="site/runs/demo",
    )
    assert isinstance(action, dict)
    assert action.get("type") == "switch_run"
    assert action.get("run_hint") == "test_my_run"
    assert action.get("create_if_missing") is True


def test_infer_safe_action_uses_recent_run_hint_for_followup_execute(tmp_path) -> None:
    history = [
        {"role": "user", "content": "feather run folder를 test_my_run으로 설정하고 예제를 만들어보자"},
        {"role": "assistant", "content": "좋아요. run을 맞춰두고 진행할게요."},
    ]
    action = help_agent._infer_safe_action(
        tmp_path,
        "실행해줘",
        run_rel="site/runs/demo",
        history=history,
    )
    assert isinstance(action, dict)
    assert action.get("type") == "run_feather"
    assert action.get("run_hint") == "test_my_run"
    assert action.get("create_if_missing") is True


def test_infer_safe_action_detects_work_phrase_as_explicit_execute(tmp_path) -> None:
    history = [
        {"role": "user", "content": "feather run folder를 test_my_run으로 설정하고 예제를 만들어보자"},
        {"role": "assistant", "content": "좋아요. run을 맞춰두고 feather 실행 준비했습니다."},
    ]
    action = help_agent._infer_safe_action(
        tmp_path,
        "작업하자",
        run_rel="site/runs/demo",
        history=history,
    )
    assert isinstance(action, dict)
    assert action.get("type") == "run_feather"
    assert action.get("run_hint") == "test_my_run"
    assert action.get("create_if_missing") is True


def test_infer_safe_action_uses_recent_target_for_followup_execute(tmp_path) -> None:
    history = [
        {"role": "user", "content": "이번에는 federlicht만 다시 돌리자"},
        {"role": "assistant", "content": "좋아요. federlicht 기준으로 준비했습니다."},
    ]
    action = help_agent._infer_safe_action(
        tmp_path,
        "실행해줘",
        run_rel="site/runs/demo",
        history=history,
    )
    assert isinstance(action, dict)
    assert action.get("type") == "run_federlicht"


def test_infer_safe_action_detects_stage_resume_preset(tmp_path) -> None:
    action = help_agent._infer_safe_action(
        tmp_path,
        "writer 단계부터 재시작해줘",
        run_rel="site/runs/demo",
    )
    assert isinstance(action, dict)
    assert action.get("type") == "preset_resume_stage"
    assert action.get("stage") == "writer"


def test_infer_safe_action_detects_focus_editor(tmp_path) -> None:
    action = help_agent._infer_safe_action(
        tmp_path,
        "inline prompt 편집창 열어줘",
        run_rel="site/runs/demo",
    )
    assert isinstance(action, dict)
    assert action.get("type") == "focus_editor"
    assert action.get("target") == "federlicht_prompt"


def test_infer_safe_action_detects_action_mode_switch(tmp_path) -> None:
    action = help_agent._infer_safe_action(
        tmp_path,
        "act 모드로 바꿔서 바로 실행해줘",
        run_rel="site/runs/demo",
    )
    assert isinstance(action, dict)
    assert action.get("type") == "set_action_mode"
    assert action.get("mode") == "act"
    assert action.get("allow_artifacts") is True


def test_infer_governed_action_skips_content_summary_even_with_rule_fallback(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("FEDERNETT_HELP_RULE_FALLBACK", "1")
    monkeypatch.setenv("FEDERNETT_HELP_AGENTIC_ACTIONS", "0")
    action = help_agent._infer_governed_action(
        tmp_path,
        "archive/youtube 의 내용을 정리해줘",
        run_rel="runs/QC_ppt",
        history=[],
        state_memory="{}",
        capabilities={},
        execution_mode="plan",
        allow_artifacts=False,
        model=None,
        llm_backend="openai_api",
        reasoning_effort="off",
        runtime_mode="auto",
        strict_model=False,
    )
    assert action is None


def test_instruction_quality_guard_keeps_run_action_and_enables_auto_instruction() -> None:
    guarded = help_agent._apply_instruction_quality_guard(
        {
            "type": "run_feather",
            "label": "Feather 실행",
            "run_rel": "site/runs/demo",
        },
        question="실행해줘",
        run_rel="site/runs/demo",
        history=[
            {"role": "user", "content": "양자컴퓨터 최신 기술 동향 보고서를 만들어줘"},
            {"role": "assistant", "content": "좋아요. 준비하겠습니다."},
        ],
    )
    assert isinstance(guarded, dict)
    assert guarded.get("type") == "run_feather"
    assert guarded.get("auto_instruction") is True
    assert guarded.get("require_instruction_confirm") is True
    assert guarded.get("instruction_confirm_reason") == "short_generic_request"
    assert "양자컴퓨터" in str(guarded.get("topic_hint") or "")


def test_instruction_quality_guard_requests_clarification_when_topic_missing() -> None:
    guarded = help_agent._apply_instruction_quality_guard(
        {
            "type": "run_feather",
            "label": "Feather 실행",
            "run_rel": "site/runs/demo",
        },
        question="실행해줘",
        run_rel="site/runs/demo",
        history=[],
    )
    assert isinstance(guarded, dict)
    assert guarded.get("type") == "focus_editor"
    assert guarded.get("target") == "feather_instruction"
    assert guarded.get("clarify_required") is True
    assert "어떤 주제로 실행할까요" in str(guarded.get("clarify_question") or "")


def test_has_explicit_execution_intent_supports_work_phrase() -> None:
    assert help_agent._has_explicit_execution_intent("작업하자")
    assert help_agent._has_explicit_execution_intent("바로 진행해줘")
    assert help_agent._has_explicit_execution_intent("run it now")
    assert help_agent._has_explicit_execution_intent("실행해")
    assert help_agent._has_explicit_execution_intent("지금 시작")
    assert help_agent._has_explicit_execution_intent("go ahead")
    assert not help_agent._has_explicit_execution_intent("차이점을 설명해줘")


def test_needs_agentic_action_planning_for_actionable_query() -> None:
    assert help_agent._needs_agentic_action_planning("run folder를 demo로 바꾸고 feather 실행해줘") is True


def test_needs_agentic_action_planning_skips_general_content_query() -> None:
    assert help_agent._needs_agentic_action_planning("간단한 QC 관련 ppt 를 한장 만들 수 있을까. 양자컴퓨터 말야") is False


def test_answer_help_question_runs_web_search_when_enabled(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(help_agent, "_select_sources", lambda *_args, **_kwargs: (_sample_sources(), 5))
    monkeypatch.setattr(help_agent, "_call_llm", lambda *_args, **_kwargs: ("웹검색 답변", "gpt-4o-mini"))
    monkeypatch.setattr(help_agent, "_run_help_web_research", lambda *_args, **_kwargs: "web research done")

    result = help_agent.answer_help_question(
        tmp_path,
        "웹검색 질문",
        model="gpt-4o-mini",
        web_search=True,
        run_rel="site/runs/demo",
    )

    assert result["answer"] == "웹검색 답변"
    assert result["web_search"] is True
    assert result["web_search_note"] == "web research done"
    assert isinstance(result.get("capabilities"), dict)


def test_stream_help_question_emits_web_search_meta(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(help_agent, "_select_sources", lambda *_args, **_kwargs: (_sample_sources(), 5))
    monkeypatch.setattr(help_agent, "_run_help_web_research", lambda *_args, **_kwargs: "web research done")

    def _fake_call_llm_stream(_q, _sources, **_kwargs):
        def _iter():
            yield "스트림 "
            yield "응답"
        return _iter(), "gpt-4o-mini"

    monkeypatch.setattr(help_agent, "_call_llm_stream", _fake_call_llm_stream)
    events = list(
        help_agent.stream_help_question(
            tmp_path,
            "웹검색 질문",
            model="gpt-4o-mini",
            web_search=True,
            run_rel="site/runs/demo",
        )
    )
    meta_event = next(evt for evt in events if evt.get("event") == "meta")
    assert meta_event["web_search"] is True
    assert meta_event["web_search_note"] == "web research done"
    assert isinstance(meta_event.get("capabilities"), dict)
    web_activity = [evt for evt in events if evt.get("event") == "activity" and evt.get("id") == "web_research"]
    assert web_activity
    assert events[-1]["event"] == "done"
    assert events[-1]["web_search"] is True
    assert events[-1]["web_search_note"] == "web research done"


def test_is_path_allowed_allows_run_prefix_when_opted_in() -> None:
    rel = "site/runs/demo/instruction/demo.txt"
    assert help_agent._is_path_allowed(rel) is False
    assert help_agent._is_path_allowed(rel, allow_run_prefixes=True) is True


def test_answer_help_question_skips_web_search_when_query_is_local(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(help_agent, "_select_sources", lambda *_args, **_kwargs: (_sample_sources(), 5))
    monkeypatch.setattr(help_agent, "_call_llm", lambda *_args, **_kwargs: ("ok", "gpt-4o-mini"))

    def _should_not_run(*_args, **_kwargs):
        raise AssertionError("web research should have been skipped")

    monkeypatch.setattr(help_agent, "_run_help_web_research", _should_not_run)
    result = help_agent.answer_help_question(
        tmp_path,
        "federlicht 옵션 설명해줘",
        web_search=True,
        run_rel="site/runs/demo",
    )
    assert result["web_search"] is True
    assert "skipped" in str(result["web_search_note"])


def test_call_llm_uses_codex_cli_backend(monkeypatch) -> None:
    class _Proc:
        returncode = 0
        stderr = ""
        stdout = "\n".join(
            [
                '{"type":"thread.started","thread_id":"t1"}',
                '{"type":"item.completed","item":{"id":"x","type":"agent_message","text":"codex answer"}}',
                '{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}',
            ]
        )

    monkeypatch.setenv("FEDERNETT_HELP_LLM_BACKEND", "codex_cli")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(help_agent.shutil, "which", lambda _name: "codex")
    monkeypatch.setattr(help_agent.subprocess, "run", lambda *args, **kwargs: _Proc())

    answer, model = help_agent._call_llm(
        "codex 질문",
        _sample_sources(),
        model="gpt-5-codex",
        history=None,
    )

    assert answer == "codex answer"
    assert model == "gpt-5-codex"


def test_call_llm_codex_cli_passes_reasoning_effort(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class _Proc:
        returncode = 0
        stderr = ""
        stdout = '{"type":"item.completed","item":{"id":"x","type":"agent_message","text":"codex answer"}}'

    def _fake_run(cmd, *args, **kwargs):
        captured["cmd"] = list(cmd)
        return _Proc()

    monkeypatch.setenv("FEDERNETT_HELP_LLM_BACKEND", "codex_cli")
    monkeypatch.setattr(help_agent.shutil, "which", lambda _name: "codex")
    monkeypatch.setattr(help_agent.subprocess, "run", _fake_run)

    answer, model = help_agent._call_llm(
        "codex 질문",
        _sample_sources(),
        model="gpt-5-codex",
        history=None,
        reasoning_effort="extra_high",
    )

    assert answer == "codex answer"
    assert model == "gpt-5-codex"
    cmd = captured.get("cmd")
    assert isinstance(cmd, list)
    assert "-c" in cmd
    assert 'reasoning_effort="extra_high"' in cmd


def test_call_llm_openai_includes_reasoning_effort(monkeypatch) -> None:
    stub = _RequestsStub()
    monkeypatch.setattr(help_agent, "requests", stub)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-5-mini")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.com")

    answer, model = help_agent._call_llm(
        "테스트 질문",
        _sample_sources(),
        model=None,
        history=None,
        reasoning_effort="extra_high",
    )

    assert answer == "요약 답변"
    assert model == "gpt-5-mini"
    assert any(call["json"].get("reasoning_effort") == "high" for call in stub.calls)


def test_call_llm_openai_omits_reasoning_effort_on_non_reasoning_model(monkeypatch) -> None:
    stub = _RequestsStub()
    monkeypatch.setattr(help_agent, "requests", stub)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o-mini")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.com")

    answer, model = help_agent._call_llm(
        "테스트 질문",
        _sample_sources(),
        model=None,
        history=None,
        reasoning_effort="extra_high",
    )

    assert answer == "요약 답변"
    assert model == "gpt-4o-mini"
    assert all("reasoning_effort" not in call["json"] for call in stub.calls)


def test_call_llm_openai_omits_reasoning_effort_on_codex_named_model(monkeypatch) -> None:
    stub = _RequestsStub()
    monkeypatch.setattr(help_agent, "requests", stub)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.com")

    answer, model = help_agent._call_llm(
        "테스트 질문",
        _sample_sources(),
        model="gpt-5.3-codex",
        history=None,
        reasoning_effort="extra_high",
    )

    assert answer == "요약 답변"
    assert model == "gpt-5.3-codex"
    assert all("reasoning_effort" not in call["json"] for call in stub.calls)


def test_call_llm_stream_uses_codex_cli_backend(monkeypatch) -> None:
    class _FakeStdin:
        def __init__(self) -> None:
            self.buffer = ""
            self.closed = False

        def write(self, text: str) -> int:
            if self.closed:
                return 0
            self.buffer += str(text or "")
            return len(text or "")

        def flush(self) -> None:
            return

        def close(self) -> None:
            self.closed = True

    class _Proc:
        def __init__(self) -> None:
            self.returncode = 0
            self.stdin = _FakeStdin()
            self.stdout = io.StringIO(
                '{"type":"item.completed","item":{"id":"x","type":"agent_message","text":"codex stream answer"}}\n'
            )
            self.stderr = io.StringIO("")

        def wait(self) -> int:
            return self.returncode

        def kill(self) -> None:
            self.returncode = -9

    monkeypatch.setenv("FEDERNETT_HELP_LLM_BACKEND", "codex_cli")
    monkeypatch.setattr(help_agent.shutil, "which", lambda _name: "codex")
    monkeypatch.setattr(help_agent.subprocess, "Popen", lambda *args, **kwargs: _Proc())

    chunk_iter, model = help_agent._call_llm_stream(
        "codex 스트림 질문",
        _sample_sources(),
        model=None,
        history=None,
    )

    assert "".join(list(chunk_iter)) == "codex stream answer"
    assert isinstance(model, str) and model.strip()


def test_answer_help_question_passes_live_log_tail_to_llm(monkeypatch, tmp_path) -> None:
    captured: dict[str, object] = {}
    monkeypatch.setattr(help_agent, "_select_sources", lambda *_args, **_kwargs: (_sample_sources(), 4))

    def _fake_call_llm(_q, _sources, **kwargs):
        captured.update(kwargs)
        return "ok", "gpt-4o-mini"

    monkeypatch.setattr(help_agent, "_call_llm", _fake_call_llm)
    result = help_agent.answer_help_question(
        tmp_path,
        "라이브 로그 기반으로 요약해줘",
        live_log_tail="line-1\nline-2\nline-3",
    )
    assert result["answer"] == "ok"
    assert captured.get("live_log_tail") == "line-1\nline-2\nline-3"
    assert result.get("live_log_chars") == len("line-1\nline-2\nline-3")
    trace = result.get("trace")
    assert isinstance(trace, dict)
    assert str(trace.get("trace_id") or "").startswith("fh-")
    steps = trace.get("steps")
    assert isinstance(steps, list)
    assert any(str(step.get("id")) == "source_index" for step in steps if isinstance(step, dict))


def test_stream_help_question_includes_live_log_char_count(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(help_agent, "_select_sources", lambda *_args, **_kwargs: (_sample_sources(), 4))

    def _fake_call_llm_stream(_q, _sources, **_kwargs):
        def _iter():
            yield "스트림"
        return _iter(), "gpt-4o-mini"

    monkeypatch.setattr(help_agent, "_call_llm_stream", _fake_call_llm_stream)
    events = list(
        help_agent.stream_help_question(
            tmp_path,
            "질문",
            live_log_tail="x" * 9000,
        )
    )
    meta = next(evt for evt in events if evt.get("event") == "meta")
    done = events[-1]
    assert meta.get("live_log_chars") == help_agent._MAX_LIVE_LOG_CONTEXT_CHARS
    assert done.get("live_log_chars") == help_agent._MAX_LIVE_LOG_CONTEXT_CHARS
    assert str(meta.get("trace_id") or "").startswith("fh-")
    activity = next(evt for evt in events if evt.get("event") == "activity")
    assert str(activity.get("trace_id") or "").startswith("fh-")
    assert isinstance(done.get("trace"), dict)
    assert str((done.get("trace") or {}).get("trace_id") or "").startswith("fh-")


def test_answer_help_question_applies_operator_controls(monkeypatch, tmp_path) -> None:
    captured: dict[str, object] = {}
    monkeypatch.setattr(help_agent, "_select_sources", lambda *_args, **_kwargs: (_sample_sources(), 4))

    def _fake_call_llm(question, _sources, **kwargs):
        captured["question"] = question
        captured["kwargs"] = kwargs
        return "ok", "gpt-4o-mini"

    monkeypatch.setattr(help_agent, "_call_llm", _fake_call_llm)
    result = help_agent.answer_help_question(
        tmp_path,
        "실행 계획을 알려줘",
        agent="ai_governance_team",
        execution_mode="act",
        allow_artifacts=True,
    )
    forwarded = str(captured.get("question") or "")
    assert "[operator-control]" in forwarded
    assert "agent=ai_governance_team" in forwarded
    assert "execution_mode=act" in forwarded
    assert "allow_artifacts=true" in forwarded
    assert result.get("agent") == "ai_governance_team"
    assert result.get("execution_mode") == "act"
    assert result.get("allow_artifacts") is True


def test_normalize_history_keeps_context_summary_with_recent_turns() -> None:
    history = [
        {"role": "assistant", "content": "[context-compress] 이전 대화 요약"},
    ]
    for idx in range(14):
        history.append({"role": "user", "content": f"user-{idx}"})
        history.append({"role": "assistant", "content": f"assistant-{idx}"})
    normalized = help_agent._normalize_history(history)
    assert normalized
    assert normalized[0]["role"] == "assistant"
    assert normalized[0]["content"].startswith("[context-compress]")
    assert any(item["content"] == "assistant-13" for item in normalized)


def test_answer_help_question_reports_reasoning_off_for_non_reasoning_model(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.com")
    monkeypatch.setattr(help_agent, "_select_sources", lambda *_args, **_kwargs: (_sample_sources(), 2))
    monkeypatch.setattr(help_agent, "_call_llm", lambda *_args, **_kwargs: ("ok", "gpt-4o-mini"))
    result = help_agent.answer_help_question(
        tmp_path,
        "요약해줘",
        llm_backend="openai_api",
        model="gpt-4o-mini",
        reasoning_effort="medium",
    )
    assert result.get("reasoning_effort") == "off"


def test_answer_help_question_reports_reasoning_for_codex_backend(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(help_agent, "_select_sources", lambda *_args, **_kwargs: (_sample_sources(), 2))
    monkeypatch.setattr(help_agent, "_call_llm", lambda *_args, **_kwargs: ("ok", "codex-cli-default"))
    result = help_agent.answer_help_question(
        tmp_path,
        "요약해줘",
        llm_backend="codex_cli",
        reasoning_effort="medium",
    )
    assert result.get("reasoning_effort") == "medium"


def test_stream_help_question_reports_reasoning_off_for_non_reasoning_model(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.com")
    monkeypatch.setattr(help_agent, "_select_sources", lambda *_args, **_kwargs: (_sample_sources(), 2))

    def _fake_stream(*_args, **_kwargs):
        def _iter():
            yield "응답"
        return _iter(), "gpt-4o-mini"

    monkeypatch.setattr(help_agent, "_call_llm_stream", _fake_stream)
    events = list(
        help_agent.stream_help_question(
            tmp_path,
            "현재 상태",
            llm_backend="openai_api",
            model="gpt-4o-mini",
            reasoning_effort="medium",
        )
    )
    done = events[-1]
    assert done.get("event") == "done"
    assert done.get("reasoning_effort") == "off"


def test_allow_rule_fallback_defaults_to_false(monkeypatch) -> None:
    monkeypatch.delenv("FEDERNETT_HELP_RULE_FALLBACK", raising=False)
    assert help_agent._allow_rule_fallback("off") is False
    assert help_agent._allow_rule_fallback("auto") is False
    assert help_agent._allow_rule_fallback("deepagent") is False


def test_allow_rule_fallback_can_be_enabled_by_env(monkeypatch) -> None:
    monkeypatch.setenv("FEDERNETT_HELP_RULE_FALLBACK", "1")
    assert help_agent._allow_rule_fallback("off") is True
