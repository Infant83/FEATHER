업데이트된 Plan (완료 체크 및 누락 단계 보강)

- [x] 아카이브/인덱스 실존 파일 확인 — `index.md`, `_job.json`, `_log.txt`, `web/pdf`, `web/text` 존재 확인 및 커버리지 확정  
  - 수집물: PDF 1개(`/archive/web/pdf/Microsoft-AI-Diffusion-Report-2025-H2.pdf`), 변환 텍스트 1개(`/archive/web/text/Microsoft-AI-Diffusion-Report-2025-H2.txt`), 인덱스/로그/잡 설정 정상
- [x] 원문 텍스트(변환본) 구조 파악 — Executive Summary(초반) + 본문 섹션(한국/DeepSeek 등) + Appendix(국가별 테이블, PAGE 15부터 확인) 위치 파악 및 핵심 주장/지표(H1↔H2, North/South, 국가 순위, 한국, DeepSeek) 근거 구간 확인
- [ ] PDF에서 핵심 Figure/표 추출 계획 수립 — **후보 리스트는 확보했으나**, 각 Figure/표의 **정확한 페이지 번호/캡션 매핑**이 아직 필요
- [ ] PDF 원본에서 Figure/표 페이지 번호 확인 — 텍스트의 `===== PAGE N =====` 마커를 기준으로 Figure/표(지도, 막대그래프, Top 30, 한국 성장 그래프, DeepSeek 점유율 지도, Appendix 테이블)의 페이지를 확정
- [ ] (누락 보강) Figure/표 “추출 실행” 단계 정의 — (필요 시) PDF → 이미지(페이지 렌더) → 크롭(그림 영역) → 파일명 규칙/캡션 정리 → 보고서 삽입 경로 확정
- [ ] 연례 리뷰(annual_review) 템플릿에 매핑 — Abstract/Introduction/Year in Review/Theme/Questions/Future 섹션별로 어떤 근거(지표/사례/해석)를 넣을지 설계
- [ ] 인용·근거 관리 규칙 정하기 — 파일+페이지(또는 텍스트 라인) 기반 인용 포맷 확정 + 수치/순위/정의 검증 체크리스트
- [ ] 최종 보고서 작성 워크플로우 정의 — 번역(요약-근거-해석)→검수(용어·수치 일관성)→도표 삽입→한계/추가자료 명시 순서로 정리
- [ ] (누락 보강) 최종 보고서 작성(한국어, 리뷰형) — 섹션별 원문 근거 인용을 달고, 도표/그림 삽입 위치를 표시하며 “번역+해설” 톤으로 본문 완성