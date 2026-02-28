import datetime as dt
import json
from pathlib import Path

from federlicht.pipeline_runner_impl import (
    _build_deck_manifest_entry,
    _count_cached_stage_hits,
    _deck_target_slide_count,
    _estimate_pass_tokens,
    _flatten_execution_stage_order,
    _merge_workflow_stage_status,
    _render_slide_deck_artifacts,
)


def test_flatten_execution_stage_order_expands_runtime_stage_bundles() -> None:
    ordered = _flatten_execution_stage_order(["evidence", "writer"])
    assert ordered[:4] == ["web", "evidence", "plan_check", "writer"]
    assert "scout" in ordered
    assert "quality" in ordered


def test_merge_workflow_stage_status_prefers_non_disabled_updates() -> None:
    merged = _merge_workflow_stage_status(
        [
            [
                "1. scout: ran",
                "2. plan: disabled",
            ],
            [
                "1. plan: ran (cached)",
                "2. scout: disabled",
            ],
        ]
    )
    assert merged["scout"] == {"status": "ran", "detail": ""}
    assert merged["plan"] == {"status": "ran", "detail": "cached"}


def test_count_cached_stage_hits_only_counts_selected_runtime_stages() -> None:
    summary = [
        "1. scout: cached",
        "2. plan: ran",
        "3. evidence: cached",
        "4. quality: skipped",
    ]
    hits = _count_cached_stage_hits(summary, ("scout", "plan", "writer"))
    assert hits == 1


def test_estimate_pass_tokens_uses_delta_from_previous_state() -> None:
    from types import SimpleNamespace

    result = SimpleNamespace(
        language="en",
        scout_notes="abcd" * 40,
        plan_text="",
        evidence_notes="",
        claim_map_text="",
        gap_text="",
        report="",
    )
    previous = SimpleNamespace(
        scout_notes="abcd" * 10,
        plan_text="",
        evidence_notes="",
        claim_map_text="",
        gap_text="",
        report="",
    )
    # Delta chars = 120, en ratio=4 -> 30 tokens
    assert _estimate_pass_tokens(result, previous) == 30


def test_reordered_pipeline_runs_multipass_with_dependency_expansion_disabled(monkeypatch, tmp_path) -> None:
    import argparse
    from types import SimpleNamespace

    import federlicht.pipeline_runner_impl as runner
    from federlicht import workflow_stages

    run_dir = tmp_path / "run"
    (run_dir / "archive").mkdir(parents=True, exist_ok=True)

    calls: list[tuple[str, bool, bool]] = []
    merged_orders: list[list[str]] = []

    class FakeOrchestrator:
        def __init__(self, context, _helpers, _overrides, _create) -> None:
            self._args = context.args

        def run(self, state=None, allow_partial=False):
            calls.append(
                (
                    str(getattr(self._args, "stages", "") or ""),
                    bool(getattr(self._args, "_disable_stage_dependency_expansion", False)),
                    bool(allow_partial),
                )
            )
            stages = [token.strip() for token in str(self._args.stages or "").split(",") if token.strip()]
            summary = [f"{idx}. {name}: ran" for idx, name in enumerate(stages, start=1)] or ["1. scout: skipped"]
            return SimpleNamespace(
                report="",
                scout_notes="",
                plan_text="",
                plan_context="",
                evidence_notes="",
                align_draft=None,
                align_final=None,
                align_scout=None,
                align_plan=None,
                align_evidence=None,
                template_spec=SimpleNamespace(name="default"),
                template_guidance_text="",
                template_adjustment_path=None,
                required_sections=[],
                report_prompt=None,
                clarification_questions=None,
                clarification_answers=None,
                output_format="md",
                language="en",
                run_dir=run_dir,
                archive_dir=run_dir / "archive",
                notes_dir=run_dir / "report_notes",
                supporting_dir=None,
                supporting_summary=None,
                source_triage_text="",
                claim_map_text="",
                gap_text="",
                context_lines=[],
                depth="normal",
                style_hint="",
                overview_path=None,
                index_file=None,
                instruction_file=None,
                quality_model="gpt-4o",
                query_id="q",
                workflow_summary=summary,
                workflow_path=None,
            )

    def fake_write_workflow_summary(**kwargs):
        merged_orders.append(list(kwargs.get("stage_order") or []))
        return (["1. scout: ran"], Path(run_dir / "report_notes" / "report_workflow.md"))

    monkeypatch.setattr(runner, "resolve_archive", lambda path: (run_dir / "archive", run_dir, "q"))
    monkeypatch.setattr(runner, "load_report_prompt", lambda _prompt, _file: "")
    monkeypatch.setattr(runner, "expand_update_prompt_with_base", lambda raw, _run: raw)
    monkeypatch.setattr(runner, "resolve_agent_overrides_from_config", lambda _args, explicit_overrides=None: (explicit_overrides or {}, {}))
    monkeypatch.setattr(runner, "prepare_runtime", lambda _args, _cfg: ("md", "gpt-4o"))
    monkeypatch.setattr(runner, "resolve_create_deep_agent", lambda value: value)
    monkeypatch.setattr(runner, "ReportOrchestrator", FakeOrchestrator)
    monkeypatch.setattr(runner, "write_workflow_summary", fake_write_workflow_summary)
    monkeypatch.setattr(runner, "build_pipeline_state", lambda _result: None)

    args = argparse.Namespace(
        run=str(run_dir),
        stages="quality,plan",
        skip_stages=None,
        _state_only=True,
        prompt=None,
        prompt_file=None,
    )
    output = runner.run_pipeline(args, state_only=True)
    assert output.meta["state_only"] is True

    requested = workflow_stages.parse_top_level_stages(stages_raw="quality,plan", skip_stages_raw=None)
    execution_plan = workflow_stages.resolve_top_level_execution_plan(requested)
    expected_passes = [",".join(workflow_stages.top_level_stage_bundle(stage)) for stage in execution_plan]
    assert [stage for stage, _flag, _partial in calls] == expected_passes
    assert all(flag for _stage, flag, _partial in calls)
    assert all(partial for _stage, _flag, partial in calls)
    assert merged_orders and merged_orders[-1] == _flatten_execution_stage_order(execution_plan)


