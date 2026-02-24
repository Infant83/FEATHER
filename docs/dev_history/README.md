# Dev History Index

Last updated: 2026-02-25

## 1) Purpose
- Archive past Codex handoffs and historical snapshots.
- Preserve context for future clones without polluting active docs.

## 2) Archived Handoffs
- `docs/dev_history/handoffs/codex_handoff_20260220.md`
- `docs/dev_history/handoffs/codex_handoff_20260222.md`
- `docs/dev_history/handoffs/codex_handoff_20260223.md`
- `docs/dev_history/handoffs/codex_handoff_20260224.md`

## 3) Historical Images
- `docs/dev_history/images/codex_handoff_20260220/`
- `docs/dev_history/images/codex_handoff_20260222/`
- `docs/dev_history/images/run_site_publish_strategy/`

## 4) Version-Oriented Summary
- Detailed file: `docs/dev_history/version_summary.md`

| Version band | Core progress | Reference |
| --- | --- | --- |
| `1.9.20 ~ 1.9.24` | DeepAgent Phase B 연결, Federnett auth/report-hub hardening | `CHANGELOG.md` |
| `1.9.25 ~ 1.9.27` | quality gate/contract consistency 강화, profile 정책 도입 | `CHANGELOG.md`, `docs/dev_history/handoffs/codex_handoff_20260223.md` |
| `1.9.28 ~ 1.9.29` | quality iteration convergence, profile compare, version consistency tooling | `CHANGELOG.md`, `docs/codex_handoff_20260224.md` |
| `1.9.30+` | FederHav governor loop metadata/live-log bridge 강화, 신규 생성물 기반 gate 운영정책 고정 | `CHANGELOG.md`, `docs/codex_handoff_20260225.md` |

## 5) Resume Path (new clone)
1. Read `docs/codex_handoff_20260225.md`.
2. Check operational rules in `docs/development_workflow_guide.md`.
3. Validate version sync: `python tools/check_version_consistency.py`.
4. If deeper context needed, open archived handoffs in `docs/dev_history/handoffs/`.
