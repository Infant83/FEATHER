from __future__ import annotations

import sys
from typing import Any

from .utils import extra_args, expand_env_reference, parse_bool, resolve_under_root
from .config import FedernettConfig

_CODEX_BACKENDS = {"codex_cli", "codex-cli", "codex", "cli"}


def _normalize_backend(value: Any) -> str:
    return str(value or "openai_api").strip().lower()


def _canonicalize_model_for_codex_backend(token: str) -> str:
    raw = str(token or "").strip()
    if not raw:
        return ""
    lowered = raw.lower()
    if lowered in {"$openai_model", "${openai_model}", "%openai_model%"}:
        return raw
    if lowered in {"$openai_model_vision", "${openai_model_vision}"}:
        return raw
    if raw.startswith("$") or (raw.startswith("${") and raw.endswith("}")):
        return raw
    if raw.startswith("%") and raw.endswith("%"):
        return raw
    return lowered


def _resolve_model_arg(value: Any, *, backend: str = "openai_api") -> str:
    token = expand_env_reference(value)
    if token is None:
        return ""
    raw = str(token).strip()
    if not raw:
        return ""
    lowered = raw.lower()
    if lowered.startswith("${") and lowered.endswith("}"):
        return ""
    if raw.startswith("$"):
        return ""
    if raw.startswith("%") and raw.endswith("%"):
        return ""
    if _normalize_backend(backend) in _CODEX_BACKENDS:
        return _canonicalize_model_for_codex_backend(raw)
    return raw


def _supports_reasoning_effort_arg(payload: dict[str, Any]) -> bool:
    backend = str(payload.get("llm_backend") or "openai_api").strip().lower()
    if backend in {"codex_cli", "codex-cli", "codex"}:
        return True
    model = _resolve_model_arg(payload.get("check_model")) or _resolve_model_arg(payload.get("model"))
    token = model.strip().lower()
    if not token:
        return False
    if "codex" in token:
        return False
    return token.startswith(("gpt-5", "o1", "o3", "o4")) or "reason" in token


def _build_feather_cmd(cfg: FedernettConfig, payload: dict[str, Any]) -> list[str]:
    input_path = payload.get("input")
    query = payload.get("query")
    output_root = payload.get("output")
    if not output_root:
        raise ValueError("Feather requires an output path.")
    if not input_path and not query:
        raise ValueError("Feather requires either input or query.")

    backend = _normalize_backend(payload.get("llm_backend"))
    cmd: list[str] = [sys.executable, "-u", "-m", "feather"]
    if input_path:
        resolved_input = resolve_under_root(cfg.root, str(input_path))
        cmd.extend(["--input", str(resolved_input)])
    elif query:
        cmd.extend(["--query", str(query)])
    resolved_output = resolve_under_root(cfg.root, str(output_root))
    cmd.extend(["--output", str(resolved_output)])
    if payload.get("lang"):
        cmd.extend(["--lang", str(payload.get("lang"))])
    if payload.get("days") is not None and str(payload.get("days")) != "":
        cmd.extend(["--days", str(payload.get("days"))])
    if payload.get("max_results") is not None and str(payload.get("max_results")) != "":
        cmd.extend(["--max-results", str(payload.get("max_results"))])
    if parse_bool(payload, "agentic_search"):
        cmd.append("--agentic-search")
        model = _resolve_model_arg(payload.get("model"), backend=backend)
        if model:
            cmd.extend(["--model", str(model)])
        if payload.get("max_iter") is not None and str(payload.get("max_iter")) != "":
            cmd.extend(["--max-iter", str(payload.get("max_iter"))])
    if parse_bool(payload, "download_pdf"):
        cmd.append("--download-pdf")
    if parse_bool(payload, "arxiv_src"):
        cmd.append("--arxiv-src")
    if parse_bool(payload, "openalex"):
        cmd.append("--openalex")
    if parse_bool(payload, "no_openalex"):
        cmd.append("--no-openalex")
    if payload.get("oa_max_results") is not None and str(payload.get("oa_max_results")) != "":
        cmd.extend(["--oa-max-results", str(payload.get("oa_max_results"))])
    if parse_bool(payload, "youtube"):
        cmd.append("--youtube")
    if parse_bool(payload, "no_youtube"):
        cmd.append("--no-youtube")
    if payload.get("yt_max_results") is not None and str(payload.get("yt_max_results")) != "":
        cmd.extend(["--yt-max-results", str(payload.get("yt_max_results"))])
    if payload.get("yt_order"):
        cmd.extend(["--yt-order", str(payload.get("yt_order"))])
    if parse_bool(payload, "yt_transcript"):
        cmd.append("--yt-transcript")
    if parse_bool(payload, "no_stdout_log"):
        cmd.append("--no-stdout-log")
    if parse_bool(payload, "no_citations"):
        cmd.append("--no-citations")
    if parse_bool(payload, "update_run"):
        cmd.append("--update-run")
    cmd.extend(extra_args(payload.get("extra_args")))
    return cmd


