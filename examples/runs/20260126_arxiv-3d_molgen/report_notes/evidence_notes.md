먼저 본 리포트 작성에 사용한 핵심 근거(아카이브 내 파일 및 원문 PDF URL)를 소스 유형별로 정리합니다. 고유명사·문서 제목은 원문 표기를 유지했습니다.

- PDF (최종 렌더링)
  - 3D Molecule Generation from Rigid Motifs via SE(3) Flows — arXiv PDF: https://arxiv.org/pdf/2601.16955v1  (원문 PDF 보관 경로: [./archive/arxiv/pdf/2601.16955v1.pdf])

- TeX / 논문 소스 (핵심 본문·수식·표·캡션)
  - 본문/방법론: [./archive/arxiv/src/2601.16955/contents/method.tex]
  - 실험·설정: [./archive/arxiv/src/2601.16955/contents/experiments.tex]
  - 배경·정의: [./archive/arxiv/src/2601.16955/contents/background.tex]
  - 소개: [./archive/arxiv/src/2601.16955/contents/intro.tex]
  - 부록(Implementation Details, Evaluation Metrics, Extended Results, Ablations): [./archive/arxiv/src/2601.16955/contents/appendix.tex]
  - 참고문헌: [./archive/arxiv/src/2601.16955/references.bib]
  - 빌드/패키지 설명: [./archive/arxiv/src/2601.16955/00README.json]
  - 소스 매니페스트(파일 목록): [./archive/arxiv/src_manifest.jsonl]

