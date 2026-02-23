# Report Quality Gate Result

- gate_result: FAIL (rc=2)
- suite: (none)
- rows_count: 3
- gate_profile: world_class
- gate_effective_band: world_class
- gate_source: profile:world_class
- gate_targets: {'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}

## Summary
- overall: 89.69
- claim_support_ratio: 50.38
- unsupported_claim_count: 25.00
- evidence_density_score: 99.48
- section_coherence_score: 90.67

## Gate Output
```text
gate-policy | profile=world_class | effective_band=world_class | source=profile:world_class | targets={'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}
gate-summary | overall=89.69 | claim_support=50.38 | unsupported=25.00 | section_coherence=90.67
gate-result | FAIL
- avg_claim_support_ratio 50.38 < 60.00
- avg_unsupported_claim_count 25.00 > 12.00
```
