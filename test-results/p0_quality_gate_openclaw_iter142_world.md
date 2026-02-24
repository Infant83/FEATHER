# Report Quality Gate Result

- gate_result: PASS (rc=0)
- suite: (none)
- rows_count: 1
- gate_profile: world_class
- gate_effective_band: world_class
- gate_source: profile:world_class
- gate_targets: {'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}

## Summary
- overall: 94.63
- claim_support_ratio: 97.22
- unsupported_claim_count: 1.00
- evidence_density_score: 100.00
- section_coherence_score: 100.00

## Quality Contract Consistency
- pass: FAIL
- skipped: NO
- stale: NO
- stale_reason: (none)
- metric_source: final_signals
- metric_version: qc-metrics.v2
- expected_metric_version: qc-metrics.v2
- failed_checks:
  - overall abs_delta=32.41 > 2.50
  - claim_support_ratio abs_delta=47.22 > 8.00
  - section_coherence_score abs_delta=45.00 > 8.00

### Metric Delta (benchmark - quality_contract)
| metric | benchmark | quality_contract | delta | abs_delta | threshold |
| --- | ---: | ---: | ---: | ---: | ---: |
| overall | 94.63 | 62.22 | +32.41 | 32.41 | 2.50 |
| claim_support_ratio | 97.22 | 50.00 | +47.22 | 47.22 | 8.00 |
| unsupported_claim_count | 1.00 | 0.00 | +1.00 | 1.00 | 8.00 |
| evidence_density_score | 100.00 | 100.00 | +0.00 | 0.00 | 8.00 |
| section_coherence_score | 100.00 | 55.00 | +45.00 | 45.00 | 8.00 |

## Gate Output
```text
gate-policy | profile=world_class | effective_band=world_class | source=profile:world_class | targets={'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}
gate-summary | overall=94.63 | claim_support=97.22 | unsupported=1.00 | section_coherence=100.00
gate-result | PASS
```
