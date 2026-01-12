## 지시/인덱스(런 범위·커버리지)
- 이번 런 커맨드/설정: `--days 30 --max-results 8 --download-pdf --openalex --oa-max-results 8 --set-id basic-oa`로 최근 30일 범위에서 Tavily 3개 쿼리+URL 2개를 수집하고 OA(OpenAlex)도 병행 다운로드함. [archive/20260104_basic-oa-index.md]
- instruction 입력(쿼리 혼재): `arxiv`, `oled`, `quantum computing`, `recent 30 days` + URL 2개(LinkedIn, Nature PDF)로 OLED 외 주제가 섞여 들어와 오프토픽 결과가 생길 구조. [instruction/20260104.txt]
- 실제 다운로드된 “학술 PDF”는 2편뿐:
  - Nature Communications (2025) 1편(웹 PDF) [archive/20260104_basic-oa-index.md]
  - “Recent Progress in Stretchable OLED Design and Applications” 1편(OpenAlex PDF, 인용 0) [archive/20260104_basic-oa-index.md]

## 피어리뷰/학술 1차 근거(다운로드된 텍스트 기준)
### Nature Communications (2025) — “High aspect ratio organic light-emitting diodes”
- 서지/원문 링크: https://doi.org/10.1038/s41467-025-67312-4 (reference PDF 기반 텍스트) [archive/web/text/s41467-025-67312-4_reference.txt]
- 문제정의(조명용 OLED의 핵심 트레이드오프):
  - 조명은 디스플레이 대비 “대략 1자릿수(≈10배) 더 높은 휘도”를 요구하며, OLED 효율과 수명은 전류밀도(=휘도 증가) 증가에 따라 저하되어 목표 달성이 어려움. [archive/web/text/s41467-025-67312-4_reference.txt]
- 핵심 아이디어(기술 변곡점 후보: “면적 증강(Area Enhancement) 기반 수명/효율 개선”):
  - sub-mm 스케일의 high aspect ratio 표면 텍스처(삼각 corrugated substrate)에 OLED를 형성해 **패널 면적당 활성 발광 면적을 증가** → 동일 패널 휘도에서 필요한 **전류밀도 감소**. [archive/web/text/s41467-025-67312-4_reference.txt]
  - 면적 증강 계수 정의: \( AE \equiv A_{dev}/A_{pan} = \sqrt{1+(2\beta)^2} \) (β=height/width). [archive/web/text/s41467-025-67312-4_reference.txt]
  - 스케일 선택 논리: 텍스처(10–100 µm)가 OLED 적층 두께보다 충분히 커 “국소적으로 전기적 평면”으로 취급 가능 + 사람 눈의 해상도보다 작아 “공간적으로 균일한 휘도”로 인지. [archive/web/text/s41467-025-67312-4_reference.txt]
- 정량 성능 주장(산업 함의에 직접 연결되는 수치):
  - 표준 VTE(진공열증착)로 corrugated 기판에서 **두께 균일성**을 확보하며 **AE 최대 1.4×**까지 구현. [archive/web/text/s41467-025-67312-4_reference.txt]
  - planar 대비(동일 패널 전류밀도 조건) **동작 수명 2.7× 증가**, **외부 광추출 효율 최대 40% 증가**. [archive/web/text/s41467-025-67312-4_reference.txt]
  - green high aspect ratio 소자는 면적+광추출 향상 결합으로 planar 대비 **“절반 이하 전류밀도”로 동일 휘도** 달성 가능하다고 기술. [archive/web/text/s41467-025-67312-4_reference.txt]
- 제조/상용 관점 포인트(연구 vs 상용 비교에 유용):
  - “표준 thermal evaporator(VTE)”로 구현 가능하다는 서술은 기존 대면적 증착 인프라와의 정합성(상용 적용 가능성)을 시사. [archive/web/text/s41467-025-67312-4_reference.txt]
  - 공저자에 OLEDWorks LLC가 포함(산업 연계 신호). [archive/web/text/s41467-025-67312-4_reference.txt]

### OpenAlex OA PDF — “Recent Progress in Stretchable OLED Design and Applications” (Academic Journal of Science and Technology)
- 소스/다운로드 URL(인덱스에 명시): https://drpress.org/ojs/index.php/ajst/article/download/33002/32289 [archive/20260104_basic-oa-index.md]
- 논문 성격/신뢰도 단서:
  - 저자 소속이 “Shanghai Weiyu international school”, “Ulink College Guangzhou”로 표기(대학/연구기관 기반 리뷰가 아님). [archive/openalex/text/W7117787413.txt]
  - OpenAlex 메타: Citations 0. [archive/20260104_basic-oa-index.md]
