## 아카이브 커버리지 빠른 요약 (20260112_ms-ai-diffusion)
- **대상 보고서(원문)**: *Global AI Adoption in 2025 — A Widening Digital Divide* (January, 2026)  
  - Microsoft Research / Microsoft AI Economy Institute 계열로 보이는 “AI Diffusion” 리포트
- **수집 범위**: URL **1개**(PDF 1개)만 포함. (OpenAlex/arXiv/YouTube 인덱스는 없음)
- **핵심 포커스**: 2025년 **H2(하반기)** 기준 생성형 AI 사용(확산) 지표, **Global North vs Global South 격차 확대**, 국가별 순위/증가폭, South Korea/DeepSeek 사례.

---

## 파일 인벤토리(구조화)

### 1) 인스트럭션/인덱스/로그
- `instruction/20260112_ms-ai-diffusion.txt`  
  - 입력 URL 1개만 포함(보고서 PDF 링크)
- `archive/20260112_ms-ai-diffusion-index.md`  
  - 어떤 파일이 생성됐는지 요약 인덱스(탐색용)
- `archive/_job.json`  
  - 실행 옵션/수집 설정(재현성, 범위 확인)
- `archive/_log.txt`  
  - 다운로드/텍스트 변환 로그(오류 여부 확인)

### 2) 본문 원천(가장 중요)
- `archive/web/pdf/Microsoft-AI-Diffusion-Report-2025-H2.pdf`  
  - 원문 PDF (그림/도표 추출은 여기서 해야 함)
- `archive/web/text/Microsoft-AI-Diffusion-Report-2025-H2.txt`  
  - PDF를 텍스트로 변환한 버전(번역/요약/인용 작업에 최우선)

### 3) 보조 추출물(중요도 중간)
- `archive/tavily_extract/0001_https_www.microsoft.com_en-us_research_wp-content_uploads_2026_01_Microsoft-AI-Diffusion-Report-2025-H2.pdf.txt`
  - Tavily가 뽑은 raw_content(JSON). 대체 텍스트 소스로 활용 가능(텍스트 파일 누락/깨짐 대비)

---

## “키 소스 파일” 하이라이트(보고서 작성에 직접 쓰일 것)
- **원문 그림/표 포함**: `archive/web/pdf/Microsoft-AI-Diffusion-Report-2025-H2.pdf`
- **번역/서술형 리뷰 본문 베이스**: `archive/web/text/Microsoft-AI-Diffusion-Report-2025-H2.txt`

(현재 텍스트 일부를 보면 Executive Summary, 국가별 확산 순위(H1 vs H2), Global North/South 비교 차트, South Korea 섹션, DeepSeek 언급 등이 포함됨)

---

## 우선순위 “읽기 계획”(최대 12개, 추천 순서 + 근거)
1. **`archive/web/text/Microsoft-AI-Diffusion-Report-2025-H2.txt`**  
   - 근거: 한글 심층 번역/리뷰 문장 작성의 메인 재료. 빠르게 전체 구조 파악 가능.
2. **`archive/web/pdf/Microsoft-AI-Diffusion-Report-2025-H2.pdf`**  
   - 근거: 보고서에서 “figure/그림 추출” 요구가 있어 필수. 도표/지도/랭킹표 등 시각자료 확인용.
3. **`archive/20260112_ms-ai-diffusion-index.md`**  
   - 근거: 아카이브 구성 한눈에 점검(누락/추가 소스 여부).
4. **`archive/tavily_extract/0001_https_...pdf.txt`**  
   - 근거: 텍스트 변환본과 대조해 누락된 문단/각주/표 텍스트가 있는지 확인하는 “세컨드 소스”.
5. **`instruction/20260112_ms-ai-diffusion.txt`**  
   - 근거: 입력이 단일 URL인지 확인(추가 참고문헌 수집이 필요한지 판단).
6. **`archive/_job.json`**  
   - 근거: 수집 옵션 확인(queries=0인 이유, openalex 결과가 없는 이유 등 커버리지 한계 설명 가능).
7. **`archive/_log.txt`**  
   - 근거: PDF→TEXT 변환 성공 여부, 문제 발생 시 근거 확보.

(현 아카이브는 총 6개 파일이라, 사실상 위 7개 중 6개만 존재/중복 없이 모두 커버됩니다.)

---

## 커버리지 갭(추가로 있으면 좋은데 현재 아카이브에 없는 것)
- 보고서에서 참조하는 **AI Diffusion technical paper [1]** 같은 “방법론 문서” 원문이 아카이브에 없음  
  → 번역/심층 해석을 강화하려면 해당 기술문서도 추가 수집 권장.
- South Korea/DeepSeek 관련 각주 [2][3][4] 등 **외부 참고자료**도 미수집  
  → 보고서 리뷰에서 “근거 확장(맥락)”을 하려면 링크 수집 필요.

원하시면, 다음 단계로는 **PDF에서 핵심 figure 목록(페이지/캡션/의미)만 먼저 뽑는 계획**(예: AI Diffusion 세계지도, Global North vs South 막대그래프, 국가 Top30 변화표, South Korea 관련 그래프)을 제안드릴 수 있어요.