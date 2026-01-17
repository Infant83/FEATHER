## 아카이브 맵(coverage 파악)

### 0) 런/지시/인덱스
- `instruction/20260117_arxiv-template.txt`  
  - 이번 런에 포함된 3개 arXiv URL만 명시(2511.00922, 2512.06029, 1901.01201).
- `archive/20260117_arxiv-template-index.md`  
  - 산출물 위치 요약(텍스트 추출본 3, PDF 3, arXiv src 3(TeX 추출본 2)).
- `archive/_job.json`, `archive/_log.txt`  
  - 실행 옵션/로그(재현성 확인용).

### 1) 메타데이터 인덱스(JSONL) — **반드시 확인 대상**
- `archive/arxiv/papers.jsonl`  
  - 3개 논문의 핵심 메타(제목/초록/카테고리/DOI/인용수) 포함.
- `archive/arxiv/src_manifest.jsonl`  
  - 각 arXiv의 src tar, 풀린 디렉토리, TeX 목록, figure/table 파일 목록을 인덱싱.  
  - 2511.00922/2512.06029는 TeX 텍스트 추출본(`src_text`) 존재. 1901.01201은 `src_text`가 보이지 않아 PDF-text 기반으로 읽어야 함.
- (OpenAlex 관련) `archive/openalex/**/*` **없음**  
- (Tavily 검색/유튜브 등) `archive/tavily_search.jsonl`, `archive/youtube/videos.jsonl` **없음**  
- Tavily “extract”는 있음: `archive/tavily_extract/*.txt` (arXiv abs 페이지 요약 스냅샷)

### 2) 논문 본문(리뷰의 1차 근거)
**PDF(원문)**
- `archive/arxiv/pdf/2511.00922v1.pdf`
- `archive/arxiv/pdf/2512.06029v1.pdf`
- `archive/arxiv/pdf/1901.01201v1.pdf`

**텍스트 추출본(빠른 인용/검색용)**
- `archive/arxiv/text/2511.00922v1.txt`
- `archive/arxiv/text/2512.06029v1.txt`
- `archive/arxiv/text/1901.01201v1.txt`

**TeX 추출본(정확한 수치/표/방법 서술 회수에 유리)**
- `archive/arxiv/src_text/2511.00922.txt` (main tex 포함)
- `archive/arxiv/src_text/2512.06029.txt` (pccp_manuscript.tex)

### 3) 보조자료(도표/테이블/ESI 단서)
- 2511.00922 소스 트리: `archive/arxiv/src/2511.00922/**`
  - 주요 tex: `article1_mainV251023.tex`, SI: `article1_SI.tex`
  - tables: `tables/supplementary_table_S1_emission.tex`, `supplementary_table_S2_st_gap.tex` 등
  - figure pdf 다수(성능 비교/분포/PCA/ML ROC 등)
- 2512.06029 소스 트리: `archive/arxiv/src/2512.06029/**`
  - 주요 tex: `pccp_manuscript.tex`
  - ESI PDF 존재: `pccp_ESI.pdf` (상세 설정/추가 결과가 들어있을 가능성 큼)
  - figures: active learning curve, parity plot, feature importance 등

---

## 3편 논문 “연결 실마리”(리뷰 내 통합 내러티브 설계 관점)
- 2511.00922: **xTB 기반 sTDA/sTD-DFT-xTB를 747-molecule 벤치마크로 ‘HTS용으로 검증’**(정량 예측 한계도 명시: ΔEST MAE ~0.17 eV vs exp, 대신 랭킹 일관성 r~0.82 등).
- 2512.06029: **동일 747 데이터/동일(혹은 매우 유사) xTB 스택을 기반으로 NTO(CT descriptor) + ML(SVR, SHAP) + Active Learning으로 “가속 설계 전략” 제시**(ΔEST 예측 MAE=0.024 eV, R²=0.96 주장; AL로 데이터 요구량 ~25% 절감).
- 1901.01201: TADF(유기 발광)와 직접 동일 계열은 아니지만, **OLED 발광체 성능을 “경쟁 소멸 채널/온도 의존 비복사 경로 포함”한 kinetic/rate formalism으로 예측**하는 일반 프레임워크 제시 →  
  위의 두 TADF 논문이 주로 다루는 ΔEST/CT/스크리닝(정적·수직 근사 중심)과 대비되어, 리뷰에서 “정적 스크리닝→동역학/수명/효율 예측으로의 확장 갭”을 **증거 기반으로** 짚는 축이 될 수 있음.

