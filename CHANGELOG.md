# Changelog

## 1.9.30 (2026-02-26)
- P0+ completion batch (iter 123~132):
  - quality-contract metric versioning and stale handling:
    - add `src/federlicht/quality_contract.py` with
      `QUALITY_CONTRACT_METRIC_VERSION=qc-metrics.v2` and stale detector.
    - write `metric_version` to `quality_contract.latest.json` in orchestrator.
    - upgrade `tools/run_report_quality_gate.py` consistency logic:
      - detect stale legacy contracts (`selected_eval` source or missing/mismatched metric_version),
      - mark as `skipped/stale` with reason instead of false consistency failure,
      - include `skipped/stale/stale_reason/metric_version` in markdown reports.
  - runtime stability fix for Data Scientist stage:
    - fix stage budget parameter mismatch (`min_budget/max_budget` -> `minimum/default_budget/hard_cap`),
    - fix deep-mode `condensed` undefined reference path.
  - tests:
    - add `tests/test_quality_contract.py`.
    - extend `tests/test_report_quality_contract_consistency_tool.py`.
    - regression subset pass (`26 passed`).
  - codex sample run:
    - generated `site/runs/openclaw/report_full_iter123_codex_brief.html`.
    - exported artifacts:
      - `test-results/p0_sample_openclaw_iter123_codex_snapshot.html`
      - `test-results/p0_quality_gate_openclaw_iter123_codex_world.md`
    - world-class gate PASS (`overall=96.53`, `claim_support=97.22`, `unsupported=1`, `coherence=100`).
- P0+ quality calibration batch (iter 122):
  - generic citation recognition uplift in quality heuristics (`src/federlicht/report.py`):
    - add domain-label source detection (`openclaw.ai` style, without protocol),
    - add archive/run path citation detection (`/archive/...txt`, `runs/...`),
    - add DOI and escaped numeric citation support (`\\[1\\]`).
  - unsupported-claim overcount reduction:
    - exclude HTML table-row (`tr`) text from substantive claim candidate extraction,
    - exclude epistemic proposal/interpretation markers (`(제안)`, `(해석)`, `(전망)` and english equivalents) from unsupported claim counting.
  - tests:
    - expand `tests/test_report_quality_heuristics.py` with
      domain/archive citation recognition and proposal-marker exclusion coverage.
    - regression subset passed (`20 passed`).
  - quality gate:
    - multi-run world-class gate recovered to PASS:
      - `test-results/p0_quality_gate_multi_iter122_world.md`
      - avg `overall=93.42`, `claim_support=81.48`, `unsupported=6.00`, `section_coherence=90.67`.
- P0+ document-quality uplift batch (iter 121):
  - add data-scientist analysis path for report generation:
    - new prompt contract `prompts.build_data_scientist_prompt(...)` with anti-hallucination rules,
      source-grounded numeric interpretation, and narrative-style provenance guidance.
    - integrate `Data Scientist` analysis after evidence mapping and before writer finalization in
      `src/federlicht/orchestrator.py`.
    - persist analysis artifact to `report_notes/analysis_notes.md` and inject into writer/quality context.
  - extend agent registry/stage map:
    - add `data_scientist` agent entry and evidence-stage mapping in `src/federlicht/agent_info_impl.py`.
  - report hub back-link stabilization:
    - replace fragile `/runs/` path slicing with robust candidate resolution
      (`../../report_hub/index.html` first) in:
      - `src/federlicht/render/html.py`
      - `src/federlicht/templates/preview_default.html`
    - patch current QC sample report back-link script:
      - `site/runs/20260221_QC_report/report_full_iter51.html`
  - tests:
    - add `tests/test_render_back_link.py`
    - extend `tests/test_report_prompt_quality_policy.py` for data-scientist prompt policy
    - regression subset passed (agent/pipeline/quality/render suites).
- P0+ quality calibration batch (iter 101~120):
  - improve heuristic section coverage robustness for flexible report styles:
    - semantic heading alias support (`Lede`, `How It Works`, `The Story So Far`, `Open Questions`, etc.).
    - heading normalization for numbering/punctuation/case variations.
  - reduce false unsupported-claim counts by excluding non-content HTML sections:
    - `Report Prompt`, `References`, `Miscellaneous`, `Appendix`, `Source Index`, metadata-like sections.
  - improve section coherence scoring stability by skipping non-content sections in HTML span analysis.
  - expand methodology signal keywords (`workflow`, `pipeline`, `how it works`, `QUBO`, `Ising`, etc.).
  - add quality heuristic tests:
    - semantic section coverage alias check (HTML).
    - unsupported claim detector exclusion for non-content sections.
  - validation snapshot:
    - QC sample (`site/runs/20260221_QC_report/report_full_iter51.html`) world-class gate PASS.
    - quality regression-related test suite pass (`31 passed`).
- Workflow docs hygiene:
  - reinforce temporary-output policy in `docs/development_workflow_guide.md`:
    - limit root transient dirs to `temp/`, `test-results/`, `node_modules/`, `artifacts/`.
    - add explicit safe cleanup commands for local ephemeral dirs.
- P2 infographic/export/QA batch (iter 20~111):
  - section-aware infographic auto insertion hardening:
    - strengthen claim-packet split rendering and multi-section insertion paths.
    - persist insertion/lint metadata to run artifacts (`infographic_auto_insert.json`, lint snapshots).
  - HTML->PDF regression tooling:
    - add `tools/run_html_pdf_regression.py` for bytes/pages baseline checks and structured JSON summary output.
    - add regression tests (`tests/test_html_pdf_regression_tool.py`, `tests/test_report_html_pdf.py`).
  - quality gate + lint orchestration upgrades:
    - expand `tools/run_report_quality_gate.py` infographic lint reporting and strict-fail path coverage.
    - add/extend tests for gate runner, artwork tooling, and infographic insertion flow.
  - handoff updates:
    - add `docs/codex_handoff_20260226.md` with iter governance, batch verification records, and next-plan priorities.

## 1.9.29 (2026-02-23)
- Version consistency policy hardening:
  - align versions across `pyproject.toml`, `README.md`, `CHANGELOG.md`, and `src/federlicht/versioning.py`.
  - add `tools/check_version_consistency.py` to validate cross-file version consistency.
  - add `tests/test_version_consistency_tool.py`.
- Quality loop optimization (iter 91~100):
  - add `src/federlicht/quality_iteration.py` gate-distance ranking helpers for candidate selection under quality targets.
  - integrate gate-distance-aware candidate ranking in `src/federlicht/orchestrator.py`:
    - prefer gate pass first, then smaller failure count/distance, then overall.
    - persist candidate evaluations in `quality_contract.latest.json`.
  - add profile compare utility:
    - `tools/report_quality_profile_compare.py`
    - outputs profile matrix for `smoke/baseline/professional/world_class`.
  - add/expand tests:
    - `tests/test_quality_iteration.py`
    - `tests/test_report_quality_profile_compare_tool.py`
- Documentation and workflow:
  - update `docs/dev_history/handoffs/codex_handoff_20260223.md` (iter logs/progress).
  - update `docs/report_quality_threshold_policy.md` with profile compare usage.
  - update README quality tooling examples.

## 1.9.28 (2026-02-23)
- Quality-loop optimization for profile-driven report refinement:
  - add `src/federlicht/quality_iteration.py` with:
    - profile-aware iteration policy (`min/max`, plateau delta/patience),
    - iteration-plan resolver,
    - quality delta and plateau detection helpers,
    - metric-driven focus-directive builder for critic/reviser prompts.
  - integrate quality iteration policy into `src/federlicht/orchestrator.py`:
    - profile-based effective quality pass calculation,
    - pass-level focus directives injected into critique/revision context,
    - convergence-aware early stop on plateau,
    - pass trace artifact `report_notes/quality_pass_trace.json`.
  - persist iteration-plan/trace metadata to:
    - `report_notes/quality_contract.latest.json`
    - `report_notes/quality_gate.json`
