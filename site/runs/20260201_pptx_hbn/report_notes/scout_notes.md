다음은 현재 아카이브 구조와, 리뷰 작성에 바로 필요한 핵심 소스 인벤토리 및 우선 읽기 계획입니다.

## 1. 아카이브 구조 개요

- 메타/로그
  - `archive/20260201_pptx_hbn-index.md` — 런 메타 정보
  - `archive/_job.json` — 수집 설정/로그
  - `archive/_log.txt`, `archive/_log_local_test.txt` — 실행 로그
- 로컬 소스 (핵심 1차 자료)
  - `archive/local/manifest.jsonl` — 로컬 파일 인덱스
  - `archive/local/raw/local-a0387b5a--201112_NCML_hBN_encapsulation_annealing_RHJ.pptx` — PPTX 원본
  - `archive/local/text/local-a0387b5a--201112_NCML_hBN_encapsulation_annealing_RHJ.txt` — PPTX에서 추출된 텍스트 (슬라이드별)
- 웹 인덱스
  - `archive/tavily_search.jsonl` — tavily 검색 결과 인덱스 (원문 PDF 미다운로드)
- 추가 메타
  - `report_notes/source_index.jsonl` — tavily 결과 인덱스(요약)
  - `report_notes/source_triage.md` — 사용 우선순위 메모
  - `instruction/20260201_pptx_hbn.txt` — 현재 작업 인스트럭션

이 중 **실제 내용 기반 1차 근거**는 PPTX 관련 두 파일(raw PPTX, text 추출본)입니다. Tavily 관련 항목은 “인덱스 참고” 용도로만 사용해야 하며, 논문 본문이 아카이브에 없으므로 리뷰의 직접 근거로 사용하지 않습니다.

---

## 2. 소스 인벤토리 (콘텐츠 관점)

### A. 1차 자료: PPTX

1. `archive/local/raw/local-a0387b5a--201112_NCML_hBN_encapsulation_annealing_RHJ.pptx`
   - 유형: 원본 프레젠테이션 (title: “NCML hBN encapsulation annealing”)
   - 역할:
     - 슬라이드 이미지/그림, 도식, 실험 조건 스키마(“Encapsulation annealing scheme”), AFM/PL 맵, band diagram 등 텍스트 추출본에 안 나온 시각 정보 포함 가능성.
     - PL intensity map (300 K) (Slide 1), “Encapsulation annealing scheme”, AFM raw data 처리 지시 등 시각 레이아웃.
     - Mechanism proposal (Slide 3) 도식, Slide 6 “산화 시작 온도와 PL 증가 온도 일치”의 그래프, Slide 9 “Our data” (O-substituted Se vacancies에 따른 defect state 변화), Slide 11 최종 메커니즘 카툰 등.
   - 중요도: ★★★★★ (리뷰의 최상위 근거, 특히 메커니즘 도식 및 조건–결과 매핑에 필수)

