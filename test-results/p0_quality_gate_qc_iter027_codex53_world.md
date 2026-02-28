# Report Quality Gate Result

- gate_result: FAIL (rc=2)
- suite: (none)
- rows_count: 1
- gate_profile: world_class
- gate_effective_band: world_class
- gate_source: profile:world_class
- gate_targets: {'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}

## Summary
- overall: 89.14
- claim_support_ratio: 60.47
- unsupported_claim_count: 17.00
- evidence_density_score: 100.00
- section_coherence_score: 100.00

## Gate Output
```text
gate-policy | profile=world_class | effective_band=world_class | source=profile:world_class | targets={'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}
gate-summary | overall=89.14 | claim_support=60.47 | unsupported=17.00 | section_coherence=100.00
gate-result | FAIL
- avg_unsupported_claim_count 17.00 > 12.00
```
