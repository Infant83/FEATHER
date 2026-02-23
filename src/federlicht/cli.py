from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from . import report as report_mod


def main() -> int:
    args = report_mod.parse_args()
    backend_token = str(os.getenv("FEDERLICHT_LLM_BACKEND") or "").strip().lower()
    if backend_token in {"codex", "codex_cli", "codex-cli", "cli"}:
        codex_model = str(os.getenv("CODEX_MODEL") or "").strip()
        if codex_model:
            model_raw = str(getattr(args, "model", "") or "").strip()
            if not model_raw or model_raw in {"$OPENAI_MODEL", report_mod.DEFAULT_MODEL}:
                args.model = codex_model
            check_raw = str(getattr(args, "check_model", "") or "").strip()
            if not check_raw or check_raw in {"$OPENAI_MODEL", report_mod.DEFAULT_CHECK_MODEL}:
                args.check_model = codex_model
            quality_raw = str(getattr(args, "quality_model", "") or "").strip()
            if not quality_raw:
                args.quality_model = codex_model
        print(
            f"[backend] FEDERLICHT_LLM_BACKEND=codex_cli (experimental bridge) model={getattr(args, 'model', '-')}",
            file=sys.stderr,
        )
    try:
        agent_overrides, config_overrides = report_mod.resolve_agent_overrides_from_config(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: failed to load agent config: {exc}", file=sys.stderr)
        return 2
    output_format, check_model = report_mod.prepare_runtime(args, config_overrides)
    if args.preview_template:
        value = args.preview_template.strip()
        if value.lower() == "all":
            out_dir = Path(args.preview_output) if args.preview_output else report_mod.templates_dir()
            out_dir.mkdir(parents=True, exist_ok=True)
            for name in report_mod.list_builtin_templates():
                spec = report_mod.load_template_spec(name, None)
                output_path = out_dir / f"preview_{spec.name}.html"
                report_mod.write_template_preview(spec, output_path)
                print(f"Wrote preview: {output_path}")
            return 0
        spec = report_mod.load_template_spec(value, None)
        output_path = report_mod.resolve_preview_output(spec, value, args.preview_output)
        report_mod.write_template_preview(spec, output_path)
        print(f"Wrote preview: {output_path}")
        return 0
    if args.agent_info:
        language = report_mod.normalize_lang(args.lang)
        report_prompt = report_mod.load_report_prompt(args.prompt, args.prompt_file)
        if args.template and str(args.template).strip().lower() != "auto":
            style_choice = args.template
        else:
            style_choice = report_mod.template_from_prompt(report_prompt) or report_mod.DEFAULT_TEMPLATE_NAME
        template_spec = report_mod.load_template_spec(style_choice, report_prompt)
        if not template_spec.sections:
            template_spec.sections = list(report_mod.DEFAULT_SECTIONS)
        required_sections = (
            list(report_mod.FREE_FORMAT_REQUIRED_SECTIONS) if args.free_format else list(template_spec.sections)
        )
        template_guidance_text = report_mod.build_template_guidance_text(template_spec)
        payload = report_mod.build_agent_info(
            args,
            output_format,
            language,
            report_prompt,
            template_spec,
            template_guidance_text,
            required_sections,
            args.free_format,
            agent_overrides,
        )
        report_mod.write_agent_info(payload, args.agent_info)
        return 0
    if args.stage_info:
        names, target = report_mod.parse_stage_info_arg(args.stage_info)
        payload = report_mod.get_stage_info(names)
        report_mod.write_stage_info(payload, target)
        return 0
    if args.site_refresh:
        site_root = report_mod.resolve_site_output(args.site_refresh)
        if not site_root:
            print("ERROR: --site-refresh requires a valid site directory.", file=sys.stderr)
            return 2
        from . import site_refresh

        manifest, index_path = site_refresh.refresh_site_from_runs(
            site_root,
            None,
            report_mod.build_site_manifest_entry,
            report_mod.write_site_manifest,
            report_mod.write_site_index,
            refresh_minutes=10,
            default_author=report_mod.DEFAULT_AUTHOR,
        )
        print(f"Wrote site manifest: {site_root / 'manifest.json'}")
        print(f"Wrote site index: {index_path}")
        return 0
    if args.generate_prompt:
        if not args.run:
            print("ERROR: --generate-prompt requires --run.", file=sys.stderr)
            return 2
        output_format, check_model = report_mod.prepare_runtime(args, config_overrides)
        create_deep_agent = report_mod.resolve_create_deep_agent(None)
        prompt_args = argparse.Namespace(**vars(args))
        prompt_args.stages = "scout"
        prompt_args.skip_stages = None
        prompt_args.alignment_check = False
        prompt_args.web_search = False
        prompt_args.template_adjust = False
        prompt_args.quality_iterations = 0
        pipeline_context = report_mod.PipelineContext(
            args=prompt_args,
            output_format=output_format,
            check_model=check_model,
        )
        orchestrator = report_mod.ReportOrchestrator(
            pipeline_context,
            report_mod,
            agent_overrides,
            create_deep_agent,
        )
        try:
            result = orchestrator.run(allow_partial=True)
        except Exception as exc:
            print(f"ERROR: failed to run scout for prompt generation: {exc}", file=sys.stderr)
            return 2
        prompt_text = report_mod.generate_prompt_from_scout(result, args, agent_overrides or {}, create_deep_agent)
        output_path = report_mod.resolve_prompt_output_path(args, result.run_dir, result.query_id)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(prompt_text, encoding="utf-8")
        print(f"Wrote prompt: {output_path}")
        return 0
    if args.generate_template:
        if not args.template_prompt or not args.template_name:
            print("ERROR: --generate-template requires --template-prompt and --template-name.", file=sys.stderr)
            return 2
        create_deep_agent = report_mod.resolve_create_deep_agent(None)
        language = report_mod.normalize_lang(args.lang)
        backend = report_mod.SafeFilesystemBackend(root_dir=Path.cwd())
        try:
            output_dir = report_mod.resolve_generated_template_dir(args)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        spec, css_text = report_mod.generate_template_from_prompt(
            args.template_prompt,
            report_mod._normalize_template_name(args.template_name),
            "Korean" if report_mod.is_korean_language(language) else language,
            args.model,
            create_deep_agent,
            backend,
        )
        md_path, css_path = report_mod.write_generated_template(spec, css_text, output_dir)
        print(f"Wrote template: {md_path}")
        print(f"Wrote template CSS: {css_path}")
        return 0
    if args.figures_preview:
        if not args.run:
            print("ERROR: --figures-preview requires --run.", file=sys.stderr)
            return 2
        if not args.output:
            print("ERROR: --figures-preview requires --output pointing to an existing report.", file=sys.stderr)
            return 2
        report_path = Path(args.output)
        if not report_path.exists():
            print(f"ERROR: report not found for --figures-preview: {report_path}", file=sys.stderr)
            return 2
        try:
            archive_dir, run_dir, _ = report_mod.resolve_archive(Path(args.run))
        except FileNotFoundError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        supporting_dir = None
        if args.supporting_dir:
            candidate = Path(args.supporting_dir)
            if not candidate.is_absolute():
                candidate = run_dir / candidate
            if candidate.exists():
                supporting_dir = candidate
            else:
                print(f"Warning: supporting dir not found, ignoring: {candidate}", file=sys.stderr)
        notes_dir = report_mod.resolve_notes_dir(run_dir, args.notes_dir)
        output_format = report_mod.choose_format(str(report_path))
        preview_path = report_mod.generate_figures_preview(
            report_path,
            run_dir,
            archive_dir,
            supporting_dir,
            notes_dir,
            output_format,
            args.figures_max_per_pdf,
            args.figures_min_area,
            args.figures_renderer,
            args.figures_dpi,
            args.model_vision,
        )
        if preview_path:
            print(f"Wrote figure preview: {preview_path}")
        else:
            print("No figure candidates found.", file=sys.stderr)
        return 0
    if not args.run:
        print("ERROR: --run is required unless --preview-template is used.", file=sys.stderr)
        return 2
    try:
        _, run_dir, _ = report_mod.resolve_archive(Path(args.run))
        report_mod.set_federlicht_log_path(run_dir)
    except Exception:
        run_dir = None
    try:
        report_mod.run_pipeline(
            args,
            agent_overrides=agent_overrides,
            config_overrides=config_overrides,
        )
        report_mod.finish_federlicht_log("JOB END")
    except RuntimeError as exc:
        report_mod.finish_federlicht_log(f"JOB FAILED: {exc}")
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
