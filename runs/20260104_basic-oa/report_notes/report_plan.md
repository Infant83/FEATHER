업데이트된 Plan(완료 체크 + 누락 단계 보강):

- [x] 지시·범위·커버리지 점검 — `instruction/20260104.txt`와 `archive/20260104_basic-oa-index.md` 확인 완료. **OLED+arxiv+quantum computing 혼재**로 오프토픽 유입 구조였고, 최근 30일/결과 8개 제한으로 **학술 PDF 2편만 확보**된 커버리지 한계 확인(학술·산업 모두 얕음).
- [ ] 1차 피어리뷰 근거 추출 — `archive/web/text/s41467-025-67312-4_reference.txt` 읽기 진행 중. 현재까지 확인된 핵심 수치/정의:
  - AE 최대 **1.4×**, 표준 VTE(thermal evaporator)로 두께 균일성 언급
  - (planar 대비, 동일 panel current density 조건) 수명 **2.7×**, 외부 광추출 효율 **최대 40%**
  - 수명 정의로 **LT95(95%까지 페이드)** 언급 라인 확인(세부 조건/표는 추가 발췌 필요)
  - EQE 관련 구간/측정 오차(각도 분포) 주의 문구 존재 → **측정조건 표 형태로 정리 필요**
- [ ] 원문(PDF)로 디테일 검증 — Nature PDF(`archive/web/pdf/s41467-025-67312-4_reference.pdf`)에서 Fig/Methods(소자 구조, 공정, 재현성, AE2.0 실패/면적 스케일링 등) 확인 필요. *(텍스트에 “AE2.0 재현성 낮음/빠른 실패” 단서가 있어 원문 확인 우선순위 높음)*
- [ ] 스트레처블 OLED 리뷰 신뢰도·핵심 요약 — `archive/openalex/text/W7117787413.txt` + PDF로 3가지 구조 분류 요약 및 **저자 소속/인용 0 기반 신뢰도 경고**, 리뷰 내 수치의 **원출처 역추적 필요** 반영
- [ ] OpenAlex 메타로 변곡점 후보 풀 만들기 — `archive/openalex/works.jsonl`에서 OLED 관련만 필터링해 상위 후보 10개 추출 후 산업 함의 기준 3–5개 압축
- [ ] 산업/상용 근거 선별·대조 — `archive/tavily_search.jsonl`에서 DOE/LG Display/OLED-Info 등 신뢰 가능한 산업·기관만 남기고 비용/수율/수명/효율 주장 정리(현재 “high cost 장벽”, “automotive niche” 정도로 정량 근거 부족 → 추가 소스 필요 가능)
- [ ] 3–5개 기술 변곡점 합성 — 변곡점별 “핵심 아이디어→증거(논문/산업)→적용처→단기 상용화 장애” + 연구 vs 상용 채택 비교표 작성
- [ ] 모순·갭 및 후속 질문 제시 — 측정 조건 불일치(EQE 각도분포 보정 등), 수명 정의(LT95/LT70), 면적/스케일, PDF/추가 논문 미확보를 명시하고 의사결정자용 후속 질문 포함
- [ ] (추가) 오프토픽 혼입 제거 규칙 확정 및 재수집 계획 — 다음 런에서 **OLED 키워드 고정 + quantum computing 배제**, (필요시) Wiley pdfdirect/Scientific Reports OA PDF 등 **미다운로드 PDF 재수집** 단계 추가(현 커버리지 공백 해소용)