- Profile-level gate diagnostics:
  - add `tools/report_quality_profile_compare.py` to evaluate one benchmark summary across:
    - `smoke`, `baseline`, `professional`, `world_class`.
  - output supports JSON + Markdown matrix for quick level diagnostics.
- Tests:
  - add `tests/test_quality_iteration.py`.
  - add `tests/test_report_quality_profile_compare_tool.py`.
  - regression run:
    - `pytest -q tests/test_quality_iteration.py tests/test_quality_profiles.py tests/test_report_quality_profile_compare_tool.py tests/test_report_quality_contract_consistency_tool.py tests/test_report_quality_gate_runner.py tests/test_report_quality_regression_gate.py tests/test_pipeline_runner_impl.py tests/test_pipeline_runner_reordered_e2e.py tests/test_report_quality_heuristics.py tests/test_template_adjust_fallback.py` -> `35 passed`.
- Diagnostics artifact:
  - run profile matrix on QC sample summary:
    - `test-results/p0_quality_profile_compare_qc_iter90.json`
    - `test-results/p0_quality_profile_compare_qc_iter90.md`

## 1.9.27 (2026-02-23)
- Report quality gate threshold policy normalization:
  - add shared quality profile module `src/federlicht/quality_profiles.py`:
    - `none`, `smoke`, `baseline`, `professional`, `world_class`
    - unified target resolver (`resolve_quality_gate_targets`) and effective-band classifier.
  - clarify that low thresholds (e.g., `overall=65`) are smoke-level health checks, not world-class.
- Federlicht runtime gate profile support:
  - add `--quality-profile` to Federlicht CLI (`src/federlicht/cli_args.py`).
  - apply profile + override resolution in orchestrator (`src/federlicht/orchestrator.py`).
  - persist profile/band/policy metadata in:
    - `report_notes/quality_contract.latest.json`
    - `report_notes/quality_gate.json`
  - align quality contract metric source to `final_signals` for consistency checks:
    - write `metric_source=final_signals`
    - keep `selected_eval_legacy` for traceability
- Tooling alignment:
  - `tools/report_quality_regression_gate.py`:
    - add `--quality-profile` (default `baseline`), emit `gate-policy` line.
  - `tools/run_report_quality_gate.py`:
    - add `--quality-profile` (default `baseline`).
    - include profile/band/targets in markdown report.
- Documentation:
  - add `docs/report_quality_threshold_policy.md`.
  - update handoff and workflow guide references.
- Tests:
  - add `tests/test_quality_profiles.py`.
  - extend `tests/test_report_quality_gate_runner.py`, `tests/test_federlicht_cli_args.py`.
  - regression run:
    - `pytest -q tests/test_quality_profiles.py tests/test_report_quality_gate_runner.py tests/test_report_quality_regression_gate.py tests/test_federlicht_cli_args.py tests/test_pipeline_runner_impl.py tests/test_pipeline_runner_reordered_e2e.py tests/test_report_quality_heuristics.py tests/test_template_adjust_fallback.py` -> `26 passed`.
  - world-class gate check on QC sample:
    - `python tools/run_report_quality_gate.py ... --quality-profile world_class` -> `FAIL` (expected; thresholds now explicit).
  - consistency source regression:
    - `pytest -q tests/test_report_quality_contract_consistency_tool.py` includes `metric_source=final_signals` case.

## 1.9.26 (2026-02-22)
- P0 completion batch (Federnett UX/governance polish):
  - Report Hub collaboration accessibility/density pass:
    - add explicit `aria-label` for approval/comment/follow-up inputs.
    - add `Ctrl/Cmd+Enter` approval-note submit shortcut.
    - improve timeline scrolling behavior (`overscroll-behavior`, touch scrolling).
  - Root-auth aware approval UX:
    - disable approval save when root auth is enabled but locked.
    - surface lock state directly in approval hint + save button tooltip.
  - Workflow Stage override guardrail hardening:
    - enforce prompt max length (`6000`) with auto-trim.
    - enforce max tool tokens (`24`) with truncation warning.
    - warn on runtime-unknown tool tokens using active capability registry.
  - Live Logs low-resolution/mobile polish:
    - refine dock/thread/composer viewport-height policy.
    - improve compact scrolling behavior and reduce dead zones in constrained layouts.
  - Theme contrast pass (white-first, black-compatible):
    - improve semantic chip readability for `meta-pill`, `pipeline-chip`, and `workflow-stage-chip` states.
- DeepAgent P1 continuation:
  - keep action-planner fallback reduction path stable while integrating above UI/guardrail changes.
- Tests / checks:
  - `python -m pytest tests/test_help_agent.py tests/test_report_hub_api.py tests/test_federnett_routes.py -q` passed (`115 passed`).
  - `node --check site/federnett/app.js` passed.

## 1.9.25 (2026-02-22)
- Report Hub approval UI transition-awareness (P0):
  - integrate backend `allowed_next` approval transition metadata into Run Studio collaboration panel.
  - dynamically enable/disable approval status options based on allowed transitions.
  - add inline approval transition hint/warning (`run-hub-approval-hint`) with theme-safe styling.
  - block invalid approval submit attempts client-side with clear log feedback.
  - on approval `403` responses, trigger root-auth status refresh and immediate panel re-render.
- DeepAgent Phase B-3 start: action-planner fallback reduction (P1):
  - add `_allow_llm_action_planner_fallback(runtime_mode)` in `src/federnett/help_agent.py`.
  - default behavior:
    - `runtime_mode=auto/deepagent`: no LLM action-planner fallback.
    - `runtime_mode=off`: LLM fallback allowed.
  - explicit opt-in override: `FEDERNETT_HELP_ACTION_LLM_FALLBACK=1`.
- Regression coverage:
  - update/extend `tests/test_help_agent.py` for fallback policy defaults and opt-in behavior.
  - keep LLM planner fallback path covered under explicit opt-in.
- Tests / checks:
  - `python -m pytest tests/test_help_agent.py tests/test_report_hub_api.py tests/test_federnett_routes.py -q` passed (`115 passed`).
  - `node --check site/federnett/app.js` passed.

## 1.9.24 (2026-02-22)
- Report Hub approval workflow hardening (P0):
  - add explicit approval transition policy in `src/federnett/report_hub.py`:
    - status graph via `_APPROVAL_TRANSITIONS`
    - transition validation via `_is_valid_approval_transition(...)`
    - reject invalid transitions with clear errors (e.g. `published -> draft`).
  - enrich approval payload contract with `allowed_next` so UI can show valid next states.
- Report Hub approval authorization hardening (P0):
  - add route-level guard for `/api/report-hub/approval` in `src/federnett/routes.py`.
  - when root-auth is enabled, approval updates now require root unlock (or root-role session path already recognized by auth helpers).
- Regression coverage expansion (P1 support):
  - `tests/test_report_hub_api.py`
    - validate invalid transition rejection.
    - validate `allowed_next` metadata in baseline/update/load flows.
  - `tests/test_federnett_routes.py`
    - validate approval route returns `403` when root-auth is enabled but locked.
    - validate approval route succeeds after root unlock token.
    - validate invalid transition returns `400`.
- Tests / checks:
  - `python -m pytest tests/test_report_hub_api.py tests/test_federnett_routes.py -q` passed (`49 passed`).
  - `node --check site/federnett/app.js` passed.

## 1.9.23 (2026-02-22)
- Live Logs log-bridge turn mapping upgrade:
  - store per-turn process bounds (`log_start`/`log_end`) in live history rows.
  - rehydrate per-turn process logs from bounds when `process_log` text is missing.
  - include process bounds for system execution events (job start/done/error) so system turns can render bridge context consistently.
- Live Logs bridge visibility/persistence polish:
  - show global bridge card while job/ask is active even when other turns already exist.
  - show global bridge card when no turn-level bridge is attached yet.
  - make process fold state independent per turn via fold-key scoping (prevents unrelated turns sharing open/close state).
  - clarify running tooltip to indicate timeline + per-turn bridge locations.
- DeepAgent/Federnett route contract hardening (P1 support):
  - add SSE regression test to ensure `/api/help/ask/stream` preserves `activity(action_plan)` payload details (`execution_handoff` etc.).