2. `archive/local/text/local-a0387b5a--201112_NCML_hBN_encapsulation_annealing_RHJ.txt`
   - 유형: PPTX 텍스트 추출
   - 슬라이드별 핵심 정보:
     - Slide 1: “1L WSe2”, “Encapsulation annealing scheme”, 300 K PL intensity map 언급 → 시스템/프로세스 개괄 근거.
     - Slide 2:
       - 10 K PL 스펙트럼 전후 비교 (Before/After annealing).
       - 여러 피크(Intervalley trion, Biexciton, Localized excitons, Negatively charged biexciton) 및 FWHM (31, 39, 19, 22, 46, 61, 65, 78, 95, 52 meV).
       - 어닐 후 특정 피크(L1, L2 감소; L3~L5 증가) 경향.
       - “W annealing / WO annealing” 비교 언급 → 산소 포함/비포함 분위기 비교 시사.
       - Nanotechnology 28 (2017) 395702, Nat. Commun. (2019) 10:2330 인용 (원문 미보유).
       - TODO 메모: vacancy diffusion barrier, oxygen thermal barrier, oxidation barrier, “다른 기체를 defect에 넣을 수 없을까?” 등 연구 방향 힌트.
     - Slide 3: “Mechanism proposal” — 도식은 PPTX 원본에서 확인 필요.
     - Slide 5:
       - Chalcogen vacancy migration barrier ≈ 2.3 eV, RT에서는 확산 거의 없고, TEM electron beam 하에서는 가능.
       - kBT ~ 0.06 eV at ~773 K (≈ 500 ℃) 언급 → 온도 스케일 감각 제공.
     - Slide 6:
       - “Oxidation이 시작되는 온도와 동일한 지점에서 PL 증가 시작” — 산화 개시 온도 vs PL 향상 온도 상관.
     - Slide 7:
       - 문헌 실험 조건 인용:
         - WSe2 나노시트 두께 2–100 nm, lateral 2–100 μm.
         - SiO2/Si 위 exfoliation.
         - Quartz tube furnace, 400 ℃까지 6분 램프, 이후 400 ℃에서 일정 시간(th) 유지, **ambient atmosphere**.
         - SeO2 승화 온도(>350 ℃) 때문에 400 ℃ 설정.
       - “Oxidation temperature ~ 400 °C”와 “PL 증가 시작 온도와 동일” 재강조.
     - Slide 8:
       - O on Se vacancy (Sevac) adsorption energy:
         - Eads(O on Sevac) ≈ −7.1 eV (atomic O 기준), Oins ≈ −2.9 eV, Oad ≈ −2.4 eV.
         - O2 기준 adsorption energy: −1.6 eV, −0.3 eV, 0.2 eV.
       - O2 dissociation barrier at Sevac ≈ 0.52 eV.
       - kBT ~ 0.06 eV (~773 K) 재언급 → 고온에서 충분히 활성화 가능.
     - Slide 9:
       - “O-substituted Se vacancies 로 인한 defect state 변화 – Our data” → PL/전자구조 변화 실험/계산 결과 도식(PPTX에서 확인 필요).
     - Slide 10:
       - TEM/STEM 한계:
         - electron-beam-induced damage 때문에 intrinsic vs beam-induced vacancy 구분 어려움.
         - C, O의 low Z로 인한 contrast 약함.
         - Se vacancy vs O substitution 구분은 고 SNR, 고 dose 필요 → 추가 결함 생성 리스크.
       - → OSe 직접 이미징의 실험적 제약 근거.
     - Slide 11:
       - 결론 문구:
         - “Interface에 trap된 O2가 이동하여 defect site에 O로 결합됨.”
         - Annealing 중 O2 diffusion → Sevac에서 O2 dissociation → O-substituted vacancy 형성.
       - “Defect site에 다른 원자를 결합시킬 수 있는 테크닉으로서의 가능성?”
       - “O2가 interface에서 이동할 수 있는 에너지 계산?” 등 follow-up 제안.
   - 인용 포맷: 텍스트에 나오는 내용은 (Slide X) 혹은 (Slide X, Fig. Y) 형태로 사용 예정.
   - 중요도: ★★★★★ (슬라이드 번호 기반 인용, 수치/장벽/온도/PL 변화 정량 요약의 직접 근거)

3. `archive/local/manifest.jsonl`
   - 로컬 PPTX에 대한 메타정보(파일명, 제목, 태그, 언어).
   - 중요도: ★★☆☆☆ (기술적 메타, 논의에는 직접 인용 불필요)

### B. 2차/보조 자료: 웹 인덱스 (tavily)

4. `archive/tavily_search.jsonl`
   - tavily 검색 결과(요약 및 메타) JSONL.
   - 예: 
     - “Optical grade transformation of monolayer transition metal ...”
     - “Hexagonal Boron Nitride assisted transfer and encapsulation of ...”
     - “Impact of thermal annealing on graphene devices encapsulated in ...”
   - **현재 런에서는 원문 PDF/HTML이 별도로 다운로드되어 있지 않으므로**, 이 파일 내용은 “이런 논문들이 존재한다”는 수준의 인덱스 신호로만 사용해야 함.
   - 중요도: ★★☆☆☆ (배경 문헌 스펙트럼 파악용, 직접 근거/수치 인용 금지)

5. `report_notes/source_index.jsonl`
   - 위 tavily 인덱스의 재정리(각 소스 id, title, url, score, source_path).
   - 중요도: ★☆☆☆☆ (메타 수준)

