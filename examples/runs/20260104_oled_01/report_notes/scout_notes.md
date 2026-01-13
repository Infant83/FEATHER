## 아카이브 맵(coverage 파악) — Query: `20260104_oled_01`
- 기간/범위: 최근 30일 설정
- 수집 채널: Tavily Search/Extract + OpenAlex(OA) + Web PDF( Nature Communications )
- 총 파일: 11개  
- 주제 적합도 요약:
  - **핵심(직접 OLED 기술/소재/산업 시사점)**: Nature Communications 논문(High aspect ratio OLED), OpenAlex의 OLED 관련 리뷰/퍼스펙티브(blue, inkjet, stretchable)
  - **부차(산업/시장)**: “OLED TDDI Market Overview”(Zenodo, 컨설팅 리포트 메타)
  - **오프토픽**: LinkedIn 글(Trio 분자설계 AI), OpenAlex의 “Quantum Computing” 2건

---

## 구조적 인벤토리(폴더별 핵심 파일)
### 1) Run/메타 & 인덱스
- `archive/20260104_oled_01-index.md`  
  - 수집 커맨드/범위/다운로드된 PDF 목록을 정리한 인덱스
- `archive/_job.json`, `archive/_log.txt`  
  - 실행 파라미터/로그(재현성·누락 확인용)

### 2) Tavily (검색/요약/추출)
- `archive/tavily_search.jsonl`  
  - “oled” 등 쿼리 결과(위키, OLED-Info, DOE 등 일반/산업 개론 소스 포함)
- `archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt`  
  - Nature Communications PDF에 대한 추출 텍스트(동일 논문)
- `archive/tavily_extract/0001_https_www.linkedin.com_posts_...txt`  
  - LinkedIn 포스트(분자설계 AI) — **OLED 포커스와 불일치**

### 3) Web (원문 PDF + 텍스트)
- `archive/web/pdf/s41467-025-67312-4_reference.pdf` (대용량 44MB)
- `archive/web/text/s41467-025-67312-4_reference.txt`  
  - 논문: **“High aspect ratio organic light-emitting diodes” (Nat Commun, 2025)**  
  - 요지(텍스트에서 확인): 패널 면적 대비 **발광 활성면적 증가(AE~1.4x)**로 **동일 휘도에서 전류밀도↓**, 결과적으로 **수명 2.7배↑**, **외부광추출 효율 최대 40%↑**. OLEDWorks 공저로 산업적 함의 존재.

### 4) OpenAlex (OA 인덱스 + 일부 원문)
- `archive/openalex/works.jsonl`  
  - OLED 관련 후보:
    - “Perspective: OLED Displays Singing with the Blues” (Advanced Materials, 2025-12-26) — **블루(Blue) 수명/효율 핵심 이슈**
    - “Research Progress on the Preparation of OLED Based on the Inkjet Printing” (Advanced Optical Materials, 2025-12-31) — **잉크젯 프린팅(대면적/원가/수율)**
    - “Recent Progress in Stretchable OLED Design and Applications” (Academic Journal of Science and Technology, 2025-12-28) — **스트레처블 구조/응용(다만 저널 신뢰도는 상대적으로 낮을 수 있음)**
    - “OLED TDDI Market Overview” 2건 (Zenodo) — **시장/공급망 관점**
  - 오프토픽: quantum computing 항목들 포함(무시 권장)
- `archive/openalex/pdf/W7117787413.pdf`, `archive/openalex/text/W7117787413.txt`  
  - 스트레처블 OLED 리뷰 원문(상대적으로 개론/리뷰 성격)

---

## 우선 읽기 플랜(최대 12개) + 이유(보고서 포커스 기준)
1) `archive/web/text/s41467-025-67312-4_reference.txt`  
   - **기술 인플렉션 포인트 후보**: “구조(고종횡비 표면 텍스처)로 전류밀도-수명 trade-off 완화”를 정량(수명 2.7x, 효율 +40%)으로 제시. **근시일 조명/특수 패널 응용** 및 제조(VTE 적층 균일도) 논의 포함.

2) `archive/web/pdf/s41467-025-67312-4_reference.pdf`  
   - 텍스트 누락된 **그림/실험조건/보충 노트 근거** 확인용(특히 AE 정의, 제조 공정 창, 결함/균일도, 실제 수명 측정 조건).

