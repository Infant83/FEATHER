# Report Quality Gate Result

- gate_result: PASS (rc=0)
- suite: (none)
- rows_count: 1
- gate_profile: none
- gate_effective_band: disabled
- gate_source: custom
- gate_targets: {'min_overall': 0.0, 'min_claim_support': 0.0, 'max_unsupported': -1.0, 'min_section_coherence': 0.0}

## Summary
- overall: 79.31
- claim_support_ratio: 75.00
- unsupported_claim_count: 1.00
- evidence_density_score: 100.00
- section_coherence_score: 28.00

## Infographic Lint
- checked_specs: 1
- failed_specs: 1
- lint_result: FAIL

| spec_path | chart_count | issues |
| --- | ---: | --- |
| C:\Users\angpa\myProjects\FEATHER\test-results\iter80_bad_infographic_spec.json | 1 | charts[1] source is missing.; charts[1] simulated flag is missing. |

## Gate Output
```text
gate-policy | profile=none | effective_band=disabled | source=custom | targets={'min_overall': 0.0, 'min_claim_support': 0.0, 'max_unsupported': -1.0, 'min_section_coherence': 0.0}
gate-summary | overall=79.31 | claim_support=75.00 | unsupported=1.00 | section_coherence=28.00
gate-result | PASS
```
