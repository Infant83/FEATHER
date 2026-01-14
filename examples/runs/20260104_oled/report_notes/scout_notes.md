## 아카이브 맵(coverage 파악)

### 1) 핵심 인덱스/설정 파일
- `archive/20260104_oled-index.md`  
  - 이번 런의 요약(쿼리/URL/산출물 위치). **arXiv ID 0개**, URL 2개.
- `instruction/20260104_oled.txt`  
  - 입력 지시문. 쿼리: `oled`, `quantum computing`, `recent 30 days` + URL 2개(LinkedIn, Nature Communications PDF).
- `archive/_job.json`  
  - 수집 파이프라인 설정. **openalex_enabled=false, youtube_enabled=false**, days=30, max_results=8.
- `archive/_log.txt`  
  - 실행 로그(에러/누락 원인 점검용).

### 2) 소스 인덱스(메타데이터 JSONL) — *반드시 열람*
- `archive/tavily_search.jsonl`  
  - Tavily 검색 결과 인덱스. 현재 확인된 상위 결과는 Wikipedia, OLED-Info, DOE, Ossila 등 **개론/백과 성격 다수**.

> 주의: 요청하신 “papers, open-access journals, credible industry sources” 관점에서 **OpenAlex/ arXiv 인덱스가 생성되지 않았고(폴더/JSONL 없음)**, 실질적인 논문 원문은 Nature Communications PDF 1개만 확보된 상태입니다.

### 3) 원문/추출 텍스트(실제 내용)
- `archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt`  
  - **Nat Commun (2025) “High aspect ratio organic light-emitting diodes”** 초안(Article in Press) 텍스트 추출본.  
  - 기술 포인트(이미 확인): corrugated substrate로 **AE~1.4x**, 수명 **2.7배**, 광추출/효율 **최대 40%↑** 등.
- `archive/tavily_extract/0001_https_www.linkedin.com_posts_fanli_ai-molecular-design-has-some-known-challenges-activity-...txt`  
  - Fan Li의 LinkedIn 포스트(Trio, molecular design)로 **OLED와 무관**.

---

## 오프토픽/갭(보고서 품질 리스크)
- `quantum computing`, `recent 30 days` 쿼리가 OLED와 무관하게 섞였고, 결과적으로 **OLED 관련 “최신 논문/산업자료” 커버리지가 매우 얕음**.
- Tavily 검색 결과도 상당수가 **기초 설명 사이트**(Wikipedia, DOE, Ossila 등)로, “트렌드/소재 혁신/상용화 비교”에 필요한 **제조·수율·원가·수명·효율** 근거가 부족.
- LinkedIn 소스는 내용 자체가 OLED가 아니라서 본 보고서에는 **제외 권장**.

---

## 우선순위 읽기 목록 (최대 12개, 근거 포함)

1. `archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt`  
   - **유일한 피어리뷰 저널급(오픈액세스) 기술 근거**. “기술 변곡점(수명/효율 개선)” 도출에 핵심.
2. `archive/tavily_search.jsonl`  
   - 어떤 출처들이 잡혔는지/산업성 소스가 있는지 스크리닝(필요시 추가 크롤링 질문 생성).
3. `archive/20260104_oled-index.md`  
   - 산출물 전체 구조/누락(예: arXiv 0개) 빠른 파악.
4. `archive/_job.json`  
   - 왜 OpenAlex/YouTube가 비활성인지 등 **커버리지 한계의 원인** 확인 및 재실행 제안 근거 마련.
5. `archive/_log.txt`  
   - 수집 실패/차단/필터링 여부 확인(특히 arXiv 힌트가 있는데도 ID 0개인 이유).
6. `instruction/20260104_oled.txt`  
   - 입력 자체가 OLED 트렌드 보고서 목적과 어긋난 부분(쿼리/URL) 확인 → 후속 의사결정 질문/재수집 플랜에 반영.
7. `archive/tavily_extract/0001_https_www.linkedin.com_posts_...txt` *(읽되, 보고서 본문에는 보통 제외)*  
   - 오프토픽 확인용. “갭/노이즈 소스”로 기록 가능.

(현재 아카이브에 파일이 6개뿐이라, 실질적으로 읽을 수 있는 OLED 관련 심층 소스는 1개입니다.)

---

## 읽기/정리 플랜(Executive brief 작성용, 단계별)

1) **논문 1개를 ‘변곡점 후보’로 구조화**  
- (Nat Commun)에서: 문제정의(고휘도에서 수명↓), 제안(High aspect ratio corrugation), 정량 결과(AE 1.4x, lifetime 2.7x, outcoupling 40%↑), 제조 제약(VTE 두께 균일도/AE2.0 재현성 문제) 추출.

2) **Tavily 검색 인덱스로 ‘산업 적용/상용화 단서’ 탐색**  
- 현재는 개론 사이트 위주라, “상용화 비교(수율/원가/수명/효율)” 근거로는 약함 → 어떤 결과가 있는지 전체 결과 목록을 훑고, 산업 리포트/기업 발표/시장조사 출처가 있는지 선별.

3) **갭/모순 포인트 명시**  
- 연구(고각 텍스처로 수명↑) vs 상용(조명용 OLED 미확산: cost, lifetime, manufacturing complexity) 간 간극을 “근거 부족”으로 표시.  
- AE2.0에서 재현성 낮음 등은 “스케일업/수율 리스크”로 연결.

4) **의사결정자용 후속 질문 설계(추가 수집 필요)**  
- (예) corrugated substrate 양산 공정(roll-to-roll 가능성?), 결함/수율 데이터, 광학 균일성/헤이즈 수용성, 자동차 조명 인증/신뢰성 테스트, 비용 모델 등.

---

## 권장: 다음 런에서 커버리지 확장(필요시)
- OpenAlex 활성화(`openalex_enabled=true`) + 쿼리 구체화: “OLED blue emitter lifetime TADF phosphorescence hyperfluorescence”, “OLED manufacturing yield FMM evaporation”, “microOLED silicon backplane”, “inkjet printed OLED”, “tandem OLED lighting” 등.
- 산업 소스 타깃: DSCC, Omdia, TrendForce, OLED-Info(뉴스/리포트), SID/Display Week proceedings, 주요 패널 메이커/소재사(Universal Display, Samsung Display, LG Display, BOE) 기술 발표자료.

원하시면, 현재 아카이브 기준으로 “변곡점 3–5개”를 만들기엔 소스가 부족하므로 **(1) 현 소스만으로 작성 가능한 최소 브리프**와 **(2) 재수집 후 보강 브리프** 두 트랙으로 읽기 전략을 더 구체화해드릴 수 있습니다.