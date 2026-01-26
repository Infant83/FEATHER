Claim | Evidence | Strength | Flags
--- | --- | --- | ---
**arXiv (PDF/TeX: 1차 근거)** | (none) | none | no_evidence
**핵심 문제의식/기여(요약) + 정량 주장(steps/압축/성능)** | (none) | none | no_evidence
원자 단위(atomic point cloud) 3D 생성은 잘 되지만 “화학적 모듈성(modularity)”을 버린다는 문제의식에서, 분자를 **rigid motif(강체 모티프)들의 집합**으로 재표현하고 **SE(3)-equivariant generative modeling**을 적용한다고 설명. 또한 평가에서 SOTA에 “comparable or superior”, 특히 **GEOM-DRUGS에서 atom stability를 상회**, 그리고 **generation steps를 2×~10× 감소**, **representation을 3.5× 압축**했다고 주장. | (none) | none | no_evidence
근거: arXiv PDF 텍스트 추출 1페이지(초록/서론 도입) 인용 가능 구간(최종 인용은 PDF 권장)  (원문 URL: http://arxiv.org/abs/2601.16955v1 , PDF: https://arxiv.org/pdf/2601.16955v1) | archive/arxiv/text/2601.16955v1.txt; http://arxiv.org/abs/2601.16955v1; https://arxiv.org/pdf/2601.16955v1 | high | -
**방법론: 분자를 rigid motifs의 SE(3) 프레임 + motif class로 재파라미터화(표현 정의/가역성)** | (none) | none | no_evidence
분자 원자 표현 \(\{(\mathbf{y}_j,h_j)\}_{j=1}^N\)을 **\(K\)개의 rigid motifs** \(\{(\mathbf{T}_i,m_i)\}_{i=1}^K\)로 바꾸며, \(\mathbf{T}_i=(\mathbf{R}_i,\mathbf{x}_i)\in \mathrm{SE}(3)\) (회전 \(\mathbf{R}_i\in \mathrm{SO}(3)\), 평행이동 \(\mathbf{x}_i\in\mathbb{R}^3\))로 정의. motif 토큰 \(m_i\in\mathcal{V}_m\)는 “exemplar fragment”로서 intra-fragment 원자 좌표/원자종/대칭군을 포함한다고 명시. | (none) | none | no_evidence
이 프레임 기반 표현은 **invertible**이며, canonical pose \(\mathbf{P}_i\)에 rigid transform을 적용해 원자 좌표를 복원: | (none) | none | no_evidence
따라서 생성은 \(\mathrm{SE}(3)^K \times \mathcal{V}_m^K\) 위 분포 샘플링으로 정식화한다고 서술. | (none) | none | no_evidence
근거: 방법 섹션(정의/수식/상태공간)  (원문 URL: http://arxiv.org/abs/2601.16955v1) | archive/arxiv/src/2601.16955/contents/method.tex; http://arxiv.org/abs/2601.16955v1 | high | -
**방법론: motif vocabulary를 위한 fragmentation 요구조건과 설계 목표** | (none) | none | no_evidence
motif vocabulary \(\mathcal{V}_m\) 구축을 위해 fragmentation scheme이 (i) **rigidity**(내부 rotatable bond가 없어 강체 근사), (ii) **non-degeneracy**(SE(3) frame 정의를 위해 최소 3개 비공선 점), (iii) **tractability**(데이터에서 각 motif class 빈도가 학습 가능할 만큼 충분) 조건을 만족해야 한다고 명시. | (none) | none | no_evidence
근거: fragmentation 요구조건 나열 | archive/arxiv/src/2601.16955/contents/method.tex | low | -
**실험 설계: 데이터셋/태스크/베이스라인/메트릭(정의 및 보고 관례)** | (none) | none | no_evidence
**Unconditional generation**: QM9, GEOM-Drugs를 사용. QM9은 134k(최대 29 atoms, heavy atoms 최대 9), GEOM-Drugs는 430k(최대 181 atoms, 평균 44.4)로 서술. | (none) | none | no_evidence
**Conditional 실험**: QM9에서 속성 조건 생성(섹션 참조). | (none) | none | no_evidence
**대형 분자/fragmentation 연구**: GEOM-Drugs와 QMugs(665k, heavy atoms 최대 100; 실험에는 300k conformations subset 사용). | (none) | none | no_evidence
**Baselines**: interatomic distances로 bond를 추론하는 동일 패러다임 모델들(edm, edm_bridge, geoldm, equifm, end, geobfn 등)과 비교한다고 명시. | (none) | none | no_evidence
**Sampling/리포팅 프로토콜**: \citet{end} 따라 3 seeds에 걸쳐 \(10^4\) 샘플 생성, mean/std 보고. baseline은 논문들에서 보고된 설정 중 QM9은 molecular stability, GEOM-Drugs는 atom stability가 최선인 step 구성을 채택했다고 서술. | (none) | none | no_evidence
**Metrics**: stable atoms(A), stable molecules(M), valid(V), valid&unique(V×U)는 RDKit 기반. GEOM-Drugs는 관례 따라 valid&connected(V×C) 보고, 또한 distance 기반 bond 추론에서는 GEOM-Drugs의 molecular stability가 “non-informative”라서 보고하지 않는다고 명시. | (none) | none | no_evidence
근거: 실험 섹션 도입/메트릭 정의/프로토콜  (원문 URL: http://arxiv.org/abs/2601.16955v1) | archive/arxiv/src/2601.16955/contents/experiments.tex; http://arxiv.org/abs/2601.16955v1 | high | -
**결과 해석(일부): QM9에서의 trade-off 설명(steps 대비 성능/uniqueness)** | (none) | none | no_evidence
QM9은 “fairly saturated”라 주로 completeness 차원에서 보고하며, \oursacro(MotiFlow)가 **10× 더 많은 generation steps를 쓰는 방법들과 비슷한 수준**이고, EquiFM 대비 molecular stability는 높지만 uniqueness는 낮을 수 있으며, 이는 “rigid motifs를 큰 빌딩블록으로 사용”한 결과이고 discrete flow의 sampling temperature 등으로 조절 가능하다고 서술. | (none) | none | no_evidence
근거: QM9 결과 해석 문장(테이블은 이후) | archive/arxiv/src/2601.16955/contents/experiments.tex | low | -
**부록: Flow Matching/CFM 목적함수(재현에 중요한 수식)** | (none) | none | no_evidence
유클리드 공간에서 flow matching을 ODE 벡터필드 \(u_t\)로 기술하고, 학습은 네트워크 \(v_\theta(\mathbf{x}_t,t)\)를 \(u_t\)에 회귀시키는 MSE 형태 \(\mathcal{L}_{FM}\)로 제시. 또한 intractable한 \(u_t, p_t\) 대신 **conditional flow matching(CFM)** 목적 \(\mathcal{L}_{CFM}\)을 사용 가능함을 식으로 정리. | (none) | none | no_evidence
근거: Supplementary “Flow Matching in Euclidean Spaces” | archive/arxiv/src/2601.16955/contents/appendix.tex | low | -
**부록: 구현 디테일(아키텍처/파라미터/입력/ self-conditioning 등)** | (none) | none | no_evidence
backbone은 **FoldFlow-Base**(IPA 기반)이며, 분자 생성용으로 수정: head당 hidden dim 64, 8 heads → unconditional 모델 **12.4M params**, conditional 변형은 추가 projection으로 **13.7M params**라고 명시. | (none) | none | no_evidence
입력은 noisy rigid frames \(\mathbf{T}_t\)와 discrete motif tokens \(m_t\). node embedding은 motif token embedding + sinusoidal timestep embedding + (훈련 중 50% 확률) self-conditioning embedding을 투영해 초기화한다고 서술. | (none) | none | no_evidence
단백질처럼 residue index offset 기반 edge 초기화가 불가(모티프에는 선형 순서가 없음)하여 이를 대체했다고 언급(이후 문단은 추가 필요). | (none) | none | no_evidence
근거: “Implementation Details – Architecture / Embeddings and Input Processing” | archive/arxiv/src/2601.16955/contents/appendix.tex | low | -
**로컬 인덱스/메타(커버리지 확인용; 직접 인용 비권장)** | (none) | none | no_evidence
아카이브 인덱스에 따르면 본 run에는 arXiv PDF 1건과 텍스트/소스가 포함되며, tavily extract에도 arXiv PDF 텍스트 추출본이 있다고 기록. | (none) | none | no_evidence
근거(커버리지 확인): | archive/20260126_arxiv-3d_molgen-index.md | low | -
**오프토픽(Tavily: 본문 근거 사용 금지)** | (none) | none | no_evidence
LinkedIn URN/StackOverflow/Microsoft Learn 관련 검색결과는 논문 기술 검토의 1차 근거가 아니므로 제외(스카우트 노트 지침 준수). | (none) | none | no_evidence