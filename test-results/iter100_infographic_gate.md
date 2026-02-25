# Report Quality Gate Result

- gate_result: FAIL (rc=2)
- suite: (none)
- rows_count: 1
- gate_profile: world_class
- gate_effective_band: world_class
- gate_source: profile:world_class
- gate_targets: {'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}

## Summary
- overall: 79.31
- claim_support_ratio: 75.00
- unsupported_claim_count: 1.00
- evidence_density_score: 100.00
- section_coherence_score: 28.00

## Infographic Lint
- checked_specs: 1
- failed_specs: 0
- lint_result: PASS

| spec_path | chart_count | issues |
| --- | ---: | --- |
| C:\Users\angpa\myProjects\FEATHER\temp\20260226\iter20_infographic_sample\report_notes\infographic_spec_iter20_infographic.json | 2 | - |

## Gate Output
```text
gate-policy | profile=world_class | effective_band=world_class | source=profile:world_class | targets={'min_overall': 82.0, 'min_claim_support': 60.0, 'max_unsupported': 12.0, 'min_section_coherence': 75.0}
gate-summary | overall=79.31 | claim_support=75.00 | unsupported=1.00 | section_coherence=28.00
gate-result | FAIL
- avg_overall 79.31 < 82.00
- avg_section_coherence_score 28.00 < 75.00
```
