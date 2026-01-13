## 1) 1차 논문(PDF/추출텍스트): Nature Communications — *High aspect ratio organic light-emitting diodes* (2025)
- **서지/URL**
  - DOI/원문 PDF: https://doi.org/10.1038/s41467-025-67312-4 (PDF: https://www.nature.com/articles/s41467-025-67312-4_reference.pdf) [`archive/web/text/s41467-025-67312-4_reference.txt`]
- **해결하려는 문제(조명용 OLED의 본질적 트레이드오프)**
  - 조명용 OLED는 **수명이 휘도에 역비례**하고, 조명은 디스플레이보다 **대략 10배 높은 휘도**를 요구하여 수명/효율 목표 달성이 어렵다고 명시 [`archive/web/text/s41467-025-67312-4_reference.txt`].
- **핵심 아이디어(기술 인플렉션 포인트 후보 #1: “패널 대비 발광 활성면적” 증가로 전류밀도↓)**
  - **sub‑mm 고종횡비(high aspect ratio) 표면 텍스처**(삼각 코루게이션) 위에 OLED를 형성해 **패널 면적당 활성 OLED 면적을 증가**시키고, 동일 패널 휘도에서 **필요 전류밀도(current density)를 감소**시키는 전략 제시 [`archive/web/text/s41467-025-67312-4_reference.txt`].
  - 면적 증대(Area enhancement, **AE**)를 **AE ≡ A_dev/A_pan = √(1 + (2β)^2)**로 정의(β=h/w)하며, 이론적으로 동일 조건이면 전류밀도 감소가 AE에 비례함을 설명 [`archive/web/text/s41467-025-67312-4_reference.txt`].
- **정량 결과(직접 인용 가능한 수치)**
  - **AE 최대 1.4×**까지(표준 **VTE** 증착 장비로) 코루게이션 기판에서 **두께 균일도**를 확보했다고 보고 [`archive/web/text/s41467-025-67312-4_reference.txt`].
  - 평탄(plane) 대비, 동일 패널 전류밀도에서 **동작 수명 2.7배 증가(2.7‑fold)** 및 **외부 광추출 효율 최대 40% 증가(up to 40%)**를 보고 [`archive/web/text/s41467-025-67312-4_reference.txt`].
  - 녹색 고종횡비 디바이스는 **면적+아웃커플링(outcoupling) 개선 결합**으로 평탄 대비 **동일 휘도에서 전류밀도 절반 이하**로 달성 가능하다고 기술 [`archive/web/text/s41467-025-67312-4_reference.txt`].
- **제조/스케일업 관련 근거(상업 채택 갭 분석에 유용)**
  - 공정: 기판은 **PDMS 몰드 + UV 경화 에폭시 복제 몰딩**, 이후 **ITO는 RF 스퍼터**, 나머지 스택은 **VTE**로 적층 [`archive/web/text/s41467-025-67312-4_reference.txt`].
  - VTE의 방향성으로 인해 로컬 증착각이 변하므로 **유기층/캐소드 명목 두께를 AE만큼 보정(증가)**해야 평탄과 동일한 로컬 두께를 유지할 수 있다고 명시 [`archive/web/text/s41467-025-67312-4_reference.txt`].
  - 활성영역 대부분인 facet 기준, 두께 변동(표준편차/평균)이 **5% 미만**이라고 보고(균일도 근거) [`archive/web/text/s41467-025-67312-4_reference.txt`].
  - **AE2.0 디바이스는 재현성이 낮고 빠르게 실패**했다고 언급(공정창 한계/리스크 근거) [`archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt`].
- **산업적 함의(신뢰도 높은 포인트)**
  - 저자 소속에 **OLEDWorks LLC**가 포함(조명/패널 산업과의 연결 시사) [`archive/web/text/s41467-025-67312-4_reference.txt`].

---

## 2) OpenAlex 메타데이터(원문 일부 포함): OLED 트렌드 후보 맵
### 2-1. Blue emitter/디스플레이 핵심 이슈(원문 부재 — “추가 확보 필요 근거”)
- **Perspective: OLED Displays Singing with the Blues** (Advanced Materials, 2025-12-26)
  - DOI: https://doi.org/10.1002/adma.202519327 [`archive/openalex/works.jsonl`]
  - 주장 요지(초록 기반):
    - 디스플레이에서 **blue 픽셀이 전력의 ~50%**를 소비하며, **deep-blue PHOLED**의 안정성 문제로 상용 채택이 지연되었다고 서술.
    - 분자설계, graded doping, triplet radiative lifetime 감소(광학적 DOS 증가), outcoupling 등을 결합해 **deep blue PHOLED 수명이 green에 근접**하고 있다고 주장.
    - 문헌 내 **양자효율/수명 측정의 지속적 문제**를 지적(재현성/표준화 이슈) [`archive/openalex/works.jsonl`].
  - **갭**: PDF가 아카이브에 없어 정량 수치/표준 논쟁의 원문 근거는 추가 확보 필요.

### 2-2. 제조 전환(잉크젯 프린팅)(원문 부재 — “추가 확보 필요 근거”)
- **Research Progress on the Preparation of OLED Based on the Inkjet Printing** (Advanced Optical Materials, 2025-12-31)
  - DOI: https://doi.org/10.1002/adom.202502807 (PDFDirect 링크 메타 포함) [`archive/openalex/works.jsonl`]
  - 요지(초록 기반):
    - 열증착 기반 대면적 균일 제조의 비용/복잡성이 장애이며, **inkjet printing(IJP)**이 **비접촉, 재료 이용률↑, roll‑to‑roll 호환**으로 대면적 제조 유력 후보라고 정리 [`archive/openalex/works.jsonl`].
  - **갭**: 실제 수율/결함/수명 정량 데이터는 원문 PDF 확보가 필요.

### 2-3. Stretchable OLED(원문 텍스트 존재, 다만 저널/인용지표 상 신뢰도 주의)
- **Recent Progress in Stretchable OLED Design and Applications** (Academic Journal of Science and Technology, 2025-12-28)
  - Landing/다운로드: https://drpress.org/ojs/index.php/ajst/article/download/33002/32289 [`archive/openalex/works.jsonl`]
  - 기술 분류(리뷰 요약):
    - **Laser‑programmed buckling**, **island‑bridge 구조(bridge 변형 설계)**, **intrinsically stretchable materials** 3가지 접근을 제시 [`archive/openalex/text/W7117787413.txt`].
  - 정량 주장(리뷰가 인용한 개별 연구 결과로 제시):
    - buckling 기반 사례에서 **0/40/70% strain에서 효율 72.5/68.5/70.0 cd A⁻¹**, **100% tensile strain**, **15,000회 stretch‑release 사이클** 등 수치를 언급 [`archive/openalex/text/W7117787413.txt`].
  - **주의**: OpenAlex 메타에서 cited_by_count=0이며, 저널/저자 소속도 학술 메이저 저널 대비 약하므로 핵심 의사결정 근거로 쓰기 전 **원출처 역추적** 필요 [`archive/openalex/works.jsonl`].

### 2-4. 산업/시장(컨설팅 리포트 메타 수준)
- **OLED TDDI Market Overview** (Zenodo, Next Move Strategy Consulting, 2025-12-09)
  - DOI: https://doi.org/10.5281/zenodo.17862627 및 https://doi.org/10.5281/zenodo.17862628 [`archive/openalex/works.jsonl`]
  - 메타 요지:
    - OLED TDDI 시장이 **2023년 97.7억 달러 → 2030년 153.8억 달러(CAGR 6.7%)** 전망, 박형/경량 통합 솔루션 수요를 강조 [`archive/openalex/works.jsonl`].
  - **한계**: “전체 리포트는 외부 링크에서 접근” 형태로, 아카이브 내에 본문 근거(PDF)가 없어 인용 시 주의.

---

## 3) Tavily Search(웹 2차 소스 요약): 배경/상업 채택 지연 근거(보조)
- **U.S. Department of Energy — OLED Basics**
  - URL: https://www.energy.gov/eere/ssl/oled-basics [`archive/tavily_search.jsonl`]
  - 핵심:
    - OLED는 면광원(diffuse-area)이며, **일반 조명에서의 광범위 채택이 아직 어려운 이유로 “높은 비용(high cost)”**을 명시(“still some years away… largely due to their high cost”) [`archive/tavily_search.jsonl`].
- **OLED-Info — An introduction to OLED displays**
  - URL: https://www.oled-info.com/oled-introduction [`archive/tavily_search.jsonl`]
  - 핵심:
    - OLED 조명은 균일 면광원/유연성 등 장점이 있으나 **mass production에 아직 도달하지 못했고**, **주로 automotive 등 니치 채택**이 증가 중이라고 서술 [`archive/tavily_search.jsonl`].
- (참고) Wikipedia 등 일반 개론 소스는 포함되어 있으나, 본 보고서의 “증거 가중(evidence-weighted)” 목적상 **보조 배경** 정도로만 적합 [`archive/tavily_search.jsonl`].

---

## 4) 오프토픽/제외 권고 근거(스코프 관리)
- 인스트럭션에 “quantum computing” 쿼리가 포함되어 OpenAlex 결과에 **Quantum Computing** 문헌들이 섞여 있으나, OLED 기술 트렌드 보고서 초점과 불일치하므로 제외가 타당 [`instruction/20260104_oled.txt`, `archive/openalex/works.jsonl`].
- LinkedIn URL 1건이 수집되어 있으나(분자설계 AI), 현재 아카이브 근거만으로는 OLED 소재/소자와의 직접 연결 고리가 약해 핵심 근거로 쓰기 어려움(필요 시 부록 수준) [`instruction/20260104_oled.txt`, `archive/20260104_oled_01-index.md`].