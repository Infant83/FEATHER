# Manual Review - QC Iter028 (Deep Research refresh)

- Target: `test-results/p0_sample_qc_iter028_codex53_ko_deepresearch_artwork_snapshot.html`
- Date: 2026-02-28

## 1) Objective Gate
- Profile: `deep_research`
- Result: `PASS`
- overall: `92.48`
- claim_support_ratio: `100.00`
- unsupported_claim_count: `0`
- section_coherence_score: `100.00`
- narrative_density_score: `51.60` (mid)
- narrative_flow_score: `83.96` (good)
- citation_integrity_score: `100.00`

## 2) Subjective Assessment (Editor View)
- Strengths:
  - 전 섹션 연결이 자연스러워졌고, 핵심 문단의 서술형 흐름이 이전 샘플보다 안정적임.
  - 주장-근거 매핑이 촘촘하여 근거 누락 인상이 거의 없음.
  - 시각 요소(로드맵/투자 비교/오류율 추세/레이더/파이프라인)를 본문 맥락에서 해석하려는 시도가 분명함.
- Major gaps:
  - SVG 블록 1곳에서 인용 rewrite가 XML 속성까지 침투해 `xmlns="[\\[13\\]](http://www.w3.org/2000/svg"` 형태의 malformed markup가 발생함.
  - `인사이트:` 라벨형 문장이 연속으로 4회 노출되어, 일부 구간에서 산문형 리듬이 다시 끊김.
  - 일부 캡션에 `Simulated/Illustrative` 문구가 중복 노출되어 문장 품질이 저하됨.

## 3) Priority Fixes
1. Citation cleanup 단계에서 raw SVG/XML attribute 영역을 보호해 링크 재작성 대상에서 제외.
2. Finalizer 규칙에서 동일 라벨 prefix(`인사이트:` 등) 연속 사용 상한을 더 낮추고 전환문을 강제.
3. Caption 후처리에서 중복 토큰(`Simulated/Illustrative`) dedupe 적용.

## 4) Regression Signals
- label_line_count (`인사이트:`): `4`
- malformed citation token count (`[[`): `1`
- primary_meta_caption markers (`Metric/Unit/Period/Normalization/Source`): `5`