def _build_federlicht_cmd(cfg: FedernettConfig, payload: dict[str, Any]) -> list[str]:
    run_dir = payload.get("run")
    if not run_dir:
        raise ValueError("Federlicht requires a run path.")
    resolved_run = resolve_under_root(cfg.root, str(run_dir))

    backend = _normalize_backend(payload.get("llm_backend"))
    cmd: list[str] = [sys.executable, "-u", "-m", "federlicht.report", "--run", str(resolved_run)]
    output_path = payload.get("output")
    if output_path:
        resolved_output = resolve_under_root(cfg.root, str(output_path))
        cmd.extend(["--output", str(resolved_output)])
    free_format = parse_bool(payload, "free_format")
    if free_format:
        cmd.append("--free-format")
    style_pack = payload.get("style_pack")
    style_pack_value = str(style_pack).strip().lower() if style_pack is not None else ""
    if free_format and style_pack_value and style_pack_value not in {"none", "off", "false", "0"}:
        cmd.extend(["--style-pack", style_pack_value])
    template = payload.get("template")
    if template and not free_format:
        cmd.extend(["--template", str(template)])
    lang = payload.get("lang")
    if lang:
        cmd.extend(["--lang", str(lang)])
    depth = payload.get("depth")
    if depth:
        cmd.extend(["--depth", str(depth)])
    template_rigidity = payload.get("template_rigidity")
    if template_rigidity and not free_format:
        cmd.extend(["--template-rigidity", str(template_rigidity)])
    prompt = payload.get("prompt")
    if prompt:
        cmd.extend(["--prompt", str(prompt)])
    prompt_file = payload.get("prompt_file")
    if prompt_file:
        resolved_prompt = resolve_under_root(cfg.root, str(prompt_file))
        # FederHav suggested actions may carry stale prompt_file paths.
        # Skip non-existent files and let Federlicht fall back to inline/default prompt resolution.
        if resolved_prompt.exists():
            cmd.extend(["--prompt-file", str(resolved_prompt)])
    stages = payload.get("stages")
    if stages:
        cmd.extend(["--stages", str(stages)])
    skip_stages = payload.get("skip_stages")
    if skip_stages:
        cmd.extend(["--skip-stages", str(skip_stages)])
    model = _resolve_model_arg(payload.get("model"), backend=backend)
    if model:
        cmd.extend(["--model", str(model)])
    check_model = _resolve_model_arg(payload.get("check_model"), backend=backend)
    if check_model:
        cmd.extend(["--check-model", str(check_model)])
    model_vision = _resolve_model_arg(payload.get("model_vision"), backend=backend)
    if model_vision:
        cmd.extend(["--model-vision", str(model_vision)])
    temperature_level = payload.get("temperature_level")
    if temperature_level:
        cmd.extend(["--temperature-level", str(temperature_level)])
    reasoning_effort = str(payload.get("reasoning_effort") or "").strip().lower()
    if (
        reasoning_effort
        and reasoning_effort not in {"off", "none", "false", "0", "disabled"}
        and _supports_reasoning_effort_arg(payload)
    ):
        cmd.extend(["--reasoning-effort", reasoning_effort])
    quality_iterations = payload.get("quality_iterations")
    if quality_iterations is not None and str(quality_iterations) != "":
        cmd.extend(["--quality-iterations", str(quality_iterations)])
    quality_strategy = payload.get("quality_strategy")
    if quality_strategy:
        cmd.extend(["--quality-strategy", str(quality_strategy)])
    max_chars = payload.get("max_chars")
    if max_chars:
        cmd.extend(["--max-chars", str(max_chars)])
    max_tool_chars = payload.get("max_tool_chars")
    if max_tool_chars is not None and str(max_tool_chars) != "":
        cmd.extend(["--max-tool-chars", str(max_tool_chars)])
    progress_chars = payload.get("progress_chars")
    if progress_chars is not None and str(progress_chars) != "":
        cmd.extend(["--progress-chars", str(progress_chars)])
    max_pdf_pages = payload.get("max_pdf_pages")
    if max_pdf_pages is not None and str(max_pdf_pages) != "":
        cmd.extend(["--max-pdf-pages", str(max_pdf_pages)])
    html_print_profile = payload.get("html_print_profile")
    if html_print_profile:
        cmd.extend(["--html-print-profile", str(html_print_profile)])
    if parse_bool(payload, "html_pdf"):
        cmd.append("--html-pdf")
    if parse_bool(payload, "no_html_pdf"):
        cmd.append("--no-html-pdf")
    html_pdf_engine = payload.get("html_pdf_engine")
    if html_pdf_engine:
        cmd.extend(["--html-pdf-engine", str(html_pdf_engine)])
    html_pdf_wait_ms = payload.get("html_pdf_wait_ms")
    if html_pdf_wait_ms is not None and str(html_pdf_wait_ms) != "":
        cmd.extend(["--html-pdf-wait-ms", str(html_pdf_wait_ms)])
    html_pdf_timeout_sec = payload.get("html_pdf_timeout_sec")
    if html_pdf_timeout_sec is not None and str(html_pdf_timeout_sec) != "":
        cmd.extend(["--html-pdf-timeout-sec", str(html_pdf_timeout_sec)])
    tags = payload.get("tags")
    if tags:
        cmd.extend(["--tags", str(tags)])
    if parse_bool(payload, "no_tags"):
        cmd.append("--no-tags")
    if parse_bool(payload, "figures"):
        cmd.append("--figures")
    if parse_bool(payload, "no_figures"):
        cmd.append("--no-figures")
    figures_mode = payload.get("figures_mode")
    if figures_mode:
        cmd.extend(["--figures-mode", str(figures_mode)])
    figures_select = payload.get("figures_select")
    if figures_select:
        resolved_select = resolve_under_root(cfg.root, str(figures_select))
        cmd.extend(["--figures-select", str(resolved_select)])
    if parse_bool(payload, "web_search"):
        cmd.append("--web-search")
    agent_profile = payload.get("agent_profile")
    if agent_profile:
        cmd.extend(["--agent-profile", str(agent_profile)])
    agent_profile_dir = payload.get("agent_profile_dir")
    if agent_profile_dir:
        resolved_dir = resolve_under_root(cfg.root, str(agent_profile_dir))
        cmd.extend(["--agent-profile-dir", str(resolved_dir)])
    agent_config = payload.get("agent_config")
    if agent_config:
        resolved_config = resolve_under_root(cfg.root, str(agent_config))
        cmd.extend(["--agent-config", str(resolved_config)])
    site_output = payload.get("site_output")
    if site_output:
        resolved_site = resolve_under_root(cfg.root, str(site_output))
        cmd.extend(["--site-output", str(resolved_site)])

    cmd.extend(extra_args(payload.get("extra_args")))
    return cmd