---

## 우선순위 읽기 계획(최대 12개) + 근거
1. `archive/arxiv/papers.jsonl`  
   - 3편의 공식 초록/메타를 한 번에 확보(리뷰 서론/논문 간 연결고리의 기준점).
2. `archive/arxiv/text/2511.00922v1.txt`  
   - 벤치마크 설계, 비교 지표(r, MAE, 데이터 규모 747/312 등)와 결론을 빠르게 회수.
3. `archive/arxiv/src_text/2511.00922.txt`  
   - 방법론 디테일(예: GFN2-xTB/ALPB, 수직 근사 한계, 통계/PCA/설계 규칙)을 정확 문장으로 인용하기 좋음.
4. `archive/arxiv/src/2511.00922/tables/supplementary_table_S2_st_gap.tex`  
   - ΔEST 관련 대규모 표/요약지표가 있을 가능성이 높아, “증거 기반” 수치 인용에 핵심.
5. `archive/arxiv/text/2512.06029v1.txt`  
   - NTO descriptor(특히 She), ML 성능(MAE=0.024 eV, R²=0.96), active learning 효과(~25%)를 본문 흐름으로 확보.
6. `archive/arxiv/src_text/2512.06029.txt`  
   - ML 파이프라인/검증(OT-LC-ωPBE, STEOM-DLPNO-CCSD 등) 및 벤치마킹 서술을 정확히 가져오기 위함.
7. `archive/arxiv/src/2512.06029/pccp_ESI.pdf`  
   - “evidence from papers only” 요구를 만족시키려면 ESI의 데이터 분할, 하이퍼파라미터, 피처 정의, AL 세부 설정 확인이 중요.
8. `archive/arxiv/text/1901.01201v1.txt`  
   - kinetic model, 경쟁 소멸 채널(kr, kISC, knr(T)), 온도 의존성 포함이라는 핵심 기여를 텍스트로 확보.
9. `archive/arxiv/pdf/1901.01201v1.pdf`  
   - 텍스트 추출본에서 수식/스킴/정의가 누락될 수 있어, 효율/수명 식과 모델 구조를 정확히 확인(필요시 직접 인용).
10. `archive/arxiv/src_manifest.jsonl`  
   - 표/그림/TeX 원본 위치를 빠르게 찾는 “지도”. 리뷰 작성 중 추가 근거가 필요할 때 탐색 비용을 줄임.
11. `archive/tavily_extract/0001_https_arxiv.org_abs_2511.00922.txt`  
   - arXiv abs 페이지의 요약/키워드(텍스트 추출본과 교차검증용; 중요도는 낮음).
12. `archive/tavily_extract/0002_https_arxiv.org_abs_2512.06029.txt`  
   - 동일 목적(낮은 우선순위 보조).

(비권장/후순위) 2511.00922의 `Figures/*.pdf`는 리뷰용 시각자료 이해에는 도움되지만, “3편 종합 기술리뷰”의 1차 근거는 본문/표/ESI가 우선이라 후순위가 적절합니다.

---

## 제안 독서 순서(작업 흐름)
- **Phase A (스레드 정의)**: papers.jsonl → 3편 초록 기반으로 “HTS 검증(2511) → CT+ML+AL 가속(2512) → 동역학/효율 예측 프레임(1901)” 연결축 확정  
- **Phase B (정량 근거 수집)**: 2511 tex+tables → 2512 tex+ESI → 1901 pdf/텍스트  
- **Phase C (갭/리스크 정리)**:  
  - 2511의 “screening not quantitative prediction(수직 근사/용매 모델 한계 등)” 근거 문장 회수  
  - 2512의 “고성능 ML”이 어떤 레퍼런스/분할/검증 위에 서 있는지(E SI 근거) 확인  
  - 1901의 “rate/kinetics”가 요구하는 입력(장벽, MECP, 온도 등)이 2511/2512 HTS 파이프라인과 어떻게 충돌/미정의인지 근거 기반으로 정리

원하시면, 위 우선순위 1–8번 파일을 실제로 더 깊게 열어(특히 2511/2512의 Methods/Results 섹션과 ESI의 핵심 표) “리뷰에 바로 쓸 수 있는 인용 후보 문장/수치 목록(논문별 10~20개)” 형태로 추가 스카우팅도 진행할 수 있습니다.