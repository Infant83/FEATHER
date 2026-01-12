## 1) 아카이브 맵(coverage 파악)
- 총 파일 수: **11개**
- 핵심 소스 유형
  - **피어리뷰 OA 논문(PDF+텍스트)**  
    - Nature Communications (2025): *High aspect ratio organic light-emitting diodes* (대형 PDF 44MB + 텍스트 추출본)
  - **OpenAlex 인덱스(works.jsonl)**: 최근 30일/키워드(oled, quantum computing 등)로 수집된 OA works 메타데이터
  - **OpenAlex로 내려받은 OA PDF 1편**  
    - *Recent Progress in Stretchable OLED Design and Applications* (Academic Journal of Science and Technology) (PDF+텍스트)
  - **Tavily 검색 인덱스(tavily_search.jsonl)**: “oled” 일반/산업 사이트 결과 다수(예: OLED-Info, LG Display, DOE 등)
  - **Tavily extract**: 링크드인 1건(분자설계/AI로 OLED와 직접 관련 낮음), Nature 논문 pdf 텍스트 1건

## 2) 키 소스 파일 인벤토리(중요도 중심)
### A. 1차 기술 근거(피어리뷰/학술)
1. `archive/web/pdf/s41467-025-67312-4_reference.pdf`  
   - Nature Communications (2025) “High aspect ratio organic light-emitting diodes” 원문 PDF
2. `archive/web/text/s41467-025-67312-4_reference.txt`  
   - 위 논문 텍스트 추출본(검색/인용에 편리)
3. `archive/openalex/pdf/W7117787413.pdf`  
   - “Recent Progress in Stretchable OLED Design and Applications” 리뷰 PDF(신뢰도는 저널 성격 확인 필요)
4. `archive/openalex/text/W7117787413.txt`  
   - 위 리뷰 텍스트 추출본

### B. 메타데이터/스카우팅 인덱스(추가 읽을거리 후보 찾기)
5. `archive/openalex/works.jsonl`  
   - OLED 관련 최근 works 다수(예: inkjet printing OLED, blue OLED perspective, nanotextured EQE 등) **단, 많은 항목이 PDF 미다운로드**
6. `archive/tavily_search.jsonl`  
   - 산업/기관 페이지(예: OLED-Info, LG Display, US DOE)로 “상용/산업 관점” 보강 가능

### C. 저신뢰/오프토픽(우선순위 낮음)
7. `archive/tavily_extract/0001_https_www.linkedin.com_posts_fanli_...txt`  
   - AI 분자설계(Trio framework) 내용. **OLED 포커스와 직접 연결 약함**
8. `archive/_job.json`, `archive/_log.txt`  
   - 실행 로그/작업 메타(리포트 근거로는 보조적)

## 3) 우선 읽기 플랜(최대 12개, 근거 포함)
1) `archive/web/text/s41467-025-67312-4_reference.txt`  
- **이유:** 보고서 포커스(기술 트렌드/재료·구조 혁신/단기 산업 함의)에 가장 직접적인 “정량 성능 개선” 근거 포함. (예: 면적 증대+추출 향상으로 **수명 2.7배**, **외부광추출/효율 최대 40%** 등)

2) `archive/web/pdf/s41467-025-67312-4_reference.pdf`  
- **이유:** 텍스트 추출본에서 빠진 **그림/방법/보충정보(공정 제약, 재현성, 측정조건)** 확인용. 제조/수율/코스트 논의에 필요한 디테일이 PDF에 있음.

3) `archive/openalex/text/W7117787413.txt`  
- **이유:** stretchable OLED 구조(버클링, island-bridge, intrinsically stretchable) 등 **응용(웨어러블/헬스케어) 방향성**을 빠르게 훑기에 좋음. 다만 리뷰의 출처 신뢰도는 점검 필요.

4) `archive/openalex/pdf/W7117787413.pdf`  
- **이유:** 위 텍스트의 **인용/도표/참고문헌 품질** 확인. “최근 진보/한계” 주장들이 실제 1차문헌 기반인지 검증.

5) `archive/openalex/works.jsonl`  
- **이유:** 이번 런에서 **다운로드되지 않은 핵심 논문 후보**가 여러 개 보임. 예:  
  - “Nanotextured light modulation for flexible OLEDs with 370% enhanced EQE…” (Scientific Reports)  
  - “Research Progress on the Preparation of OLED Based on the Inkjet Printing” (Adv. Optical Materials)  
  - “Perspective: OLED Displays Singing with the Blues” (Advanced Materials)  
  → “기술 변곡점 3–5개”를 뽑기 위해 추가 소스 확보가 필요.

6) `archive/tavily_search.jsonl`  
- **이유:** 연구 vs 상용 채택 비교(제조, 수율, 비용, 수명, 효율)를 위해 **산업/기관 관점** 레퍼런스가 필요. (OLED-Info, LG Display, US DOE 등) 단, 일반 소개글은 깊이가 낮을 수 있어 선별 필요.

7) `archive/20260104_basic-oa-index.md`  
- **이유:** 현재 커버리지 공백(다운로드된 학술 PDF가 2개뿐)을 빠르게 파악하고, 어떤 경로(OpenAlex/web)로 확보됐는지 추적.

8) `instruction/20260104.txt`  
- **이유:** 검색 지시가 “oled / quantum computing / recent 30 days + 2 URLs”로 혼재. 왜 오프토픽이 섞였는지 확인(추가 런 설계에 필요).

9) `archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt`  
- **이유:** Nature 논문 텍스트가 중복이지만, 추출 품질 차이가 있을 수 있어 **검색/인용용 백업**으로 확인.

10) `archive/_job.json`  
- **이유:** 수집 파라미터(결과 제한, OA 상태, 다운로드 옵션) 확인 → 다음 번에 OLED 핵심 논문(PDFdirect) 더 많이 받도록 튜닝할 근거.

11) `archive/_log.txt`  
- **이유:** 다운로드 실패/차단(PDFdirect 등) 여부 확인. “상용 vs 연구” 비교에 필요한 추가 소스 확보 장애요인 진단.

12) `archive/tavily_extract/0001_https_www.linkedin.com_posts_fanli_...txt`  
- **이유(낮음):** OLED 자체보다는 “재료 설계 자동화” 간접 힌트 정도. OLED 재료(블루 안정화 등)로 연결할 계획이 있을 때만 참고.

## 4) 현재 아카이브 기준 ‘보고서 포커스’ 대비 공백(gaps) 메모
- **학술 근거가 매우 좁음:** 피어리뷰급 OLED 핵심 논문이 사실상 Nature Communications 1편 중심.  
- **OpenAlex에 보이는 OLED 핵심 주제(블루, 잉크젯 프린팅, 나노텍스처 outcoupling 등)**는 메타만 있고 PDF가 없음 → “3–5개 기술 변곡점”을 충분히 비교하기 어려움.
- **산업/상용 관점 소스는 인덱스에만 존재**(OLED-Info, LG Display 등)하고, 실제로 추출/요약된 산업 리포트는 거의 없음.

원하시면, `openalex/works.jsonl`에 있는 OLED 관련 항목 중 **단기 산업 함의가 큰 것(inkjet printing, blue OLED, light extraction, TDDI 통합 등)**을 우선순위로 재다운로드하도록 다음 수집 계획(쿼리/필터/다운로드 전략)도 같이 제안할 수 있어요.