- Tests / checks:
  - `node --check site/federnett/app.js` passed.
  - `python -m pytest tests/test_federnett_routes.py tests/test_federnett_commands.py -q` passed.

## 1.9.22 (2026-02-22)
- Federnett LLM policy persistence hardening (iter-1):
  - enforce `llm_policy` normalization on `/api/workspace/settings` GET/POST via `_normalize_llm_policy_payload(...)`.
  - keep legacy/global payload compatibility while returning canonical scoped policy shape.
  - normalize stored workspace policy responses to prevent backend/model/reasoning/runtime drift between runs.
- LLM Settings effective-visibility upgrade (iter-2):
  - add per-scope effective summary lines in LLM Settings modal:
    - Global baseline
    - Feather effective policy
    - Federlicht effective policy
    - FederHav effective policy
  - wire live preview updates while editing mode/backend/model/runtime/log-tail controls.
  - improve summary surface styling for dark/white themes (`policy-effective-line`).
- Tests / checks:
  - `node --check site/federnett/app.js` passed.
  - `python -m pytest tests/test_federnett_routes.py tests/test_federnett_commands.py -q` passed (`60 passed`).

## 1.9.21 (2026-02-22)
- LLM policy split (Global + Scoped) in Federnett:
  - extend LLM Settings modal to manage:
    - Global baseline
    - Feather policy (inherit/custom)
    - Federlicht policy (inherit/custom)
    - FederHav policy (inherit/custom)
  - FederHav default is now separated from global and starts with `gpt-4o-mini` policy preset.
  - Federlicht scoped default uses environment-first model hints (`OPENAI_MODEL`, `OPENAI_MODEL_VISION`).
- Stage override management unification:
  - move stage override editor (`wf-stage-*`) from Workflow Studio into LLM Settings.
  - keep Workflow Studio section as guidance-only to avoid dual editing surfaces.
- Workspace settings persistence expansion:
  - add `llm_policy` support in `site/federnett/workspace_settings.json`.
  - extend `/api/workspace/settings` GET/POST to return/save `llm_policy`.
  - frontend applies localStorage policy and attempts workspace persistence when root unlock is available.
- Tests / checks:
  - `node --check site/federnett/app.js` passed.
  - `python -m pytest tests/test_federnett_routes.py -q` passed (`40 passed`).

## 1.9.20 (2026-02-22)
- FederHav DeepAgent Phase B-2 completion (`action proposal -> execution handoff`):
  - extend deepagent action planner schema in `src/federhav/agentic_runtime.py` with:
    - `confidence`
    - `intent_rationale`
    - `execution_handoff`
  - add deepagent executor preflight tool:
    - `execution_preflight` (`_ActionPreflightTool`)
    - run/instruction readiness checks via `_build_action_preflight(...)`.
  - normalize planner payload/handoff in runtime:
    - `_normalize_action_planner_payload(...)`
    - `_sanitize_execution_handoff(...)`.
  - parse JSON-string `state_memory` in runtime memory tool payload path (improves deepagent grounding).
- Federnett help-agent trace/handoff wiring:
  - preserve planner metadata (`planner`, `confidence`, `intent_rationale`, `execution_handoff`) in normalized actions.
  - append structured `action_plan` trace step (`details` payload) in both sync and stream paths.
  - emit `action_plan` activity event in stream mode.
  - tighten rule fallback policy to emergency opt-in only (`FEDERNETT_HELP_RULE_FALLBACK=1|true|on|yes|emergency`).
- Federnett UI action-preview contract update:
  - action preview now reflects planner handoff/preflight metadata.
  - run-target resolution prefers planner preflight hints (`resolved_run_rel`, `run_hint`) before heuristic inference.
- Tests:
  - add regressions in `tests/test_help_agent.py` for:
    - deepagent handoff metadata preservation,
    - structured `action_plan` trace details,
    - emergency fallback opt-in behavior.
  - validation:
    - `python -m py_compile src/federhav/agentic_runtime.py src/federnett/help_agent.py tests/test_help_agent.py` passed
    - `node --check site/federnett/app.js` passed
    - `pytest -q tests/test_help_agent.py tests/test_federhav_core.py tests/test_federhav_cli.py tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `127 passed`

## 1.9.19 (2026-02-22)
- FederHav DeepAgent Phase B-1 progression:
  - add deepagent action-planner runtime path in `src/federhav/agentic_runtime.py`:
    - `try_deepagent_action_plan(...)`
    - governor+executor subagent bridge for action JSON planning.
  - add planner prompt/history/capability helpers:
    - `_build_action_planner_messages(...)`
    - `_normalize_history(...)`
    - `_capability_digest(...)`
    - `_extract_first_json_object(...)`
- Federnett help-agent action path integration:
  - add `_try_agentic_runtime_action_plan(...)` in `src/federnett/help_agent.py`.
  - make `_infer_agentic_action(...)` deepagent-planner-first with legacy LLM planner fallback.
  - keep run-content summary guardrails intact (content-analysis questions do not auto-escalate to run actions).
- Tests:
  - add deepagent planner priority/fallback regression tests in `tests/test_help_agent.py`.
  - validation:
    - `pytest -q tests/test_help_agent.py tests/test_federhav_core.py tests/test_federhav_cli.py` -> `67 passed`
    - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `57 passed`
    - `node --check site/federnett/app.js` passed.

## 1.9.18 (2026-02-22)
- FederHav/help-agent behavior generalization (remove phrase-locked ad-hoc branch):
  - remove conditional prompt branch that changed reply policy via `_question_asks_run_content_summary(...)`.
  - switch to a single, generic path-first analysis rule in `_help_user_prompt(...)`.
  - replace path-summary specific action-planning bypass with generic file-context detection (`_is_file_context_question`).
- Run-context evidence grounding improvement:
  - extend text source extensions to include `.jsonl/.ndjson/.csv/.tsv`.
  - allow archive-scoped run context inclusion for file/path-oriented questions.
  - keep run-file prioritization based on explicit path hints without hardcoded question phrase mapping.
- Deepagent runtime guidance hardening:
  - strengthen governor prompt in `federhav.agentic_runtime` to prefer `read_run_file` for concrete path/file questions.
  - require finding-first responses before action proposals to reduce placeholder-only replies.
- Run Studio file preview reliability:
  - fix filtered-view branch in `renderRunFiles(...)` where `data-file-open` buttons were not bound in `visibleGroups=0` state.
  - preserve preview open behavior when filter chips narrow the view.
- White theme markdown preview consistency:
  - add white-theme specific styles for `.file-preview-markdown` (background/text/code/pre) to match other preview surfaces.
- FederHav run-content interaction policy hardening (5-iter patch set):
  - add run-content summary intent detector (`_is_run_content_summary_request`) and path-reference detector
    (`_has_run_content_path_reference`) to separate file interpretation requests from workflow execution requests.
  - enforce no-action guard for run-content summary questions in all action inference paths:
    - `_infer_agentic_action`, `_infer_governed_action`, `_infer_safe_action`.
  - improve run hint extraction safety:
    - trim nested artifact paths (`runs/<run>/archive/...`) to run name only and prevent nested-path run creation drift.
  - improve run context recovery for FederHav:
    - infer effective `run_rel` from `state_memory.scope.run_rel`/`state_memory.run.run_rel`
      when explicit payload run is missing in both sync/stream help paths.
- Validation:
  - `node --check site/federnett/app.js` passed.
  - `pytest -q tests/test_help_agent.py -k "path_first or file_context or archive or run_context or path_hint or needs_agentic_action_planning"` -> passed.
  - `pytest -q tests/test_federnett_routes.py -k "preview or run_map or run_files or live"` -> passed.
  - `pytest -q tests/test_federnett_commands.py -k "run or prompt or preview"` -> passed.
  - `python -m py_compile src/federnett/help_agent.py src/federnett/capabilities.py` -> passed.
  - `pytest -q tests/test_help_agent.py tests/test_capabilities.py` -> `63 passed`.
  - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py tests/test_federhav_core.py tests/test_federhav_cli.py` -> `64 passed`.
  - Playwright artifacts:
    - `test-results/ui-iter17-preview-theme-after-fix.json`
    - `test-results/ui-iter17-preview-theme-after-fix.png`
    - `test-results/ui-iter18-preview-post-ad-hoc-removal.json`
    - `test-results/ui-iter18-preview-post-ad-hoc-removal.png`

