## 1) 아카이브 맵(coverage 진단)

### A. 상위 인덱스/지시문
- `instruction/20260110.txt`  
  - 검색 의도: “quantum computing materials discovery OLED emitters industrial applications” + 삼성/LG/UDC 키워드 조합.
  - **특징**: OLED·양자컴퓨팅을 직접 겨냥한 질의는 있으나, 결과 수집/다운로드가 제한적으로 보임.
- `archive/20260110_qc-oled-index.md`  
  - 지난 365일 범위로 실행되었으나 **URLs: 0, arXiv: 0**로 표기(수집 파이프라인이 OpenAlex PDF 위주로만 남은 상태).
  - OpenAlex PDF 7편 + Tavily JSONL 존재.

### B. 핵심 “인덱스형” 메타데이터(JSONL) — 반드시 활용
- `archive/tavily_search.jsonl` (웹 검색 결과/요약; supporting 후보)
  - **OLED×양자컴퓨팅 관련 직접 단서가 여기 포함**:
    - IBM Research 블로그: “Unlocking today's quantum computers for OLED applications” (과거 연구 소개/맥락 제공)
    - npj Computational Materials 논문 페이지 링크(2021년; 범위 밖이지만 **기술적 기준점**으로 중요)
    - Mitsubishi Chemical/Keio IBM Q Hub PDF(보도자료 성격)
    - OTI Lumionics 보도자료(2025-06-18) — **산업 적용 주장** 포함(단, press release라 근거 강도 평가 필요)
- `archive/openalex/works.jsonl` (학술 인덱스; OA 여부/DOI/PDF URL)
  - **문제점**: OLED/양자컴퓨팅에 직접 대응하는 논문이 거의 없고, 다수가 오프토픽(건축 파사드, 간암, 센서 등).
  - 그나마 범용적으로 쓸만한 것은 “Quantum-AI Synergy…”(비정통 저널로 보임) 정도.

### C. OpenAlex 풀텍스트/PDF(7편) — 주제 적합도 평가
OpenAlex에서 다운로드된 7편 중 **OLED 발광재료×양자컴퓨팅 기반 재료탐색**에 직접 기여하는 문서는 사실상 부재합니다.

- 상대적으로 “배경(quantum materials 일반)”으로만 쓸 수 있음
  - `archive/openalex/pdf/W4406477905.pdf` / `.../text/W4406477905.txt`  
    - *Exploring quantum materials and applications: a review*  
    - **양자컴퓨팅으로 재료를 설계한다**가 아니라, “quantum materials” 리뷰(개념 혼동 위험).
- 신뢰도/정합성 낮거나 오프토픽 가능성이 큰 항목
  - `W4417018335` *Quantum-AI Synergy and the Framework for Assessing Quantum Advantage*  
    - 저널/서지 형태가 비주류로 보이며, 주장(예: 효율 40% 개선 등)이 광범위. **교차검증 필요**.
  - `W4410193211` *Using GNN property predictors as molecule generators*  
    - 분자 생성/ML이지만 양자컴퓨팅이 핵심이 아닐 가능성 큼(확인 필요).
  - 나머지(`W4406399672`, `W4406707630`, `W4410446803`, `W4406330631`)는 OLED·양자컴퓨팅과 직접 관련성이 낮아 보임.

---

## 2) “키 소스 파일” 인벤토리(구조화)

### (1) 리서치 인덱스/로그
1. `archive/20260110_qc-oled-index.md` — 수집 범위/파일 포인터
2. `instruction/20260110.txt` — 질의 설계(coverage gap 진단에 필요)
3. `archive/_log.txt` / `archive/_job.json` — 실행 설정/에러·누락 점검(왜 URLs=0인지 원인 추적)

### (2) 메타데이터(JSONL 인덱스)
4. `archive/tavily_search.jsonl` — **OLED×양자컴퓨팅 직접 언급 소스가 들어있음**(supporting 라벨링 근거)
5. `archive/openalex/works.jsonl` — 학술 수집 결과의 적합도 선별

### (3) OpenAlex 텍스트/PDF(선별)
6. `archive/openalex/text/W4406477905.txt` (+pdf) — quantum materials 배경용(개념 혼동 주의)
7. `archive/openalex/text/W4417018335.txt` (+pdf) — quantum advantage 프레임워크(신뢰도 검증 전제)
8. `archive/openalex/text/W4410193211.txt` (+pdf) — 분자 생성/재료탐색 워크플로 참고 가능성(양자컴퓨팅 직접성은 확인 필요)