6. `report_notes/source_triage.md`
   - tavily 소스별 triage 메모. 예: graphene/hBN encapsulation annealing 논문, hBN 기반 quantum emitter 리뷰 등.
   - 사용 방식:
     - 리뷰에서 “문헌적 컨텍스트”를 말할 때, **정량 수치/구체적 결과를 옮기지 않고**, “그래핀 디바이스에서 hBN encapsulation + annealing이 contact resistance, mobility 등에 영향을 주는 연구들이 보고되어 있다(문헌 목록 수준)” 정도의 서술에 참고.
     - 하지만 **원문 미확보**이므로, pptx 외 세부 주장 일반화는 “공개정보 한계”를 명시하고 조심스럽게.
   - 중요도: ★★☆☆☆ (배경 방향성 참고용, 직접 인용은 매우 제한)

---

## 3. 우선 읽기/확인 목록 (최대 12개)

**1순위 – PPTX 내용 정밀 파악**

1. `archive/local/raw/local-a0387b5a--201112_NCML_hBN_encapsulation_annealing_RHJ.pptx`
   - 이유:
     - 텍스트 추출본에서 누락된 핵심: 
       - Encapsulation annealing scheme (Slide 1) – 온도 프로파일, 분위기, hBN stack 구조 도식.
       - AFM raw data 및 계면 버블/오염 변화 이미지.
       - Before/After PL 맵(300 K, 10 K) 실제 스케일바/컬러바.
       - Mechanism proposal (Slide 3), Our data (Slide 9), 결론 도식 (Slide 11)에서 계면 O2 → vacancy 패시베이션 → PL 증가 흐름을 시각적으로 확인.
     - “Current Landscape”, “Mechanistic Insights” 섹션에서 공정-구조-광학 연계 설명을 구체화하기 위한 1차 시각 근거.
   - 작업:
     - 각 슬라이드별 그림/축 라벨/주석을 확인해 텍스트 노트로 재정리.
     - 슬라이드 번호/그림 번호를 명시해 인용 레이블 정의: 예) (Slide 2, PL spectra), (Slide 6, Oxidation vs PL), (Slide 9, Defect states).

2. `archive/local/text/local-a0387b5a--201112_NCML_hBN_encapsulation_annealing_RHJ.txt`
   - 이유:
     - 이미 1차로 읽었지만, 리뷰 작성 전:
       - 각 슬라이드별 요소를 섹션별로 매핑:
         - Abstract/Introduction: Slide 1, 2 개괄문.
         - Current Landscape: Slide 2의 “Before/After”, W vs WO annealing 키워드.
         - Mechanistic Insights: Slide 5–8, 10–11 수치/장벽/adsorption energy, 산화온도.
       - 수치/키워드 정확한 표기(에너지 단위, 온도, kBT 등) 및 가설/합의 레벨 태깅.
     - 인용 포맷을 미리 정제: 예) “O2 dissociation barrier of 0.52 eV at Se vacancy (Slide 8)” 식으로.
   - 작업:
     - 현재 추출 내용 기반으로 상세 노트 테이블(슬라이드 번호 vs 핵심 메시지 vs 사용 섹션)을 만들 계획.

**2순위 – 로컬 메타/구조 확인**

3. `archive/local/manifest.jsonl`
   - 이유:
     - 로컬 PPTX 외 추가 local 파일이 없는지 최종 확인 (이번 런에선 1개로 보이지만 manifest로 재확인).
     - PPTX 제목/태그/언어를 리뷰 front matter(예: Supporting Information 설명)에서 참고할 수 있음.
   - 작업:
     - 간단히 열람해 파일 리스트와 메타 정보 확인.

4. `archive/20260201_pptx_hbn-index.md`
   - 이유:
     - 독립적인 과학 내용은 없지만, 보고서 서두에서 “본 리뷰는 NCML 내부 프레젠테이션(날짜/제목)을 1차 근거로 한다”는 식의 설명을 넣을 때, 정확한 파일명/경로/출처를 명기하기 위함.
   - 작업:
     - 해당 메타를 보고 citation 스타일의 기술 문장 초안 메모.

**3순위 – Tavily 인덱스 기반 배경 문헌 맵 (정성적 참고)**

(원문 미확보이므로, 정량/세부 메커니즘은 인용 불가, 단지 “이런 연구축이 존재” 정도 수준으로.)

