## 1) 아카이브 맵(coverage) 요약 (Query: `20260112_MS-AI-2025`)
이번 रन은 **Microsoft Research가 공개한 단일 PDF 보고서**(“Global AI Adoption in 2025 — A Widening Digital Divide”, January 2026)를 내려받아 **PDF 원문 + 텍스트 추출본**을 만든 구성입니다.  
별도의 Tavily 검색 결과(여러 URL), OpenAlex, arXiv, YouTube 인덱스는 **생성되지 않았습니다**(JSONL 메타데이터 파일 없음).

- 입력 지시 파일: `instruction/20260112.txt`  
  - 포함 URL 1개: Microsoft AI Diffusion Report PDF
- 인덱스: `archive/20260112_MS-AI-2025-index.md`  
  - 수집물 목록/경로 정리
- 핵심 원문(PDF): `archive/web/pdf/Microsoft-AI-Diffusion-Report-2025-H2.pdf`
- 핵심 텍스트(추출):  
  - `archive/web/text/Microsoft-AI-Diffusion-Report-2025-H2.txt` (페이지 구분 포함)  
  - `archive/tavily_extract/0001_https_www.microsoft.com_...pdf.txt` (Tavily extract 형태의 raw_content; 실질적으로 위 텍스트와 유사)
- 실행 로그/설정:
  - `archive/_job.json` (수집 파라미터, URL, 옵션)
  - `archive/_log.txt` (다운로드/변환 기록)

---

## 2) 주요 소스 파일 인벤토리(핵심/보조로 구분)

### A. 리포트 본문(가장 중요)
1. `archive/web/pdf/Microsoft-AI-Diffusion-Report-2025-H2.pdf`  
   - **원문 1차 소스**. 표/그림(figure) 위치와 시각 요소를 확인하기에 필수.
2. `archive/web/text/Microsoft-AI-Diffusion-Report-2025-H2.txt`  
   - **작성용 1순위 텍스트 소스**. 페이지 단위로 내용이 끊겨 있어 번역/리뷰 구성에 유리.
3. `archive/tavily_extract/0001_https_www.microsoft.com_en-us_research_wp-content_uploads_2026_01_Microsoft-AI-Diffusion-Report-2025-H2.pdf.txt`  
   - raw_content로 길게 합쳐진 형태. 본문 누락/깨짐 여부를 **교차검증**할 때 도움.

### B. 수집/재현성(메타)
4. `instruction/20260112.txt`  
   - 보고서 출처 URL 확인(인용에 유용).
5. `archive/20260112_MS-AI-2025-index.md`  
   - 아카이브 구조 빠른 파악용.
6. `archive/_job.json`, `archive/_log.txt`  
   - 수집 시점/옵션/변환 성공 여부 확인용(보고서 방법론 섹션에는 직접 인용 X, 부록 느낌으로만 참고).

---

## 3) “키 소스 파일” 제안(최대 12) + 읽는 이유(우선순위)
1) `archive/web/text/Microsoft-AI-Diffusion-Report-2025-H2.txt`  
- 이유: 한국어 심층 번역/리뷰의 **주된 재료**. Executive Summary, 국가 랭킹, 지역 격차( Global North vs Global South ), South Korea/DeepSeek 서술 등 핵심 문장 확보.

2) `archive/web/pdf/Microsoft-AI-Diffusion-Report-2025-H2.pdf`  
- 이유: 보고서에서 “figure/표/지도(확산률 색상 지도, 랭킹 표 등)”가 메시지를 좌우. **그림 추출/캡션 정확성** 확보를 위해 필요.

3) `archive/tavily_extract/0001_https_...pdf.txt`  
- 이유: 텍스트 추출본에서 페이지 경계 때문에 끊긴 문장, 표 깨짐이 있을 때 **원문 텍스트를 보완**.

4) `archive/20260112_MS-AI-2025-index.md`  
- 이유: 최종 리포트 작성 전에 “이번 रन에 무엇이 들어있고 무엇이 없는지”를 명확히 정리(출처 투명성).

5) `instruction/20260112.txt`  
- 이유: 보고서 **공식 URL** 재확인(참고문헌/각주 처리에 필요).

6) `archive/_job.json`  
- 이유: “telemetry 기반 측정치” 같은 표현을 쓸 때, 데이터 출처가 **Microsoft 텔레메트리 기반**이라는 점을 보고서에 정확히 적기 위한 배경 확인.

7) `archive/_log.txt`  
- 이유: PDF 다운로드/변환이 정상 수행되었는지 확인(작업 안정성 점검).

(현재 아카이브 파일이 6개뿐이라, 실질적으로 위 7개가 전부입니다. 12개까지 확장할 추가 소스는 이번 रन에는 없습니다.)

---

## 4) 추천 읽기/작성 플로우(자연스러운 “요약-근거-해석” 문체를 위한 계획)
1. **`web/text`로 전체 구조 스캔**  
   - Executive Summary → 핵심 주장(확산은 늘었지만 격차 확대) → 지역/국가 랭킹 → 사례(대한민국 급등, DeepSeek 부상) 순으로 “목차 없이도” 흐름 파악.
2. **PDF에서 figure/표 위치 확인 및 후보 선정**  
   - 예: “AI Diffusion by Economy H2 2025” 지도/랭킹, Global North vs South 비교 그래프, South Korea 관련 벤치마크 도표 등.
3. **텍스트 추출본 vs Tavily extract 교차검증**  
   - 특히 수치(예: 16.3%, 24.7%, 14.1%, 격차 10.6pp 등)와 고유명사(DeepSeek, AI Basic Act 등) 문장 단위로 확인.
4. **리포트 집필(한국어 심층 번역+해설)**  
   - 단순 번역이 아니라 문단마다:  
     - (요약) 이 문단이 말하는 바 1~2문장  
     - (근거) 수치/사례/인용 포인트  
     - (해석) 왜 중요하고 어떤 함의인지(디지털 격차, 정책/언어모델/제품요소, 미·중 경쟁 구도)
5. **그림 삽입 결정**  
   - “핵심 메시지 2~3개를 강화하는 figure”만 선별해 과밀 방지.

원하시면 다음 단계로, 제가 바로 `Microsoft-AI-Diffusion-Report-2025-H2.pdf`에서 **사용할 figure 후보(페이지/캡션/의미)**를 먼저 뽑아드릴 수도 있어요.