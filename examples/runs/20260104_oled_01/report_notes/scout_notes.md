## 아카이브 맵(coverage 파악용 인덱스/메타데이터 우선)

### 0) 런/아카이브 구조 요약
- 런 폴더 기준(루트 `/`에 매핑됨): **20260104_oled_01**
- 총 파일: **11개**
- 검색 범위: **최근 30일**
- 쿼리: `oled`, `quantum computing`(후자는 보고서 초점과 무관 → 제외 권장)
- 핵심 소스 유형
  - Tavily(웹 검색 + 추출 텍스트)
  - OpenAlex(논문 메타 + OA PDF/텍스트)
  - Web PDF(Nature Communications OA PDF + 텍스트)

---

## 1) 핵심 인덱스(JSONL/로그) — “반드시 먼저 볼 것”
아카이브에 존재하는 JSONL 인덱스는 아래 2개입니다(요구사항대로 확인 완료).

1. **`archive/tavily_search.jsonl`** (65 KB)  
   - 웹 검색 결과 리스트(위키/산업 허브/DOE 등 포함)  
   - “산업적 함의/시장/적용” 근거를 넓히는 용도지만, 일부는 일반 설명 수준(위키 등)이라 신뢰도/깊이 필터링 필요.

2. **`archive/openalex/works.jsonl`** (23 KB)  
   - 최근(2025-12~) OA 논문/리포트 메타데이터 묶음.
   - **Stephen R. Forrest의 blue PHOLED 관점글(Advanced Materials)**, **inkjet printing OLED 리뷰(Advanced Optical Materials)** 등, “기술 인플렉션 포인트” 후보가 포함됨.
   - `quantum computing` 항목들도 섞여 있음 → OLED 보고서에서는 제외.

추가로 런 상태 확인용:
- **`archive/_job.json`**, **`archive/_log.txt`**: 수집 파이프라인/다운로드 성공 여부 트러블슈팅용.

---

## 2) 콘텐트 소스 인벤토리(파일별 역할)

### A. 1차(가장 중요한) 연구 논문/원문
1. **`archive/web/pdf/s41467-025-67312-4_reference.pdf`** (44 MB)  
   - Nature Communications (2025)  
   - 제목: **“High aspect ratio organic light-emitting diodes”**  
   - 포커스 적합도: 매우 높음(수명/효율/조명용 OLED의 current density–lifetime tradeoff를 구조적으로 해결)  
   - 산학/산업 연계: OLEDWorks LLC 저자 포함 → “상용화 관점” 연결점 존재.

2. **`archive/web/text/s41467-025-67312-4_reference.txt`** (42 KB)  
   - 위 Nature Communications PDF의 텍스트 추출본(빠른 스캐닝/인용용)

3. **`archive/openalex/pdf/W7117787413.pdf`** (268 KB)  
   - 제목: **“Recent Progress in Stretchable OLED Design and Applications”**  
   - 성격: 리뷰/개요 성격(저널 신뢰도는 메이저 탑티어는 아님)  
   - 포커스 적합도: 중간(트렌드/응용 아이디어엔 유용, 기술 근거는 교차검증 필요)

4. **`archive/openalex/text/W7117787413.txt`** (30 KB)  
   - 위 PDF 텍스트 추출본

### B. Tavily 추출(웹 문서 스냅샷)
5. **`archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt`** (40 KB)  
   - Nature Communications 논문을 Tavily가 별도 추출한 텍스트(초반부/핵심 수치가 잘 잡혀 있어 요약에 유리)

6. **`archive/tavily_extract/0001_https_www.linkedin.com_posts_fanli_ai-molecular-design-has-some-known-challenges-activity-7406324682192441344-60n3_utm_s.txt`** (7 KB)  
   - LinkedIn 포스트 기반(“AI molecular design…” 관련)  
   - 포커스 적합도: 낮~중(‘재료 설계 트렌드’ 힌트는 되지만, 1차 근거로 쓰기엔 약함)

### C. 런 인덱스/설정
7. **`archive/20260104_oled_01-index.md`** (1.6 KB)  
   - 무엇을 수집했는지 한눈에 보는 목차. 읽기 계획의 출발점.

---

## 3) 보고서 초점 대비 “현재 커버리지 진단”
- 강점
  - **조명용 OLED의 수명/효율 개선(고종횡비 구조)**: Nat Commun 1편이 강력한 근거 제공(2.7× lifetime, 최대 40% outcoupling 등 수치 포함).
  - OpenAlex에 **blue PHOLED 안정성**(Forrest 관점글), **잉크젯 프린팅 대면적 제조**(Advanced Optical Materials 리뷰) 같은 “인플렉션 포인트 후보”가 메타로 포착됨.
