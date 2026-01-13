업데이트된 Plan(완료 표시 + 누락 단계 추가):

- [x] 인스트럭션/인덱스/템플릿 요구사항 확정 — `instruction/20260104_oled.txt`와 `archive/20260104_oled_01-index.md`로 **스코프(최근 30일, 쿼리 혼재)·포함/제외(quantum computing 제외, LinkedIn은 부록급)·산출물 섹션** 확인
- [ ] 핵심 1차 근거 정독(High aspect ratio OLED) — `archive/web/text/s41467-025-67312-4_reference.txt`(+ tavily 중복본)에서 **2.7× 수명, outcoupling 최대 40%↑, AE/두께균일도/공정창 한계(AE2.0 실패)**를 “인용 가능한 문장+조건” 형태로 발췌
- [ ] OpenAlex 기반 트렌드 지도화 — `archive/openalex/works.jsonl` 스캔 후 **blue/inkjet/stretchable/TDDI-market** 클러스터링, 원문 부재 항목은 **추가 확보 필요(doi/저널/프리프린트)** 태깅
- [ ] 스트레처블 OLED 리뷰 신뢰도 점검 — `archive/openalex/text/W7117787413.txt`에서 **구조 카테고리+정량 주장** 추출, 단 **cited_by_count=0 등 증거 강도 낮음/원출처 역추적 필요** 명시
- [ ] 3–5개 기술 인플렉션 포인트 도출 — 포인트별로 **‘현재 아카이브 근거 vs 추가 필요 근거’** 표 작성
- [ ] 연구 vs 상업 채택 갭 분석 — 제조(수율/원가/공정창/장비호환)·성능(수명/효율/휘도)·신뢰성(표준/재현성) 축 비교 + Nat Commun의 **적용 가능 영역(조명/특수 패널 등)** 정리
- [ ] 모순·갭 및 의사결정자 후속 질문 정리 — **blue/inkjet 원문 부재**, off-topic 제외 근거, 스케일업/벤더/측정조건 확인 질문 리스트화
- [ ] Nature Reviews 스타일 아웃라인 작성 — Abstract→Intro→Landscape→Methods→Comparative Evidence→Key Points→Challenges→Outlook, **표(인플렉션 매트릭스/증거강도표)** 배치

추가로 누락되어 보완한 단계:
- [ ] 보고서 템플릿 파일 위치 확인(/report_notes 등) 및 **런 폴더 밖 템플릿 접근 불가 시 대체 템플릿 정의** (현재 루트에 `/report_notes/`가 있어 여기부터 확인 필요)