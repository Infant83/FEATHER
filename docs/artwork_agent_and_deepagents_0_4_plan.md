# Federlicht Artwork-Agent + DeepAgents 0.4 Plan

## Goals
- Keep report generation stable under context pressure.
- Add professional diagram/figure output without breaking template discipline.
- Enable staged adoption of DeepAgents 0.4+ features with safe rollback.

## Compatibility Reality
- Current project runtime floor is Python `>=3.10` (`pyproject.toml`).
- DeepAgents `0.4.x` requires Python `>=3.11` (upstream package policy).
- Direct hard switch to `0.4.x` would break 3.10 users.

## Proposed Runtime Split
1. Keep default path on current compatible stack for Python 3.10.
2. Add optional "enhanced runtime" path for Python 3.11+:
   - Enable DeepAgents 0.4 middleware chain.
   - Keep same orchestrator interface via adapter layer.
3. Gate by runtime capability check at startup:
   - If unavailable, log fallback and continue on legacy path.

## Middleware Adoption Order (0.4+ path)
1. Summarization/context-editing middleware on scout/evidence first.
2. Tool-selection middleware on evidence and quality-evaluator stages.
3. Call-limit middleware for high-risk loops (quality, pairwise compare).
4. Canary rollout: 10-20% runs, compare overflow rate, latency, citation quality.

## Artwork-Agent Scope (Phase 1)
- Add controlled tools that only write into run-local artifacts:
  - `render_mermaid` (workflow/timeline/flow diagrams)
  - `render_d2` (architecture/logic diagrams)
  - `run_plot_script` (Plotly static PNG/SVG)
- Store all generated visuals in:
  - `report_notes/figures/`
  - `report_notes/figures_manifest.json`
- Writer consumes manifest metadata, not raw plotting code.

## Template Policy Updates Needed
- Current templates focus strongly on textual rigor; visual composition is secondary.
- Add template-level guidance fields:
  - `figure_slots`: where figures are allowed by section.
  - `figure_intent`: why each figure exists (comparison, timeline, pipeline, KPI).
  - `figure_density`: maximum figures per section.
  - `caption_style`: analytical caption structure (claim -> evidence -> implication).
- Enforce anti-clutter rule:
  - no decorative figure insertions without explicit argumentative role.

## Collision Risks and Mitigations
- Risk: auto-generated visuals drift from source evidence.
  - Mitigation: require figure provenance in manifest (`source_refs`, `generator`, `inputs_hash`).
- Risk: visuals dominate report and break readability.
  - Mitigation: section-level figure cap and mandatory prose bridge paragraph.
- Risk: increased tool usage causes context/token regressions.
  - Mitigation: artifact-first exchange (manifest pointers), never inline large binaries/DSL in prompts.

## Metrics to Track
- Overflow/fallback rate by stage.
- Average input tokens for writer/quality.
- Citation validity pass rate.
- Index-only evidence ratio.
- Figure usage quality (caption completeness + source linkage).
