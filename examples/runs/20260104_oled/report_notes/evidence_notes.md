## 1) 인덱스/설정(런 커버리지·제약) 근거

- 이번 런은 **Queries 3개, URLs 2개, arXiv IDs 0개**로 기록됨. 또한 Tavily search/extract 산출물 경로가 명시됨.  
  - 근거: `archive/20260104_oled-index.md`에 “Queries: 3 | URLs: 2 | arXiv IDs: 0” 및 Tavily 파일 목록 기재. [ /C:/Users/angpa/myProjects/FEATHER/examples/runs/20260104_oled/archive/20260104_oled-index.md ]

- Instruction(입력 지시문)에는 `arxiv`, `oled`, `quantum computing`, `recent 30 days`가 함께 포함되어 있고, URL 2개(LinkedIn, Nature Communications PDF)가 지정됨.  
  - 근거: `instruction/20260104_oled.txt` 원문 라인. [ /C:/Users/angpa/myProjects/FEATHER/examples/runs/20260104_oled/instruction/20260104_oled.txt ]

- 파이프라인 설정상 **OpenAlex/YouTube가 비활성화(openalex_enabled=false, youtube_enabled=false)** 되어 있어 “논문/저널” 커버리지가 구조적으로 제한됨. 또한 `query_specs`에 arXiv 힌트가 걸려 있으나 `arxiv_ids`는 빈 배열임.  
  - 근거: `archive/_job.json`의 `openalex_enabled:false`, `youtube_enabled:false`, `arxiv_ids:[]`. [ /C:/Users/angpa/myProjects/FEATHER/examples/runs/20260104_oled/archive/_job.json ]

- 로그상 arXiv recent search가 **‘quantum computing’에 대해서만 수행**됨(‘oled’로 arXiv recent search 수행 기록 없음).  
  - 근거: `archive/_log.txt`에 “ARXIV RECENT SEARCH: query='quantum computing' days=30” 기록. [ /C:/Users/angpa/myProjects/FEATHER/examples/runs/20260104_oled/archive/_log.txt ]


## 2) Tavily 검색 결과(출처 성격·오프토픽) 근거

- `oled` 검색 결과 상위는 Wikipedia, OLED-Info, DOE(energy.gov), Ossila 등 **개론/설명형**이 중심으로 나타남(산업 리포트/학회 프로시딩/시장조사 등 “의사결정용 정량 비교” 소스는 상위에 보이지 않음).  
  - 근거: `archive/tavily_search.jsonl`의 `query="oled"` 결과 URL/요약에 Wikipedia/OLED-Info/DOE/Ossila 등이 포함. (실제 원문은 각 URL)  
    - https://en.wikipedia.org/wiki/OLED  
    - https://www.oled-info.com/oled-introduction  
    - https://www.energy.gov/eere/ssl/oled-basics  
    - https://www.ossila.com/pages/what-is-an-oled  
  - [ /C:/Users/angpa/myProjects/FEATHER/examples/runs/20260104_oled/archive/tavily_search.jsonl ]

- `recent 30 days` 검색은 **OLED와 무관한 뉴스/유틸리티/기타 페이지**가 다수로 잡혀, 쿼리 오염(범위 불명확) 문제가 확인됨.  
  - 근거: `archive/tavily_search.jsonl`의 `query="recent 30 days"` 결과에 avian flu 기사, 날짜 계산기, IMDb 등 포함. (실제 원문은 각 URL)  
    - https://healthpolicy-watch.news/as-more-us-dairy-herds-infected-with-avian-flu-americans-in-the-dark-on-the-risks-of-raw-milk/  
    - https://www.inchcalculator.com/days-from/30-days-ago-from-today/  
    - https://www.imdb.com/title/tt19718422/  
  - [ /C:/Users/angpa/myProjects/FEATHER/examples/runs/20260104_oled/archive/tavily_search.jsonl ]


## 3) 오픈액세스 저널(PDF 추출 텍스트) — 핵심 기술 증거(Nature Communications, 2025)

- 논문 식별/오픈액세스 라이선스: “High aspect ratio organic light-emitting diodes”, **Nat Commun (2025)**, DOI **10.1038/s41467-025-67312-4**, “Open Access … CC BY-NC-ND 4.0” 문구 포함.  
  - 원문 URL: https://www.nature.com/articles/s41467-025-67312-4_reference.pdf  
  - 근거 텍스트: PDF 추출본 서두(doi/received/accepted/라이선스). [ /C:/Users/angpa/myProjects/FEATHER/examples/runs/20260104_oled/archive/tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt ]

