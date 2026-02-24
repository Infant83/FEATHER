# Dev History Summary by Version

Last updated: 2026-02-25

## Scope
- Consolidated summary for versions `1.9.20 ~ 1.9.29`.
- Detailed logs remain in archived handoffs and changelog.

## Version Timeline

| Version | Summary | Primary references |
| --- | --- | --- |
| `1.9.20` | FederHav DeepAgent Phase B-2 handoff metadata/preflight integration, action-plan trace 강화 | `CHANGELOG.md` |
| `1.9.21` | LLM policy split(Global/Scoped), settings persistence 확장 | `CHANGELOG.md` |
| `1.9.22` | LLM policy normalization + live effective policy visibility 개선 | `CHANGELOG.md` |
| `1.9.23` | Live Logs turn/process bridge 매핑 개선 | `CHANGELOG.md` |
| `1.9.24` | Report Hub approval transition/authorization hardening | `CHANGELOG.md` |
| `1.9.25` | Root-auth aware approval UX + fallback policy tightening | `CHANGELOG.md` |
| `1.9.26` | P0 UX/governance polish + stage override guardrail 강화 | `CHANGELOG.md` |
| `1.9.27` | quality profile 도입(`smoke/baseline/professional/world_class`) + gate policy 명시화 | `CHANGELOG.md`, `docs/dev_history/handoffs/codex_handoff_20260223.md` |
| `1.9.28` | quality loop convergence(plateau) + profile compare 도구 추가 | `CHANGELOG.md`, `docs/dev_history/handoffs/codex_handoff_20260223.md` |
| `1.9.29` | 버전 일관성 자동검증 도구 + gate-distance ranking 적용 | `CHANGELOG.md`, `docs/dev_history/handoffs/codex_handoff_20260224.md` |

## Progress Context (Quality Program)
- `P0(core)`: 100% 유지
- `P0+(quality uplift)`: 72% (latest snapshot)
- `P1`: 0% (P0+ stabilization 이후 착수)

## How to Use
1. Start with `docs/codex_handoff_20260225.md` for current status.
2. Use this file for version-band orientation.
3. Open archived handoffs under `docs/dev_history/handoffs/` when deeper execution traces are needed.