def test_deck_target_slide_count_by_depth() -> None:
    assert _deck_target_slide_count("brief") == 6
    assert _deck_target_slide_count("normal") == 9
    assert _deck_target_slide_count("deep") == 12
    assert _deck_target_slide_count("exhaustive") == 16


def test_render_slide_deck_artifacts_generates_html_fallback(monkeypatch, tmp_path) -> None:
    import federlicht.pipeline_runner_impl as runner

    run_dir = tmp_path / "run"
    notes_dir = run_dir / "report_notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    claim_packet = {
        "schema_version": "v1",
        "claims": [
            {
                "claim_id": "C001",
                "claim_text": "Demo claim for deck export.",
                "section_hint": "key_findings",
                "evidence_ids": ["E001"],
                "source_kind": "web",
                "score": 0.9,
            }
        ],
        "evidence_registry": [{"evidence_id": "E001", "ref": "https://example.com/source"}],
    }
    (notes_dir / "claim_evidence_map.json").write_text(json.dumps(claim_packet, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(runner.pptx_renderer, "_pptx_available", lambda: False)

    output_pptx = run_dir / "deck.pptx"
    meta = _render_slide_deck_artifacts(
        run_dir=run_dir,
        notes_dir=notes_dir,
        output_pptx_path=output_pptx,
        report_prompt="Deck prompt",
        depth="normal",
        report_title="Demo Deck",
        quality_profile="deep_research",
    )

    assert meta["deck_status"] == "partial_html_only"
    html_path = Path(str(meta.get("deck_html_path") or ""))
    assert html_path.exists()
    assert output_pptx.exists() is False
    assert (notes_dir / "slide_outline.v1.json").exists()
    assert (notes_dir / "slide_ast.v1.json").exists()
    assert (notes_dir / "slide_quality.summary.json").exists()
    assert (notes_dir / "slide_quality.md").exists()
    assert (notes_dir / "slide_quality.trace.json").exists()
    assert isinstance(meta.get("deck_quality_gate_pass"), bool)
    assert meta.get("deck_quality_profile") == "deep_research"
    assert isinstance(meta.get("deck_diagram_snapshot_count"), int)
    assert int(meta.get("deck_quality_iterations") or 0) >= 1


def test_build_deck_manifest_entry_includes_companion_paths(tmp_path) -> None:
    site_root = tmp_path / "site" / "report_hub"
    run_dir = site_root / "runs" / "demo_run"
    report_dir = run_dir / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    primary = report_dir / "deck.html"
    primary.write_text("<html></html>", encoding="utf-8")
    deck_pptx = report_dir / "deck.pptx"
    deck_pptx.write_bytes(b"pptx")

    entry = _build_deck_manifest_entry(
        site_root=site_root,
        run_dir=run_dir,
        title="Deck Demo",
        author="Tester",
        summary="Deck summary",
        language="en",
        template_name="default",
        generated_at=dt.datetime(2026, 2, 26, 10, 0, 0),
        model_name="gpt-5",
        tags=["deck"],
        primary_artifact_path=primary,
        deck_html_path=primary,
        deck_pptx_path=deck_pptx,
        deck_quality_profile="deep_research",
        deck_quality_effective_band="deep_research",
        deck_quality_overall=92.4,
        deck_quality_gate_pass=True,
        deck_quality_iterations=2,
        report_overview_path=None,
        workflow_path=None,
    )

    assert entry is not None
    payload = dict(entry or {})
    assert payload.get("format") == "pptx"
    paths = dict(payload.get("paths") or {})
    assert paths.get("report") == "runs/demo_run/report/deck.html"
    assert paths.get("deck_html") == "runs/demo_run/report/deck.html"
    assert paths.get("deck_pptx") == "runs/demo_run/report/deck.pptx"
    quality = dict(payload.get("deck_quality") or {})
    assert quality.get("profile") == "deep_research"
    assert quality.get("effective_band") == "deep_research"
    assert quality.get("overall") == 92.4
    assert quality.get("gate_pass") is True
    assert quality.get("iterations") == 2
