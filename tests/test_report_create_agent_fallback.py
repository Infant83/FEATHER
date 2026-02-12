from __future__ import annotations

from federlicht import report


def test_create_agent_with_fallback_drops_subagents_on_typeerror() -> None:
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
