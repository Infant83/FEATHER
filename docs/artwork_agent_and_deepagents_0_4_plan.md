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

## Current Diagram Tooling Status (Repository Reality)
- Federlicht writer already has an internal `artwork_agent` subagent path.
- Built-in artwork tools now cover:
  - `artwork_mermaid_flowchart` (inline Mermaid snippet)
  - `artwork_mermaid_timeline` (inline Mermaid snippet)
  - `artwork_mermaid_render` (Mermaid source -> SVG/PNG/PDF artifact via `mmdc`)
  - `artwork_d2_render` (D2 source -> SVG artifact via `d2` CLI)
- Generated files are run-local under `report_assets/artwork/` and logged in `report_notes/artwork_tool_calls.*`.

## Integration with External Mermaid Subagent Prototype
Reference prototype:
- `C:/Users/angpa/myProjects/myMCP/documentations/create_mermaid/mermaid_subagent_tools.py`
- It already implements `render_mermaid_diagram`, `render_mermaid_from_markdown`, `render_all_mermaid_from_markdown`.

Recommended bridge strategy:
1. Keep Federlicht built-ins as the default stable path.
2. Add optional adapter that imports the external toolset when available and exposes the same contract.
3. Gate by capability check:
   - `mmdc` installed -> enable render path.
   - external package importable -> enable markdown-batch render path.
   - otherwise fallback to inline Mermaid snippets.

## Capability Studio Mapping
Add/manage these as explicit capabilities in Workspace Settings:
- `artwork.artwork_mermaid_flowchart`
- `artwork.artwork_mermaid_timeline`
- `artwork.artwork_mermaid_render`
- `artwork.artwork_d2_render`

Operational policy:
- Enable by default for writer stage only.
- Keep evidence/scout stages read-heavy; avoid heavy renderer calls there.
- Require caption + source refs for every generated figure.

## Report Usage Policy (Practical)
- Use Mermaid inline for:
  - workflow overview
  - stage timeline
  - simple process maps
- Use D2 render for:
  - architecture diagrams with many nodes/edges
  - reusable SVG assets
- Use markdown-batch Mermaid render (external prototype) for:
  - pre-authored report templates with many Mermaid blocks

Acceptance criteria:
- Figure has argumentative purpose (not decorative).
- Figure caption includes claim/evidence implication.
- Figure provenance links to source refs (`[S#]` + path in manifest/log).