- 기술 분류(기술 변곡점 후보: “기계적 변형 대응 구조/재료 플랫폼”):
  - stretchable OLED 접근 3가지로 정리:
    1) Laser-Programmed Buckling Process
    2) 3D height-alternating island-bridge 구조(예: Fold Bridge/Curved Bridge, Serpentine Bridge, Fractal Bridge 언급)
    3) Intrinsically stretchable materials(소자 구성요소 자체를 신축성 재료로) [archive/openalex/text/W7117787413.txt]
- 인용된(2차) 성능 수치 예시(원문 1차 검증 필요):
  - Jilin University 그룹 사례로 “최대 효율 72.5/68.5/70.0 cd A⁻¹(0%/40%/70% strain)”, “최대 100% strain”, “15,000 stretch-release cycles” 등의 수치를 제시. [archive/openalex/text/W7117787413.txt]
  - 다만 이는 리뷰 내 재서술이며, 해당 [5] 원 논문을 추가 확보해 조건/정의(효율 종류, 측정 휘도, 수명 기준)를 검증해야 함. [archive/openalex/text/W7117787413.txt]
- 응용 포커스(근시일 산업 적용처 후보):
  - 헬스케어(심박/산소포화도 모니터링), 웨어러블/가변형 디스플레이, phototherapy 등을 응용 예로 듦. [archive/openalex/text/W7117787413.txt]

## OpenAlex 메타데이터(다운로드되지 않은 핵심 변곡점 후보 풀)
- “블루 OLED” 관점(퍼스펙티브):
  - *Perspective: OLED Displays Singing with the Blues* (Advanced Materials, 2025-12-26), OA status: hybrid, PDF URL 없음. [archive/openalex/works.jsonl]
- “제조 공정 변곡점(잉크젯 프린팅)”:
  - *Research Progress on the Preparation of OLED Based on the Inkjet Printing* (Advanced Optical Materials, 2025-12-31)
  - pdfdirect URL 존재(https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/adom.202502807)지만 이번 런에서는 PDF 미다운로드. [archive/openalex/works.jsonl]
- “광추출/광학 구조(나노텍스처)”:
  - *Nanotextured light modulation for flexible OLEDs with 370% enhanced EQE and angular color stability* (Scientific Reports, 2025-12-23), OA status: gold, PDF URL 필드 비어있음(다운로드 공백). [archive/openalex/works.jsonl]
- “특수 기능 OLED 소재(원형편광/딥블루)”:
  - *Efficient Chiral Ultraviolet and Deep‑Blue Materials for High‑Performance Circularly Polarized OLEDs* (Aggregate, 2025-12-15), Wiley pdfdirect 링크 존재. [archive/openalex/works.jsonl]
- 산업/시장 문서(기술 자체보다는 시장):
  - *OLED TDDI Market Overview* (Zenodo, 2025-12-09) 2건(landing page가 Zenodo/NextMSC로 갈림), PDF URL 없음. [archive/openalex/works.jsonl]
- 오프토픽 혼입(런 설계 이슈의 결과):
  - quantum computing 관련 Zenodo/Communications of the ACM 항목 다수 포함. [archive/openalex/works.jsonl]

## Tavily 검색(산업/기관 관점 — “신뢰 가능한 출처” 위주로만 발췌)
- US DOE(기관) 기본 포인트:
  - OLED는 시트 형태의 확산 면광원이며, LED와 유사한 efficacy/lifetime/color quality 수준의 제품도 일부 있으나 **일반 조명으로의 광범위 확산은 “high cost” 때문에 아직 수년 필요**하다고 명시. (near-term 산업 함의: 비용장벽) [archive/tavily_search.jsonl]
  - URL: https://www.energy.gov/eere/ssl/oled-basics [archive/tavily_search.jsonl]
- LG Display(기업 기술 소개):
  - OLED 구조 개요(자발광, HIL/HTL/EML/ETL/EIL, encapsulation 등) 및 “self-emissive, no backlight” 메시지. (정량 수치/제조 데이터는 부족) [archive/tavily_search.jsonl]
  - URL: https://www.lgdisplay.com/eng/technology/oled [archive/tavily_search.jsonl]
- OLED-Info(산업 허브/미디어 성격):
  - OLED 조명은 아직 대량생산/주류 채택이 제한적이나, **automotive 중심의 niche adoption**이 증가 중이라는 서술. (near-term 적용처 힌트) [archive/tavily_search.jsonl]
  - URL: https://www.oled-info.com/oled-introduction [archive/tavily_search.jsonl]

## 오프토픽/저우선 소스(스킵 또는 주의)
- Tavily 결과 중 “quantum computing”, “recent 30 days 날짜 계산” 등은 OLED 리포트 포커스와 무관. [archive/tavily_search.jsonl]
- instruction에 포함된 LinkedIn URL은 OLED 핵심 트렌드/재료·구조 혁신 근거로는 약할 가능성이 큼(현 단계 근거 추출 생략). [instruction/20260104.txt]