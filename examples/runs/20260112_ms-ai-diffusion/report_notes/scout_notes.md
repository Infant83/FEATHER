## 아카이브 맵(coverage 파악) — 20260112_ms-ai-diffusion
보고서 포커스(“MS 에서 발간한 AI 확산 보고서” 심층 번역/리뷰)에 맞는 소스는 **Microsoft Research PDF 1건**으로 거의 단일 출처입니다. OpenAlex/arXiv/YouTube 인덱스는 생성되지 않았고(조회 0), 보조 웹 리서치 산출물도 없습니다.

### 1) 핵심 산출물(원문)
- **`archive/web/pdf/Microsoft-AI-Diffusion-Report-2025-H2.pdf`** (1.9MB)  
  - 원문 PDF. figure/표를 “추출해 리포트에 사용”하려면 최우선.
- **`archive/web/text/Microsoft-AI-Diffusion-Report-2025-H2.txt`** (29KB)  
  - PDF 텍스트 추출본(페이지 마커 `===== PAGE N =====` 포함). 번역/요약/인용 작업에 가장 빠르게 활용 가능.
- **`archive/tavily_extract/0001_https_...pdf.txt`** (27KB)  
  - Tavily가 뽑은 raw_content(상당 부분이 `web/text`와 중복). 누락/깨짐 비교용 보조.

### 2) 인덱스/작업 메타
- **`archive/20260112_ms-ai-diffusion-index.md`**  
  - 아카이브 구성 요약(어떤 파일이 무엇인지).
- **`instruction/20260112_ms-ai-diffusion.txt`**  
  - 입력 URL 1개(해당 PDF).
- **`archive/_job.json`**, **`archive/_log.txt`**  
  - 실행 설정/로그(재현성, 수집 범위 확인용). 내용 품질 자체에는 영향 적음.

### 3) 부재(없음을 확인)
- `archive/tavily_search.jsonl`, `archive/openalex/works.jsonl`, `archive/arxiv/papers.jsonl`, `archive/youtube/videos.jsonl`, `archive/local/manifest.jsonl`  
  - **현재 run에는 존재하지 않음** → 외부 참고문헌/2차 자료 기반 확장은 아카이브만으로는 어렵고, PDF 내부의 참고 링크([1][2][3] 등) 정도만 활용 가능.

---

## 우선순위 “읽기” 리스트(최대 12개) + 이유
1. **`archive/web/pdf/Microsoft-AI-Diffusion-Report-2025-H2.pdf`**  
   - figure/지도/표 등 시각자료를 정확히 반영해야 “번역+리뷰형 보고서” 품질이 올라감.
2. **`archive/web/text/Microsoft-AI-Diffusion-Report-2025-H2.txt`**  
   - 빠른 전체 구조 파악, 장/섹션별 번역 초안 작성, 문장 인용에 최적.
3. **`archive/tavily_extract/0001_https_...pdf.txt`**  
   - 텍스트 추출 누락/오탈자 비교, 특정 문단이 `web/text`에서 깨졌을 때 백업.
4. **`archive/20260112_ms-ai-diffusion-index.md`**  
   - 작업 착수 시 파일 위치/구성 재확인(팀 작업/재현성에 도움).
5. **`instruction/20260112_ms-ai-diffusion.txt`**  
   - 원 출처 URL 확인(보고서 서지 정보/참조 링크 정리 시 필요).
6. **`archive/_job.json`**  
   - 데이터 수집 범위(30일, URL 1개) 확인 → “이 보고서는 단일 출처 번역임”을 명확히 하는 근거.
7. **`archive/_log.txt`**  
   - 다운로드/추출 과정에서 오류 없었는지 확인(텍스트 누락 원인 추적용).

(실질 콘텐츠는 1~3이 전부라고 봐도 무방합니다.)

---

## 추천 읽기/작성 플로우(리딩 플랜)
1) **`web/text`로 전체 스캔**: Executive Summary → 핵심 지표(16.3%, Global North 24.7% vs Global South 14.1% 등) → 국가 랭킹/변화 → 한국 관련 섹션(“South Korea’s AI Surge…”) 순으로 구조 잡기  
2) **`pdf`로 figure/표 정확화**: 지도(“AI Diffusion by Economy H2 2025”), Top30 랭킹 표, Global North/South 격차 바 차트, 한국 SAT(CSAT) 모델 성능 그래프 등 “보고서에 넣을 그림 후보” 체크  
3) **번역은 ‘요약-근거-해석’ 단락 단위로**: 원문 문단을 그대로 옮기기보다, (요약 2~3문장) → (원문 수치/사례 근거) → (의미/시사점 해석) 흐름으로 재서술  
4) **중복/깨짐 검증**: 애매한 문장이나 끊긴 부분은 `tavily_extract`와 대조  
5) **최종 보고서 구성 제안**: (1) 한눈에 보는 결론 (2) 측정 방법/한계 (3) 글로벌 격차(북/남) (4) 상위 국가와 미국의 ‘역설’ (5) South Korea 사례 심층 (6) DeepSeek/지정학적 확산 (7) 시사점/체크리스트

원하면 제가 다음 단계로 **PDF에서 “리포트에 쓸 figure 후보(캡션/페이지/의미)” 목록을 먼저 뽑는 읽기 계획**으로 더 촘촘하게 쪼개드릴 수도 있어요.