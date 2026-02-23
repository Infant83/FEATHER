from __future__ import annotations

import types

from federlicht import report


class _DummyTool:
    name = "demo_tool"
    description = "Demo tool."

    def __init__(self) -> None:
        self.calls = []

    def invoke(self, args):
        self.calls.append(dict(args))
        return {"ok": True, "value": args.get("x", 0) + 1}


def test_codex_bridge_executes_tool_protocol(monkeypatch) -> None:
    monkeypatch.setattr(report.shutil, "which", lambda _: "codex")
    monkeypatch.setenv("FEDERLICHT_CODEX_TOOL_CALLS", "1")
    monkeypatch.setenv("FEDERLICHT_CODEX_TOOL_MAX_CALLS", "3")

    outputs = [
        (
            '{"type":"message.completed","message":{"content":"'
            '{\\"tool_call\\":{\\"name\\":\\"demo_tool\\",\\"arguments\\":{\\"x\\":41}}}'
            '"}}',
            "",
            0,
        ),
        (
            '{"type":"message.completed","message":{"content":"final answer"}}',
            "",
            0,
        ),
    ]

    def fake_run(cmd, input, text, capture_output, encoding, errors):  # noqa: ANN001
        stdout, stderr, code = outputs.pop(0)
        return types.SimpleNamespace(stdout=stdout, stderr=stderr, returncode=code)

    monkeypatch.setattr(report.subprocess, "run", fake_run)

    tool = _DummyTool()
    bridge = report._CodexCliBridgeAgent("gpt-5.3-codex", "system", tools=[tool])
    result = bridge.invoke({"messages": [{"role": "user", "content": "test"}]})

    assert result["messages"][0]["content"] == "final answer"
    assert tool.calls == [{"x": 41}]