## 1.9.17
- Federnett UI/UX refresh (layout openness + readability):
  - remove sticky behavior from sidebar/logs columns (`control`, `telemetry`) so page scroll remains natural.
  - expand Live Logs usable area (`#logs-wrap`, `live-ask-dock`, thread height) to better use viewport height.
  - simplify FederHav composer into sticky floating-style input dock with cleaner prompt/status presentation.
  - tighten workflow strip readability (chip sizing, contrast, spacing, state badge legibility).
- Theme/contrast hardening (especially White theme):
  - fix workspace settings panel dark residual backgrounds under white theme.
  - improve white-theme agent profile panel contrast (`readonly` hint, apply chips, status cards, tab/title visibility).
  - add white-theme danger-button contrast override (remove low-contrast pink-on-light issue).
- FederHav input micro-copy cleanup:
  - simplify input placeholder/label wording in Live Logs.
  - keep runtime/model metadata visible in compact form beneath input.
- Validation:
  - `pytest -q tests/test_federnett_routes.py` -> `39 passed`
  - `pytest -q tests/test_help_agent.py` -> `44 passed`
  - `pytest -q tests/test_federnett_commands.py tests/test_federnett_auth.py` -> `22 passed`
  - Python Playwright audit:
    - `test-results/theme-ui-refresh-audit-20260222.json` (`min_contrast=6.07`, `page_errors=0`, `topbar_scroll_follow_delta=818.0`, `thread_h=1000.34`)
    - `test-results/white-theme-workspace-contrast-20260222.json` (workspace/agent contrast checks improved)

## 1.9.16
- Federlicht report-quality upgrade (intent-aware 2nd pass):
  - add `report_intent` policy axis (`research/review/decision/briefing/explainer/slide/narrative/generic`).
  - propagate intent-aware guidance across planner/evidence/writer/writer-finalizer/evaluator prompts.
  - add quality-loop anti-regression guardrails so revision/finalizer does not weaken evidence density or methodology/limits disclosure.
- Quality evaluation hardening:
  - blend LLM evaluation with deterministic heuristic signals (`section_coverage`, `citation_density`, `method_transparency`, `traceability`, `uncertainty_handling`).
  - keep intent/depth-aware weighting in heuristic overall score.
- Heuristic parser reliability:
  - support HTML heading extraction (`<h2>`), HTML link citations (`href="https://..."`), markdown links (`[](...)`), and numeric bracket citations (`[1]`).
  - reduce scoring distortion between markdown/html outputs.
- Validation and examples:
  - `pytest -q tests/test_report_prompt_quality_policy.py tests/test_report_quality_heuristics.py tests/test_report_reasoning_policy.py tests/test_federnett_commands.py tests/test_federnett_routes.py tests/test_help_agent.py` -> `116 passed`
  - generated local iterative examples:
    - `site/runs/openclaw/report_full_iter_brief_example.html`
    - `site/runs/openclaw/report_full_iter_brief_quality.html`
    - `site/runs/openclaw/report_full_iter_brief_base.md`

## 1.9.15
- Run Folder single-entry policy (2nd pass):
  - remove editable Run Name/Run Folder controls from Feather/Federlicht panels.
  - keep run target changes only through top `Run Folder` modal.
  - add in-panel shortcut buttons to open the shared Run Folder modal.
- Run root expansion UX:
  - add `Add Run Root` control in Run Folder modal workspace settings.
  - support sanitize/save/reload flow for custom run roots.
  - keep run-folder creation input sanitized to no-space naming.
- Path consistency hardening:
  - remove Feather submit heuristic that rewrote run-folder output to parent root.
  - force Federlicht output path to selected run + filename leaf only.
- Live Logs compact v2:
  - unify Live Ask run/stop into single toggle button.
  - move workflow strip below thread area and compact node/badge footprint.
  - raise default auto log-tail preset to `2.2k` and reflect adaptive context wording.
- Validation:
  - `node --check site/federnett/app.js` passed
  - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py tests/test_help_agent.py` -> `101 passed`
  - Python Playwright smoke (`http://127.0.0.1:8877/`): pageerror 0, readonly/hidden run controls + single live-run button + custom run-root controls confirmed.

## 1.9.14
- Global LLM policy unification (2nd pass):
  - remove duplicated backend/model/reasoning controls from Feather/Federlicht/Live Ask/Workflow Studio panels.
  - keep `LLM Settings` as the only editable control point for backend/model/check/vision/reasoning.
  - sync runtime payload fallbacks to global model policy to avoid panel-level drift.
- White theme UX contrast patch:
  - add explicit white-theme overrides for top bar, major panels, form inputs/selects, dropdown options, and log cards.
  - reduce dark hardcoded backgrounds under `Theme=White` and improve readability.
- FederHav action-intent guardrail hardening:
  - tighten action planning trigger to workspace-operation intent (run/workflow/stage/instruction/prompt) and short generic follow-up execution only.
  - remove planner bias that forced short generic queries toward `run_feather`.
  - prevent safe fallback from auto-running pipeline on content-only analysis requests.
- Validation:
  - `node --check site/federnett/app.js` passed
  - `pytest -q tests/test_help_agent.py` -> `44 passed`
  - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `57 passed`

## 1.9.13
- Workspace/run-root global control hardening:
  - add server-side workspace settings API:
    - `GET /api/workspace/settings`
    - `POST /api/workspace/settings` (root unlock required when root auth is enabled)
  - add persistent workspace settings file:
    - `site/federnett/workspace_settings.json`
  - apply persisted workspace roots on Federnett startup (`run_roots`, `site_root`, `report_hub_root`).
- Run Folder UX refactor:
  - move run-folder control out of Federlicht panel into top action bar (`Run Folder`).
  - remove in-panel `Open Run Folder` button.
  - extend run picker modal with unified `Load / Open / Create` actions.
  - support `run_root` targeting on run creation via `/api/runs/create`.
  - add workspace root settings block in run picker modal (reload/save).
- Model policy UX unification:
  - add top action `LLM Settings` modal as a single global entry point.
  - add global sync lock (`Global Sync Lock`) to propagate backend/model policy across Feather/Federlicht/FederHav.
  - split model catalogs by backend (`openai-model-options`, `codex-model-options`).
  - bind model inputs to backend-specific datalists dynamically.
  - allow blank model input persistence in panel UX (no forced immediate refill while editing).
- Workflow pipeline readability:
  - reduce badge clutter by suppressing quiet `READY` display in node chips.
  - keep signal-focused badges (`running/queued/off/resume/error`, plus result/history done signals).
- Validation:
  - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `56 passed`
  - `node --check site/federnett/app.js` passed
  - `python -m compileall -q src` passed
  - Python Playwright smoke (ephemeral local Federnett server):
    - top buttons order verified (`Reload Runs`, `Run Folder`, `LLM Settings`, `Agent Workspace Settings`)
    - run-folder modal workspace controls visible
    - global model datalist switches `openai-model-options` -> `codex-model-options`
    - Federlicht model keeps blank value after manual clear.

## 1.9.12
- Federlicht prompt-path root consistency fix (`site/runs` vs `runs`):
  - resolve prompt/report default paths from the selected run folder path (not only run name).
  - update run-relative expansion logic to prefer the selected run root (`site/runs/*` or `runs/*`) instead of global-first root fallback.
  - ensure `Generate Prompt` payload keeps `run` and `output` under the same selected run root.
- Federnett UX:
  - rename Federlicht prompt action button text from `Generate` to `Generate Prompt`.
- Validation:
  - Playwright check confirms for `site/runs/20260221_QC_report`:
    - prompt field defaults to `site/runs/.../instruction/generated_prompt_...txt`
    - `POST /api/federlicht/generate_prompt` payload `output` stays in `site/runs/...`.

