# Report Quality Benchmark Prompts v1

Last updated: 2026-02-22

## 목적
- Federlicht 보고서 품질 회귀를 일정한 프롬프트 세트로 비교한다.
- 산업/학술/전략/브리핑 유형을 혼합해 편향을 줄인다.

## Prompt Set (12)

1. Industrial Deep Research  
`양자컴퓨팅의 산업 적용(제조/물류)에서 실제 ROI가 발생한 사례를 방법론, 근거 강도, 한계까지 포함해 심층 보고서로 작성해줘.`

2. Scientific Review  
`OLED blue dopant/host 시스템 관련 계산재료 연구를 최근 5년 중심으로 리뷰하고, 합의/불일치/공백을 정리해줘.`

3. Decision Memo  
`우리 조직이 12개월 내 PoC를 시작할지 판단해야 한다. 옵션 A/B/C를 비용, 리스크, 실행난이도 기준으로 비교하고 권고안을 제시해줘.`

4. Executive Brief  
`경영진을 위한 1페이지 브리핑: AI 에이전트 도입의 기대효과와 실패 리스크를 핵심 근거 3개 중심으로 요약해줘.`

5. Policy/Regulation  
`EU AI Act 관점에서 생성형 AI 보고서 시스템의 운영 리스크와 통제전략을 실무 체크리스트 형태로 정리해줘.`

6. Technical Deep Dive  
`RAG + Tool-calling + Multi-agent 오케스트레이션 아키텍처를 기술적으로 비교하고, 장애지점과 관측성 설계를 포함해 작성해줘.`

7. Market/Strategy  
`2026-2028년 AI infra 시장에서 온프레미스 추세를 근거 기반으로 분석하고, 공급망 리스크를 포함해 전망해줘.`

8. Contrarian Review  
`AI 자동화의 생산성 향상 주장에 대한 반례와 실패 사례를 체계적으로 정리해줘.`

9. Method-First  
`연구 방법론을 최우선으로: 포함/제외 기준, 데이터 품질, 검증 절차를 먼저 설명하고 그 다음 결과를 제시해줘.`

10. Slide-ready Brief  
`8분 발표용으로, 핵심 주장 5개를 각 주장당 근거 1-2개와 함께 슬라이드 친화적 구조로 정리해줘.`

11. Comparative Benchmark  
`오픈소스 LLM 운영전략(직접 서빙 vs API 혼합 vs 멀티벤더)을 비교하고, 운영복잡도와 품질의 trade-off를 정리해줘.`

12. Uncertainty-heavy Topic  
`AGI 타임라인처럼 불확실성이 큰 주제에서, 확정 사실/추정/논쟁지점을 분리해 보고서를 작성해줘.`

## 사용 가이드
- 각 프롬프트마다 depth(`brief|normal|deep`)와 intent(`briefing|decision|review|research`)를 고정해 반복 비교한다.
- 최소 저장 항목:
- overall
- claim_support_ratio
- unsupported_claim_count
- evidence_density_score
- section_coherence_score
- 결과 파일은 `test-results/` 아래 JSON으로 누적한다.

