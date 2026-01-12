업데이트된 Plan(완료 표시 + 누락 단계 보강):

- [x] 수집 범위/메타 고정 — `instruction/20260112.txt`, `archive/...-index.md`, `_job.json`, `_log.txt`로 공식 URL·파일 구성·수집 조건을 확인하고 보고서 서지정보를 정리  
- [x] (보강) 1차 소스 범위 확정 — 본 런의 1차 소스는 **PDF 1건**(Microsoft Research URL)이며, web/text는 해당 PDF에서 추출된 텍스트임을 명시(보조 근거는 supporting/web_extract로만 사용)  
- [ ] 본문 구조 스캔 — `archive/web/text/Microsoft-AI-Diffusion-Report-2025-H2.txt`를 훑어 섹션 흐름(요약→지표→지역/국가→사례→결론)을 잡고 핵심 주장 지도를 만든다  
- [ ] (추가) 인용 위치 체계 확정 — **TXT는 줄번호(line)**, **PDF는 페이지(page)**로 병기하는 규칙을 확정한다(최종 보고서 표기 통일 목적)  
- [ ] 근거 문장·수치 발췌 — 핵심 주장별로 원문 문장(영문)과 페이지/위치, 관련 수치·랭킹·정의 문구를 함께 뽑아 인용 후보 리스트를 만든다  
- [ ] (추가) 용어/범주 정의 표준화 — Global North/South, working-age population, AI diffusion 등 **핵심 용어 한국어 번역어**를 고정하고 문서 전반에 일관 적용  
- [ ] PDF 기반 figure 후보 선정 — `archive/web/pdf/...pdf`에서 메시지를 강화하는 표/지도/그래프 2~3개를 페이지 번호+캡션 원문으로 기록하고 본문 연결 포인트를 메모한다  
- [ ] 텍스트 교차검증 — `web/text` vs `tavily_extract`/`supporting/web_extract`를 대조해 끊긴 문장·깨진 표·고유명사/수치 오탈자를 수정하고 “최종 인용 문장”을 확정한다  
- [ ] 템플릿 아웃라인 확정 — `nature_journal` 구성(초록–Main Findings–Methods–Discussion–Outlook)에 맞춰 한국어 서술형 리뷰 목차와 각 절의 “요약-근거-해석” 작성 규칙을 고정한다  
- [ ] 초안 작성 및 그림 삽입 — 섹션별로 심층 번역+해설을 작성하고, figure는 캡션(영문 원문+한국어 설명)과 함께 적절한 위치에 배치한다  
- [ ] (추가) 한계/주의사항 박스 작성 — telemetry 기반 사용률 지표의 해석 한계(“1회 사용 vs 업무 통합” 등)를 별도 박스로 정리(3자 요약은 보조로만)  
- [ ] 최종 정리/검증 — 문체(자연스러운 전환, 과도한 학술체 배제) 다듬기, 출처·페이지 표기 통일, 수치/고유명사 재점검 후 최종 보고서로 출력한다