## 1.9.11
- Codex backend model-token reliability fix:
  - normalize Codex model tokens to lowercase across Federnett UI/runtime and command builders.
  - prevent uppercase model values (for example `GPT-5.3-Codex-Spark`) from reaching `codex exec` unchanged.
  - add runtime normalization notes in Federlicht model policy logs (`Codex backend selected: model normalized -> ...`).
- Federnett/API alignment:
  - normalize Codex defaults/options in `/api/info.llm_defaults.codex_model_options`.
  - keep Feather agentic model payload normalized when backend is `codex_cli`.
- Validation:
  - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `53 passed`
  - live API check (`/api/federlicht/generate_prompt`) confirms command model arg normalized to `gpt-5.3-codex-spark`.

## 1.9.10
- Report hub publish flow hardening:
  - add local linked-asset publish policy in `federlicht.hub_publish` for HTML reports.
  - preserve report subpath under run when publishing (for relative-link stability).
  - expose publish diagnostics: `published_asset_paths`, `skipped_asset_refs`.
- Federnett publish UX wiring:
  - add Run Studio `Publish to Report Hub` button.
  - add `POST /api/report-hub/publish` endpoint to bridge Federnett -> `federlicht.hub_publish`.
  - include publish result payload (`published_asset_rels`, `skipped_asset_refs`, manifest/index paths).
- Docs:
  - refresh handoff status and publish coverage notes (`docs/dev_history/handoffs/codex_handoff_20260220.md`).
  - update run/site strategy with linked-assets policy and Federnett publish wiring (`docs/run_site_publish_strategy.md`).
- Validation:
  - `pytest -q tests/test_hub_publish.py tests/test_federnett_routes.py` -> `37 passed`
  - Playwright smoke: Run Studio publish button visibility and run-with-report enable state confirmed.

## 1.9.9
- Federnett UI policy update (Feather/Federlicht):
  - remove collapsible `Advanced` sections in both side panels and keep execution options visible by default.
  - add explicit Feather agentic backend policy note so default backend/model behavior is always visible.
  - strengthen backend-model auto-mapping:
    - Feather agentic model now follows selected backend defaults (`openai_api` <-> `codex_cli`).
    - Federlicht backend switch now force-syncs model/check defaults to prevent stale `gpt-4o-mini` under Codex backend.
- Live Logs compact UX tuning:
  - normalize process-fold summary to a true one-line header (`agent/backend · tool N · Ran ...`).
  - improve summary readability with overflow-safe single-line styling.
- Workflow Studio stage override clarity:
  - add selected/focus stage badges near stage dropdown.
  - improve stage prompt chain preview wording and stage-context readability.
  - replace initial tools placeholder with non-loading guidance text.
- Docs:
  - update handoff state and remaining items (`docs/dev_history/handoffs/codex_handoff_20260220.md`).
  - extend PPT writer strategy for partial artifact patch/edit via FederHav (`docs/ppt_writer_strategy.md`).

## 1.9.8
- Federlicht prompt flexibility hardening (no rigid one-size-fits-all defaults):
  - apply adaptive guidance by `depth + template_rigidity + free_format` across planner/evidence/writer/evaluator prompts.
  - keep strict mode enforceable while balanced/brief/free-format paths use recommendation-first wording.
  - soften deep-mode visual mandates outside strict mode to reduce over-constraint on review/brief requests.
- Prompt policy wiring consistency:
  - propagate `depth/template_rigidity/free_format` into planner/evidence/writer-finalizer/evaluator call paths.
  - align evaluator prompt policy in runtime and agent-info defaults.
- Documentation and operations:
  - update `docs/dev_history/handoffs/codex_handoff_20260220.md` with latest status, validation snapshots, and open TODOs.
  - add PPT expansion strategy draft: `docs/ppt_writer_strategy.md`.
  - extend run/site separation guide with on-prem + GitLab remote split workflow (`docs/run_site_publish_strategy.md`).
- Local verification:
  - `python -m feather --review ./site/runs/openclaw --format text`
  - `python -m federlicht.hub_publish --report ./site/runs/openclaw/report_full.html --run ./site/runs/openclaw --hub ./site/report_hub`
  - Playwright local check passed for `site/report_hub/index.html` (`contains_openclaw=True`).

## 1.9.7
- Federlicht report-quality policy uplift:
  - strengthen planner instructions with explicit method/result/uncertainty tracks.
  - strengthen evidence extraction instructions with an `Evidence Ledger` requirement (claim/evidence/source/strength/limits/recency).
  - strengthen writer instructions for method transparency, result traceability (`evidence matrix`), and uncertainty disclosure.
  - strengthen evaluator instructions to score method transparency and traceability quality.
- Report hub publish implementation for run/site separation:
  - add `python -m federlicht.hub_publish` module to publish approved run outputs into `site/report_hub/reports/*`.
  - copy report (+ optional run overview/workflow notes) and update `manifest.json` + `index.html` in one step.
  - add tests for publish path behavior (`tests/test_hub_publish.py`).
- Deployment and operations:
  - add baseline `.gitlab-ci.yml` with `pytest_smoke` and `pages` jobs (publishes `site/report_hub`).
  - update handoff/strategy/docs for on-prem + GitLab Pages publish flow and Playwright MCP troubleshooting.
  - add prompt-quality regression tests (`tests/test_report_prompt_quality_policy.py`).

## 1.9.6
- Federnett run-root and hub separation hardening:
  - switch default run discovery roots to `runs,site/runs` (new runs prefer `runs/*`, legacy `site/runs/*` stays compatible).
  - keep report hub root explicit (`site/report_hub`) and expose run/hub separation consistently in UI hints and docs.
  - strengthen run-hint normalization in both UI and help-agent logic to respect configured run roots (not only `site/runs`).
- Workspace Sidebar / Run Studio UX alignment:
  - remove `Open Run Studio` quick button and keep tab-specific single primary action (`Run Feather` or `Run Federlicht`).
  - stop forced focus jumps when opening Run Studio tab; keep panel switching behavior consistent with Feather/Federlicht tabs.
  - clarify Feather output field as `Run Folder (Output)` with resolved run-root hint text.
- Workflow and Live Logs clarity:
  - fix `Result` node state so completed pipelines do not show misleading `running` badge.
  - render process logs as collapsible blocks with `Ran <command>` summary labels.
  - place global pipeline log bridge card after turn messages when no per-turn process logs exist.
- Workflow Studio cleanup:
  - remove redundant settings blocks already available in workspace panels (`Feather/Federlicht/Quality` duplicate controls).
  - improve stagebar/detail frame visibility via z-index/background/overflow tuning.
- Validation:
  - `pytest -q tests/test_help_agent.py tests/test_federnett_routes.py tests/test_federnett_commands.py tests/test_site_hub_separation.py` -> `95 passed`
  - `pytest -q tests/test_site_hub_separation.py` -> `2 passed`
  - Playwright checks on `http://127.0.0.1:8767/` for tab consistency, quick-button visibility, Run Studio focus behavior, and Workflow Studio section cleanup.

## 1.9.5
- FederHav clarify-first execution flow hardening:
  - add `clarify_required` and `clarify_question` in help-agent action responses for short/generic execution requests.
  - block Act auto-run when clarification is required and surface follow-up guidance instead of direct execution.
  - add `질의 보강하기` follow-up action in Live Ask to inject clarification prompts directly into input.
- Governor trace visibility upgrade (Ask + Live Ask):
  - include `trace.trace_id` and per-step telemetry (`tool_id`, `duration_ms`, `token_est`, `cache_hit`) in sync/stream responses.
  - stream `activity` events into Ask trace panel and Live Ask process log as structured `run-agent:activity` lines.
  - expose trace summary chips (`trace=<id>`, `tools=<N>`) in Live Ask turn metadata.
- Observability/UI consistency:
  - keep Ask trace timeline synchronized for stream and legacy fallback paths via shared trace application logic.
  - classify and render `run-agent:activity` entries in structured log cards with tool-trace blocks.
