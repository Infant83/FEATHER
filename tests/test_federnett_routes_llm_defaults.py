from __future__ import annotations

from federnett import routes


def _clear_env(monkeypatch) -> None:
    for key in (
        "OPENAI_BASE_URL",
        "OPENAI_API_BASE",
        "OPENAI_MODEL",
        "OPENAI_MODEL_VISION",
        "FEDERHAV_MODEL",
        "FEATHER_AGENTIC_MODEL",
        "FEDERLICHT_CHECK_MODEL",
    ):
        monkeypatch.delenv(key, raising=False)


def test_cloud_defaults_prefer_gpt5_nano_and_federhav_lightweight(monkeypatch) -> None:
    _clear_env(monkeypatch)
    assert routes._is_onprem_openai_compatible() is False
    assert routes._preferred_openai_model() == "gpt-5-nano"
    assert routes._preferred_federhav_model() == "gpt-4o-mini"
    assert routes._preferred_feather_agentic_model() == "gpt-5-nano"


def test_onprem_defaults_select_qwen_and_llama_policy(monkeypatch) -> None:
    _clear_env(monkeypatch)
    monkeypatch.setenv("OPENAI_BASE_URL", "http://127.0.0.1:8000/v1")
    assert routes._is_onprem_openai_compatible() is True
    assert routes._preferred_openai_model() == "Qwen3-235B-A22B-Instruct-2507"
    assert routes._preferred_openai_vision_model() == "Llama-4-Scout"
    assert routes._preferred_federhav_model() == "Qwen3-235B-A22B-Thinking-2507"
    assert routes._preferred_feather_agentic_model() == "Qwen3-Coder-480B-A35B-Instruct"
    assert routes._preferred_federlicht_check_model("Qwen3-235B-A22B-Instruct-2507") == "Qwen3-235B-A22B-Thinking-2507"


def test_explicit_env_overrides_win_over_defaults(monkeypatch) -> None:
    _clear_env(monkeypatch)
    monkeypatch.setenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
    monkeypatch.setenv("OPENAI_MODEL", "custom-writer-model")
    monkeypatch.setenv("OPENAI_MODEL_VISION", "custom-vision-model")
    monkeypatch.setenv("FEDERHAV_MODEL", "custom-hav-model")
    monkeypatch.setenv("FEATHER_AGENTIC_MODEL", "custom-feather-model")
    monkeypatch.setenv("FEDERLICHT_CHECK_MODEL", "custom-check-model")
    assert routes._preferred_openai_model() == "custom-writer-model"
    assert routes._preferred_openai_vision_model() == "custom-vision-model"
    assert routes._preferred_federhav_model() == "custom-hav-model"
    assert routes._preferred_feather_agentic_model() == "custom-feather-model"
    assert routes._preferred_federlicht_check_model("fallback-model") == "custom-check-model"