- 텍스트 추출본 (빠른 검색·전체 문장 확인)
  - arXiv 텍스트 추출: [./archive/arxiv/text/2601.16955v1.txt]  (원문 PDF URL: https://arxiv.org/pdf/2601.16955v1)

- 시각자료 / 그림 (주장·압축비·ablation 근거)
  - Fragmentation / ablation: [./archive/arxiv/src/2601.16955/visuals/ablations/frag_comparison.png]
  - Motif / entity distributions (QMugs): [./archive/arxiv/src/2601.16955/visuals/entity_distributions/distribution_qmugs_middle_threshold.pdf]
  - Conditional generation examples: [./archive/arxiv/src/2601.16955/visuals/cond_generation/main.png]
  - 기타 샘플 이미지(appendix): [./archive/arxiv/src/2601.16955/visuals/uncond_samples/]

- 색인 / 메타데이터
  - arXiv 메타데이터(검색용): [./archive/arxiv/papers.jsonl]
  - src manifest: [./archive/arxiv/src_manifest.jsonl]

이제 요청하신 템플릿(technical_deep_dive)에 따라 논문 “3D Molecule Generation from Rigid Motifs via SE(3) Flows” (arXiv:2601.16955v1, 2026)의 핵심 기술·실험·재현성 관점의 심층 검토를 제시합니다. 각 핵심 주장/근거에는 본문 섹션·표/그림/식 번호 또는 파일 경로를 함께 표시합니다.

Executive Summary
- 주장 요약: 저자들은 분자 생성을 기존의 원자 수준 좌표(atomic coordinates) 대신 “rigid motifs” (각 motif는 canonical pose + atom types + 유한 회전 대칭군)을 단위로 하는 SE(3)-equivariant multimodal flow(continuous SE(3) flow + discrete CTMC 기반 discrete flow)로 모델링하는 MOTIFLOW을 제안한다. 이 접근은 표현 압축(≈3.5×, QMugs 기준), 세대(샘플링) 단계 수 감소(약 2×–10×), 그리고 GEOM-DRUGS에서의 향상된 atom stability 등의 이점을 보고한다 ([./archive/arxiv/src/2601.16955/contents/method.tex], [./archive/arxiv/text/2601.16955v1.txt], PDF https://arxiv.org/pdf/2601.16955v1).
- 핵심 근거: 표현 정의 및 수식(메서드 섹션), discrete CTMC 정의(메서드 섹션), 구현·하이퍼파라미터·확장 결과(부록: Implementation Details, Extended Results), 시각적 분포·ablation 그림(visuals) — 각 파일 참조 ([./archive/arxiv/src/2601.16955/contents/method.tex], [./archive/arxiv/src/2601.16955/contents/appendix.tex], [./archive/arxiv/src/2601.16955/visuals/*]).

Scope & Methodology (본 리포트의 범위와 근거 수집 방식)
- 범위: 논문 본문 및 부록(TeX 소스 및 시각자료)에 한정해 기술적 본질(표현·모델·학습 목표·알고리즘), 실험 설정·메트릭, 정량 결과·ablation, 재현 체크리스트 및 추천 실험을 다룸. 외부 자료(동일 분야 선행작)는 논문 참조목록을 통해 교차검증(참조문헌들: EDM, END, EquiFM 등)하되, 본 리포트의 1차 근거는 오직 위의 아카이브 자료들이다 ([./archive/arxiv/src/2601.16955/contents/appendix.tex], [./archive/arxiv/src/2601.16955/references.bib]).
- 근거 수집: TeX 소스(method/appendix/experiments/background), 텍스트 추출본(검색·초록 확인), 시각자료(압축비·ablation), 확장표/테이블(부록)을 우선 검토하였다. 주요 수치·표/그림 번호는 TeX/appendix의 표/그림 라벨을 사용해 연결했다.

Technical Background
- SE(3) 및 흐름(Flow Matching) 개념
  - SE(3) = R^3 ⋊ SO(3): rigid frame(translation x ∈ R^3와 rotation R ∈ SO(3))으로 표현되는 물체 위치의 군 구조 및 회전 성분의 리만니안 성질을 사용. 회전의 tangent space와 exp/log 맵을 사용한 지오데식 보간이 설명됨 ([./archive/arxiv/src/2601.16955/contents/background.tex], Appendix A.1 in [./archive/arxiv/src/2601.16955/contents/appendix.tex]).
  - Flow matching on manifolds: SE(3)에서 translation은 선형 보간, rotation은 지오데식 보간으로 분리하여 conditional vector field를 정의하고, 네트워크가 이 벡터장을 회귀하도록 학습(L_SE(3) 식) ([./archive/arxiv/text/2601.16955v1.txt], [./archive/arxiv/src/2601.16955/contents/method.tex], Appendix [./archive/arxiv/src/2601.16955/contents/appendix.tex]).
- Discrete flows via CTMC
  - 이산 모달리티(모티프 클래스)는 continuous-time Markov chains(CTMC)을 이용하여 masking → target으로 선형 보간하는 경로로 모델링(식 형태 및 rate matrix 정의 제공) — masking prior와 analytic rate matrix (mask → true class로만 mass 이동) 정의가 명세되어 있음 ([./archive/arxiv/src/2601.16955/contents/method.tex], eqns (80–89) 참조).
- Motif / frame 표현
  - 모티프는 canonical pose P ∈ R^{N_i×3}, atom types h_i, 그리고 motif의 유한 회전 대칭군 S_i로 정의. 각 모티프 인스턴스에는 frame T = (R, x) ∈ SE(3)을 할당, atom-level 좌표는 P R + 1 x^T로 복원 가능(가환식) — 즉 표현은 가역적(invertible)임 ([./archive/arxiv/src/2601.16955/contents/method.tex], eqn lines ~11–14).
- 비교 축(표현–학습 목표–샘플링 비용)으로 본 논문과 선행작
  - Atom-based diffusion/flow: EDM, END, GeoLDM 등은 atom 좌표 및 atom type을 직접 모델링. 일반적으로 diffusion은 많은 샘플링 스텝(수백~천) 필요(참조: EDM, END) ([./archive/arxiv/src/2601.16955/contents/appendix.tex], references).
  - Frame/motif 기반: MOTIFLOW은 SE(3)^K × V_m^K 상에서 multimodal flow를 구성하여 discrete/continuous를 분리 처리. 선행의 protein frame 접근 (FoldFlow, RFdiffusion 등)을 분자(비선형·분기 구조)에 확대 ([./archive/arxiv/src/2601.16955/contents/method.tex], refs: foldflow, se3diffusion).

Methods & Data — 알고리즘·수식·데이터 파이프라인
- 표현 및 문제정의
  - 데이터: 분자 = 원자 포인트 클라우드 { (y_j, h_j) }_{j=1}^N (atom coords + atom types). 목표: 분자를 K개의 rigid motifs { (T_i, m_i) }_{i=1}^K 로 분해하여 SE(3)^K × V_m^K 상에서 샘플링 ([./archive/arxiv/src/2601.16955/contents/method.tex], §Method).
  - Fragment 정의: fragmentation 규칙 — (i) rigidity(회전 결합 없음), (ii) non-degeneracy(3개 이상의 비공선 점), (iii) tractability(데이터상 빈도 충분) — bonds 보존/절단 규칙(평면 고리와 fused rings는 보존, 수소 결합은 자르지 않음), 소수 빈도(occurrence < α%) motif에 대해 재분해(pruning) — 기본 α = 0.1 ([./archive/arxiv/src/2601.16955/contents/method.tex], §Rigid-Motif Decomposition).
  - Canonical pose & symmetry: motif별 graph automorphism으로부터 유도한 rotation matrices 집합 S_i(유한 회전 대칭군)를 계산해 vocabulary에 저장, 데이터 인스턴스는 Kabsch를 사용해 representative rotation R_j 계산 ([./archive/arxiv/src/2601.16955/contents/method.tex], §Canonicalisation and Vocabulary).
- Generative 모델: Multimodal Flow
  - 상태공간: SE(3)^K × V_m^K. 모델은 각 motif에 대해 조건부 factorisation p_t(M_t | M_1) = ∏_k p_t(m_t^k | m_1^k) p_t(T_t^k | T_1^k)로 훈련(§Multimodal Flow) — discrete/continuous loss 합산으로 학습 ([./archive/arxiv/src/2601.16955/contents/method.tex], eqns ~61–69).
  - Continuous (SE(3)) component: translation은 linear interpolant, rotation은 geodesic interpolant; conditional vector fields u_t^x, u_t^R가 closed-form으로 정의되고 네트워크는 v_θ ≈ u_t를 회귀(L_SE(3) loss) ([./archive/arxiv/text/2601.16955v1.txt], method/appendix).
  - Discrete component: masking prior p_0 = δ_{[MASK]}로 설정하고 CTMC rate matrix는 mask → target 로만 질량을 이동하도록 analytic form 사용(식(80–89)); discrete objective = cross-entropy between denoiser logits and true motif type ([./archive/arxiv/src/2601.16955/contents/method.tex], §Multimodal Flow).
- 네트워크 아키텍처·훈련 세부
  - Backbone: FoldFlow-Base(IPA 기반) 확장. 주요 변형: (i) self-conditioning for discrete modality (p=0.5), (ii) triangular multiplicative updates for fragment pairs, (iii) 추가 discrete readout head. 모델 크기: unconditional 12.4M 파라미터, conditional 13.7M ([./archive/arxiv/src/2601.16955/contents/appendix.tex], Implementation Details).
  - 입력 피처: motif token embedding + timestep embedding + (self-conditioning), pairwise 거리 RBF(64)로 엣지 초기화(무순서성에 대응). Backbone: 4 blocks (IPA + transitions + 2 transformer encoder), split-head for rot/trans updates ([./archive/arxiv/src/2601.16955/contents/appendix.tex]).
  - 학습/샘플링 하이퍼: learning rate = 1e-4; rotational component는 exponential rate scheduler (factor 10); QM9: 1000 epochs, GEOM-Drugs: 135 epochs (부록), sampling steps 보통 50–100에서 최적(흐름 모델은 diffusion보다 적은 steps로 충분) ([./archive/arxiv/src/2601.16955/contents/appendix.tex], Extended Results).
- 데이터셋·전처리·평가
  - 사용 데이터셋: QM9 (134k; 소분자), GEOM-Drugs (430k; 중형), QMugs (subset 300k; 대형 drug-like) — 실험별 세부 분할은 experiments/appendix 참조 ([./archive/arxiv/src/2601.16955/contents/experiments.tex], Appendix).
  - Fragmentation 설정: 기본 Planar Rings strategy + α (threshold) 실험(0.5%, 0.1% (기본), 0.01%) — 결과는 ablation에서 비교 ([./archive/arxiv/src/2601.16955/contents/method.tex], §Rigid-Motif Decomposition; ablation tables: [./archive/arxiv/src/2601.16955/contents/appendix.tex]).
  - 평가 메트릭: Atom stability (valency 기반), Molecule stability, Validity (RDKit sanitisation), Connectivity (valid & connected), Uniqueness, Total Variation (atom/bond type marginals), Strain energy (MMFF relaxation in RDKit), SA/QED — 계산 절차와 툴( RDKit, OpenBabel ) 명시 ([./archive/arxiv/src/2601.16955/contents/appendix.tex], §Evaluation Metrics).
- 알고리즘 단계 요약 (샘플링/학습)
  1. 데이터 전처리: bond-cut rules → preliminary rigid motifs → prune rare motifs below α → canonical pose selection 및 symmetry S_i 계산 → 각 fragment instance에 frame T_j via Kabsch 할당 ([./archive/arxiv/src/2601.16955/contents/method.tex]).
  2. 모델 입력 구성: noisy frames T_t^k, partially masked motif tokens m_t^k, distance RBF edge features → 모델 통과 → continuous vector field v_θ^x, v_θ^R 및 discrete logits output ([./archive/arxiv/src/2601.16955/contents/appendix.tex], Architecture).
  3. 학습: SE(3) flow matching loss + discrete cross-entropy denoising loss 합산으로 최적화(learning rate 1e-4, rot scheduler 적용) ([./archive/arxiv/src/2601.16955/contents/appendix.tex]).
  4. 샘플링: prior (N(0,I)×U(SO(3)) for frames, mask token for discrete)에서 초기화 후 learned joint vector field를 수치적 적분(역경로 통합) 및 CTMC를 통해 mask→target 상태 복원 ([./archive/arxiv/src/2601.16955/contents/method.tex], [./archive/arxiv/text/2601.16955v1.txt]).

Results & Evidence — 정량 결과와 근거 맵핑
- 전반적 주장: MOTIFLOW은 atom-based SOTA(EDM/END/EquiFM 등)와 비교해 (i) 동등하거나 우수한 품질, (ii) GEOM-DRUGS에서 향상된 atom stability, (iii) 샘플링 스텝 수 2×–10× 감소, (iv) 표현 압축 ≈ 3.4–3.5× (QMugs 기준) 등을 보고한다 ([./archive/arxiv/text/2601.16955v1.txt], abstract; method 및 experiments/appendix).
- 압축(compression) 주장
  - 근거: method.tex 에서 QMugs에 대해 fragment 기반 표현이 all-atom 대비 평균 3.4×, heavy-atom 대비 1.8× 압축을 제공한다고 밝힘 (Figure \ref{qmugs_distr}, [./archive/arxiv/src/2601.16955/contents/method.tex], lines ~48–56; 시각적 분포: [./archive/arxiv/src/2601.16955/visuals/entity_distributions/distribution_qmugs_middle_threshold.pdf]).
- 샘플링 단계 수(steps) 감소 주장
  - 근거: QM9/GEOM-DRUGS 비교에서 atom-based diffusion/flow 모델들이 통상 500–1000 steps를 사용하는 반면, MOTIFLOW은 50–100 steps에서 동등하거나 더 나은 결과를 보고(예: QM9에서 MOTIFLOW 100 steps로 A=99.1%, M=92.6% vs EDM/END 1000 steps) — 표(메인/부록)를 참조 ([./archive/arxiv/src/2601.16955/contents/experiments.tex], Table qm9_uncond; [./archive/arxiv/src/2601.16955/contents/appendix.tex], Table qm9_uncond_extended).
  - 구체 숫자 예: Appendix Table (QM9 extended)에서 MOTIFLOW (50 steps) A = 99.1%, M = 92.3%; 100 steps A = 99.1%, M = 92.6% ([./archive/arxiv/src/2601.16955/contents/appendix.tex], Table qm9_uncond_extended, lines ~159–161).
- GEOM-DRUGS에서 atom stability 향상 주장
  - 근거: Appendix GEOM-Drugs extended results: MOTIFLOW (50 steps) Stable A = 96.2%, V×C = 81.3% (50 steps), 100 steps Stable A = 96.3% 및 V×C = 82.4% — 이는 END, EDM 등 atom-based 결과(예: END 100 steps Stable A ≈ 87.2%)보다 높은 수치임 ([./archive/arxiv/src/2601.16955/contents/appendix.tex], Table geom_uncond_extended, lines ~238–241; experiments 메인 테이블도 참조).
- Conditional generation (composition / substructure)
  - 근거: QM9 conditional tasks에서 cMOTIFLOW (100 steps) Composition matching = 95.4%, Substructure Tanimoto = 0.862 — 이는 cEND 등 대비 우수한 성능을 보임 ([./archive/arxiv/src/2601.16955/contents/appendix.tex], Table cond_gen_table_extended lines ~302–304; experiments Table cond_gen_table lines ~160–163).
- Ablation (fragmentation α 및 전략)
  - 근거: ablation 섹션과 부록의 여러 표에서 Planar Rings 전략과 α 값(0.5%, 0.1%, 0.01%)에 따른 fragment vocabulary 크기, fragments per molecule, 그리고 생성 성능(Atom stability, V×C 등)의 변화가 보고됨. 요약: 비교적 높은 threshold α=0.1이 현 실험 조건에서 균형(빈도 높은 motif 학습성능 vs uncommon motif coverage)을 제공함 ([./archive/arxiv/src/2601.16955/contents/experiments.tex], §Ablations; [./archive/arxiv/src/2601.16955/contents/appendix.tex], tables ~352–377 및 ablation tables).
- 추가 메트릭(Strain energy, TV, SA, QED)
  - 근거: Extended results 테이블에 strain energy(ΔE), TV(원자/결합 분포), SA, QED 값이 포함되어 있으며, MOTIFLOW이 일부 메트릭에서 경쟁력을 보임. 단, strain energy는 MMFF 기반 relaxation으로 계산되며 이는 근사값임(부록 §Evaluation Metrics) ([./archive/arxiv/src/2601.16955/contents/appendix.tex], §Evaluation Metrics 및 Extended Results tables).

Limitations & Open Questions (논문에서 확인된 한계 및 미해결 쟁점)
- 불균형/희귀 모티프 처리
  - 근거: ablation에서 vocabulary 크기와 α threshold가 uncommon motif의 under-/oversampling에 직접적 영향(예: finer-grained / No Rings는 uncommon motif 과다샘플링; Planar Rings with small α는 under-sampling) — 따라서 rare-substructure 일반화는 제한적일 수 있음 ([./archive/arxiv/src/2601.16955/contents/experiments.tex], §Ablations; appendix).
- 화학적 타당성/에너지 기반 검증의 한계
  - 근거: strain energy는 MMFF로 계산(부록), MMFF/force-field 기반 relaxation은 DFT 수준의 정확도를 제공하지 않음. 물리적 / 합성 가능성(실험적 합성성) 검증은 추가 실험 필요 ([./archive/arxiv/src/2601.16955/contents/appendix.tex], §Evaluation Metrics).
- 재현성 관련 (필요 항목들이 있지만 몇 가지 민감 포인트 존재)
  - 필요 정보(있음): 모델 아키텍처/파라미터, 학습률, epoch 수, sampling 설정(steps, discrete temperature, remasking η) 등은 부록에 명시되어 있으나(예: lr=1e-4, QM9 1000 epochs, remasking η 값 논의), 훈련 스크립트/시드·데이터 전처리 스크립트(실제 코드)는 소스 패키지의 압축/visuals는 있으나(README에 빌드 지시) 공개되는 실행 스크립트·환경 종속성·GPU/시간 정보가 부족하면 완전 재현은 일부 추가 작업 필요 ([./archive/arxiv/src/2601.16955/contents/appendix.tex], [./archive/arxiv/src/2601.16955/00README.json]).
- 평가 프로토콜 일관성 문제
  - 근거: 논문은 RDKit/OpenBabel pipeline을 사용하지만 baseline 결과(각 논문)의 평가 세부(예: bond lookup table 사용 여부, connectivity 조건 등)가 다를 수 있음. 저자도 GEOM-Drugs에서 molecular stability를 직접 보고하지 않는다고 명시(부록) — 따라서 cross-paper 비교에는 표준화된 파이프라인 제어가 필요 ([./archive/arxiv/src/2601.16955/contents/appendix.tex], §Experimental Details).

Risks & Gaps — 검증 부족/가정과 권장 추가 실험
- 위험·갭
  1. Motif priors 편향: 빈도 기반 pruning(α)과 canonical exemplar 선택이 데이터셋 편향을 학습시킬 위험 — uncommon 화학기능이 소실될 수 있음 (ablation에서 관찰) ([./archive/arxiv/src/2601.16955/contents/method.tex], §Rigid-Motif Decomposition; appendix ablation tables).
  2. Bond 추론/valency 판단의 민감성: 생성 좌표 → bond type 추론이 RDKit/OpenBabel 룩업 기준에 의존하므로 평가 결과(예: atom stability)가 추론 규칙에 민감함(부록에 언급) — 특히 GEOM-Drugs에서는 molecular stability를 보고하지 않은 이유로 평가 절차의 한계가 명시됨 ([./archive/arxiv/src/2601.16955/contents/appendix.tex], §Evaluation Metrics).
  3. 실제 화학적 유효성(에너지/합성성): MMFF 기반 strain energy는 근사이며 DFT 수준의 물리적 타당성 검증(geometry optimization, single-point energy, reaction feasibility 등)은 수행되지 않음.
  4. 비교 공정성: 샘플링 steps 수를 줄여 얻은 시간/성능 우위가 모델 파라미터 수, 학습/추론 비용(함수평가 수, ODE solver steps), 하드웨어 차이 등을 통제하지 않으면 해석이 과대평가될 가능성.
- 권장 추가 실험 (Short actionable proposals; “Speculation/Recommendation” 구분)
  - (Speculation/Recommendation) Energy validation: MOTIFLOW 샘플에 대해 DFT 수준(예: B3LYP/6-31G*)의 single-point 에너지/geometry optimization을 소수 샘플에 적용해 MMFF와의 상관성 및 안정성 주장을 검증.
  - (Speculation/Recommendation) Controlled compute comparison: 동일한 파라미터 예산(파라미터 수), 동일한 평가 파이프라인에서 EDM/END/EquiFM과 wall-clock 및 FLOPs를 비교해 “샘플링 steps” 우위가 실제 계산비용 우위인지 확인.
  - (Speculation/Recommendation) Novelty/generalization: test set에 존재하지 않는(hold-out) rare motifs 또는 합성적으로 생성한 새로운 motifs로 generalization 성능 평가.
  - (Speculation/Recommendation) Ablate masking prior / discrete temperature schedule / remasking η와 self-conditioning의 기여도를 더 세밀히 분리.

Critics (반대 관점 — 핵심 헤드라인 + 짧은 설명·핵심 포인트)
- Headline 1: “Motif 기반은 구조적 제약 때문에 창발적(creative) 소분자 설계 능력을 제한할 수 있다.”
  - 설명: motif로 압축하면 자주 등장하는 subgraph는 잘 복원하지만 희귀한 결합 패턴이나 새로운 결합 조합을 생성하는 능력이 떨어질 수 있음(논문도 ablation에서 uncommon motif undersampling 보고). 실무적 의미: 새로운 화학적 아이디어 탐색(exploratory molecule design)엔 제약이 될 수 있음 ([./archive/arxiv/src/2601.16955/contents/experiments.tex], §Ablations).
- Headline 2: “샘플링 단계 수 감소의 실효성은 계산 비용 측면에서 온전히 입증되지 않았다.”
  - 설명: steps 수 감소는 분명하지만 실제 함수 평가 수(ODE solver evaluations), discrete CTMC 샘플링 오버헤드, GPU 메모리·병렬성 차이를 통제한 비교가 부족. 따라서 ‘실제 추론 시간/비용 우위’는 추가 검증 필요 ([./archive/arxiv/src/2601.16955/contents/appendix.tex], qm9_uncond_extended note re: EquiFM adaptive solver).
- Headline 3: “평가 메트릭(특히 atom stability, validity)은 bond 추론 규칙에 민감하다.”
  - 설명: RDKit/OpenBabel의 bond inference 및 sanitisation에 의존하는 현재 pipeline은 평가 결과에 편향을 줄 수 있음. GEOM-Drugs 관련 문단에서 저자도 이러한 한계를 언급함 ([./archive/arxiv/src/2601.16955/contents/appendix.tex], §Evaluation Metrics).

Appendix — 재현 체크리스트 및 용어표
- 필수 파일(소스에서 확인)
  1. 논문 PDF(원문): https://arxiv.org/pdf/2601.16955v1  ([./archive/arxiv/pdf/2601.16955v1.pdf])
  2. TeX 소스: main.tex 및 contents/*.tex ([./archive/arxiv/src/2601.16955/main.tex], [./archive/arxiv/src/2601.16955/contents/*.tex])
  3. 부록(Implementation Details / Extended Results): [./archive/arxiv/src/2601.16955/contents/appendix.tex]
  4. 시각자료: visuals 폴더의 PNG/PDF (frag_comparison.png, distribution_qmugs_middle_threshold.pdf, cond_generation images 등) — 결과 재확인용 ([./archive/arxiv/src/2601.16955/visuals/])
  5. 참고문헌: references.bib ([./archive/arxiv/src/2601.16955/references.bib])
  6. README(빌드 지시): [./archive/arxiv/src/2601.16955/00README.json]
- 핵심 재현 하이퍼파라미터(부록에 명시된 값들)
  - 모델 크기: unconditional ≈ 12.4M parameters, conditional ≈ 13.7M ([./archive/arxiv/src/2601.16955/contents/appendix.tex]).
  - Learning rate: 1e-4 (appendix).
  - Rotational exponential rate scheduler: factor 10 (appendix).
  - QM9 training: 1000 epochs; GEOM-Drugs: 135 epochs; QMugs ablations: epochs noted in appendix (부록 참조).
  - Sampling steps: effective range 50–100 (권장), discrete flow temperature schedule (linear) min=1.0, max=1.5 (appendix).
  - Fragmentation threshold α: default = 0.1 (method.tex); ablation: 0.5%, 0.1%, 0.01% (appendix tables).
  - Remasking probability η (discrete flow): QM9 experiments set η=0; GEOM-Drugs uses η=1.5 (appendix).
- 평가 재현 체크
  - RDKit 기반 sanitisation 및 bond inference(lookup table from EDM)을 동일하게 적용할 것 ([./archive/arxiv/src/2601.16955/contents/appendix.tex], §Evaluation Metrics).
  - Property calculation: SA/QED via standard implementations; strain energy via MMFF relaxation in RDKit.
  - 샘플 수/시드: unconditional sampling 10^4 molecules × 3 seeds (paper의 비교 설정) — 재현 시 동일 샘플 수·시드 고정 권장 ([./archive/arxiv/src/2601.16955/contents/experiments.tex], §Unconditional Generation).
- 구현·실행 환경(권장)
  - Build: pdflatex (TeXLive 2025 per README), Python 패키지: RDKit, OpenBabel, PyTorch 등(정확한 requirements.txt는 소스에 별도 제공 여부 확인 필요). 소스 패키지(압축본)가 존재하면 실행 스크립트 확인 권장 ([./archive/arxiv/src/2601.16955/00README.json], src_manifest).
- 용어/기호표 (간단)
  - SE(3): Special Euclidean group in 3D (R^3 ⋊ SO(3))
  - T = (R, x): rigid frame (R ∈ SO(3), x ∈ R^3)
  - m ∈ V_m: motif class; P canonical pose; S motif symmetry group
  - L_SE(3): flow-matching loss for geometric component (translation + rotation terms)
  - CTMC: continuous-time Markov chain for discrete flow (mask → target analytic rate matrix)

결론(요약 평가 및 권장)
- 평가 요약: MOTIFLOW은 rigid-motif 표현 + SE(3)-equivariant flow를 결합하여 대형 분자 데이터셋에서 효율적인 샘플링(샘플링 단계 수 현저히 감소)과 competitive한/우수한 구조 품질(특히 atom stability)을 달성했다는 강력한 증거를 제시한다. 근거는 논문 본문의 방법론 수식 및 부록의 확장표/ablation(정량수치), 그리고 시각자료(압축비·motif 분포)에서 확인된다 ([./archive/arxiv/src/2601.16955/contents/method.tex], [./archive/arxiv/src/2601.16955/contents/appendix.tex], [./archive/arxiv/src/2601.16955/visuals/entity_distributions/distribution_qmugs_middle_threshold.pdf]).
- 주요 우려 및 권장 조치: rare-motif 일반화, 에너지 기반 물리적 타당성 검증(DFT), 비교 실험의 계산비용 정교화(함수평가 수·wall-clock) 및 평가 파이프라인 표준화가 필요하다. 위 권장 추가 실험(appendix의 Speculation/Recommendation)을 실행하면 MOTIFLOW의 실무적 가치(신약 설계파이프라인에서의 적용 가능성)를 보다 명확히 입증할 수 있다.

참고(빠른 근거 위치 인덱스)
- Method(표현·multimodal flow·symmetry alignment): [./archive/arxiv/src/2601.16955/contents/method.tex]
- Experiments(데이터셋·metrics·ablation): [./archive/arxiv/src/2601.16955/contents/experiments.tex]
- Appendix(Implementation Details, Extended Results, Tables): [./archive/arxiv/src/2601.16955/contents/appendix.tex]
- Visuals (compression/ablation/conditional examples): [./archive/arxiv/src/2601.16955/visuals/...] (예: distribution_qmugs_middle_threshold.pdf, frag_comparison.png, cond_generation/main.png)
- 원문 PDF: https://arxiv.org/pdf/2601.16955v1  (백업 로컬: [./archive/arxiv/pdf/2601.16955v1.pdf])
- 메타데이터: [./archive/arxiv/papers.jsonl], manifest: [./archive/arxiv/src_manifest.jsonl]

원하시면 다음 단계로 아래 작업을 수행하겠습니다.
- (A) 재현성 체크리스트에 따라 실행 가능한 실행 스크립트(실험 재현용 명령어·환경 파일 템플릿) 초안 작성 — 필요 시 구현 가능한 Dockerfile / conda env 템플릿 포함.
- (B) 권장 추가 실험(DFT 검증·compute-controlled 비교·rare motif generalization)에 대한 상세 실험계획(데이터, 비용 산정, 예상 결과) 작성.
- (C) 논문 결과의 통계적 유의성 검증을 위한 부트스트랩/표준오차 확인 스크립트 초안 작성.

원하시는 다음 작업(A/B/C 중 하나 또는 모두)을 지정해 주세요.