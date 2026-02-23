# Report Quality Threshold Policy

Last updated: 2026-02-23

## 1) Why `overall=65` Is Not World-Class
- `overall=65` is a **smoke/health-check** threshold.
- It only indicates that a run is not totally broken and has minimum structural quality.
- It must not be used as a publication-quality target.

## 2) Quality Profiles (Gate Presets)

| Profile | Purpose | min_overall | min_claim_support | max_unsupported | min_section_coherence |
| --- | --- | ---: | ---: | ---: | ---: |
| `smoke` | pipeline health only | 65 | 2 | 70 | 55 |
| `baseline` | routine regression baseline | 70 | 40 | 25 | 60 |
| `professional` | production-grade report quality | 76 | 50 | 18 | 68 |
| `world_class` | top-tier research quality gate | 82 | 60 | 12 | 75 |

Notes:
- Lower `max_unsupported` is stricter.
- Per-metric CLI values override profile defaults.

## 3) Heuristic Score Inputs
`compute_heuristic_quality_signals(...)` currently combines:
- `section_coverage`
- `citation_density`
- `evidence_density_score`
- `claim_support_ratio`
- `unsupported_claim_count`
- `section_coherence_score`
- `method_transparency`
- `traceability`
- `uncertainty_handling`

Weights vary by intent/depth (`briefing`, `research`, `decision`, etc.).

## 4) World-Class Pass Policy (Operational)
World-class is treated as **composite pass**, not one scalar score.

Required:
1. `quality_profile=world_class` gate pass.
2. `quality_contract.latest.json` and benchmark summary consistency pass.
3. No critical unsupported-claim clusters in key sections.
4. Section-level coherence and method/result traceability preserved after finalizer.

## 5) CLI Usage

Federlicht runtime quality gate:
```bash
python -m federlicht.report \
  --run site/runs/20260221_QC_report \
  --output site/runs/20260221_QC_report/report_full.html \
  --quality-profile world_class \
  --quality-iterations 3 \
  --quality-auto-extra-iterations 2
```

Benchmark + regression gate:
```bash
python tools/run_report_quality_gate.py \
  --input site/runs/20260221_QC_report/report_full.html \
  --summary-output test-results/qc.summary.json \
  --report-md test-results/qc.gate.md \
  --quality-profile world_class
```

## 6) Design Principle
- Do not hard-code one template shape for every request.
- Keep flexible intent/depth handling.
- Raise quality through better agentic decomposition (scout/plan/evidence/writer/quality), evidence contracts, and section-level revision, not via rigid section forcing.

