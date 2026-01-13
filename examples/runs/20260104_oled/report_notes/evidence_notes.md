## 런/아카이브 메타(커버리지·신뢰도 진단)

- **아카이브 요약(범위 한계 명시 근거)**  
  - “Queries: 3 | URLs: 2 | arXiv IDs: 0”로, OLED 트렌드/소재/산업 함의를 다루기엔 수집량이 매우 제한적임. [archive/20260104_oled-index.md]  
  - 실행 커맨드/입력 지시서 경로가 기록되어 재현 가능. [archive/20260104_oled-index.md]

- **채널 비활성/포커스 희석의 직접 근거**  
  - `openalex_enabled=false`, `youtube_enabled=false`로 OA 저널/리뷰·영상 채널 확장이 막혀 있음. 또한 queries에 `"oled"`, `"quantum computing"`, `"recent 30 days"`가 함께 들어가 포커스가 희석됨. [archive/_job.json]  
  - 로그에서 Tavily search는 3개 쿼리 모두 수행되었지만, **“ARXIV RECENT SEARCH: query='quantum computing' days=30”만 실행**되어 OLED 관련 arXiv 수집이 0건이 된 정황이 확인됨. [archive/_log.txt]

---

## 1차 논문(PDF 추출 텍스트) — OLED 기술 변곡점/정량 근거

- **Nature Communications (2025), “High aspect ratio organic light-emitting diodes” (Wang et al.)**  
  - **문제정의(조명용 OLED의 구조적 난제):** 조명용은 디스플레이 대비 “order of magnitude higher luminance”가 필요하며, **효율·수명이 전류밀도/휘도 증가에 따라 감소**해 목표 수명 달성이 어렵다고 설명. [https://www.nature.com/articles/s41467-025-67312-4_reference.pdf] [archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt]  
  - **핵심 레버(기술 변곡점 후보):** “sub-mm, high aspect ratio surface texture”로 **패널 면적 대비 발광 ‘유효 소자 면적’을 증가(AE)**시켜, 동일 패널 휘도를 더 낮은 전류밀도로 달성하는 전략 제시. [https://www.nature.com/articles/s41467-025-67312-4_reference.pdf] [archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt]  
  - **정량 성과(효율·수명):** 평면 대비 **operating lifetime 2.7배**, **external light extraction efficiency 최대 40% 증가**를 보고. [https://www.nature.com/articles/s41467-025-67312-4_reference.pdf] [archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt]  
  - **제조/양산 관점 포인트(연구 vs 상용화 연결):**
    - 표준 **VTE(진공 열증착)**로 **AE 최대 1.4x**까지 “good thickness uniformity” 확보했다고 명시. [https://www.nature.com/articles/s41467-025-67312-4_reference.pdf] [archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt]  
    - 유기층 두께 균일도: facet 중심으로 **두께 변동(표준편차/평균) < 5%**라고 보고. [https://www.nature.com/articles/s41467-025-67312-4_reference.pdf] [archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt]  
    - **재현성/신뢰성 경고 신호:** “Functional AE2.0 devices… tended to fail quickly and were not reproducible.” 즉, **AE를 더 키우면(고종횡비) 조기 실패·재현성 문제가 병목**이 될 수 있음을 스스로 인정. [https://www.nature.com/articles/s41467-025-67312-4_reference.pdf] [archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt]  
    - 결함 민감도: AE1.1에서 “many dark spots… attributed to… defects in the master mold”로 **마스터 몰드 결함이 광학/균일도 결함으로 직결**됨을 시사. [https://www.nature.com/articles/s41467-025-67312-4_reference.pdf] [archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt]

---

## 웹 검색 인덱스(Tavily Search) — 추가 근거 후보(단, 현재 아카이브에는 ‘검색 결과 요약’ 수준)

- **U.S. Department of Energy, “OLED Basics”**  
  - OLED는 “diffuse-area light sources”, LED와 비교해 “widespread use… largely due to their high cost”라고 언급(조명 상용화 지연의 비용 요인). [https://www.energy.gov/eere/ssl/oled-basics] [archive/tavily_search.jsonl 내 해당 결과 요약]

- **OLED-Info, “An introduction to OLED displays” (Last updated 13/06/2025)**  
  - OLED 조명은 “haven't yet managed to reach mass production… niche applications, mainly automotive, is on the rise”라고 기술(니치/자동차 중심 채택). [https://www.oled-info.com/oled-introduction] [archive/tavily_search.jsonl 내 해당 결과 요약]

- (참고) Wikipedia 등 기초 설명성 출처 다수 포함 — 트렌드/소재/제조 이슈의 1차 근거로는 한계. [archive/tavily_search.jsonl]

---

## SNS/2차(맥락) — 직접 OLED 근거는 약함

- **LinkedIn post: “Trio Framework Addresses Molecular Design Challenges”**  
  - 분자 설계 AI의 구조적 과제(유효성, 합성가능성, 다목적 최적화, 해석가능성)와 “Trio” 프레임워크를 소개하나, **OLED/발광재료/제조 트렌드에 대한 직접 증거는 없음**(소재 탐색 자동화 ‘맥락’으로만 제한적으로 사용 가능). [https://www.linkedin.com/posts/fanli_ai-molecular-design-has-some-known-challenges-activity-7406324682192441344-60n3?utm_source=share&utm_medium=member_desktop&rcm=ACoAADrVxc4BEqb4PF0MiiEBRbbQJ7tfp6CkF3Q] [archive/tavily_extract/0001_https_www.linkedin.com_posts_fanli_ai-molecular-design-has-some-known-challenges-activity-7406324682192441344-60n3_utm_s.txt]