def _build_generate_prompt_cmd(cfg: FedernettConfig, payload: dict[str, Any]) -> list[str]:
    run_dir = payload.get("run")
    if not run_dir:
        raise ValueError("Prompt generation requires a run path.")
    resolved_run = resolve_under_root(cfg.root, str(run_dir))

    backend = _normalize_backend(payload.get("llm_backend"))
    cmd: list[str] = [
        sys.executable,
        "-u",
        "-m",
        "federlicht.report",
        "--run",
        str(resolved_run),
        "--generate-prompt",
    ]
    output_path = payload.get("output")
    if output_path:
        resolved_output = resolve_under_root(cfg.root, str(output_path))
        cmd.extend(["--output", str(resolved_output)])
    free_format = parse_bool(payload, "free_format")
    if free_format:
        cmd.append("--free-format")
    style_pack = payload.get("style_pack")
    style_pack_value = str(style_pack).strip().lower() if style_pack is not None else ""
    if free_format and style_pack_value and style_pack_value not in {"none", "off", "false", "0"}:
        cmd.extend(["--style-pack", style_pack_value])
    template = payload.get("template")
    if template and not free_format:
        cmd.extend(["--template", str(template)])
    lang = payload.get("lang")
    if lang:
        cmd.extend(["--lang", str(lang)])
    depth = payload.get("depth")
    if depth:
        cmd.extend(["--depth", str(depth)])
    template_rigidity = payload.get("template_rigidity")
    if template_rigidity and not free_format:
        cmd.extend(["--template-rigidity", str(template_rigidity)])
    model = _resolve_model_arg(payload.get("model"), backend=backend)
    if model:
        cmd.extend(["--model", str(model)])
    check_model = _resolve_model_arg(payload.get("check_model"), backend=backend)
    if check_model:
        cmd.extend(["--check-model", str(check_model)])
    agent_config = payload.get("agent_config")
    if agent_config:
        resolved_config = resolve_under_root(cfg.root, str(agent_config))
        cmd.extend(["--agent-config", str(resolved_config)])
    temperature_level = payload.get("temperature_level")
    if temperature_level:
        cmd.extend(["--temperature-level", str(temperature_level)])
    reasoning_effort = str(payload.get("reasoning_effort") or "").strip().lower()
    if (
        reasoning_effort
        and reasoning_effort not in {"off", "none", "false", "0", "disabled"}
        and _supports_reasoning_effort_arg(payload)
    ):
        cmd.extend(["--reasoning-effort", reasoning_effort])
    cmd.extend(extra_args(payload.get("extra_args")))
    return cmd


