from __future__ import annotations

from pathlib import Path

import federhav.cli as cli_mod


def test_main_routes_legacy_flags_to_update(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def _fake_update(args):
        captured["command"] = args.command
        captured["run"] = args.run
        return 0

    monkeypatch.setattr(cli_mod, "_run_update_command", _fake_update)

    code = cli_mod.main(
        [
            "--run",
            "site/runs/demo",
            "--base-report",
            "report_full.html",
            "--update",
            "수정해줘",
        ]
    )

    assert code == 0
    assert captured["command"] == "update"
    assert captured["run"] == "site/runs/demo"


def test_main_defaults_to_chat(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def _fake_chat(args):
        captured["command"] = args.command
        captured["question"] = args.question
        return 0

    monkeypatch.setattr(cli_mod, "_run_chat_command", _fake_chat)

    code = cli_mod.main(["--question", "hello"])

    assert code == 0
    assert captured["command"] == "chat"
    assert captured["question"] == "hello"


def test_parse_prefixed_mode_question() -> None:
    mode, question = cli_mod._parse_prefixed_mode_question("/act 실행해줘")
    assert mode == "act"
    assert question == "실행해줘"

    mode, question = cli_mod._parse_prefixed_mode_question("/plan")
    assert mode == "plan"
    assert question == ""

    mode, question = cli_mod._parse_prefixed_mode_question("그냥 질문")
    assert mode is None
    assert question == "그냥 질문"


def test_run_chat_command_applies_prefixed_mode_question(tmp_path: Path, monkeypatch) -> None:
    captured: dict[str, object] = {}

    def _fake_run_chat_once(_args, config, question):
        captured["mode"] = config.execution_mode
        captured["question"] = question
        captured["agent"] = config.agent
        captured["profile_id"] = config.profile_id
        return 0

    monkeypatch.setattr(cli_mod, "_run_chat_once", _fake_run_chat_once)
    parser = cli_mod._build_parser()
    args = parser.parse_args(
        [
            "chat",
            "--root",
            str(tmp_path),
            "--agent",
            "ai_governance_team",
            "--profile-id",
            "team_main",
            "--question",
            "/act 실행해줘",
        ]
    )
    code = cli_mod._run_chat_command(args)
    assert code == 0
    assert captured["mode"] == "act"
    assert captured["question"] == "실행해줘"
    assert captured["agent"] == "ai_governance_team"
    assert captured["profile_id"] == "team_main"


def test_run_chat_command_normalizes_bounds_and_flags(tmp_path: Path, monkeypatch) -> None:
    captured: dict[str, object] = {}

    def _fake_run_chat_once(_args, config, question):
        captured["config"] = config
        captured["question"] = question
        return 0

    monkeypatch.setattr(cli_mod, "_run_chat_once", _fake_run_chat_once)
    parser = cli_mod._build_parser()
    args = parser.parse_args(
        [
            "chat",
            "--root",
            str(tmp_path),
            "--max-sources",
            "99",
            "--history-turns",
            "1",
            "--execution-mode",
            "act",
            "--runtime-mode",
            "deepagent",
            "--strict-model",
            "--allow-artifacts",
            "--question",
            "질문",
        ]
    )
    code = cli_mod._run_chat_command(args)
    assert code == 0
    config = captured["config"]
    assert config.max_sources == 16
    assert config.history_turns == 2
    assert config.execution_mode == "act"
    assert config.runtime_mode == "deepagent"
    assert config.strict_model is True
    assert config.allow_artifacts is True
    assert captured["question"] == "질문"