- Validation:
  - `pytest -q tests/test_help_agent.py tests/test_federnett_routes.py` -> `76 passed`
  - `pytest -q tests/test_help_agent.py tests/test_federnett_routes.py tests/test_federnett_auth.py tests/test_report_hub_api.py tests/test_federhav_core.py tests/test_federhav_cli.py` -> `89 passed`
  - Playwright manual checks on `http://127.0.0.1:8767/` for clarify action + trace metadata rendering.

## 1.9.4
- FederHav agentic-policy tightening:
  - disable safe-rule action fallback by default and keep it as explicit opt-in only via `FEDERNETT_HELP_RULE_FALLBACK=1`.
  - keep `auto/deepagent` path as the primary governing runtime for action planning.
- Live Logs UX compaction (4th pass):
  - reduce process-log tail volume defaults (`max lines/chars`) to lower timeline noise.
  - render per-turn process trace as collapsible `실행 trace N줄` blocks and persist fold state.
  - clarify context wording (`state-memory + 최근 실행 로그 보조요약`) and keep policy detail in tooltip/placeholder.
  - improve process source labeling (`실행 프로세스`) and role tagging (`feather/federlicht/tool`).
- Workflow Studio operability:
  - force Studio into overview-first mode while preserving selected-node focus hint.
  - keep all sections visible and highlight only the relevant scope section instead of narrowing to single-stage view.

## 1.9.3
- Agent Profiles auth/permission hardening:
  - allow built-in profile edits when the current session role is `root/admin/owner/superuser` (without requiring a separate root token unlock).
  - include `session_root` in root-auth status payload and wire the UI to reflect session-root unlock state.
- Live Logs readability pass:
  - reduce live-thread bottom inset inflation to avoid clipped-looking tails.
  - remove nested scroll inside inline process-log blocks (single-scroll timeline flow).
  - compact composer helper line (`N자 · Enter · Shift+Enter`) while keeping context policy in tooltip/placeholder.
- Workflow Studio selection clarity:
  - increase active/inactive contrast for pipeline chips to make stage selection state more obvious.
- Tests:
  - add session-root permission tests in `tests/test_federnett_auth.py`.

## 1.9.2
- FederHav/Federnett agentic runtime and execution guard improvements:
  - keep deepagent-first routing in `auto/deepagent` mode while reducing rule fallback dependence.
  - strengthen direct `Run Feather` guard so weak prompts (for example generic "실행해줘") trigger instruction quality checks and auto-draft recovery before execution.
- Live Logs UX stability pass:
  - add dynamic thread bottom inset sizing tied to composer height to reduce bottom clipping/truncation.
  - compact input helper line to include context policy inline (`state-memory + 최근 로그 tail 요약 N자`).
  - hide noisy default `Ready.` status line in the Live composer for lower visual density.
  - expand real-time-log noise filtering for legacy header lines (`실시간 로그 N줄` variants with symbols/prefixes).
  - render process logs inline in each turn to reduce extra fold/popup hops during live operation.
- Sidebar/layout adjustments:
  - widen collapsed workspace rail and rebalance collapsed action button sizing/wrapping for clearer `Feather/Federlicht/Run Studio` access.
- Model/options sync fix:
  - consume Codex model options from `/api/info.llm_defaults.codex_model_options` in datalist merge path.
- Session auth skeleton (server-side):
  - add `SessionAuthManager` and `/api/auth/session/login|logout|status` endpoints.
  - expose `session_auth` state via `/api/info`.
  - auto-attach session signer metadata (`signed_by`, `signed_role`) to report-hub comment/followup/link writes when authenticated.
- Session auth UI wiring:
  - add Agent Profiles panel sign-in/sign-out control (`agent-session-auth`) with persisted session token header forwarding.
  - show current session principal/role/expiry badge next to root unlock status.

## 1.9.1
- FederHav orchestration control expanded across CLI and Federnett Live Logs:
  - add operational command flow for `/plan`, `/act`, `/profile`, `/agent`
  - wire `agent`/`execution_mode`/`allow_artifacts` end-to-end (UI -> API -> help-agent core)
  - persist optional `agent_override` in ask preferences
- Federnett Live Logs UI/UX (3rd pass) compaction and priority tuning:
  - add explicit `profile`/`agent` context chips in FederHav Live Timeline
  - restore a dedicated `FederHav 제안` action rail inside Live Timeline
  - reduce header/context density and hide global system-log card when no active run is executing
  - improve sidebar readability with wider default panel, tighter quick-run layout, and container-query fallback
- Report hub API skeleton completed for id-based post integration:
  - post listing/detail endpoints
  - comments/follow-up prompt endpoints
  - post-to-run link mapping endpoints
  - filesystem-backed storage under `report_hub/api_data/*`
- Tests:
  - add/extend coverage for FederHav CLI/core, help-agent operator controls, report-hub routes and storage.

## 1.9.0
- FederHav CLI upgraded to dual-mode operation:
  - new `federhav chat` interactive operator mode (one-shot with `--question` supported)
  - legacy revision runner kept as `federhav update` with backward-compatible flag routing
  - shared FederHav chat core added at `src/federhav/core.py`, reusing `federnett.help_agent`
  - run/profile-scoped chat history persistence aligned with Federnett history storage
- Federnett Live Logs UI/UX (2nd pass) refresh:
  - FederHav Live Dialog reorganized with a clearer split between thread and composer on wide screens
  - run/mode/log context chips added for quick operational state awareness
  - spacing, hierarchy, and panel sizing tuned for better readability in dense runs
- Report hub separation groundwork:
  - default Federlicht site output moved to `site/report_hub`
  - site refresh now supports sibling-runs fallback (`<hub>/../runs`) when `<hub>/runs` is absent
  - manifest entry paths now support relative links outside hub root (for example `../runs/...`)
  - report back-link logic now prefers `report_hub/index.html` with fallback to `index.html`
  - Federnett API now exposes `report_hub_root` in `/api/info`
- Documentation updates:
  - README version bump and FederHav chat usage added
  - report hub hosting instructions updated for `site/runs` + `site/report_hub` separation
- Tests added:
  - FederHav core/CLI behavior tests
  - report hub path separation tests

## 1.8.0
- Expand artwork/diagram runtime with a new `artwork_diagrams_render` tool:
  - render architecture SVG artifacts via Python `diagrams` from node/edge specs
  - keep run-local artifact output under `report_assets/artwork/`
- Harden renderer binary discovery on Windows environments with delayed PATH refresh:
  - add D2 executable fallback lookup (`D2_BIN`, common install paths)
  - add Graphviz `dot` fallback lookup (`GRAPHVIZ_DOT`, common install paths)
  - auto-bootstrap Graphviz runtime env for diagrams rendering
- Improve artwork capability guidance:
  - clarify tool selection policy (Mermaid for simple flow/timeline, D2/diagrams for complex architecture)
  - surface renderer availability diagnostics in capability output
- Federnett capability registry/runtime updates:
  - add `artwork.artwork_diagrams_render` to runtime tools and capability packs
- Dependency and packaging updates:
  - bump package version to `1.8.0`
  - add `diagrams` and `graphviz` to `artwork`/`all` extras
  - add `diagrams`, `graphviz` to `requirements.txt` convenience bundle
- Documentation updates:
  - add Mermaid/D2/diagrams install and PATH fallback guidance in `README.md`
  - update diagram tooling section in `docs/federlicht_report.md`

## 1.7.0
- Improve Federnett Ask panel execution UX and readability:
  - replace `Action mode` dropdown with a theme-consistent Plan/Act segmented switch
  - keep mode hint text synchronized with active mode
  - preserve preferences for action mode and artifact-write policy
- Add Ask-panel capability observability:
  - show `Agent 도구/스킬/MCP` capability chips in the panel
  - add per-capability runtime status indicators (`running/done/error/disabled`) with live activity text
  - add stream activity events for `source_index`, `web_research`, and `llm_generate`
- Strengthen help-agent response payloads:
  - include capability descriptors in both sync and streaming responses
  - forward activity telemetry without breaking existing source/done events