- 약점/갭
  - OpenAlex에 잡힌 **핵심 2편(blue PHOLED perspective, inkjet printing review)**은 *메타데이터만 있고 PDF가 아카이브에 없음* → 상용/제조 비교(수율/원가/공정) 파트를 채우려면 원문 확보 필요.
  - Tavily 검색 결과는 위키/소개성 산업 사이트가 다수 → **“credible industry sources”** 관점에선 추가로 (예: Display Supply Chain, DSCC / SID / Samsung Display, LG Display 기술 블로그/백서 / Universal Display(UUD) 자료 등) 보강 필요.

---

## 4) 우선순위 읽기 리스트 (Max 12) + 이유
1. **`archive/web/text/s41467-025-67312-4_reference.txt`**  
   - 가장 빠르게 핵심 수치/메시지 파악(인플렉션 포인트 후보: “면적증가로 current density↓ → lifetime↑”)

2. **`archive/web/pdf/s41467-025-67312-4_reference.pdf`**  
   - 그림/방법/실험 조건/재현성/한계(AE 2.0 재현성 이슈 등) 확인 필수

3. **`archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt`**  
   - Nat Commun 논문 요약/초록/도입부가 잘 뽑혀 있어 보고서 서술(배경-문제정의)에 유리

4. **`archive/openalex/works.jsonl`**  
   - “블루”/“제조(inkjet)”/“시장(TDDI)” 등 후보 소스 선별용. 보고서의 3–5개 인플렉션 포인트를 구성하는 재료.

5. **`archive/openalex/text/W7117787413.txt`**  
   - Stretchable OLED 트렌드/응용(웨어러블, 포토테라피 등) 빠른 체크

6. **`archive/openalex/pdf/W7117787413.pdf`**  
   - (가능하면) 도표/참고문헌 기반으로 더 신뢰도 높은 1차문헌을 역추적하기 위해 확인

7. **`archive/tavily_search.jsonl`**  
   - 산업/정부(예: DOE OLED basics) 출처 후보 추출. 다만 “일반 설명”은 과감히 버리고 근거성 있는 페이지만 채택.

8. **`archive/tavily_extract/0001_https_www.linkedin.com_posts_...txt`**  
   - AI 기반 분자 설계 트렌드 언급이 “재료 개발 가속” 인플렉션 포인트 보조근거가 될 수 있는지 검토(단, 검증 질문 포함해 제한적으로 인용)

9. **`archive/20260104_oled_01-index.md`**  
   - 인용/링크 정리, 누락 파일 확인용(리포트 작성 시 소스 트레이서 역할)

10. **`archive/_log.txt`** / 11. **`archive/_job.json`**  
   - 왜 Advanced Materials / Advanced Optical Materials PDF가 누락됐는지(다운로드 실패/권한/링크 문제) 확인 → 후속 수집 의사결정에 필요

(현재 아카이브에 파일 자체가 없어 더 읽을 수 없는, 그러나 *반드시 확보 권장* 소스)
- OpenAlex 메타에 존재: **“Perspective: OLED Displays Singing with the Blues” (Advanced Materials, 2025-12-26, DOI: 10.1002/adma.202519327)**  
- OpenAlex 메타에 존재: **“Research Progress on the Preparation of OLED Based on the Inkjet Printing” (Advanced Optical Materials, 2025-12-31, DOI: 10.1002/adom.202502807)**  
→ 보고서 초점(재료 진보 + 제조/상용화 비교)을 위해 원문 접근이 거의 필수입니다.

---

## 5) 추천 읽기 플랜(작업 순서)
1) **Nat Commun(High aspect ratio OLED)** 텍스트→PDF 순으로 완독:  
- 인플렉션 포인트(구조 설계로 current density-lifetime tradeoff 완화)와 수치(2.7× lifetime, ~40% outcoupling 등) 확보  
- 제조 난점/재현성 한계(AE2.0 실패/결함 민감도)도 같이 표시

2) **OpenAlex works 메타**에서 인플렉션 후보 3–4개를 더 뽑고(blue emitter, inkjet printing, stretchable 등),  
3) **Stretchable OLED 리뷰**로 “응용/단기 산업 임팩트”를 보강하되, 신뢰도 낮은 주장은 “갭/추가 질문”으로 처리  
4) **Tavily 검색 결과**에서 정부/산업 출처만 선별(위키/홍보성 페이지는 배경 1문단 이상 쓰지 않기)

원하시면, 다음 단계로 **OpenAlex works.jsonl에서 OLED 관련 항목만 추려(quantum computing 제거) ‘인플렉션 포인트 후보 리스트’**를 먼저 뽑아드릴 수 있습니다.