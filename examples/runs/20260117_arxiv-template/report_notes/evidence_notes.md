## arXiv 메타데이터(초록/서지)
- **Validation of Semi-Empirical xTB Methods for High-Throughput Screening of TADF Emitters: A 747-Molecule Benchmark Study (2511.00922v1)**  
  - 747개 실험 기반 TADF 데이터셋으로 sTDA-xTB, sTD-DFT-xTB를 HTS 관점에서 벤치마크.  
  - TD-DFT 대비 **계산비용 99%+ 절감**, 두 방법 간 **내적 일관성 Pearson r≈0.82(ΔE_ST)**, 실험(312개 ΔE_ST) 대비 **MAE≈0.17 eV**(수직근사 한계로 설명), D-A-D 우수/비틀림각 50–90° 규칙, PCA 3개 성분이 분산 ~90% 포착 주장.  
  - URL: https://arxiv.org/abs/2511.00922  (PDF: https://arxiv.org/pdf/2511.00922v1)  
  - 근거: [/archive/arxiv/papers.jsonl], [/archive/arxiv/text/2511.00922v1.txt], [/archive/arxiv/src_text/2511.00922.txt]

- **From orbital analysis to active learning: an integrated strategy for the accelerated design of TADF emitters (2512.06029v1)**  
  - 747개 분자에 대해 (GFN2-xTB 구조 + sTDA/sTD-DFT-xTB 여기상태) + **NTO 기반 CT descriptor**를 결합, **SVR로 ΔE_ST 예측 MAE=0.024 eV, R²=0.96** 주장.  
  - hole-electron overlap **S_he**가 중요한 예측자(예: triplet state 단독에서 feature importance 21% 언급).  
  - **Active learning이 목표 정확도 도달에 필요한 데이터 ~25% 절감** 주장.  
  - URL: https://arxiv.org/abs/2512.06029  (PDF: https://arxiv.org/pdf/2512.06029v1)  
  - 근거: [/archive/arxiv/papers.jsonl], [/archive/arxiv/text/2512.06029v1.txt], [/archive/arxiv/src_text/2512.06029.txt]

- **General Approach To Compute Phosphorescent OLED Efficiency (1901.01201v1)**  
  - Ir(III) PhOLED에 대해 **경쟁 소멸 채널을 모두 포함**하고, 특히 **강한 온도의존 비복사 채널 knr(T)**을 명시적으로 포함하는 **수명/효율 예측 일반 프로토콜** 제시.  
  - Photoluminescence 효율/수명 식(예: Φ, τ)을 kr, kISC, knr(T)로 기술, 3MLCT↔3MC(장벽 Ea, TS, MECP 등) 기반의 kinetic model을 강조.  
  - URL: https://arxiv.org/abs/1901.01201  (PDF: https://arxiv.org/pdf/1901.01201v1)  
  - 근거: [/archive/arxiv/papers.jsonl], [/archive/arxiv/text/1901.01201v1.txt]

---

## arXiv 본문(PDF-text/TeX-text)에서 회수한 핵심 “정량/설계/가정” 근거

### 2511.00922 (HTS용 xTB 검증)
- **대규모 벤치마크 규모/검증 타깃**
  - “747 experimentally characterized emitters”, “312 experimental ΔE_ST values”, “213 emission wavelengths(λ_PL)”로 검증 범위를 명시.  
  - 근거: [/archive/arxiv/text/2511.00922v1.txt], [/archive/arxiv/src_text/2511.00922.txt]
- **HTS 비용절감 및 내부 일관성**
  - TD-DFT 대비 **99% 이상 비용 절감** 및 sTDA-xTB vs sTD-DFT-xTB **Pearson r≈0.82(ΔE_ST)**로 “상대 랭킹” 유용성을 강조.  
  - 근거: [/archive/arxiv/text/2511.00922v1.txt], [/archive/arxiv/src_text/2511.00922.txt]
- **정량예측 한계(수직근사)**
  - 실험 ΔE_ST(312개) 대비 **MAE≈0.17 eV**, 이를 **vertical approximation**에 귀속시켜 “screening vs quantitative prediction” 역할을 구분.  
  - 근거: [/archive/arxiv/text/2511.00922v1.txt], [/archive/arxiv/src_text/2511.00922.txt]
- **프로토콜 구성(재현성 단서)**
  - RDKit(SMILES→3D), CREST 3.0 + xTB 6.7.0(GFN2-xTB)로 컨포머 탐색/최적화, 용매로 **ALPB**(toluene) 사용을 명시.  
  - 근거: [/archive/arxiv/text/2511.00922v1.txt]

### 2512.06029 (NTO descriptor + ML + Active Learning)
- **문제정의(ΔE_ST와 k_RISC의 트레이드오프)**
  - 설계 조건을 “ΔE_ST < 0.2 eV”, “k_RISC > 10^6 s^-1”로 제시(열역학 vs 동역학 요구).  
  - 근거: [/archive/arxiv/text/2512.06029v1.txt], [/archive/arxiv/src_text/2512.06029.txt]