def _build_generate_template_cmd(cfg: FedernettConfig, payload: dict[str, Any]) -> list[str]:
    prompt = payload.get("prompt")
    name = payload.get("name")
    if not prompt:
        raise ValueError("Template generation requires a prompt.")
    if not name:
        raise ValueError("Template generation requires a template name.")
    store = payload.get("store") or "run"
    cmd: list[str] = [sys.executable, "-u", "-m", "federlicht.report", "--generate-template"]
    if payload.get("run"):
        resolved_run = resolve_under_root(cfg.root, str(payload.get("run")))
        if resolved_run:
            cmd.extend(["--run", str(resolved_run)])
    cmd.extend(["--template-name", str(name)])
    cmd.extend(["--template-prompt", str(prompt)])
    cmd.extend(["--template-store", str(store)])
    model = _resolve_model_arg(payload.get("model"))
    if model:
        cmd.extend(["--model", str(model)])
    lang = payload.get("lang")
    if lang:
        cmd.extend(["--lang", str(lang)])
    site_output = payload.get("site_output")
    if site_output:
        resolved_site = resolve_under_root(cfg.root, str(site_output))
        if resolved_site:
            cmd.extend(["--site-output", str(resolved_site)])
    cmd.extend(extra_args(payload.get("extra_args")))
    return cmd
