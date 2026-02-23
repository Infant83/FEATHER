# Report Quality Gate Result

- gate_result: FAIL (rc=2)
- suite: report_quality_v1
- rows_count: 1
- gate_profile: world_class
- gate_effective_band: world_class
- gate_source: profile:world_class
- gate_targets: {'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}

## Summary
- overall: 60.92
- claim_support_ratio: 47.50
- unsupported_claim_count: 21.00
- evidence_density_score: 100.00
- section_coherence_score: 60.00

## Quality Contract Consistency
- pass: FAIL
- metric_source: selected_eval
- failed_checks:
  - overall abs_delta=16.02 > 2.50
  - unsupported_claim_count abs_delta=21.00 > 8.00

### Metric Delta (benchmark - quality_contract)
| metric | benchmark | quality_contract | delta | abs_delta | threshold |
| --- | ---: | ---: | ---: | ---: | ---: |
| overall | 60.92 | 76.94 | -16.02 | 16.02 | 2.50 |
| claim_support_ratio | 47.50 | 50.00 | -2.50 | 2.50 | 8.00 |
| unsupported_claim_count | 21.00 | 0.00 | +21.00 | 21.00 | 8.00 |
| evidence_density_score | 100.00 | 100.00 | +0.00 | 0.00 | 8.00 |
| section_coherence_score | 60.00 | 55.00 | +5.00 | 5.00 | 8.00 |

## Gate Output
```text
gate-policy | profile=world_class | effective_band=world_class | source=profile:world_class | targets={'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}
gate-summary | overall=60.92 | claim_support=47.50 | unsupported=21.00 | section_coherence=60.00
gate-result | FAIL
- avg_overall 60.92 < 82.00
- avg_claim_support_ratio 47.50 < 60.00
- avg_unsupported_claim_count 21.00 > 12.00
- avg_section_coherence_score 60.00 < 75.00
```
