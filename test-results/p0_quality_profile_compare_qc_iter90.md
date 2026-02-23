# Quality Profile Compare

## Summary
- overall: 60.92
- claim_support_ratio: 47.50
- unsupported_claim_count: 21.00
- section_coherence_score: 60.00

## Profile Matrix
| profile | pass | min_overall | min_claim_support | max_unsupported | min_section_coherence |
| --- | --- | ---: | ---: | ---: | ---: |
| smoke | FAIL | 65.0 | 2.0 | 70.0 | 55.0 |
| baseline | FAIL | 70.0 | 40.0 | 25.0 | 60.0 |
| professional | FAIL | 76.0 | 50.0 | 18.0 | 68.0 |
| world_class | FAIL | 82.0 | 60.0 | 12.0 | 75.0 |

## Failure Details
- smoke: overall 60.92 < 65.00
- baseline: overall 60.92 < 70.00
- professional: overall 60.92 < 76.00; claim_support_ratio 47.50 < 50.00; unsupported_claim_count 21.00 > 18.00; section_coherence_score 60.00 < 68.00
- world_class: overall 60.92 < 82.00; claim_support_ratio 47.50 < 60.00; unsupported_claim_count 21.00 > 12.00; section_coherence_score 60.00 < 75.00
