업데이트된 Plan(체크 반영 + 누락 단계 보강):

- [x] 리포트 범위·평가기준 확정 — “지난 12개월” 타임윈도/ OLED 발광재료 범주(형광·인광·TADF·CP‑OLED) / 근거강도(논문·리뷰·공식발표·업계자료·PR·supporting) 라벨 규칙 고정  
- [x] 수집 파이프라인 진단 — `archive/_log.txt`, `archive/_job.json`, `archive/*index.md`로 URLs=0 원인(주로 Wiley/ASME/MDPI 403, OpenAlex PDF 편향)과 재수집 필요 포인트 정리  
- [x] Tavily 결과 정독 및 “1차 출처” 역추적 — `archive/tavily_search.jsonl`에서 OLED×QC 직접 단서(IBM/Keio/Mitsubishi 2021, OTI Lumionics 2025 PR, Science.org 논문 등) 추출 및 DOI/공식페이지/PDF 연결 후보 정리  
- [x] OpenAlex 메타데이터 스크리닝 — `archive/openalex/works.jsonl`에서 오프토픽(건축/암/센서 등) 제외, 남는 문헌을 “배경/방법론/응용”으로 재분류(현재 OA PDF 셋은 QC×OLED 직접성 낮음 확인)  
- [x] 핵심 풀텍스트 근거 채굴 — `openalex/text/*.txt` 중 2~3건 선독해(예: Nature Communications 2025 GNN‑inverse design 워크플로 등)에서 “파이프라인/재현 가능한 서술 근거” 발췌 포인트 확보  
- [x] 산업 파트 증거체계 설계 — 삼성디스플레이/LG디스플레이/UDC “공식 채널 우선순위(특허→학회(SID/IMID)→IR/연차·지속가능→공식 PR)” 체크리스트 + ‘공개정보 한계’ 문장 구조 준비  
- [x] 대표 시나리오 2~3개 구성 — (QC 기반 excited‑state 계산 보조, QC+ML 후보 생성‑필터링, 산업 PoC/파트너십)로 “주장→근거→한계→의미 + 근거강도” 틀 확정  
- [ ] Nature_journal 템플릿 합성/교차검증 — Abstract–Main Findings–Methods–Discussion–Outlook 문단 배치, supporting 인용 분리 원칙을 최종 원고 뼈대에 반영  
- [ ] 추가 수집 대상(URL/DOI) 리스트 확정 — 특히 OTI Lumionics JCTC 논문(원문 DOI/arXiv), Science.org(icomputing.0037) 및 IBM 관련 특허/논문을 “1차 근거 확보용”으로 우선순위화  
- [ ] (추가) ‘지난 12개월’ 범위 내 QC×OLED 직접 근거 부재 여부 최종 확인 및 범위 밖 핵심(예: npj Comp Mater 2021) 인용 처리 규칙(“배경 근거로만 사용” 등) 명문화  
- [ ] (추가) 인용/서지 섹션 구성 — 1차(논문·특허·공식발표) vs supporting(블로그·PR·뉴스) 분리 표(핵심 주장에 supporting 단독 사용 금지 규칙 포함) 생성