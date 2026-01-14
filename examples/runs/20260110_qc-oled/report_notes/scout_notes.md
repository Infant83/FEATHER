## 1) 아카이브 커버리지/구성 파악(인덱스 기반)

- **Run/Archive 개요 (archive/20260110_qc-oled-index.md)**
  - 기간: **최근 365일**(2026-01-10 기준)
  - Tavily 검색: **Queries 9, URLs 0**로 표시되나, 실제로는 `archive/tavily_search.jsonl`에 URL 결과가 포함되어 있음(인덱스 집계 방식 이슈 가능).
  - OpenAlex: `archive/openalex/works.jsonl`에 **다수 work 메타데이터**, 그중 **PDF 다운로드 7건 + 텍스트 추출 7건** 존재.
- **지원(supporting) 폴더**
  - `list_supporting_files` 결과: **Supporting folder not available.**
  - 따라서 웹검색 보강 출처는 현재로서는 **Tavily 결과(JSONL)**가 사실상 supporting 역할을 수행(단, “지원” 구분을 엄밀히 하려면 향후 supporting 산출물 생성 필요).

---

## 2) 파일 인벤토리(핵심 파일/디렉토리 맵)

### A. 실행/메타
- `archive/_job.json` : 실행 설정/파라미터 추정(수집 범위·옵션 추적용)
- `archive/_log.txt` : 수집 로그/에러/누락 확인(커버리지 한계 진단용)
- `archive/20260110_qc-oled-index.md` : 아카이브 인덱스(다운로드된 OA PDF/텍스트 목록)

### B. 질의/웹 검색 인덱스(= supporting 성격)
- `archive/tavily_search.jsonl` : 쿼리별 결과 URL/요약 포함(산업계 공개정보·공식 블로그/보도자료 트레이싱에 핵심)

### C. 학술(OpenAlex) 인덱스
- `archive/openalex/works.jsonl` : 논문 메타데이터(제목/DOI/연도/저널/인용/다운로드 링크)

### D. OpenAlex 본문(텍스트/원문 PDF)
- `archive/openalex/text/W4406330631.txt` (+ pdf)
- `archive/openalex/text/W4406399672.txt` (+ pdf)
- `archive/openalex/text/W4406477905.txt` (+ pdf)
- `archive/openalex/text/W4406707630.txt` (+ pdf)
- `archive/openalex/text/W4410193211.txt` (+ pdf)
- `archive/openalex/text/W4410446803.txt` (+ pdf)
- `archive/openalex/text/W4417018335.txt` (+ pdf)

---

## 3) 주제 적합도(포커스 대비) 빠른 진단 노트

- **OLED 발광재료 × 양자컴퓨팅** 직접 교차점은 OpenAlex PDF 세트보다는 **Tavily에 포함된 IBM Research 글/MCGC PDF/업계 기사(OLED-Info)** 쪽이 더 강함.
- OpenAlex로 내려받힌 PDF 7개 중 다수는 **OLED/양자컴퓨팅 재료탐색**과 직접 관련이 약함(예: building facade, liver cancer AI-nano 등).  
- 예외적으로,
  - `W4410193211 (Nature Communications 2025) Using GNN property predictors as molecule generators`는 **재료 탐색 워크플로(ML 기반 생성/최적화)** 파트에 유용(양자컴퓨팅 직접 언급은 약할 수 있으나 “워크플로/파이프라인” 논의에 재료).
  - `W4406477905`는 “quantum materials” 리뷰로 **양자컴퓨팅 기반 ‘재료 연구’**라기보다 **양자물질(quantum materials)** 리뷰 성격이라 포커스와 어긋날 가능성 큼.
  - `W4417018335`, `W4410446803`는 저널/출처 신뢰도 및 내용 적합성 재검토 필요(일반론/전망 성격).

---

## 4) 우선 읽기 리스트(최대 12개) + 선정 근거/활용 포인트  
(중요: “보고서 포커스(최근 12개월, 양자컴퓨팅 기반 재료 연구, OLED 발광재료 관점, 산업 적용)”에 직접 기여하는 순으로 정렬)

1) **`archive/tavily_search.jsonl`**  
   - 근거: OLED×양자컴퓨팅 관련 **공식/업계 링크(IBM Research, MCGC PDF, OLED-Info 등)**가 여기에서 추출됨.  
   - 활용: 산업계 공개정보(삼성/LG/UDC 포함 여부), “supporting” 출처 구분, 추가 1차 출처(논문/프리프린트/공식발표)로 점프.

