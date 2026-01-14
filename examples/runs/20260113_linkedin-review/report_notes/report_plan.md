업데이트된 Plan (완료 표시 및 누락 단계 보강):

- [x] 요구사항 고정 — `instruction/20260113_linkedin-review.txt`와 `archive/20260113_linkedin-review-index.md`를 읽어 목표·분량·섹션·인용 규칙을 확정  
- [x] 핵심 소스 정독(1차→2차) — `tavily_extract`의 arXiv(0002)→LinkedIn(0001)→블로그(0003) 순으로 핵심 주장/조건/수치 문장을 원문 그대로 발췌  
- [ ] 근거-주장 매핑표 작성 — 발췌 문장에 [arXiv]/[LinkedIn]/[blog] 태그를 붙이고 “supported by source” vs “inferred/secondary”로 구획화  
- [x] 기존 산출물 재사용 가능성 점검 — `archive/20260113_linkedin-review-final*.md` 및 `archive/20260113_linkedin-review.md` 대조 결과, 현 산출물에 **근거 불명(예: community adoption)** 문장이 포함되어 ‘개선 편집’이 아니라 **재작성(근거 중심) 모드**가 적절  
- [x] 커버리지/품질 리스크 확인 — `archive/_log.txt`와 `archive/_job.json`으로 추출 범위(입력 URL 3개) 및 한계 확인 완료(Risks & Caveats 반영 예정)  
- [ ] 실무 인사이트/ROI 합성 — 제품·비즈 전략 관점에서 의사결정에 영향 큰 3~5개 인사이트(도입 이점/제약/비용 구조/대체안 비교)를 근거와 함께 정리  
- [ ] 최종 보고서 구성 확정 — LinkedIn 스타일(짧은 문단+간결 불릿)로 Practitioner Review → Risks & Caveats → Actionable Takeaways(3~6개, 조건 포함) 순서로 아웃라인 확정 및 작성 준비  
- [x] (추가) arXiv PDF 본문 존재 여부 확인 및 필요 시 다운로드/추출본에서 실험 수치/세부 구현 근거 보강 — 이번 런 아카이브에 **PDF가 없음**(abs/블로그/LinkedIn 추출만 존재) → 실험 디테일/수치는 2차 주장으로 처리 필요  
- [ ] (추가) 인용 포맷 확정 — 문장 말미에 (출처: URL, `archive/tavily_extract/...`) 형태로 통일하고, 2차 주장에는 “1차(PDF) 검증 불가” 라벨 규칙 추가  
- [ ] (추가) 최종 원고 QA — “supported vs inferred” 라벨 누락 점검, 과장/추정 문장 제거, 섹션별 길이/톤(대화체·프로페셔널) 정합성 체크