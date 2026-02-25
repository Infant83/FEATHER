from __future__ import annotations

import io
import json
from pathlib import Path

import federnett.routes as routes_mod
from federnett.config import FedernettConfig
from federnett.jobs import JobRegistry
from federnett.routes import handle_api_get, handle_api_post


class DummyHandler:
    def __init__(self, cfg: FedernettConfig, path: str, payload: dict | None = None) -> None:
        self._cfg_obj = cfg
        self._jobs_obj = JobRegistry()
        self.path = path
        raw = json.dumps(payload or {}, ensure_ascii=False).encode("utf-8")
        self.headers = {"Content-Length": str(len(raw))}
        self.rfile = io.BytesIO(raw)
        self.json_response: tuple[int, object] | None = None
        self.bytes_response: tuple[int, bytes, str] | None = None
        self.streamed_job = None
        self.stream_status: int | None = None
        self.stream_headers: list[tuple[str, str]] = []
        self.wfile = io.BytesIO()

    def _cfg(self) -> FedernettConfig:
        return self._cfg_obj

    def _jobs(self) -> JobRegistry:
        return self._jobs_obj

    def _send_json(self, payload: object, status: int = 200) -> None:
        self.json_response = (status, payload)

    def _send_bytes(self, data: bytes, content_type: str, status: int = 200) -> None:
        self.bytes_response = (status, data, content_type)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def _stream_job(self, job) -> None:
        self.streamed_job = job

    def send_response(self, code: int, message: str | None = None) -> None:
        self.stream_status = code

    def send_header(self, keyword: str, value: str) -> None:
        self.stream_headers.append((keyword, value))

    def end_headers(self) -> None:
        return


def make_cfg(tmp_path: Path) -> FedernettConfig:
    root = tmp_path
    static_dir = root / "site" / "federnett"
    static_dir.mkdir(parents=True, exist_ok=True)
    site_root = root / "site"
    site_root.mkdir(parents=True, exist_ok=True)
    run_root = root / "site" / "runs"
    run_root.mkdir(parents=True, exist_ok=True)
    return FedernettConfig(
        root=root,
        static_dir=static_dir,
        run_roots=[run_root],
        site_root=site_root,
    )