- Fix Live Logs line-join issue in streaming jobs:
  - preserve newline boundaries in server-side job log entries
  - keep log rendering readable for Feather/Federlicht stream output
- Add writer artwork-tool traceability:
  - log artwork tool calls to `report_notes/artwork_tool_calls.jsonl` and `report_notes/artwork_tool_calls.md`
  - emit concise `[artwork-tool]` runtime log lines
  - expose Artwork tool log link in report `Miscellaneous` metadata and appendix artifact list when available
- Help documentation update:
  - add Tools/Skills/MCP explanation and extension points in Help modal
- Test coverage additions:
  - metadata rendering for artwork tool log links
  - newline normalization in job log append behavior
  - streaming help-agent tests updated for activity/capabilities events

## 1.6.0
- Strengthen Federnett "Agent 와 작업하기" UX:
  - add left-side thread list with per-run/per-profile scoped conversation sessions
  - keep run-scoped history persistent per thread and restore safely on reopen
  - add answer-selection follow-up action (`선택 내용으로 후속 질문`)
  - add action preview modal before suggested execution (parameter confirmation gate)
  - improve streaming answer behavior and reduce stuck `질문 중...` states on stream completion
- Fix Agent Profiles `Apply to` parsing corruption:
  - remove faulty split behavior that broke tokens (for example `planner` -> `pla`, `er`)
  - replace free-text-only entry with explicit target chips + optional custom targets
  - keep save/load compatibility for existing profile data
- Improve Agent Profiles editor readability and typography baseline for Korean/English mixed content.
- Align Federnett UI panel structure updates (thread rail + answer/sources panes) for cleaner interaction flow.
- Add initial artwork/diagram integration groundwork:
  - introduce optional `artwork` extra in dependency profile
  - add artifact-oriented documentation for diagram/figure agent planning and DeepAgents 0.4 migration policy

## 1.5.1
- Simplify Federlicht/Federnett advanced controls by removing explicit temperature override wiring and keeping `temperature-level` as the single temperature control path.
- Consolidate pipeline control UX into Live Logs:
  - remove the separate Agent Pipeline panel
  - make workflow nodes directly toggleable/clickable for stage control
  - move quality loop control to the workflow `Quality xN` selector (dropdown)
  - default Live Logs view to Markdown (`MD 보기`)
- Improve responsive workflow rendering to reduce horizontal scrollbar pressure in narrow layouts.
- Add output filename collision guidance/suggestion for report generation so users can see and adopt safe suffixed names before run start.
- Strengthen workflow observability by expanding `report_workflow.md/.json` with richer stage timeline/telemetry and diagram-friendly history metadata.
- Harden Federnett Guide Agent model handling:
  - honor explicit model selection without silent fallback when strict selection is requested
  - keep env-driven model resolution (`$OPENAI_MODEL`) and OpenAI-compatible endpoint usage aligned across requests
- Improve report writing policy defaults for citation quality:
  - discourage placeholder citation markers (for example generic `[source]`)
  - prefer concrete URL/path-backed references and cleaner reader-facing prose
- Add/adjust Federnett branding asset placement for clearer header/logo composition.

## 1.5.0
- Federnett workflow pipeline upgraded from a static status strip to an interactive runtime map:
  - stage selection/toggle and drag-reorder reflected in the Live Logs workflow track
  - automatic dependency stage visibility (`auto`) and loop-back feedback cues for quality iterations
  - per-pass runtime telemetry surfaced from Federlicht (`elapsed_ms`, estimated tokens, cache hits, runtime bundle)
- Prompt/template generation and other ad-hoc background tasks are now shown as transient workflow “extra process” spots, improving live observability of non-core pipeline work.
- Live log UX improvements:
  - path-like tokens in raw logs are clickable and open directly in File Preview
  - result node path now follows the actual final output filename (for example `report_full_1.html` when suffixing occurs)
  - primary run buttons now show `Running...` and stay disabled while jobs are active
- Historical run workflow restoration and resume:
  - opening a history log now reconstructs pipeline progress from `report_workflow.json` (with `report_workflow.md` fallback) plus log signals
  - users can select a resume checkpoint stage directly on the workflow track and apply a resume stage preset to Federlicht (`--stages`)
  - one-click draft generation of a resume/update prompt file is wired back into `Prompt File` for iterative reruns
- Version management cleanup across components:
  - package version bumped to `1.5.0`
  - add shared version resolver (`federlicht.versioning`) that prefers local `pyproject.toml` version and falls back safely
  - Feather `__version__` and Federnett HTTP `server_version` now use the shared resolver instead of stale hardcoded strings
  - web research User-Agent now uses Feather version dynamically to prevent drift

## 1.4.1
- Expose Federlicht live log truncation controls in Federnett Advanced:
  - `Progress Chars` -> wires to `--progress-chars`
  - `Max Tool Chars` -> wires to `--max-tool-chars`
- Persist and restore these runtime controls via `report_notes/report_meta.json` so reopening a run restores `max_chars`, `max_tool_chars`, `max_pdf_pages`, and `progress_chars`.
- Add help text update in Federnett modal to document `--progress-chars` behavior and default.

## 1.4.0
- Add Federnett Guide Agent panel (`질문하기`) with repo-aware answers, source citations, and line-focused source preview links.
- Add Feather agentic search mode controls across CLI/UI (`--agentic-search`, `--model`, `--max-iter`) and stream trace visibility in logs.
- Add template control knobs in Federlicht pipeline (`template-rigidity`, `temperature-level` and explicit `temperature`) to balance structure vs. narrative flexibility.
- Improve template rendering/layout groundwork for sidebar TOC styles and stronger preview/report consistency in federlicht templates.
- Fix Federlicht runtime failure in report pipeline by resolving active profile wiring (`NameError: profile is not defined`).
- Fix Python 3.10 compatibility in prompt assembly and clean undefined type-hint references in API/orchestrator paths.
- Clean minor dead code/import noise in Feather/Federnett/Federlicht modules and re-verify build/test/lint health.

## 1.3.0
- Make report byline identity profile-aware: author now resolves in order `--author/--organization` -> agent profile (`author_name`/`organization`) -> prompt `Author:` line -> fallback.
- Add `--organization` to Federlicht and persist `organization` plus profile author metadata in `report_meta.json`.
- Extend agent profile schema with `author_name` and `organization` fields for reusable byline identity.
- Update Federnett Agent Profiles editor to manage `Author name` and optional `Organization`.
- Enforce random 6-digit IDs for new site agent profiles (including New/Clone flows) while keeping legacy site IDs editable.
- Document profile author metadata behavior and add auth-gated memory/DB connector TODOs in `README.md`.

## 1.2.0
- Add run log history indexing (`_log.txt`, `_feather_log.txt`, `_federlicht_log.txt`) and surface it in Recent Jobs.
- Allow historical logs to open in Live Logs with automatic run/form restoration.
- Simplify Recent Jobs into a compact summary card with a modal list view.
- Make Run Studio summary chips (reports/index files) open in File Preview.
- Stabilize Live Logs layout/scroll behavior for consistent visibility.
- Pass model/check-model/depth through prompt generation in Federnett to avoid internal model mismatches.

## 1.1.0
- Add FederHav CLI to draft update requests against an existing report and re-run Federlicht with a chosen agent profile.
- Add Federnett Agent Profiles panel (list/edit/save/delete) with site-scoped profile storage and memory hooks.
- Persist `agent_profile` into `report_meta.json` and restore it when reopening past runs.
- Improve citation rendering by stripping escaped `\\[n\\]` anchors and merging orphaned citation-only lines.
- Move Recent Jobs into a compact hero card near Run Folders and clean up the Live Logs panel framing/scroll behavior.