- **ML 성능 주장**
  - **SVR: MAE=0.024 eV, R²=0.96(ΔE_ST)**.  
  - 근거: [/archive/arxiv/text/2512.06029v1.txt], [/archive/arxiv/src_text/2512.06029.txt]
- **핵심 descriptor(S_he)와 해석 가능성 도구**
  - NTO 기반 CT descriptor, 특히 **S_he**를 핵심 예측자(예: triplet 단독 21% feature importance)로 언급; SHAP를 사용한다고 명시.  
  - 근거: [/archive/arxiv/text/2512.06029v1.txt], [/archive/arxiv/src_text/2512.06029.txt]
- **프로토콜 검증(고정밀 reference)**
  - hybrid protocol(GFN2-xTB//sTD/sTDA-xTB)을 subset(8–27개)에서 **OT-LC-ωPBE**, **STEOM-DLPNO-CCSD** 등과 비교해 vertical ΔE_ST의 MAE(≈0.10–0.12 eV)를 서술.  
  - 근거: [/archive/arxiv/text/2512.06029v1.txt]
- **재현성/아카이빙 단서**
  - “All workflows, scripts, and environment lockfiles … archived at Zenodo (DOI: 10.5281/zenodo.17436069)” 명시.  
  - 근거: [/archive/arxiv/text/2512.06029v1.txt], [/archive/arxiv/src_text/2512.06029.txt]

---

## Supplementary(TeX tables / ESI PDF) 기반 근거

### 2511.00922 Supplementary tables (TeX)
- **ΔE_ST 검증 데이터 전체표 제공**
  - “Complete validation dataset for singlet-triplet gap predictions” 캡션과 함께, 분자별 **sTDA/sTD-DFT (gas/toluene) vs reference(eV)** 및 문헌 citation을 longtable로 제공.  
  - 근거: [/archive/arxiv/src/2511.00922/tables/supplementary_table_S2_st_gap.tex]
- **발광 파장(λ_PL) 검증 데이터 전체표 제공**
  - “Complete validation dataset for emission wavelength predictions” 캡션과 함께, 분자별 **sTDA/sTD-DFT (gas/toluene) vs reference(nm)** 및 citation 제공.  
  - 근거: [/archive/arxiv/src/2511.00922/tables/supplementary_table_S1_emission.tex]

### 2512.06029 Electronic Supplementary Information (PDF)
- **소프트웨어/환경 버전 명시(재현성)**
  - xTB 6.7.1, CREST 3.0.2, sTDA 1.6.3, Multiwfn 3.8(dev), Python 3.12.3, NumPy 2.0.2, pandas 2.2.3, scikit-learn 1.7.2, SHAP 0.50.0 등.  
  - 근거: [/archive/arxiv/src/2512.06029/pccp_ESI.pdf]
- **계산 절차/커맨드 라인 수준 설정**
  - GFN2-xTB 최적화: `xtb molecule.xyz --opt tight` 및 `--gbsa toluene(ε=2.38)`  
  - excited state: `stda -xtb -e 10`(singlet), `-t`(triplet), `-rpa`(sTD-DFT) 등.  
  - 근거: [/archive/arxiv/src/2512.06029/pccp_ESI.pdf]
- **S_he 및 k_RISC 공식(정의)**
  - S_he: 원자 A에 대한 hole/electron Mulliken population을 사용한 합으로 정의(S1).  
  - k_RISC: Marcus-type 식으로 제시되며 SOC 행렬원소, 재구성에너지 λ, 온도(k_BT) 항을 포함(S3).  
  - 근거: [/archive/arxiv/src/2512.06029/pccp_ESI.pdf]
- **ΔE_ST 임계값(열역학적 기준)**
  - “For efficient TADF, ΔE_ST < 0.2 eV… k_BT ≈ 0.026 eV at 300 K”로 명시.  
  - 근거: [/archive/arxiv/src/2512.06029/pccp_ESI.pdf]

---

## PhOLED kinetics 프레임(1901.01201)에서 회수한 모델 구조/변수 정의
- **효율/수명 수식과 rate 정의**
  - photoluminescence 효율 Φ 및 수명 τ를 kr, kISC, knr(T)로 표현하는 식(1)(2) 제시.  
  - knr(T)를 **강한 온도의존 nonradiative decay rate**로 정의하고, kr(방사), kISC(비복사 ISC)와 경쟁하는 채널로 설명.  
  - 근거: [/archive/arxiv/text/1901.01201v1.txt]
- **온도의존 비복사 채널의 구조적/반응좌표 설명**
  - 3MLCT→3MC well로의 population(transition state TS, MECP, 장벽 Ea가 rate-limiting) 등을 Scheme 설명으로 명시.  
  - 근거: [/archive/arxiv/text/1901.01201v1.txt]

---

## (참고) 템플릿 경로/파일 상태
- 사용자 제공 템플릿 경로 `examples\runs\20260117_arxiv-template\template_src\2601.05567\template.md`는 현재 FS에서 미발견(읽기 오류).  
  - 근거: [/archive/20260117_arxiv-template-index.md] (템플릿 소스는 별도 제공이라 인덱스에 “없음”이 아닌, 본 실행환경에서 경로 불일치 가능)