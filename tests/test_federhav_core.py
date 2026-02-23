from __future__ import annotations

from pathlib import Path

from federnett.filesystem import read_help_history
import federhav.core as core_mod
from federhav.core import FederHavChatConfig, ask_question, stream_question


def test_ask_question_persists_history(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path.resolve()

    captured: dict[str, object] = {}

    def _fake_answer(root_path, question, **kwargs):
        captured["root"] = root_path
        captured["question"] = question
        captured["kwargs"] = kwargs
        return {"answer": "테스트 답변", "sources": [], "used_llm": False, "model": ""}

    monkeypatch.setattr("federhav.core.answer_help_question", _fake_answer)

    cfg = FederHavChatConfig(root=root, profile_id="main", history_turns=4)
    result = ask_question(cfg, "질문 1")

    assert result["answer"] == "테스트 답변"
    assert captured["question"] == "질문 1"
    history = read_help_history(root, None, profile_id="main")
    assert isinstance(history.get("items"), list)
    items = history["items"]
    assert len(items) == 2
    assert items[0]["role"] == "user"
    assert items[0]["content"] == "질문 1"
    assert items[1]["role"] == "assistant"
    assert items[1]["content"] == "테스트 답변"


def test_stream_question_persists_delta_answer(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path.resolve()

    def _fake_stream(root_path, question, **kwargs):
        yield {"event": "activity", "id": "source_index", "status": "done"}
        yield {"event": "delta", "text": "스트리밍 "}
        yield {"event": "delta", "text": "답변"}
        yield {"event": "done", "answer": "", "sources": [], "used_llm": True, "model": "x"}

    monkeypatch.setattr("federhav.core.stream_help_question", _fake_stream)

    cfg = FederHavChatConfig(root=root, profile_id="streamer", history_turns=4)
    events = list(stream_question(cfg, "질문 2"))

    assert any(str(ev.get("event")) == "done" for ev in events)
    history = read_help_history(root, None, profile_id="streamer")
    items = history["items"]
    assert len(items) == 2
    assert items[0]["role"] == "user"
    assert items[0]["content"] == "질문 2"
    assert items[1]["role"] == "assistant"
    assert items[1]["content"] == "스트리밍 답변"


def test_compact_history_injects_context_summary() -> None:
    rows = []
    for idx in range(20):
        rows.append({"role": "user", "content": f"user-{idx}"})
        rows.append({"role": "assistant", "content": f"assistant-{idx}"})
    compacted = core_mod._compact_history(rows, turns=4)
    assert compacted
    assert compacted[0]["role"] == "assistant"
    assert compacted[0]["content"].startswith("[context-compress]")
    assert any(item["content"] == "assistant-19" for item in compacted)
    assert len(compacted) <= 9


def test_ask_question_normalizes_execution_mode_to_act(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path.resolve()
    captured: dict[str, object] = {}

    def _fake_answer(_root_path, _question, **kwargs):
        captured["execution_mode"] = kwargs.get("execution_mode")
        return {"answer": "ok", "sources": [], "used_llm": False, "model": ""}

    monkeypatch.setattr("federhav.core.answer_help_question", _fake_answer)
    cfg = FederHavChatConfig(root=root, execution_mode="execute")
    ask_question(cfg, "질문")
    assert captured["execution_mode"] == "act"


def test_normalize_run_relpath_uses_custom_run_roots(tmp_path: Path) -> None:
    root = tmp_path.resolve()
    run_dir = root / "custom" / "runs_root" / "demo"
    run_dir.mkdir(parents=True, exist_ok=True)
    rel = core_mod.normalize_run_relpath(root, "demo", run_roots=["custom/runs_root"])
    assert rel == "custom/runs_root/demo"