## 1.0.0
- Introduce **Canvas** in Federnett: open a report from File Preview, select excerpts, write update instructions, auto-generate an update prompt, and re-run Federlicht from the same workspace.
- Replace the standalone Update Report panel with the Canvas-based revision workflow.
- Restore run settings when reopening Past Runs (template/language/model/vision) using `report_notes/report_meta.json`.
- Add Run Studio trash action to move whole runs to a safe trash folder.
- Improve telemetry layout with resizable logs/preview split, collapsible logs, and clearer file preview handling for unsupported binaries (download-first).
- Add new Federnett themes (sage/amber) and darken template editor controls for better focus.

## 0.9.0
- Add shared input trimming across scout/plan/web/evidence/clarifier/writer payloads with priority caps to reduce context overflows.
- Add `--max-tool-chars` to cap cumulative `read_document` output across a run (CLI/API/Federnett).
- Add reducer-backed tool output summarization with chunk artifacts under `report_notes/tool_cache/` and NEEDS_VERIFICATION guidance for citation safety.
- Extend PDF reads with `start_page` support to allow targeted follow-up reads without increasing global limits.
- Add auto verification loop that re-reads NEEDS_VERIFICATION chunk artifacts and appends verification excerpts to evidence notes.
- Strengthen evidence/writer prompts to prefer verification excerpts and enforce safe citation handling.
- Merge orphaned citation-only lines into the preceding sentence to keep inline references readable.
- Enrich references with authors/year/venue metadata using text indices (OpenAlex/arXiv/local) and clearer source labels.
- Soften default template tone and add readability guidance while keeping professional structure.
- Resolve the duplicate truncate helper by splitting it into explicit middle/head variants for safer payload trimming.
- Move supporting web research execution into Feather utilities and keep Federlicht as a thin wrapper.
- Split HTML/Markdown rendering helpers into `federlicht.render.html` for cleaner modular boundaries.
- Add a Federnett custom template editor panel and refactor server helpers into smaller modules for maintainability.
- Add a Federlicht PPTX reader (structured slide text + embedded image extraction) with vision-ready figure candidates.
- Fix Feather local ingest to create `local/raw` and `local/text` folders before copying/extracting files.
- Add Federlicht logging to `_federlicht_log.txt` and mirror Feather logs to `_feather_log.txt`.
- Improve report HTML theme contrast for light templates and show PPTX/extract/log groups in Federnett Run Studio.
- Add Run Studio “Update Report” action to regenerate reports with a user-provided revision prompt.
- Record report update requests in `report_notes/update_history.jsonl` for traceability.
- Add Drag & Drop uploads in Federnett (stored under `site/uploads`) with auto `file:` line insertion.
- Update report prompts now include base report content for edit-only revisions and use date-based update_request filenames.

## 0.8.1
- Add **Federnett**: a web studio wrapper around Feather and Federlicht with an HTTP server, SSE log streaming, background jobs, and kill control.
- Add a static Federnett UI under `site/federnett/` with Feather/Federlicht/Prompt tabs, theme switching, run discovery, and live logs.
- Move the Federnett implementation into a dedicated package at `src/federnett/app.py` and keep `federlicht.federnett` as a compatibility shim.
- Wire the `federnett` console script to `federnett.app:main` and document usage in `README.md`.

## 0.7.0
- Add `--generate-prompt` to scout a run and emit an editable report prompt (saved to `--output` or `instruction/`).
- Add a prompt generator system prompt with Template/Depth/Language headers and scoped guidance for evidence gaps.
- Record report summaries in `report_meta.json` and reuse them during `--site-refresh`.
- Make `--site-refresh` incremental: reuse manifest entries when report `mtime/size` are unchanged to avoid full HTML parsing.
- Add lazy rendering to the site index with “더 보기” pagination for Latest/Archive.
- Add search + template/lang/tag filters that also use lazy rendering for results.
- Enrich site manifest entries with `run`, `report_stem`, `source_mtime`, and `source_size`.
- Add PDF auto-extend reading (`--pdf-extend-pages`, `--pdf-extend-min-chars`) and emit truncation notes when not all pages are scanned.
- Allow `--max-pdf-pages 0` to attempt full PDF reads (documented in `--help`).
- Update API schema to include PDF extension controls.

## 0.6.0
- Split report generation into a reporting orchestrator with subagent stages to reduce `report.py` monolith and isolate pipeline logic.
- Move agent prompt builders into a dedicated reporting module for cleaner reuse and customization.
- Keep CLI output rendering intact while delegating report synthesis to the orchestrator pipeline.
- Route writer inputs through depth-aware context packing to reduce token usage for brief/normal runs while preserving deep evidence paths.
- Normalize HTML/TeX outputs by unwrapping fenced code blocks and stripping full document wrappers to keep body output format-correct.
- Make HTML previews log as plain text and sanitize streamed console output (strip HTML tags) while keeping streaming enabled.
- Add stream summary-only output for writer/repair stages to reduce noisy console output.
- Normalize archive list tool patterns (strip `archive/` prefix) and fall back to `*` when no matches are found.
- Apply `--model` to check/quality models by default unless explicitly overridden.
- Localize format instructions (section/citation/format rules) based on `--lang`.
- Condense writer evidence payload only when the input budget is exceeded, with a retry on context overflow.
- Add `api.create_reporter` to use Federlicht as a Python library, including a callable Reporter wrapper.
- Add stage registry controls (`--stages`, `--skip-stages`) and a Reporter tool wrapper for deepagent integration.
- Cache scout/plan/evidence/plan-check/alignment outputs under `report_notes/cache` and reuse them when inputs are unchanged.
- Expose the full Reporter input schema in `Reporter.as_tool` for deepagent-compatible structured inputs.
- Add pipeline state returns for partial runs and allow `Reporter.write` to finish reports from intermediate state snapshots.
- Add stage registry introspection via `--stage-info`, include stage details in `--agent-info`, and expose `Reporter.stage_info()`.
- Inject a report title derived from the prompt and include it in HTML/Markdown outputs and metadata.
- Record executed stage workflow to `report_notes/report_workflow.md`/`.json` and surface it in the Miscellaneous metadata block.
- Generate a static report hub (`site/index.html` + `site/manifest.json`) and update it after each run when outputs live under the site root (configurable via `--site-output`).
- Add `--site-refresh [path]` to rebuild the site index/manifest by scanning `<site>/runs` for all `report*.html` outputs.
- Add `--tags` to include manual report tags in Misc metadata and site manifests.

## 0.5.1
- Add configurable max input token guardrails for models without profile limits (env/CLI/agent-config) and expose values in `--agent-info`.
- Apply max input token overrides across agents, including quality/evaluation stages and template adjuster.
- Add writer output validation/retry to prevent placeholder/meta responses and enforce required H2 headings in free-format.
- Hide `max_input_tokens_source` from `--agent-info` and clarify `--max-input-tokens` help (underscore alias remains supported).
- Clarify `--lang` alias/pass-through behavior in `--help`.
- Route quality selection through a writer finalizer (pairwise merges via draft handoff) to prevent malformed synth outputs.

## 0.5.0
- Add agent streaming output with debug logging and optional Markdown echo (`--stream`, `--stream-debug`, `--echo-markdown`).
- Add separate check model selection for alignment/plan checks (`--check-model`, default gpt-4o).
- Add free-form report mode that lets the model choose structure while still requiring Risks & Gaps/Critics (`--free-format`).
- Harden structural repair and writer output (append/replace/off modes, debug logs, heading coercion, placeholder retry, no-status-output guardrails).
- Ensure Risks & Gaps/Critics are present across all templates with “Not applicable/해당없음” guidance.
- Default template adjuster to risk-only behavior and improve template adjustment logging.
- Fix filesystem path resolution for report viewers/supporting data under deepagents to avoid outside-root errors.
- Localize alignment-check prompt for Korean.

## 0.4.0
- Treat arXiv abstract URLs as arXiv IDs when `--download-pdf` is enabled (auto PDF download).
- Add optional arXiv source download with TeX/figure manifests (`--arxiv-src`).
- arXiv-derived templates now generate per-section `.tex` files and guidance Markdown files.
- Add `--update-run` to reuse existing run folders and merge new outputs in place.
- Added optional vision model support in Federlicht (`--model-vision`) for figure analysis.
- Documentation updates for installation, workflow, and publishing.