---

## 3) 우선순위 읽기 계획(최대 12개, 근거 포함)

1) `archive/tavily_search.jsonl`  
- **이유**: OLED×양자컴퓨팅(특히 excited-state/TADF) 관련 “직접 링크”가 여기에만 존재. 산업 시도(OTI Lumionics)도 포함.  
- **활용**: 보고서에서 “supporting”로 구분 인용, 공식/논문 원문 링크를 역추적해 1차 출처 확보.

2) `archive/20260110_qc-oled-index.md`  
- **이유**: 전체 수집 커버리지(365일, OA 7편, URL 0 등) 진단 및 결측 확인.

3) `archive/openalex/works.jsonl`  
- **이유**: OA로 잡힌 논문들의 제목/DOI/연도/저널을 빠르게 스크리닝해서 오프토픽 제거, 추가 수집 필요 지점 식별.

4) `archive/_log.txt`  
- **이유**: URL이 0으로 나온 이유(크롤 실패/설정 문제/다운로드 실패)를 파악하면 **추가 소스 보강 전략**을 세울 수 있음.

5) `archive/openalex/text/W4410193211.txt` (Nature Communications)  
- **이유**: “재료/분자 생성 워크플로(모델→생성→검증)” 관점에서, 양자컴퓨팅이 아니더라도 **현실적 파이프라인**(GNN/생성모델)을 비교축으로 사용 가능.

6) `archive/openalex/text/W4417018335.txt`  
- **이유**: “quantum advantage 평가 프레임”은 산업 적용 간극/병목을 논할 때 유용.  
- **주의**: 출처 신뢰도와 개별 수치 주장들은 **반드시 외부 1차 출처로 교차검증**해야 함.

7) `archive/openalex/text/W4406477905.txt`  
- **이유**: “quantum materials” 일반 리뷰로서 배경 서술에 제한적으로 사용 가능.  
- **주의**: “quantum materials”와 “quantum computing for materials discovery”를 혼동하지 않도록, 정의/범위 구분 파트에서만 인용 권장.

8) `instruction/20260110.txt`  
- **이유**: 질의 설계가 OLED 발광재료(형광/인광/TADF/CP-OLED) 세부를 충분히 커버했는지 점검하여, 추가 검색 키워드(예: *qEOM-VQE*, *VQD*, *active space*, *excited states*, *TADF ΔEST*)를 도출.

9) `archive/openalex/text/W4406330631.txt`  
- **이유**: 발광 유기재료(organoluminophores) 리뷰이긴 하나, 양자컴퓨팅과 직접 연결이 약함. **OLED 발광재료 분류·용어 정의 보조** 정도로만.

(10~12는 현재 아카이브 내에서는 우선도가 낮아 제외 권장: `W4406399672`, `W4406707630`, `W4410446803`는 주제 부합도가 낮음)

---

## 4) 커버리지 갭(보고서 초점 대비)과 다음 액션 제안

- **가장 큰 갭**: “지난 12개월” 기준의 **양자컴퓨팅 기반 재료 탐색/설계가 OLED 발광재료에 적용된 최신 논문/리뷰**가 아카이브(OpenAlex PDF 7편)에는 거의 없음.  
- **현 아카이브에서 OLED×양자컴퓨팅 직접 근거가 될 가능성이 높은 것은** `tavily_search.jsonl`이 가리키는 IBM/npj Computational Materials(연도는 2021로 범위 밖) 및 OTI Lumionics 2025 press release뿐입니다.  
- 따라서 최종 보고서 품질을 맞추려면:
  - Tavily 결과의 링크를 따라가 **1차 논문(JCTC/npj 등) 원문을 추가 확보**(가능하면 DOI 기반).
  - 산업 파트(삼성디스플레이, LG디스플레이, UDC)는 공개자료가 제한적이므로 **공식 발표/특허/기술보고/컨퍼런스(예: SID Display Week, IMID, 회사 지속가능경영보고서/기술 백서)** 중심으로 보강 필요.

원하시면, 위 갭을 메우기 위해 “추가로 아카이브에 들어와야 할 1차 출처 목록(논문/컨퍼런스/특허/기업 발표) + 권장 검색식(키워드/사이트 제한)”도 함께 설계해 드릴 수 있습니다.