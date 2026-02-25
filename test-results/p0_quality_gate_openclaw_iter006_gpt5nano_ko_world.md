# Report Quality Gate Result

- gate_result: FAIL (rc=2)
- suite: (none)
- rows_count: 1
- gate_profile: world_class
- gate_effective_band: world_class
- gate_source: profile:world_class
- gate_targets: {'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}

## Summary
- overall: 83.94
- claim_support_ratio: 20.51
- unsupported_claim_count: 31.00
- evidence_density_score: 100.00
- section_coherence_score: 100.00

## Gate Output
```text
gate-policy | profile=world_class | effective_band=world_class | source=profile:world_class | targets={'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}
gate-summary | overall=83.94 | claim_support=20.51 | unsupported=31.00 | section_coherence=100.00
gate-result | FAIL
- avg_claim_support_ratio 20.51 < 60.00
- avg_unsupported_claim_count 31.00 > 12.00
```
