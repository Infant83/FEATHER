# Report Quality Gate Result

- gate_result: PASS (rc=0)
- suite: (none)
- rows_count: 1
- gate_profile: world_class
- gate_effective_band: world_class
- gate_source: profile:world_class
- gate_targets: {'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}

## Summary
- overall: 91.05
- claim_support_ratio: 72.73
- unsupported_claim_count: 6.00
- evidence_density_score: 100.00
- section_coherence_score: 92.00

## Quality Contract Consistency
- pass: PASS
- skipped: YES
- stale: YES
- stale_reason: missing_metric_version
- metric_source: selected_eval
- metric_version: (missing)
- expected_metric_version: qc-metrics.v2
- failed_checks: (none)

### Metric Delta (benchmark - quality_contract)
| metric | benchmark | quality_contract | delta | abs_delta | threshold |
| --- | ---: | ---: | ---: | ---: | ---: |
| overall | 91.05 | 76.94 | +0.00 | 0.00 | 2.50 |
| claim_support_ratio | 72.73 | 50.00 | +0.00 | 0.00 | 8.00 |
| unsupported_claim_count | 6.00 | 0.00 | +0.00 | 0.00 | 8.00 |
| evidence_density_score | 100.00 | 100.00 | +0.00 | 0.00 | 8.00 |
| section_coherence_score | 92.00 | 55.00 | +0.00 | 0.00 | 8.00 |

## Gate Output
```text
gate-policy | profile=world_class | effective_band=world_class | source=profile:world_class | targets={'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}
gate-summary | overall=91.05 | claim_support=72.73 | unsupported=6.00 | section_coherence=92.00
gate-result | PASS
```