def test_handle_api_get_health(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    handler = DummyHandler(cfg, "/api/health")
    handle_api_get(handler, list_models=lambda: [])
    assert handler.json_response == (200, {"status": "ok"})


def test_handle_api_get_session_status_defaults_disabled(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    handler = DummyHandler(cfg, "/api/auth/session/status")
    handle_api_get(handler, list_models=lambda: [])
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("enabled") is False
    assert body.get("authenticated") is False


def test_handle_api_get_models_uses_callback(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    handler = DummyHandler(cfg, "/api/models")
    handle_api_get(handler, list_models=lambda: ["gpt-5", "gpt-5-mini"])
    assert handler.json_response == (200, ["gpt-5", "gpt-5-mini"])


def test_handle_api_get_workspace_settings_returns_effective_paths(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    handler = DummyHandler(cfg, "/api/workspace/settings")
    handle_api_get(handler, list_models=lambda: [])
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    effective = body.get("effective")
    assert isinstance(effective, dict)
    assert effective.get("run_roots") == ["site/runs"]
    assert effective.get("site_root") == "site"
    assert effective.get("report_hub_root") == "site"


def test_handle_api_post_workspace_settings_updates_cfg_and_persists(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    handler = DummyHandler(
        cfg,
        "/api/workspace/settings",
        payload={
            "run_roots": ["runs", "site/runs"],
            "site_root": "site",
            "report_hub_root": "site/report_hub",
        },
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("saved") is True
    effective = body.get("effective")
    assert isinstance(effective, dict)
    assert effective.get("run_roots") == ["runs", "site/runs"]
    assert effective.get("report_hub_root") == "site/report_hub"
    assert [p.relative_to(tmp_path).as_posix() for p in cfg.run_roots] == ["runs", "site/runs"]
    settings_file = tmp_path / "site" / "federnett" / "workspace_settings.json"
    assert settings_file.exists()


def test_handle_api_workspace_settings_roundtrip_llm_policy(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    llm_policy = {
        "global": {
            "backend": "openai_api",
            "model": "$OPENAI_MODEL",
            "checkModel": "$OPENAI_MODEL",
            "visionModel": "$OPENAI_MODEL_VISION",
            "reasoningEffort": "off",
        },
        "overrides": {
            "federhav": {
                "mode": "custom",
                "backend": "openai_api",
                "model": "gpt-4o-mini",
                "reasoningEffort": "off",
                "runtimeMode": "auto",
            }
        },
    }
    expected_policy = routes_mod._normalize_llm_policy_payload(llm_policy)
    save_handler = DummyHandler(
        cfg,
        "/api/workspace/settings",
        payload={
            "run_roots": ["site/runs"],
            "site_root": "site",
            "report_hub_root": "site/report_hub",
            "llm_policy": llm_policy,
        },
    )
    handle_api_post(save_handler, render_template_preview=lambda _root, _payload: "")
    assert save_handler.json_response is not None
    status, body = save_handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    effective = body.get("effective")
    assert isinstance(effective, dict)
    assert effective.get("llm_policy") == expected_policy

    load_handler = DummyHandler(cfg, "/api/workspace/settings")
    handle_api_get(load_handler, list_models=lambda: [])
    assert load_handler.json_response is not None
    load_status, load_body = load_handler.json_response
    assert load_status == 200
    assert isinstance(load_body, dict)
    stored = load_body.get("stored")
    assert isinstance(stored, dict)
    assert stored.get("llm_policy") == expected_policy


def test_handle_api_workspace_settings_normalizes_legacy_llm_policy_payload(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    legacy_policy = {
        "backend": "CLI",
        "model": "GPT-5.3-CODEX-SPARK",
        "reasoning_effort": "ultra",
        "overrides": {
            "federlicht": {
                "mode": "CUSTOM",
                "backend": "codex",
                "model": "GPT-5.3-Codex-Spark",
                "check_model": "GPT-5.3-CODEX",
                "vision_model": "$OPENAI_MODEL_VISION",
                "reasoning_effort": "MEDIUM",
            },
            "federhav": {
                "mode": "??",
                "backend": "invalid",
                "model": "GPT-4O-mini",
                "runtime_mode": "fast",
                "live_auto_log_chars": 99999,
            },
        },
    }
    expected_policy = routes_mod._normalize_llm_policy_payload(legacy_policy)
    save_handler = DummyHandler(
        cfg,
        "/api/workspace/settings",
        payload={
            "run_roots": ["site/runs"],
            "site_root": "site",
            "report_hub_root": "site/report_hub",
            "llm_policy": legacy_policy,
        },
    )
    handle_api_post(save_handler, render_template_preview=lambda _root, _payload: "")
    assert save_handler.json_response is not None
    status, body = save_handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    effective = body.get("effective")
    assert isinstance(effective, dict)
    assert effective.get("llm_policy") == expected_policy

    load_handler = DummyHandler(cfg, "/api/workspace/settings")
    handle_api_get(load_handler, list_models=lambda: [])
    assert load_handler.json_response is not None
    load_status, load_body = load_handler.json_response
    assert load_status == 200
    assert isinstance(load_body, dict)
    stored = load_body.get("stored")
    assert isinstance(stored, dict)
    assert stored.get("llm_policy") == expected_policy


def test_handle_api_get_workspace_settings_normalizes_stored_llm_policy(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    raw_policy = {
        "global": {
            "backend": "codex",
            "model": "GPT-5.3-CODEX-SPARK",
            "check_model": "GPT-5.3-CODEX",
            "vision_model": "$OPENAI_MODEL_VISION",
            "reasoning_effort": "high",
        },
        "overrides": {
            "federhav": {
                "mode": "custom",
                "backend": "openai_api",
                "model": "gpt-4o-mini",
                "runtime_mode": "deepagent",
            }
        },
    }
    expected_policy = routes_mod._normalize_llm_policy_payload(raw_policy)
    settings_file = tmp_path / "site" / "federnett" / "workspace_settings.json"
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    settings_file.write_text(
        json.dumps(
            {
                "run_roots": ["site/runs"],
                "site_root": "site",
                "report_hub_root": "site/report_hub",
                "llm_policy": raw_policy,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    handler = DummyHandler(cfg, "/api/workspace/settings")
    handle_api_get(handler, list_models=lambda: [])
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    effective = body.get("effective")
    stored = body.get("stored")
    assert isinstance(effective, dict)
    assert isinstance(stored, dict)
    assert effective.get("llm_policy") == expected_policy
    assert stored.get("llm_policy") == expected_policy


def test_handle_api_post_help_ask_rejects_blank_question(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    handler = DummyHandler(cfg, "/api/help/ask", payload={"question": "   "})
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 400
    assert isinstance(body, dict)
    assert "question must be a non-empty string" in str(body.get("error"))


def test_handle_api_post_unknown_endpoint(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    handler = DummyHandler(cfg, "/api/does-not-exist", payload={})
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.json_response == (404, {"error": "unknown_endpoint"})


def test_handle_api_post_runs_create_creates_run_folder(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    handler = DummyHandler(
        cfg,
        "/api/runs/create",
        payload={"topic": "양자컴퓨터 최신 기술소개"},
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("created") is True
    run_rel = str(body.get("run_rel") or "")
    instruction_path = str(body.get("instruction_path") or "")
    assert run_rel.startswith("site/runs/")
    assert instruction_path.startswith(run_rel + "/instruction/")
    assert (tmp_path / run_rel / "archive").exists()
    assert (tmp_path / run_rel / "report_notes").exists()


def test_handle_api_post_runs_create_sanitizes_spaces_in_run_name(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    handler = DummyHandler(
        cfg,
        "/api/runs/create",
        payload={"run_name": "QC 관련 PPT 생성"},
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    run_rel = str(body.get("run_rel") or "")
    assert run_rel.startswith("site/runs/")
    assert " " not in run_rel
    assert run_rel.endswith("QC_관련_PPT_생성")


def test_handle_api_post_runs_create_respects_run_root_selection(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    runs_root = tmp_path / "runs"
    runs_root.mkdir(parents=True, exist_ok=True)
    cfg.run_roots = [cfg.run_roots[0], runs_root]
    handler = DummyHandler(
        cfg,
        "/api/runs/create",
        payload={"run_name": "selected_root_demo", "run_root": "runs"},
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("run_rel") == "runs/selected_root_demo"
    assert (tmp_path / "runs" / "selected_root_demo" / "instruction").exists()


def test_handle_api_get_output_suggestion_appends_suffix(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    existing = tmp_path / "site" / "runs" / "demo" / "report_full.html"
    existing.parent.mkdir(parents=True, exist_ok=True)
    existing.write_text("old", encoding="utf-8")
    handler = DummyHandler(cfg, "/api/federlicht/output-suggestion?output=site/runs/demo/report_full.html")
    handle_api_get(handler, list_models=lambda: [])
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("requested_output") == "site/runs/demo/report_full.html"
    assert body.get("suggested_output") == "site/runs/demo/report_full_1.html"
    assert body.get("changed") is True


def test_handle_api_get_output_suggestion_with_run_prefix(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    handler = DummyHandler(
        cfg,
        "/api/federlicht/output-suggestion?run=site/runs/demo&output=report_full.html",
    )
    handle_api_get(handler, list_models=lambda: [])
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("requested_output") == "site/runs/demo/report_full.html"
    assert body.get("suggested_output") == "site/runs/demo/report_full.html"
    assert body.get("changed") is False


def test_handle_api_post_help_ask_forwards_strict_model(tmp_path: Path, monkeypatch) -> None:
    cfg = make_cfg(tmp_path)
    captured: dict[str, object] = {}

    def _fake_answer(root, question, **kwargs):
        captured["root"] = root
        captured["question"] = question
        captured.update(kwargs)
        return {"answer": "ok", "sources": [], "used_llm": False, "model": ""}

    monkeypatch.setattr(routes_mod, "answer_help_question", _fake_answer)
    handler = DummyHandler(
        cfg,
        "/api/help/ask",
        payload={"question": "테스트", "model": "gpt-5", "strict_model": True},
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert captured.get("model") == "gpt-5"
    assert captured.get("strict_model") is True


def test_handle_api_post_help_ask_forwards_web_search_flag(tmp_path: Path, monkeypatch) -> None:
    cfg = make_cfg(tmp_path)
    captured: dict[str, object] = {}

    def _fake_answer(root, question, **kwargs):
        captured["root"] = root
        captured["question"] = question
        captured.update(kwargs)
        return {"answer": "ok", "sources": [], "used_llm": False, "model": ""}

    monkeypatch.setattr(routes_mod, "answer_help_question", _fake_answer)
    handler = DummyHandler(
        cfg,
        "/api/help/ask",
        payload={"question": "테스트", "web_search": True},
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert captured.get("web_search") is True


def test_handle_api_post_help_ask_forwards_llm_backend(tmp_path: Path, monkeypatch) -> None:
    cfg = make_cfg(tmp_path)
    captured: dict[str, object] = {}

    def _fake_answer(root, question, **kwargs):
        captured["root"] = root
        captured["question"] = question
        captured.update(kwargs)
        return {"answer": "ok", "sources": [], "used_llm": False, "model": ""}

    monkeypatch.setattr(routes_mod, "answer_help_question", _fake_answer)
    handler = DummyHandler(
        cfg,
        "/api/help/ask",
        payload={"question": "테스트", "llm_backend": "codex_cli"},
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert captured.get("llm_backend") == "codex_cli"


def test_handle_api_post_help_ask_forwards_reasoning_effort(tmp_path: Path, monkeypatch) -> None:
    cfg = make_cfg(tmp_path)
    captured: dict[str, object] = {}

    def _fake_answer(root, question, **kwargs):
        captured["root"] = root
        captured["question"] = question
        captured.update(kwargs)
        return {"answer": "ok", "sources": [], "used_llm": False, "model": ""}

    monkeypatch.setattr(routes_mod, "answer_help_question", _fake_answer)
    handler = DummyHandler(
        cfg,
        "/api/help/ask",
        payload={"question": "테스트", "reasoning_effort": "extra_high"},
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert captured.get("reasoning_effort") == "extra_high"


def test_handle_api_post_help_ask_forwards_live_log_tail(tmp_path: Path, monkeypatch) -> None:
    cfg = make_cfg(tmp_path)
    captured: dict[str, object] = {}

    def _fake_answer(root, question, **kwargs):
        captured["root"] = root
        captured["question"] = question
        captured.update(kwargs)
        return {"answer": "ok", "sources": [], "used_llm": False, "model": ""}

    monkeypatch.setattr(routes_mod, "answer_help_question", _fake_answer)
    handler = DummyHandler(
        cfg,
        "/api/help/ask",
        payload={"question": "테스트", "live_log_tail": "[run] line1\nline2"},
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert captured.get("live_log_tail") == "[run] line1\nline2"


def test_handle_api_post_help_ask_forwards_operator_controls(tmp_path: Path, monkeypatch) -> None:
    cfg = make_cfg(tmp_path)
    captured: dict[str, object] = {}

    def _fake_answer(root, question, **kwargs):
        captured["root"] = root
        captured["question"] = question
        captured.update(kwargs)
        return {"answer": "ok", "sources": [], "used_llm": False, "model": ""}

    monkeypatch.setattr(routes_mod, "answer_help_question", _fake_answer)
    handler = DummyHandler(
        cfg,
        "/api/help/ask",
        payload={
            "question": "테스트",
            "agent": "ai_governance_team",
            "execution_mode": "act",
            "allow_artifacts": True,
        },
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert captured.get("agent") == "ai_governance_team"
    assert captured.get("execution_mode") == "act"
    assert captured.get("allow_artifacts") is True


def test_handle_api_post_help_ask_stream_emits_sse(tmp_path: Path, monkeypatch) -> None:
    cfg = make_cfg(tmp_path)

    def _fake_stream(_root, _question, **_kwargs):
        yield {"event": "meta", "requested_model": "gpt-5.2"}
        yield {"event": "delta", "text": "안녕하세요"}
        yield {"event": "done", "answer": "안녕하세요", "sources": []}

    monkeypatch.setattr(routes_mod, "stream_help_question", _fake_stream)
    handler = DummyHandler(
        cfg,
        "/api/help/ask/stream",
        payload={"question": "테스트 스트림"},
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.stream_status == 200
    raw = handler.wfile.getvalue().decode("utf-8")
    assert "event: meta" in raw
    assert "event: delta" in raw
    assert "event: done" in raw


def test_handle_api_post_help_ask_stream_preserves_action_plan_activity_event(
    tmp_path: Path,
    monkeypatch,
) -> None:
    cfg = make_cfg(tmp_path)

    def _fake_stream(_root, _question, **_kwargs):
        yield {
            "event": "activity",
            "step": "action_plan",
            "tool_id": "action_planner",
            "details": {
                "planner": "deepagent",
                "confidence": 0.82,
                "intent_rationale": "explicit execute intent",
                "execution_handoff": {"preflight": {"status": "ok"}},
            },
        }
        yield {"event": "done", "answer": "ok", "sources": []}

    monkeypatch.setattr(routes_mod, "stream_help_question", _fake_stream)
    handler = DummyHandler(
        cfg,
        "/api/help/ask/stream",
        payload={"question": "테스트 스트림"},
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.stream_status == 200
    raw = handler.wfile.getvalue().decode("utf-8")
    assert "event: activity" in raw
    assert "action_plan" in raw
    assert "execution_handoff" in raw


def test_handle_api_post_help_ask_stream_forwards_web_search_flag(tmp_path: Path, monkeypatch) -> None:
    cfg = make_cfg(tmp_path)
    captured: dict[str, object] = {}

    def _fake_stream(_root, _question, **kwargs):
        captured.update(kwargs)
        yield {"event": "done", "answer": "ok", "sources": []}

    monkeypatch.setattr(routes_mod, "stream_help_question", _fake_stream)
    handler = DummyHandler(
        cfg,
        "/api/help/ask/stream",
        payload={"question": "테스트 스트림", "web_search": True},
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.stream_status == 200
    assert captured.get("web_search") is True


def test_handle_api_post_help_ask_stream_forwards_llm_backend(tmp_path: Path, monkeypatch) -> None:
    cfg = make_cfg(tmp_path)
    captured: dict[str, object] = {}

    def _fake_stream(_root, _question, **kwargs):
        captured.update(kwargs)
        yield {"event": "done", "answer": "ok", "sources": []}

    monkeypatch.setattr(routes_mod, "stream_help_question", _fake_stream)
    handler = DummyHandler(
        cfg,
        "/api/help/ask/stream",
        payload={"question": "테스트 스트림", "llm_backend": "codex_cli"},
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.stream_status == 200
    assert captured.get("llm_backend") == "codex_cli"


def test_handle_api_post_help_ask_stream_forwards_reasoning_effort(tmp_path: Path, monkeypatch) -> None:
    cfg = make_cfg(tmp_path)
    captured: dict[str, object] = {}

    def _fake_stream(_root, _question, **kwargs):
        captured.update(kwargs)
        yield {"event": "done", "answer": "ok", "sources": []}

    monkeypatch.setattr(routes_mod, "stream_help_question", _fake_stream)
    handler = DummyHandler(
        cfg,
        "/api/help/ask/stream",
        payload={"question": "테스트 스트림", "reasoning_effort": "high"},
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.stream_status == 200
    assert captured.get("reasoning_effort") == "high"


def test_handle_api_post_help_ask_stream_forwards_live_log_tail(tmp_path: Path, monkeypatch) -> None:
    cfg = make_cfg(tmp_path)
    captured: dict[str, object] = {}

    def _fake_stream(_root, _question, **kwargs):
        captured.update(kwargs)
        yield {"event": "done", "answer": "ok", "sources": []}

    monkeypatch.setattr(routes_mod, "stream_help_question", _fake_stream)
    handler = DummyHandler(
        cfg,
        "/api/help/ask/stream",
        payload={"question": "테스트 스트림", "live_log_tail": "tail-line"},
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.stream_status == 200
    assert captured.get("live_log_tail") == "tail-line"


def test_handle_api_post_help_ask_stream_forwards_operator_controls(tmp_path: Path, monkeypatch) -> None:
    cfg = make_cfg(tmp_path)
    captured: dict[str, object] = {}

    def _fake_stream(_root, _question, **kwargs):
        captured.update(kwargs)
        yield {"event": "done", "answer": "ok", "sources": []}

    monkeypatch.setattr(routes_mod, "stream_help_question", _fake_stream)
    handler = DummyHandler(
        cfg,
        "/api/help/ask/stream",
        payload={
            "question": "테스트 스트림",
            "agent": "ai_governance_team",
            "execution_mode": "act",
            "allow_artifacts": True,
        },
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.stream_status == 200
    assert captured.get("agent") == "ai_governance_team"
    assert captured.get("execution_mode") == "act"
    assert captured.get("allow_artifacts") is True


def test_handle_api_get_capabilities_returns_registry_and_runtime(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    handler = DummyHandler(cfg, "/api/capabilities?web_search=1")
    handle_api_get(handler, list_models=lambda: [])
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert isinstance(body.get("registry"), dict)
    runtime = body.get("runtime")
    assert isinstance(runtime, dict)
    tools = runtime.get("tools") if isinstance(runtime, dict) else []
    assert isinstance(tools, list)
    web_entry = next((entry for entry in tools if entry.get("id") == "web_research"), None)
    assert isinstance(web_entry, dict)
    assert web_entry.get("enabled") is True


def test_handle_api_post_capabilities_save_persists_registry(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    payload = {
        "registry": {
            "tools": [
                {
                    "id": "custom_lookup",
                    "label": "Custom Lookup",
                    "description": "local lookup tool",
                    "enabled": True,
                }
            ],
            "skills": [],
            "mcp_servers": [],
        },
        "web_search": False,
    }
    handler = DummyHandler(cfg, "/api/capabilities/save", payload=payload)
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("saved") is True
    registry = body.get("registry")
    assert isinstance(registry, dict)
    tools = registry.get("tools")
    assert isinstance(tools, list)
    assert any(str(entry.get("id")) == "custom_lookup" for entry in tools if isinstance(entry, dict))


def test_handle_api_post_capabilities_execute_runs_action(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    readme = tmp_path / "README.md"
    readme.write_text("hello\n", encoding="utf-8")
    save_handler = DummyHandler(
        cfg,
        "/api/capabilities/save",
        payload={
            "registry": {
                "tools": [
                    {
                        "id": "open_readme",
                        "label": "Open README",
                        "action": {"kind": "open_path", "target": "README.md"},
                    }
                ],
                "skills": [],
                "mcp_servers": [],
            }
        },
    )
    handle_api_post(save_handler, render_template_preview=lambda _root, _payload: "")
    exec_handler = DummyHandler(
        cfg,
        "/api/capabilities/execute",
        payload={"id": "open_readme", "dry_run": False},
    )
    handle_api_post(exec_handler, render_template_preview=lambda _root, _payload: "")
    assert exec_handler.json_response is not None
    status, body = exec_handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("effect") == "open_path"
    assert body.get("path") == "README.md"


def test_handle_api_post_capabilities_execute_edits_text_file(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    note = tmp_path / "docs" / "note.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text("author: old\n", encoding="utf-8")
    save_handler = DummyHandler(
        cfg,
        "/api/capabilities/save",
        payload={
            "registry": {
                "tools": [
                    {
                        "id": "edit_note",
                        "label": "Edit Note",
                        "action": {"kind": "edit_text_file", "target": "docs/note.md"},
                    }
                ],
                "skills": [],
                "mcp_servers": [],
            }
        },
    )
    handle_api_post(save_handler, render_template_preview=lambda _root, _payload: "")
    exec_handler = DummyHandler(
        cfg,
        "/api/capabilities/execute",
        payload={
            "id": "edit_note",
            "dry_run": False,
            "action_override": {
                "mode": "replace_first",
                "find": "old",
                "replace": "new",
            },
            "request_text": 'author를 "new"로 바꿔줘',
        },
    )
    handle_api_post(exec_handler, render_template_preview=lambda _root, _payload: "")
    assert exec_handler.json_response is not None
    status, body = exec_handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("effect") == "edit_text_file"
    assert body.get("changed") is True
    assert "author: new" in note.read_text(encoding="utf-8")


def test_handle_api_post_capabilities_execute_rewrite_section(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    report = tmp_path / "site" / "runs" / "demo" / "report" / "report_full.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("## Executive Summary\nold summary\n", encoding="utf-8")
    save_handler = DummyHandler(
        cfg,
        "/api/capabilities/save",
        payload={
            "registry": {
                "tools": [
                    {
                        "id": "rewrite_summary",
                        "label": "Rewrite Summary",
                        "action": {"kind": "rewrite_section", "target": "report/report_full.md#Executive Summary"},
                    }
                ],
                "skills": [],
                "mcp_servers": [],
            }
        },
    )
    handle_api_post(save_handler, render_template_preview=lambda _root, _payload: "")
    exec_handler = DummyHandler(
        cfg,
        "/api/capabilities/execute",
        payload={
            "id": "rewrite_summary",
            "dry_run": False,
            "run": "site/runs/demo",
            "action_override": {
                "replacement": "new summary in objective style",
            },
        },
    )
    handle_api_post(exec_handler, render_template_preview=lambda _root, _payload: "")
    assert exec_handler.json_response is not None
    status, body = exec_handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("effect") == "rewrite_section"
    assert body.get("rewrite_mode") == "direct_upsert"
    assert body.get("changed") is True
    assert "new summary in objective style" in report.read_text(encoding="utf-8")


def test_handle_api_get_help_history_forwards_profile_id(tmp_path: Path, monkeypatch) -> None:
    cfg = make_cfg(tmp_path)
    captured: dict[str, object] = {}

    def _fake_read_help_history(root, run_rel, profile_id=None):
        captured["root"] = root
        captured["run_rel"] = run_rel
        captured["profile_id"] = profile_id
        return {"run_rel": run_rel or "", "profile_id": profile_id or "", "items": []}

    monkeypatch.setattr(routes_mod, "read_help_history", _fake_read_help_history)
    handler = DummyHandler(cfg, "/api/help/history?run=site/runs/demo&profile_id=team_a")
    handle_api_get(handler, list_models=lambda: [])
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert captured.get("profile_id") == "team_a"


def test_handle_api_get_run_logs_accepts_short_run_name(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    run_dir = tmp_path / "site" / "runs" / "test_my_run"
    (run_dir / "instruction").mkdir(parents=True, exist_ok=True)
    (run_dir / "report_notes").mkdir(parents=True, exist_ok=True)
    handler = DummyHandler(cfg, "/api/run-logs?run=test_my_run")
    handle_api_get(handler, list_models=lambda: [])
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 200
    assert isinstance(body, list)


def test_report_hub_posts_and_comment_routes(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    manifest = {
        "revision": "r1",
        "items": [
            {
                "id": "post_001",
                "run": "demo_run",
                "title": "Demo Report",
                "summary": "summary",
                "author": "tester",
                "paths": {"report": "../runs/demo_run/report_full.html"},
            }
        ],
    }
    (cfg.site_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    posts_handler = DummyHandler(cfg, "/api/report-hub/posts?limit=5")
    handle_api_get(posts_handler, list_models=lambda: [])
    assert posts_handler.json_response is not None
    status, body = posts_handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("total") == 1

    comment_handler = DummyHandler(
        cfg,
        "/api/report-hub/comments",
        payload={
            "post_id": "post_001",
            "text": "좋은 보고서입니다.",
            "author": "alice",
            "run_rel": "site/runs/demo_run",
        },
    )
    handle_api_post(comment_handler, render_template_preview=lambda _root, _payload: "")
    assert comment_handler.json_response is not None
    status, body = comment_handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("post_id") == "post_001"

    comments_get = DummyHandler(cfg, "/api/report-hub/posts/post_001/comments")
    handle_api_get(comments_get, list_models=lambda: [])
    assert comments_get.json_response is not None
    status, body = comments_get.json_response
    assert status == 200
    assert isinstance(body, dict)
    rows = body.get("items")
    assert isinstance(rows, list)
    assert rows[-1]["text"] == "좋은 보고서입니다."


def test_report_hub_followup_and_link_routes(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    manifest = {
        "revision": "r1",
        "items": [
            {
                "id": "post_001",
                "run": "demo_run",
                "title": "Demo Report",
                "summary": "summary",
                "author": "tester",
                "paths": {"report": "../runs/demo_run/report_full.html"},
            }
        ],
    }
    (cfg.site_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    followup_post = DummyHandler(
        cfg,
        "/api/report-hub/followups",
        payload={
            "post_id": "post_001",
            "prompt": "다음 버전에서 표를 추가해줘",
            "author": "alice",
            "status": "proposed",
        },
    )
    handle_api_post(followup_post, render_template_preview=lambda _root, _payload: "")
    assert followup_post.json_response is not None
    status, body = followup_post.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("post_id") == "post_001"

    followup_get = DummyHandler(cfg, "/api/report-hub/posts/post_001/followups")
    handle_api_get(followup_get, list_models=lambda: [])
    assert followup_get.json_response is not None
    status, body = followup_get.json_response
    assert status == 200
    assert isinstance(body, dict)
    rows = body.get("items")
    assert isinstance(rows, list)
    assert rows[-1]["prompt"].startswith("다음 버전")

    link_post = DummyHandler(
        cfg,
        "/api/report-hub/link",
        payload={"post_id": "post_001", "run_rel": "site/runs/demo_run", "linked_by": "federnett"},
    )
    handle_api_post(link_post, render_template_preview=lambda _root, _payload: "")
    assert link_post.json_response is not None
    status, body = link_post.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("post_id") == "post_001"

    link_get = DummyHandler(cfg, "/api/report-hub/posts/post_001/link")
    handle_api_get(link_get, list_models=lambda: [])
    assert link_get.json_response is not None
    status, body = link_get.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("link", {}).get("run_rel") == "site/runs/demo_run"

    approval_post = DummyHandler(
        cfg,
        "/api/report-hub/approval",
        payload={
            "post_id": "post_001",
            "status": "review",
            "updated_by": "qa_team",
            "note": "Need stronger evidence matrix.",
        },
    )
    handle_api_post(approval_post, render_template_preview=lambda _root, _payload: "")
    assert approval_post.json_response is not None
    status, body = approval_post.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("status") == "review"

    approval_get = DummyHandler(cfg, "/api/report-hub/posts/post_001/approval")
    handle_api_get(approval_get, list_models=lambda: [])
    assert approval_get.json_response is not None
    status, body = approval_get.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("status") == "review"


def test_report_hub_approval_route_requires_root_unlock_when_enabled(tmp_path: Path, monkeypatch) -> None:
    cfg = make_cfg(tmp_path)
    manifest = {
        "revision": "r1",
        "items": [
            {
                "id": "post_001",
                "run": "demo_run",
                "title": "Demo Report",
                "summary": "summary",
                "author": "tester",
                "paths": {"report": "../runs/demo_run/report_full.html"},
            }
        ],
    }
    (cfg.site_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    monkeypatch.setenv("FEDERNETT_ROOT_PASSWORD", "root-secret")
    manager = routes_mod.RootAuthManager()

    locked_handler = DummyHandler(
        cfg,
        "/api/report-hub/approval",
        payload={
            "post_id": "post_001",
            "status": "review",
            "updated_by": "qa_team",
            "note": "Needs stronger evidence matrix.",
        },
    )
    locked_handler._root_auth = lambda: manager
    handle_api_post(locked_handler, render_template_preview=lambda _root, _payload: "")
    assert locked_handler.json_response is not None
    locked_status, locked_body = locked_handler.json_response
    assert locked_status == 403
    assert isinstance(locked_body, dict)
    assert "Root unlock is required" in str(locked_body.get("error"))

    unlock = manager.unlock("root-secret")
    unlocked_handler = DummyHandler(
        cfg,
        "/api/report-hub/approval",
        payload={
            "post_id": "post_001",
            "status": "review",
            "updated_by": "qa_team",
            "note": "Needs stronger evidence matrix.",
        },
    )
    unlocked_handler._root_auth = lambda: manager
    unlocked_handler.headers["X-Federnett-Root-Token"] = str(unlock.token or "")
    handle_api_post(unlocked_handler, render_template_preview=lambda _root, _payload: "")
    assert unlocked_handler.json_response is not None
    unlocked_status, unlocked_body = unlocked_handler.json_response
    assert unlocked_status == 200
    assert isinstance(unlocked_body, dict)
    assert unlocked_body.get("status") == "review"


def test_report_hub_approval_route_rejects_invalid_transition(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    manifest = {
        "revision": "r1",
        "items": [
            {
                "id": "post_001",
                "run": "demo_run",
                "title": "Demo Report",
                "summary": "summary",
                "author": "tester",
                "paths": {"report": "../runs/demo_run/report_full.html"},
            }
        ],
    }
    (cfg.site_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    handler = DummyHandler(
        cfg,
        "/api/report-hub/approval",
        payload={
            "post_id": "post_001",
            "status": "draft",
            "updated_by": "qa_team",
            "note": "Trying to move published artifact back to draft.",
        },
    )
    handle_api_post(handler, render_template_preview=lambda _root, _payload: "")
    assert handler.json_response is not None
    status, body = handler.json_response
    assert status == 400
    assert isinstance(body, dict)
    assert "invalid approval transition" in str(body.get("error"))


def test_report_hub_publish_route_copies_report_and_linked_assets(tmp_path: Path) -> None:
    cfg = make_cfg(tmp_path)
    run_dir = cfg.run_roots[0] / "publish_demo"
    (run_dir / "assets").mkdir(parents=True, exist_ok=True)
    (run_dir / "report_notes").mkdir(parents=True, exist_ok=True)
    report_path = run_dir / "report_full.html"
    (run_dir / "assets" / "chart.png").write_bytes(b"png")
    report_path.write_text(
        "<html><body><h1>demo</h1><img src='assets/chart.png'><img src='assets/missing.png'></body></html>",
        encoding="utf-8",
    )

    publish_handler = DummyHandler(
        cfg,
        "/api/report-hub/publish",
        payload={"run": "site/runs/publish_demo"},
    )
    handle_api_post(publish_handler, render_template_preview=lambda _root, _payload: "")
    assert publish_handler.json_response is not None
    status, body = publish_handler.json_response
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("published_report_rel") == "site/reports/publish_demo/report_full.html"
    assert "site/reports/publish_demo/assets/chart.png" in (body.get("published_asset_rels") or [])
    skipped = body.get("skipped_asset_refs")
    assert isinstance(skipped, list)
    assert any("assets/missing.png" in str(item) for item in skipped)
    assert (cfg.site_root / "reports" / "publish_demo" / "report_full.html").exists()
    assert (cfg.site_root / "reports" / "publish_demo" / "assets" / "chart.png").exists()

def test_prepare_federlicht_payload_falls_back_codex_model_on_openai_backend(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o-mini")
    payload, notes = routes_mod._prepare_federlicht_payload(
        {
            "llm_backend": "openai_api",
            "model": "gpt-5.3-codex",
            "check_model": "gpt-5.3-codex",
        }
    )
    assert payload.get("model") == "gpt-4o-mini"
    assert payload.get("check_model") == "gpt-4o-mini"
    assert any("fallback" in str(note).lower() for note in notes)


def test_prepare_federlicht_payload_uses_safe_default_when_openai_model_env_is_codex(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_MODEL", "gpt-5.3-codex")
    payload, notes = routes_mod._prepare_federlicht_payload(
        {
            "llm_backend": "openai_api",
            "model": "$OPENAI_MODEL",
            "check_model": "$OPENAI_MODEL",
        }
    )
    assert payload.get("model") == "gpt-4o-mini"
    assert payload.get("check_model") == "gpt-4o-mini"
    assert any("resolved" in str(note).lower() for note in notes)


def test_prepare_federlicht_payload_drops_reasoning_effort_for_non_reasoning_model() -> None:
    payload, notes = routes_mod._prepare_federlicht_payload(
        {
            "llm_backend": "openai_api",
            "model": "gpt-4o-mini",
            "reasoning_effort": "high",
        }
    )
    assert "reasoning_effort" not in payload
    assert any("reasoning_effort" in str(note) for note in notes)


def test_prepare_federlicht_payload_drops_reasoning_effort_for_compatible_gateway(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_BASE_URL", "http://127.0.0.1:11434/v1")
    payload, notes = routes_mod._prepare_federlicht_payload(
        {
            "llm_backend": "openai_api",
            "model": "gpt-5-mini",
            "reasoning_effort": "high",
        }
    )
    assert "reasoning_effort" not in payload
    assert any("reasoning_effort" in str(note) for note in notes)


def test_prepare_federlicht_payload_drops_reasoning_effort_when_off() -> None:
    payload, notes = routes_mod._prepare_federlicht_payload(
        {
            "llm_backend": "openai_api",
            "model": "gpt-5-mini",
            "reasoning_effort": "off",
        }
    )
    assert "reasoning_effort" not in payload
    assert notes == [] or all("reasoning_effort" not in str(note) for note in notes)


def test_prepare_federlicht_payload_uses_codex_model_when_backend_is_codex(monkeypatch) -> None:
    monkeypatch.setenv("CODEX_MODEL", "gpt-5.3-codex")
    payload, notes = routes_mod._prepare_federlicht_payload(
        {
            "llm_backend": "codex_cli",
            "model": "$OPENAI_MODEL",
        }
    )
    assert payload.get("model") == "gpt-5.3-codex"
    assert any("codex backend" in str(note).lower() for note in notes)


def test_prepare_federlicht_payload_normalizes_codex_model_tokens_to_lowercase() -> None:
    payload, notes = routes_mod._prepare_federlicht_payload(
        {
            "llm_backend": "codex_cli",
            "model": "GPT-5.3-Codex-Spark",
            "check_model": "GPT-5.3-Codex",
        }
    )
    assert payload.get("model") == "gpt-5.3-codex-spark"
    assert payload.get("check_model") == "gpt-5.3-codex"
    assert any("normalized" in str(note).lower() for note in notes)


def test_federlicht_runtime_snapshot_includes_html_pdf_fields() -> None:
    snapshot = routes_mod._federlicht_runtime_snapshot(
        {
            "llm_backend": "openai_api",
            "model": "gpt-5-mini",
            "check_model": "gpt-4o",
            "html_print_profile": "letter",
            "html_pdf": True,
            "html_pdf_engine": "weasyprint",
        }
    )
    assert snapshot.get("html_print_profile") == "letter"
    assert snapshot.get("html_pdf") is True
    assert snapshot.get("html_pdf_engine") == "weasyprint"
