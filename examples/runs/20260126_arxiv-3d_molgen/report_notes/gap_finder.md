Gaps Summary
Claims missing evidence:
- **arXiv (PDF/TeX: 1차 근거)**
- **핵심 문제의식/기여(요약) + 정량 주장(steps/압축/성능)**
- 원자 단위(atomic point cloud) 3D 생성은 잘 되지만 “화학적 모듈성(modularity)”을 버린다는 문제의식에서, 분자를 **rigid motif(강체 모티프)들의 집합**으로 재표현하고 **SE(3)-equivariant generative modeling**을 적용한다고 설명. 또한 평가에서 SOTA에 “comparable or superior”, 특히 **GEOM-DRUGS에서 atom stability를 상회**, 그리고 **generation steps를 2×~10× 감소**, **representation을 3.5× 압축**했다고 주장.
- **방법론: 분자를 rigid motifs의 SE(3) 프레임 + motif class로 재파라미터화(표현 정의/가역성)**
- 분자 원자 표현 \(\{(\mathbf{y}_j,h_j)\}_{j=1}^N\)을 **\(K\)개의 rigid motifs** \(\{(\mathbf{T}_i,m_i)\}_{i=1}^K\)로 바꾸며, \(\mathbf{T}_i=(\mathbf{R}_i,\mathbf{x}_i)\in \mathrm{SE}(3)\) (회전 \(\mathbf{R}_i\in \mathrm{SO}(3)\), 평행이동 \(\mathbf{x}_i\in\mathbb{R}^3\))로 정의. motif 토큰 \(m_i\in\mathcal{V}_m\)는 “exemplar fragment”로서 intra-fragment 원자 좌표/원자종/대칭군을 포함한다고 명시.
- 이 프레임 기반 표현은 **invertible**이며, canonical pose \(\mathbf{P}_i\)에 rigid transform을 적용해 원자 좌표를 복원:
- 따라서 생성은 \(\mathrm{SE}(3)^K \times \mathcal{V}_m^K\) 위 분포 샘플링으로 정식화한다고 서술.
- **방법론: motif vocabulary를 위한 fragmentation 요구조건과 설계 목표**
- motif vocabulary \(\mathcal{V}_m\) 구축을 위해 fragmentation scheme이 (i) **rigidity**(내부 rotatable bond가 없어 강체 근사), (ii) **non-degeneracy**(SE(3) frame 정의를 위해 최소 3개 비공선 점), (iii) **tractability**(데이터에서 각 motif class 빈도가 학습 가능할 만큼 충분) 조건을 만족해야 한다고 명시.
- **실험 설계: 데이터셋/태스크/베이스라인/메트릭(정의 및 보고 관례)**
- ... and 18 more