- 문제정의(상용 조명용 OLED의 핵심 난점): **OLED lifetime은 luminance에 반비례**하고 조명은 디스플레이 대비 **약 10배 높은 휘도 요구**, 효율/수명 모두 전류밀도 증가와 함께 저하.  
  - 원문 URL: https://www.nature.com/articles/s41467-025-67312-4_reference.pdf  
  - 근거 텍스트: Abstract/Introduction에서 “OLED lifetime is inversely proportional to luminance… lighting applications demand high luminance… roughly an order of magnitude higher luminance than displays… efficiency and operating lifetime both decline with increasing current density”. [ /.../0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt ]

- 제안(기술적 변곡점 후보): **sub‑mm high aspect ratio(고종횡비) 텍스처 기판(corrugated substrate)** 위에 OLED를 만들어 **패널 면적 대비 활성 면적을 증가(AE)** → 동일 패널 휘도를 더 낮은 전류밀도로 달성.  
  - 원문 URL: https://www.nature.com/articles/s41467-025-67312-4_reference.pdf  
  - 근거 텍스트: Abstract/Results의 “constructing OLEDs on a substrate with sub-mm, high aspect ratio surface texture… more active OLED area per unit lighting panel area… current density decreases”, AE 정의(“AE ≡ Adev/Apan”). [ /.../0002_...pdf.txt ]

- 정량 결과(효율/수명):  
  - **AE up to 1.4×**(표준 thermal evaporator/VTE로 두께 균일도 확보)  
  - planar 대비 **operating lifetime 2.7×(LT95 기준)**  
  - **external light extraction efficiency 최대 40% 증가**  
  - 원문 URL: https://www.nature.com/articles/s41467-025-67312-4_reference.pdf  
  - 근거 텍스트: Abstract에 “area enhancement factors up to 1.4x… 2.7-fold increase in operating lifetime… up to a 40% increase in external light extraction efficiency”. [ /.../0002_...pdf.txt ]

- 수명 측정 조건(해석에 중요한 실험 조건): **constant panel current density Jpan = 3 mA cm⁻²**, 초기 휘도 언급(대략 200 cd m⁻²), **LT95 = 초기 휘도의 95%까지 감소하는 시간**으로 정의. 또한 outcoupling 변화의 혼입을 피하기 위해 **constant luminance가 아닌 constant current**로 에이징했다고 명시.  
  - 원문 URL: https://www.nature.com/articles/s41467-025-67312-4_reference.pdf  
  - 근거 텍스트: Results/Fig.7 설명 “2.7-fold increase in LT95… devices are aged at a constant panel current density of Jpan=3 mA cm-2… instead of constant panel luminance… LT95 defined as time required to reach 95% of initial luminance”. [ /.../0002_...pdf.txt ]

- 제조/스케일업 리스크(상용화 비교에서 핵심):  
  - **AE2.0(고 AE) 디바이스는 제작되었으나 빠르게 실패·재현성 낮음** (“Functional AE2.0 devices… tended to fail quickly and were not reproducible.”)  
  - VTE의 방향성 증착 때문에 텍스처에서 **두께 보정(AE 배수 보정)**이 필요하고, 균일 코팅이 핵심 난제라고 명시.  
  - 원문 URL: https://www.nature.com/articles/s41467-025-67312-4_reference.pdf  
  - 근거 텍스트: Results/Fig.5 근처 “Functional AE2.0… not reproducible”, Results/Fabrication에서 “directional nature of VTE… nominal thickness must be increased by factor AE… key challenge… uniform thickness/no hot spots”. [ /.../0002_...pdf.txt ]

- 산업적 이해상충(credibility/industry tie): 일부 저자가 **OLEDWorks LLC 직원**이며 회사가 OLED lighting 제품을 제조한다고 “Competing interests”에 명시.  
  - 원문 URL: https://www.nature.com/articles/s41467-025-67312-4_reference.pdf  
  - 근거 텍스트: “R.M., D.C., and M.K. are employees of OLEDWorks, LLC, a company that manufactures OLED lighting products.” [ /.../0002_...pdf.txt ]