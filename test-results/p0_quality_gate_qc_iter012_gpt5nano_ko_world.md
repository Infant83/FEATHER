# Report Quality Gate Result

- gate_result: FAIL (rc=2)
- suite: (none)
- rows_count: 1
- gate_profile: world_class
- gate_effective_band: world_class
- gate_source: profile:world_class
- gate_targets: {'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}

## Summary
- overall: 88.56
- claim_support_ratio: 45.71
- unsupported_claim_count: 19.00
- evidence_density_score: 100.00
- section_coherence_score: 92.00

## Gate Output
```text
gate-policy | profile=world_class | effective_band=world_class | source=profile:world_class | targets={'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}
gate-summary | overall=88.56 | claim_support=45.71 | unsupported=19.00 | section_coherence=92.00
gate-result | FAIL
- avg_claim_support_ratio 45.71 < 60.00
- avg_unsupported_claim_count 19.00 > 12.00
```
