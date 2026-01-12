## 1) 아카이브/런 설정·커버리지(진단 근거)

- **수집 결과 요약(인덱스)**: 실행 범위 “last 365 days”로 설정되었으나, 인덱스에 **Queries 9 | URLs 0 | arXiv IDs 0**로 기록됨. OpenAlex PDF 7편만 남아 있고 웹 URL 수집이 “0”으로 표시됨.  
  - 근거: `archive/20260110_qc-oled-index.md` [archive/20260110_qc-oled-index.md]

- **URLs=0 원인(파이프라인 관점)**: OpenAlex PDF 다운로드 과정에서 **Wiley/ASME/MDPI 등 여러 도메인이 403 Forbidden으로 실패**. 결과적으로 OA/PDF 직접 링크가 가능한 일부만 남았고, OLED×양자컴퓨팅 직접 문헌은 OpenAlex PDF 셋에 거의 포함되지 못함.  
  - 근거: `archive/_log.txt`에 Wiley/ASME/MDPI 403 에러 로그 다수 [archive/_log.txt]

- **질의 설계(의도)**: OLED 발광재료 산업 적용을 겨냥해 삼성/LG/UDC site: 검색 및 “quantum algorithms… OLED phosphorescent TADF emitters” 등의 쿼리가 포함됨.  
  - 근거: `instruction/20260110.txt` [instruction/20260110.txt]

---

## 2) (핵심 1차) 학술 논문/저널 페이지에서 확보되는 “OLED×양자컴퓨팅” 직접 근거

### npj Computational Materials (2021) — OLED TADF emitter excited-state를 QC로 계산
- **주장(논문 초록 수준의 사실)**: phenylsulfonyl-carbazole 계열 TADF 후보의 *S1/T1* excited state를 **qEOM‑VQE, VQD**로(시뮬레이터 및 실제 디바이스에서) 계산했고, **ΔE_ST 예측이 실험과 “excellent agreement”**라고 서술.  
- **워크플로/데이터 파이프라인 단서**: double‑zeta basis, active space를 HOMO/LUMO로 제한. **에러 미티게이션 전후**에서 디바이스 결과 오차(예: 17/88 mHa → tomography 기반 정제로 최대 4 mHa) 개선을 보고.  
- **출처(원문 URL)**: https://www.nature.com/articles/s41524-021-00540-6  
- **근거 위치**: 논문 페이지의 Abstract에 위 내용이 직접 기재됨 [supporting/20260112_223853/web_extract/004_nature.com_articles_s41524-021-00540-6-6c0c1677.txt]

> 비고: “지난 12개월” 범위 밖(2021)이지만, 아카이브 내에서 **OLED×양자컴퓨팅 직접 적용**을 가장 명확히 기술한 1차 출처로 확인됨.

---

## 3) (학술적 방법론 보조) OpenAlex로 수집된 논문 PDF/텍스트에서의 관련 근거

### Nature Communications (2025) — “재료/분자 탐색 파이프라인” 관점(양자컴퓨팅 직접은 아님)
- **주장(논문 서술)**: GNN property predictor를 “invertible”하게 활용하여 **원하는 전자적 물성(예: HOMO‑LUMO gap)**을 목표로 **molecular graph 자체를 gradient ascent로 최적화**하여 분자를 생성.  
- **검증 파이프라인**: 생성 분자의 목표 물성을 **DFT로 검증**, 그리고 **1617개 신규 분자+DFT 물성 데이터셋**을 생성했다고 서술.  
- **OLED 직접 언급/양자컴퓨팅 직접 연결**: 제공된 본문 발췌 범위에서는 OLED/양자컴퓨팅 직접 적용은 확인되지 않음(‘계산-생성-검증’ 워크플로 참고용).  
- **출처(원문 URL)**: https://doi.org/10.1038/s41467-025-59439-1 (PDF: https://www.nature.com/articles/s41467-025-59439-1.pdf)  
- **근거 위치**: 논문 서론/방법 개요에서 workflow 및 DFT 검증, HOMO‑LUMO gap targeting이 명시됨 [archive/openalex/text/W4410193211.txt]

---

## 4) (Supporting: 웹/보도자료/블로그) OLED×양자컴퓨팅 “산업/협업” 단서

### IBM Research 블로그 — “Unlocking today’s quantum computers for OLED applications”(2021 연구 소개)
- **주장(블로그 서술)**: Mitsubishi Chemical(Keio Q Hub의 IBM Quantum Innovation Center 멤버)과 IBM/Keio/JSR 협업으로 **TADF emitter 후보(phenylsulfonyl‑carbazole) excited states를 QC로 계산**했다고 소개하며, 해당 preprint가 **npj Computational Materials(2021-05-20)로 출판**되었다고 명시.  
- **출처(원문 URL)**: https://research.ibm.com/blog/quantum-for-oled  
- **근거 위치**: Tavily 결과에 블로그 본문 요약/인용이 포함(“excited states… could potentially be used… efficient OLED devices”, “Update: … published… May 20, 2021”) [archive/tavily_search.jsonl]