2) **`archive/_log.txt`**  
   - 근거: “지난 12개월” 커버리지에서 **누락/다운로드 실패/쿼리 편향**을 확인해야 보고서의 한계(불확실성)를 정직하게 기술 가능.  

3) **`archive/openalex/works.jsonl`**  
   - 근거: OA로 들어온 학술 소스의 **주제 적합도 선별** 및 인용 가능한 1차 문헌 후보 재정렬에 필수.  
   - 활용: OLED/quantum/chemistry/VQE/QPE/excited states/TADF 키워드로 빠르게 스크리닝(추가 수집 필요성 판단).

4) **`archive/20260110_qc-oled-index.md`**  
   - 근거: 현재 아카이브 범위를 한눈에 확인. 보고서에 “자료 범위/한계” 절의 근거로 사용.

5) **`archive/openalex/text/W4410193211.txt`** (Using GNN property predictors as molecule generators, Nature Communications, 2025)  
   - 근거: “재료 탐색/설계 워크플로·데이터 파이프라인”에서 **생성 모델/역설계(inverse design)** 사례로 유용(근거 강도는 ‘중간’ 예상).  
   - 한계: 양자컴퓨팅 자체보다는 ML 쪽일 가능성 → 양자-고전 하이브리드 흐름과 연결해 해석해야 함.

6) **`archive/openalex/pdf/W4410193211.pdf`**  
   - 근거: 텍스트 추출 누락/그림/방법 섹션 확인용(재현성·조건·모델 세부 파라미터 확보).

7) **`archive/openalex/text/W4406477905.txt`** (Exploring quantum materials and applications: a review)  
   - 근거: “양자” 키워드로 혼동될 수 있는 **‘quantum materials’ vs ‘quantum computing for materials’** 개념 구분에 참고(비교·대조용).  
   - 한계: OLED 관점 직접 기여는 낮을 가능성.

8) **`archive/openalex/text/W4417018335.txt`** (Quantum-AI Synergy…)  
   - 근거: “양자-고전 하이브리드/에러완화/워크플로” 일반론을 정리할 때 참고 가능.  
   - 한계: 저널 신뢰도/사례 검증 필요(인용시 근거 강도 낮게 평가 가능).

9) **`archive/openalex/text/W4410446803.txt`** (Forecasting the future…)  
   - 근거: “향후 12–24개월 전망” 서술의 배경 참고.  
   - 한계: 전망서/챕터 성격으로 보이며 OLED/양자화학 직접 근거로는 약할 가능성.

10) **`archive/openalex/text/W4406330631.txt`** (Organoluminophores 관련 리뷰)  
   - 근거: OLED 발광재료(organoluminophores) 배경 정리에 일부 도움 가능.  
   - 한계: 양자컴퓨팅 기반 탐색/설계와의 직접 연결이 약할 가능성.

11) **`archive/_job.json`**  
   - 근거: 수집 파이프라인(검색엔진·필터·max-results 등) 확인 → “데이터 파이프라인/한계” 메타 논의에 사용.

12) **`archive/openalex/text/W4406707630.txt`** 또는 `W4406399672.txt` (둘 다 주제 적합도 낮음)  
   - 근거: **오프토픽 여부를 최종 판정**해 인용 목록에서 배제하기 위한 확인용(시간이 부족하면 생략 가능).

---

## 5) 추천 읽기 순서(실행 가능한 플랜)

1. `tavily_search.jsonl`에서 **OLED×quantum computing** 직접 근거(IBM Research 글, MCGC PDF, 업계 기사)를 먼저 확보  
2. `_log.txt` + `_job.json`으로 **수집 편향/누락 원인**을 파악(“공개 정보의 한계”와 연결)  
3. `openalex/works.jsonl`로 학술 소스 중 **OLED/quantum chemistry/ excited states/ VQE/EOM-VQE/VQD/QPE** 관련이 있는지 재선별(현재 PDF 7개가 포커스에 충분치 않아 보임)  
4. 남는 학술 근거는 `W4410193211` 중심으로 “워크플로/파이프라인” 섹션의 기술적 근거를 보강  
5. 나머지 OpenAlex 리뷰류는 **개념 정리·비교/대조·전망**에서 “근거 강도: 낮음/중간”으로 제한적으로 사용

원하시면 다음 단계로, `tavily_search.jsonl`에서 **OLED 관련 1차 출처(논문/arXiv/npj Computational Materials 등)로 연결되는 링크들만 추출**해 “학술(주출처)” vs “supporting(웹)”로 재분류한 정리표까지 만들어 드릴 수 있습니다.