5. `archive/tavily_search.jsonl`
   - 이유:
     - hBN encapsulation + annealing과 관련된 문헌 축:
       - graphene/hBN encapsulation annealing on device performance (`Impact of thermal annealing on graphene devices encapsulated in ...`).
       - TMD monolayer optical quality 향상 (`Optical grade transformation of monolayer transition metal ...`).
       - hBN quantum emitters (`Synthesis of Quantum Emitters in Hexagonal Boron Nitride and ...`, `Hexagonal Boron Nitride Based Photonic Quantum Technologies` 등).
       - hBN growth/pressure role (`Role of Pressure in the Growth of Hexagonal Boron Nitride Thin ...`).
     - Introduction/Current Landscape/Outlook에서 “문헌 경향성”을 한두 문장으로 정리할 때 참고.
   - 작업:
     - 각 entry 제목/저널/연도 정도만 정리해, 후기 논의에서 ‘문헌적 컨텍스트’ 수준으로 언급.

6. `report_notes/source_index.jsonl`
   - 이유:
     - 위 tavily_search를 간략한 high-score subset으로 보여주므로, 어떤 축(예: encapsulation transfer 기술, vdW heterostructure fabrication)이 있는지 파악에 용이.
   - 작업:
     - 이미 일부 내용 확인했지만, 중요 타이틀만 따로 메모.

7. `report_notes/source_triage.md`
   - 이유:
     - 사용자가 이미 triage한 리스트이므로, 어떤 웹 소스를 상대적으로 더 관련성 높게 본 것인지 파악.
     - 예를 들어 graphene/hBN encapsulated devices annealing 논문은 Current Landscape에서 “graphene/hBN encapsulation device 사례” 항목에 간단 인용 가능.
   - 작업:
     - 목록을 리뷰 구조의 “Current Landscape – (iii) 그래핀/hBN 캡슐화 디바이스 사례”에 매핑하는 용도로 정리.

**4순위 – 기타 메타**

8. `archive/_job.json`
   - 이유:
     - 과학적 내용은 없을 가능성이 크나, 필요하다면 런 설정을 보고 “이번 리뷰는 추가적인 OpenAlex/arXiv PDF 다운로드 없이 수행되었다”는 meta-remark의 근거가 될 수 있음.
   - 작업:
     - 필요성이 낮지만, 데이터 출처 설명에서 필요할 경우 열람.

9. `archive/_log.txt`, `archive/_log_local_test.txt`
   - 이유:
     - 마찬가지로 내용보다는 런 과정 확인용. 리뷰 본문에는 인용하지 않을 예정.
   - 작업:
     - 일반적으로 불필요, 문제 발생 시에만 확인.

(총 9개; 추가 소스 필요 없음)

---

## 4. 이 인벤토리를 바탕으로 한 읽기/정리 전략 (요약)

1. **PPTX 텍스트 정합화 (2순위 파일까지)**  
   - 이미 읽은 `.txt`를 기준으로, 슬라이드별로 “온도/시간/분위기 – 구조/계면 변화 – PL/결함/도핑 지표 – 메커니즘 키워드(에너지 장벽, 산화 온도, adsorption energy)”를 표로 재조직.
   - 각 항목에 (Slide 번호) 태그 부여.

2. **PPTX 원본 슬라이드 이미지 검토 (1순위)**  
   - Mechanism proposal / Our data / 결론 도식에서 “원인→중간상→결과” 흐름을 정확히 해석.
   - AFM/PL map, 300 K vs 10 K 차이, W vs WO annealing의 실제 데이터 모양을 파악해 서술에 반영.

3. **문헌 컨텍스트 레벨에서 tavily 인덱스 훑기 (3순위)**  
   - Graphene/hBN annealing, TMD optical grade transformation, hBN quantum emitters 등 카테고리별로, **“원문 미확보” 태그와 함께** 간단히 landscape 언급.

4. **ACS 스타일 섹션 구성**  
   - 사용자가 지정한 섹션(Abstract, Introduction, Current Landscape, Mechanistic Insights, Applications, Challenges, Outlook, Risks & Gaps, Critics, Appendix)을 PPTX 슬라이드 컨텐츠에 매핑.
   - 각 문장에 대해: 
     - PPTX 근거가 명확한지 (Consensus 수준: 슬라이드 데이터로 직접 뒷받침),
     - 혹은 메커니즘 해석/확장 수준인지 (Speculative: 가설로 라벨) 구분.

이제 위 우선순위에 따라 PPTX 내용을 정교하게 재구성한 뒤, 요청하신 ACS-style Korean 리뷰 초안을 단계적으로 작성하겠습니다.