### IBM Newsroom(archive) — 기업 커뮤니케이션 형태의 요약
- **주장(뉴스룸 서술)**: Keio University Q Hub 연구가 OLED 재료의 excited states를 다루며, **IBM Quantum 20‑qubit computers**를 사용했다는 요약.  
- **출처(원문 URL)**: https://newsroom.ibm.com/archive-IBM-research?item=32320  
- **근거 위치**: Tavily 결과 요약에 “IBM Quantum 20-qubit computers” 및 OLED excited-states study가 직접 언급됨 [archive/tavily_search.jsonl]

### Mitsubishi Chemical(문서 PDF, 보도자료 성격) — “world-first” 주장 포함
- **주장(문서 서술)**: npj Computational Materials 게재 사실과 함께, noisy QC에서의 **error mitigation scheme**으로 excited-state 계산 정확도를 개선했고, “commercial materials”에 대해 excited-state 계산에 QC 적용이 **world-first**라는 취지의 문구가 포함.  
- **출처(원문 URL)**: https://www.mcgc.com/english/news_mcc/2021/__icsFiles/afieldfile/2021/05/26/qhubeng.pdf  
- **근거 위치**: Tavily 결과에 해당 PDF의 핵심 문구가 인용됨 [archive/tavily_search.jsonl]

### OTI Lumionics 보도자료(2025-06-18, GlobeNewswire) — “OLED 응용/납품” 등 강한 산업 주장(검증 필요)
- **주장(보도자료 서술)**: “quantum computing… materials design pipelines… especially for OLED applications”을 강조하며, JCTC 논문(“Optimization of the Qubit Coupled Cluster Ansatz on classical computers”)을 발표했다고 소개. 또한 “OLED displays developed using its platform”을 **leading display manufacturers에 deliver** 중이라고 서술.  
- **출처(원문 URL)**: https://www.globenewswire.com/news-release/2025/06/18/3101674/0/en/OTI-Lumionics-Releases-Breakthrough-Algorithms-for-Quantum-Chemistry-Simulations.html  
- **근거 위치**: Tavily 결과 본문/요약에 위 문구가 직접 포함됨 [archive/tavily_search.jsonl]  
- **주의(근거 강도)**: 보도자료/자사 PR이므로 “납품/상용 적용” 주장 자체는 **추가 1차 근거(논문 원문, 특허, 고객사 발표 등) 없이는** 강하게 단정하기 어려움.

---

## 5) (Supporting: 인물/조직 페이지) 연구그룹/출력(논문·특허) 단서

### IBM Research People: Gavin Jones (연구그룹/출력 목록)
- **사실(프로필 서술)**: “Quantum Applications group focused on Chemistry and Materials”의 매니저로 소개.  
- **특허 단서**: “System-based Extension Of Qeom Algorithm For Quantum Computation Of Excited-state Properties” (Google Patents 링크) 항목이 포함.  
- **출처(원문 URL)**: https://research.ibm.com/people/gavin-jones  
- **근거 위치**: 프로필 텍스트에 연구그룹 설명, 특허/출판 목록이 기재 [supporting/20260112_223853/web_extract/001_research.ibm.com_people_gavin-jones-7499a743.txt]

---

## 6) 산업계(삼성디스플레이/LG디스플레이/UDC) 관련: “공개 정보 한계”에 대한 아카이브 내 증거

- 본 런의 질의에 삼성/LG/UDC 및 site:samsung.com/lgdisplay.com/udc.com이 포함되어 있으나, 결과적으로 **수집된 ‘직접 1차 문헌/공식 발표’가 아카이브에 남아있지 않음**(URLs=0, OpenAlex PDF도 해당 기업 관련 문헌이 사실상 없음).  
  - 근거: 인덱스에 URLs 0로 기록 [archive/20260110_qc-oled-index.md]  
  - 근거(간접): 실행 로그에서 기업 쿼리들은 수행되었으나, OpenAlex PDF는 주제 비관련 문헌 위주로 다운로드됨 [archive/_log.txt]  
  - 해석: “공개 채널에서 ‘OLED 발광재료 개발에 양자컴퓨팅을 적용’했다는 기업 공식자료”는 최소한 본 수집 파이프라인/기간/접근 범위 내에서 **발견·확보가 어렵거나 접근 제한(403 등)으로 누락**된 정황.

---

원하시면, 위 supporting 항목(OTI Lumionics JCTC 논문/IBM‑Keio‑Mitsubishi 협업)의 **실제 1차 논문 DOI/PDF(특히 JCTC/arXiv 원문)**를 아카이브에 추가로 당겨올 수 있도록, “추가 수집 대상 URL/DOI 리스트”만 따로 뽑아드릴 수도 있습니다.