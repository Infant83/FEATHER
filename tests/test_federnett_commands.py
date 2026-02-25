from __future__ import annotations

from pathlib import Path

from federnett.commands import _build_federlicht_cmd, _build_generate_prompt_cmd
from federnett.config import FedernettConfig


def _cfg(tmp_path: Path) -> FedernettConfig:
    root = tmp_path.resolve()
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


def test_build_federlicht_cmd_includes_agent_config(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "output": "site/runs/demo/report_full.md",
        "agent_config": "site/runs/demo/instruction/agent_config.json",
    }

    cmd = _build_federlicht_cmd(cfg, payload)

    assert "--agent-config" in cmd
    idx = cmd.index("--agent-config")
    assert cmd[idx + 1] == str((tmp_path / "site" / "runs" / "demo" / "instruction" / "agent_config.json").resolve())


def test_build_generate_prompt_cmd_includes_agent_config(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "agent_config": "site/runs/demo/instruction/agent_config.json",
    }

    cmd = _build_generate_prompt_cmd(cfg, payload)

    assert "--agent-config" in cmd
    idx = cmd.index("--agent-config")
    assert cmd[idx + 1] == str((tmp_path / "site" / "runs" / "demo" / "instruction" / "agent_config.json").resolve())


def test_build_federlicht_cmd_omits_missing_prompt_file(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "output": "site/runs/demo/report_full.md",
        "prompt_file": "site/runs/demo/instruction/generated_prompt_demo.txt",
    }

    cmd = _build_federlicht_cmd(cfg, payload)

    assert "--prompt-file" not in cmd


