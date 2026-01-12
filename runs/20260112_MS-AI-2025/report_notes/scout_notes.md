## 아카이브 맵(coverage 파악)

### 1) 핵심 원문(보고서 본문)
- `archive/web/pdf/Microsoft-AI-Diffusion-Report-2025-H2.pdf` (1.9MB)  
  - Microsoft Research 발간 PDF 원본. 최종 인용/페이지 구조 확인용(도표·캡션·각주 포함).
- `archive/web/text/Microsoft-AI-Diffusion-Report-2025-H2.txt` (29.7KB)  
  - PDF에서 추출된 텍스트. 실제 보고서 작성(한글 번역/리뷰) 작업의 1차 본문으로 쓰기 가장 좋음.

### 2) 검색/추출 인덱스(보조)
- `archive/tavily_extract/0001_https_www.microsoft.com_..._Microsoft-AI-Diffusion-Report-2025-H2.pdf.txt` (27.9KB)  
  - Tavily가 PDF에서 추출한 raw_content + 메타. 본문은 거의 동일하지만, “출처/제목/URL” 같은 정리된 메타가 있어 링크 확인에 유용.

### 3) 런/작업 메타(프로세스 확인)
- `instruction/20260112.txt`  
  - 수집 대상 URL 1개만 명시(= 이번 런은 “MS AI Diffusion Report 2025 H2” 단일 소스 중심).
- `archive/20260112_MS-AI-2025-index.md`  
  - 아카이브 인덱스. 어떤 파일이 생성됐는지 빠르게 확인 가능.
- `archive/_job.json`, `archive/_log.txt`  
  - 크롤/다운로드/텍스트화 성공 여부 및 옵션 기록(재현성 확인용).

> 참고: 이번 run에는 `tavily_search.jsonl`, `openalex/works.jsonl`, `arxiv/papers.jsonl`, `youtube/videos.jsonl`, `local/manifest.jsonl` 같은 “JSONL 메타데이터 인덱스”가 **없습니다**. 즉, 외부 문헌을 넓게 모은 세트가 아니라, MS 보고서 1건을 중심으로 만든 아카이브입니다.

---

## 보고서 포커스에 맞는 “핵심 내용 스코프”(현재 확보된 본문 기준)

보고서 제목: **“Global AI Adoption in 2025 — A Widening Digital Divide”** (January, 2026)

본문에서 잡히는 큰 축(섹션/논지):
1. **Executive Summary**: 2025년 하반기(H2) 기준 전세계 생성형 AI 사용 확산(16.3%), 그러나 **Global North vs Global South 격차 확대**(24.7% vs 14.1%).
2. **상위 국가 랭킹/변화**: UAE, Singapore 등 선도. 미국은 인프라는 강하지만 사용 비중은 상대적으로 낮음(순위 하락 언급).
3. **South Korea case**: 2025 H2에 가장 큰 랭킹 상승(25→18위), 정책/한국어 모델 성능 향상/Ghibli-style 이미지 바이럴 등 복합 요인.
4. **DeepSeek case**: 오픈소스(MIT license)·무료 챗봇으로 **제약/비서구권·아프리카 등에서 확산**, AI 확산이 “품질”뿐 아니라 “접근성/유통/정치경제 조건”에 의해 결정됨을 강조.
5. **References**: 측정 방법론(“AI diffusion” 정의) 및 각종 기사/자료 링크(각주 기반 근거).

---

## 우선순위 읽기 목록(최대 12개) + 읽는 이유

1) `archive/web/text/Microsoft-AI-Diffusion-Report-2025-H2.txt`  
- **이유**: 보고서 본문 전체가 들어있고, 한글 번역/서술형 리뷰 작성의 “주 텍스트”로 가장 효율적.

2) `archive/web/pdf/Microsoft-AI-Diffusion-Report-2025-H2.pdf`  
- **이유**: 도표(국가별 확산 지도/랭킹표/DeepSeek 점유 등)와 캡션, 페이지 구성을 확인해 **정확한 인용·해석** 가능. 텍스트 추출본에서 깨진 표/문장도 원본으로 복원.

3) `archive/tavily_extract/0001_https_www.microsoft.com_..._Microsoft-AI-Diffusion-Report-2025-H2.pdf.txt`  
- **이유**: URL/제목 메타가 정리돼 있고, 본문 일부 누락/깨짐 발생 시 **대조본**으로 사용.

4) `archive/web/text/Microsoft-AI-Diffusion-Report-2025-H2.txt`의 **References(페이지 12~13)** 구간(같은 파일 내 섹션 재정독)  
- **이유**: 보고서가 인용하는 근거(예: “Measuring AI Diffusion” arXiv, Edelman Trust Barometer, DeepSeek 관련 Bloomberg/Carnegie 등)를 명시하므로, 리뷰 문체에서 “근거-해석”을 매끄럽게 엮기 좋음.

5) `archive/20260112_MS-AI-2025-index.md`  
- **이유**: 이번 아카이브 범위를 명확히 하고(소스 1개), 보고서 작성 시 “자료 범위”를 투명하게 설명할 수 있음.

6) `instruction/20260112.txt`  
- **이유**: 사용자가 준 인스트럭션(수집 소스가 MS PDF 1개임)을 확인해 **보고서의 한계/범위**를 명시할 때 도움.

7) `archive/_job.json`  
- **이유**: 다운로드 옵션, 날짜, query_id 등 메타를 확인해 “언제/어떻게 수집된 자료인지” 간단히 기록 가능.

8) `archive/_log.txt`  
- **이유**: 수집/변환 성공 로그 확인(재현성/결함 여부 체크).

(현재 파일이 총 6개뿐이라, 실질적으로는 위 1~3이 “콘텐츠 독해”의 전부이고 나머지는 메타 확인용입니다.)

---

## 추천 읽기/작성 플랜(자연스러운 한국어 ‘번역+리뷰’ 목적에 맞춘 순서)

1. **텍스트본 전체 훑기**: `archive/web/text/Microsoft-AI-Diffusion-Report-2025-H2.txt`  
   - 핵심 메시지(확산 증가 vs 격차 확대), 케이스 스터디 2개(South Korea, UAE, DeepSeek)의 논리 연결을 표시.

2. **PDF로 도표/표 확인**: `archive/web/pdf/Microsoft-AI-Diffusion-Report-2025-H2.pdf`  
   - “Global North/South 수치”, “Top 30 랭킹 변화”, “DeepSeek market share” 같은 시각자료를 보고 문장으로 자연스럽게 풀어쓰기.

3. **References 기반으로 ‘근거 문장’ 보강**: (같은 txt 파일의 References 섹션)  
   - 번역문이 단순 전달로 끝나지 않게, “어떤 자료를 근거로 삼는지”를 짧게 짚고 해석을 덧붙이는 방식으로 구성.

4. **Tavily 추출본으로 누락/오탈자 교차검증**  
   - 텍스트 변환 과정에서 끊긴 문장(특히 페이지 전환부)을 보완.

원하시면, 다음 단계로는 제가 위 텍스트를 기준으로 **섹션별 한국어 심층 번역+설명형 리뷰 구조(요약-근거-해석 흐름)**에 맞춰 실제 보고서 원고(템플릿 nature_journal 톤)로 재구성할 때, 어떤 목차가 자연스러운지도 함께 잡아드릴 수 있어요.