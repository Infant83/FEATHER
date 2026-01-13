## 아카이브 맵(coverage 요약) — 20260104_oled
- **리포트 포커스 요구사항**(OLED 트렌드/소재/산업 함의, 3–5 기술 변곡점, 연구 vs 상용화 비교, 모순·갭·추가질문)에 비해, 현 아카이브는 **실질적으로 1편의 핵심 논문 + 일반 검색 인덱스** 중심으로 커버리지가 매우 얕습니다.
- **수집 채널 상태**
  - OpenAlex: **비활성화(openalex_enabled=false)** → OA 저널/리뷰 논문 확장 수집이 막혀 있음
  - arXiv: 힌트는 있으나 실제 recent search는 **‘quantum computing’만 수행**되어 OLED arXiv 0건
  - YouTube: 비활성화
- **실제 주요 근거로 쓸 만한 1차 소스는 Nature Communications 논문 1건**이 거의 전부입니다. LinkedIn은 OLED 직접 근거로는 약함.

---

## 구조화 인벤토리(관련도 중심)

### A) 런/작업 메타(커버리지 진단용)
- `archive/_job.json`  
  - 쿼리/설정/활성화 채널 확인. **queries에 ‘quantum computing’, ‘recent 30 days’가 포함**되어 포커스가 희석.
- `archive/_log.txt`  
  - 실제 실행된 검색/추출 로그. **ARXIV RECENT SEARCH가 quantum computing만** 찍힘(원인 추적 핵심).
- `archive/20260104_oled-index.md`  
  - “Queries: 3 | URLs: 2 | arXiv IDs: 0” 등 런 결과 요약 목차.

### B) 인덱스(JSONL) — 추가 읽을 출처 “선별”용
- `archive/tavily_search.jsonl`  
  - tavily 검색 결과 전체 인덱스. 다수는 Wikipedia/기관 기초설명 성격이라 **트렌드·소재·제조 이슈에 직접 연결되는 결과만 골라야 함**.

### C) 본문(추출 텍스트) — 실제 “증거” 소스
- `archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt`  
  - **Nature Communications (2025)**: *High aspect ratio organic light-emitting diodes* (Wang et al.)  
  - 조명용 OLED의 **수명-휘도/전류밀도 트레이드오프**를 “고종횡비 텍스처(면적증대+outcoupling)”로 완화.  
  - 정량 근거: **수명 2.7x**, **외부 광추출 효율 최대 +40%**, **표준 VTE 공정에서 AE 1.4까지**, 두께 변동 **<5%**, **AE2.0은 재현성 낮고 빠른 실패**.
- `archive/tavily_extract/0001_https_www.linkedin.com_posts_...txt`  
  - 분자설계 AI(Trio) 소개로 **OLED 직접 증거는 없음**(보조적 맥락 정도).

---

## 우선순위 “읽기 계획”(max 12) + 선정 이유
1) **`archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt`**  
   - 이유: 현재 아카이브에서 유일하게 포커스 요구(기술 변곡점, 정량 성능, 제조/재현성 이슈)를 **동시에 충족**하는 1차 논문.

2) **`archive/tavily_search.jsonl`**  
   - 이유: 커버리지가 빈약하므로, 여기서 **상용화/소재 트렌드/제조(inkjet/VTE/OVJP), blue emitter 수명, TADF/hyperfluorescence, tandem, encapsulation, microOLED/QD-OLED** 등으로 이어질 “그나마 쓸 만한” 산업·학술 출처를 선별해야 함.

3) **`archive/_job.json`**  
   - 이유: 왜 OLED 중심 수집이 안 되었는지(쿼리 설계/채널 비활성화) 진단 → 다음 라운드 수집 전략(특히 OpenAlex on) 근거.

4) **`archive/_log.txt`**  
   - 이유: arXiv OLED 0건의 직접 원인 확인(실제로 quantum computing만 arXiv recent search 수행) → 파이프라인/인스트럭션 수정 포인트 도출.

5) **`archive/20260104_oled-index.md`**  
   - 이유: 보고서에 “자료 범위 한계(coverage gap)”를 투명하게 명시할 때 근거로 사용.

6) **`archive/tavily_extract/0001_https_www.linkedin.com_posts_...txt`**  
   - 이유: OLED 직접 근거는 약하지만, “소재 발견 자동화/멀티목표 최적화” 트렌드 문단에 **매우 제한적으로만** 참고 가능(단, 핵심 근거로 쓰기엔 부적절).

---

## 커버리지 갭/모순 포인트(의사결정자용 후속 질문으로 전환 가능)
- **갭:** “OLED 기술 트렌드/소재(청색, TADF/PHOLED, hyperfluorescence), 제조/수율/비용, 디스플레이 상용 로드맵” 관련 1차/산업 소스가 아카이브에 사실상 없음.  
- **모순/불확실성 후보:** 논문은 조명용 OLED에서 AE1.4까지 유효하나, **AE2.0 재현성 실패** → 스케일업/양산에서 텍스처 마스터몰드 결함·공정 윈도우가 병목일 가능성.
- **후속 질문 예시**
  - 고종횡비 텍스처가 **양산 수율/결함 밀도/검사 비용**에 미치는 영향은?
  - 디스플레이(모바일/TV)와 조명용에서 **수명 메커니즘/전류밀도 한계**가 얼마나 다른가?
  - VTE 외 **inkjet/OVJP** 같은 대면적 공정과의 호환성/비용 구조는?

원하시면 `tavily_search.jsonl`에서 “트렌드/소재/제조/산업”에 직접 연결되는 결과만 추려서, **추가 수집해야 할 URL·쿼리 리스트(의사결정자 질문에 매핑)**까지 만들어 드릴 수 있습니다.