3) `archive/openalex/works.jsonl`  
   - “Blue”, “Inkjet printing”, “Stretchable”, “TDDI market” 등 **후속 핵심 소스(논문 원문 링크/DOI)**를 한 번에 스캐닝하여 **기술 트렌드 지도화**.

4) `archive/tavily_search.jsonl`  
   - OLED-Info, DOE 등에서 **산업 채택 vs 연구**(조명 시장 지연 원인: cost/lifetime 등) 대비용 배경 근거 확보. (단, 위키류는 보조로만)

5) `archive/openalex/text/W7117787413.txt`  
   - 스트레처블 OLED의 **구조적 접근(버클링, island-bridge, intrinsically stretchable)**을 정리해 **웨어러블/헬스케어 근시일 응용**과 연결 가능. (증거 강도는 선별 필요)

6) `archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt`  
   - Nature 논문 텍스트가 web/text와 중복 가능하지만, 추출 품질 차이를 비교해 **누락 단락 보완**.

7) `archive/_log.txt`  
   - 수집 누락/실패 URL, 다운로드 실패 등 **coverage 갭** 점검(“왜 arXiv 결과가 0인가” 등).

8) `archive/_job.json`  
   - 실행 옵션(예: `oa-max-results 5`, `max-results 8`)으로 인해 **검색이 좁아진 한계**를 파악하고, 추가 질의 필요 여부 판단.

9) `archive/tavily_extract/0001_https_www.linkedin.com_posts_...txt` *(낮은 우선순위/대체로 제외 권장)*  
   - OLED와 직접 관련이 없어 보임. 다만 “분자 설계/최적화”가 OLED 소재 발굴(TADF/PHOLED)과 연결될 여지가 있으면 **부록 아이디어**로만 활용.

10) `archive/20260104_oled_01-index.md`  
   - 보고서 작성 시 **출처/수집 경로/파일 매핑**을 빠르게 재확인하는 용도.

11) `archive/openalex/pdf/W7117787413.pdf`  
   - 텍스트 대비 표/그림 확인용(스트레처블 쪽에 정량 데이터가 있으면 활용).

12) (선택) `archive/tavily_search.jsonl` 내 OLED-Info/DOE 결과 원문 URL들  
   - 아카이브 내부 파일은 아니지만, **산업 신뢰 가능한 2차 소스**로 인용할지 판단(필요 시 추가 크롤링 질문 도출).

---

## 현재 아카이브의 “갭/모순 가능 지점”(의사결정자 후속 질문으로 연결)
- **Blue emitter(특히 deep-blue PHOLED/TADF) 핵심 논문(Advanced Materials Perspective)은 메타만 있고 원문 PDF가 없음** → 실제 수명/효율 수치, 측정 표준 논쟁(논문 초록에 “measurement of quantum efficiency and operational lifetime의 문제” 언급) 확인 필요.
- **Inkjet printing OLED(Advanced Optical Materials)도 메타만 존재** → 제조 관점(수율, 잉크 레올로지, 커피링, 패터닝 정밀도, 수명/결함) 정량 근거가 아카이브에 부족.
- “Stretchable OLED” 원문은 있으나 저널/저자 소속을 보면 **리뷰 품질(신뢰도) 편차 가능** → 핵심 주장(예: 100% strain, 15,000 cycles 등)은 원출처(원 논문)로 역추적 필요.
- 조명용 OLED는 **상업 채택이 늦은 이유(cost/lifetime/outcoupling)**가 핵심인데, 이번 아카이브는 **조명 중심의 Nat Commun 1편에 편중**.

원하면 위 플랜 기준으로 “3–5개 기술 인플렉션 포인트” 후보를 먼저 뽑고(예: 고종횡비 텍스처로 lifetime trade-off 완화, deep-blue 안정성 진전, inkjet 대면적 제조 전환, stretchable 구조 상용화 임계점, TDDI 통합으로 모듈 얇아짐 등), 각 포인트별로 **이 아카이브에서 확보 가능한 근거 vs 추가로 필요한 근거**를 표 형태로 정리하는 독서/정리 순서도 제안할 수 있어요.