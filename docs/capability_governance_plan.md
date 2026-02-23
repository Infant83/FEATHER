# Capability Governance Plan

Updated: 2026-02-13

## 1) Terminology
- Use a single umbrella term: **Capability Pack**.
- Capability Pack contains:
  - Tool (callable function/integration)
  - Skill (workflow logic/policy)
  - MCP Server (external context/tool endpoint)

## 2) Why this matters
- Ask panel previously exposed only a small static list (source/web/llm).
- Runtime tools used by Federlicht and deepagents were not visible to users.
- Governance and audit require one shared registry + runtime view.

## 3) Current implementation in Federnett
- Registry file: `site/agent_profiles/capability_registry.json`
- API:
  - `GET /api/capabilities`
  - `POST /api/capabilities/save`
- Ask UI:
  - capability chips (runtime status)
  - capability packs detail
  - manager panel (add/remove custom Tool/Skill/MCP metadata)
- Runtime exposure includes:
  - Ask core tools
  - Federlicht internal runtime tools (filesystem/artwork)
  - deepagents runtime path (subagent router/tool executor)

## 4) Governance policy (next phase)
- Capability manifest schema:
  - id, type(tool|skill|mcp), owner, risk_level, allowed_scope, endpoint, enabled
- Execution policy:
  - `Plan` mode: human confirmation before side-effect actions
  - `Act` mode: bounded auto-run, run-folder/artifacts only
- Safety controls:
  - allowlist by run scope
  - read-only default for source tree
  - explicit write scope for `site/runs/<run>/artifacts/**`
- Observability:
  - per-capability start/end/error logs
  - token/time/cost counters per capability
  - trace id link from Ask answer to runtime logs

## 5) Standards alignment references
- Model Context Protocol (spec/docs): https://modelcontextprotocol.io/
- OpenAI function/tool schema patterns: https://platform.openai.com/docs/guides/function-calling
- OpenTelemetry semantic conventions (traces/metrics): https://opentelemetry.io/docs/specs/semconv/
- Google A2A protocol repository: https://github.com/google/A2A

## 6) Rollout
- Phase 1 (done): registry + runtime visibility in Ask panel.
- Phase 2: capability permission model and per-profile capability bindings.
- Phase 3: signed manifests, tenant-level policy packs, CI policy checks.