def test_build_federlicht_cmd_includes_existing_prompt_file(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    prompt_path = tmp_path / "site" / "runs" / "demo" / "instruction" / "generated_prompt_demo.txt"
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text("demo prompt", encoding="utf-8")
    payload = {
        "run": "site/runs/demo",
        "output": "site/runs/demo/report_full.md",
        "prompt_file": "site/runs/demo/instruction/generated_prompt_demo.txt",
    }

    cmd = _build_federlicht_cmd(cfg, payload)

    assert "--prompt-file" in cmd
    idx = cmd.index("--prompt-file")
    assert cmd[idx + 1] == str(prompt_path.resolve())


def test_build_federlicht_cmd_free_format_disables_template_args(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "output": "site/runs/demo/report_full.md",
        "template": "default",
        "template_rigidity": "balanced",
        "free_format": True,
    }

    cmd = _build_federlicht_cmd(cfg, payload)

    assert "--free-format" in cmd
    assert "--template" not in cmd
    assert "--template-rigidity" not in cmd


def test_build_federlicht_cmd_free_format_includes_style_pack(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "output": "site/runs/demo/report_full.md",
        "free_format": True,
        "style_pack": "dark",
    }

    cmd = _build_federlicht_cmd(cfg, payload)

    assert "--style-pack" in cmd
    idx = cmd.index("--style-pack")
    assert cmd[idx + 1] == "dark"


def test_build_federlicht_cmd_ignores_style_pack_without_free_format(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "output": "site/runs/demo/report_full.md",
        "style_pack": "dark",
    }

    cmd = _build_federlicht_cmd(cfg, payload)

    assert "--style-pack" not in cmd


def test_build_generate_prompt_cmd_free_format_disables_template_args(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "template": "default",
        "template_rigidity": "balanced",
        "free_format": True,
    }

    cmd = _build_generate_prompt_cmd(cfg, payload)

    assert "--free-format" in cmd
    assert "--template" not in cmd
    assert "--template-rigidity" not in cmd


def test_build_generate_prompt_cmd_free_format_includes_style_pack(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "free_format": True,
        "style_pack": "journal",
    }

    cmd = _build_generate_prompt_cmd(cfg, payload)

    assert "--style-pack" in cmd
    idx = cmd.index("--style-pack")
    assert cmd[idx + 1] == "journal"


def test_build_federlicht_cmd_ignores_temperature_override(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "output": "site/runs/demo/report_full.md",
        "temperature_level": "high",
        "temperature": 0.9,
    }

    cmd = _build_federlicht_cmd(cfg, payload)

    assert "--temperature-level" in cmd
    assert "--temperature" not in cmd


def test_build_generate_prompt_cmd_ignores_temperature_override(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "temperature_level": "high",
        "temperature": 0.9,
    }

    cmd = _build_generate_prompt_cmd(cfg, payload)

    assert "--temperature-level" in cmd
    assert "--temperature" not in cmd


def test_build_federlicht_cmd_includes_reasoning_effort(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "output": "site/runs/demo/report_full.md",
        "model": "gpt-5-mini",
        "reasoning_effort": "extra_high",
    }

    cmd = _build_federlicht_cmd(cfg, payload)

    assert "--reasoning-effort" in cmd
    idx = cmd.index("--reasoning-effort")
    assert cmd[idx + 1] == "extra_high"


def test_build_generate_prompt_cmd_includes_reasoning_effort(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "model": "gpt-5-mini",
        "reasoning_effort": "high",
    }

    cmd = _build_generate_prompt_cmd(cfg, payload)

    assert "--reasoning-effort" in cmd
    idx = cmd.index("--reasoning-effort")
    assert cmd[idx + 1] == "high"


def test_build_federlicht_cmd_omits_reasoning_effort_when_off(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "output": "site/runs/demo/report_full.md",
        "reasoning_effort": "off",
    }

    cmd = _build_federlicht_cmd(cfg, payload)

    assert "--reasoning-effort" not in cmd


def test_build_generate_prompt_cmd_omits_reasoning_effort_when_off(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "reasoning_effort": "off",
    }

    cmd = _build_generate_prompt_cmd(cfg, payload)

    assert "--reasoning-effort" not in cmd


def test_build_federlicht_cmd_omits_reasoning_effort_for_codex_named_openai_model(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "output": "site/runs/demo/report_full.md",
        "llm_backend": "openai_api",
        "model": "gpt-5.3-codex",
        "reasoning_effort": "high",
    }

    cmd = _build_federlicht_cmd(cfg, payload)

    assert "--reasoning-effort" not in cmd


def test_build_generate_prompt_cmd_omits_reasoning_effort_for_non_reasoning_model(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "llm_backend": "openai_api",
        "model": "gpt-4o-mini",
        "reasoning_effort": "high",
    }

    cmd = _build_generate_prompt_cmd(cfg, payload)

    assert "--reasoning-effort" not in cmd


def test_build_generate_prompt_cmd_normalizes_codex_model_to_lowercase(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "llm_backend": "codex_cli",
        "model": "GPT-5.3-Codex-Spark",
    }

    cmd = _build_generate_prompt_cmd(cfg, payload)

    assert "--model" in cmd
    idx = cmd.index("--model")
    assert cmd[idx + 1] == "gpt-5.3-codex-spark"


def test_build_federlicht_cmd_includes_html_pdf_export_options(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "output": "site/runs/demo/report_full.html",
        "html_print_profile": "letter",
        "html_pdf": True,
        "html_pdf_engine": "auto",
        "html_pdf_wait_ms": 2200,
        "html_pdf_timeout_sec": 90,
    }

    cmd = _build_federlicht_cmd(cfg, payload)

    assert "--html-print-profile" in cmd
    assert cmd[cmd.index("--html-print-profile") + 1] == "letter"
    assert "--html-pdf" in cmd
    assert "--html-pdf-engine" in cmd
    assert cmd[cmd.index("--html-pdf-engine") + 1] == "auto"
    assert "--html-pdf-wait-ms" in cmd
    assert cmd[cmd.index("--html-pdf-wait-ms") + 1] == "2200"
    assert "--html-pdf-timeout-sec" in cmd
    assert cmd[cmd.index("--html-pdf-timeout-sec") + 1] == "90"


def test_build_federlicht_cmd_supports_disabling_html_pdf(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path)
    payload = {
        "run": "site/runs/demo",
        "output": "site/runs/demo/report_full.html",
        "no_html_pdf": True,
    }

    cmd = _build_federlicht_cmd(cfg, payload)

    assert "--no-html-pdf" in cmd
