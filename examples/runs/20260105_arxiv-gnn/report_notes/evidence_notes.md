## Run scope / inputs (provenance)

- **Instruction inputs**: keyword query “graph neural networks”, one explicit arXiv ID (**arXiv:2101.00001**), and one LinkedIn URL (molecular design post). The arXiv ID is **not GNN-related** (multi-armed bandits review). [instruction/20260105_arxiv-gnn.txt]
- **Captured primary technical corpus** (downloaded PDFs + extracted text): 3 GNN-related papers from OpenAlex + 1 arXiv paper (bandits). [archive/20260105_arxiv-gnn-index.md]

---

## Primary technical sources (papers) — extracted salient evidence

### 1) HISTOGRAPH: pooling via “historical activations” in deep GNNs (arXiv)
**Source**: *Learning from Historical Activations in Graph Neural Networks* (Galron et al., arXiv:2601.01123, 2026-01-03). PDF URL: https://arxiv.org/pdf/2601.01123  [archive/openalex/text/W7119235243.txt]

- **Core problem framing**
  - Typical graph pooling/readout uses only **last-layer node embeddings**, potentially “under-utilizing important activations of previous layers” (“historical graph activations”). This is especially harmful when node representations shift across many layers and with **over-smoothing** in deep GNNs. [archive/openalex/text/W7119235243.txt]
- **Main method: HISTOGRAPH (two-stage attention head)**
  - Introduces **HISTOGRAPH**, a “two-stage attention-based final aggregation layer”:
    1) **Layer-wise attention** over intermediate activations (“unified layer-wise attention over intermediate activations”), then
    2) **Node-wise attention** (self-attention across nodes). [archive/openalex/text/W7119235243.txt]
  - Can be used **(1) end-to-end** with backbone training or **(2) post-processing head on a frozen pretrained GNN**, training only the head for “substantial gains with minimal overhead.” [archive/openalex/text/W7119235243.txt]
- **Key formulation details (evidence-level)**
  - Treats historical activations as tensor **X ∈ R^{N×L×D}** (nodes × layers × features). [archive/openalex/text/W7119235243.txt]
  - Uses final-layer embedding as the **query** to attend over all layer states; computes a **layer weighting** vector by averaging attention scores across nodes. [archive/openalex/text/W7119235243.txt]
  - Notably uses a **signed normalization instead of softmax**, allowing negative layer contributions (“permits signed contributions… akin to finite-difference approximations in dynamical systems”). [archive/openalex/text/W7119235243.txt]
  - Graph representation obtained via **multi-head self-attention across nodes**, then average pooling to graph embedding. [archive/openalex/text/W7119235243.txt]
- **Complexity / scalability claim**
  - Two-stage decomposition yields per-graph complexity **O(N(L+N)D)**, dominated by **O(N²D)** (node attention), avoiding naive joint node-layer attention **O(L²N²D)**. [archive/openalex/text/W7119235243.txt]
  - Frozen-backbone mode caches **N×L×D** activations and avoids backprop through backbone, reducing memory/time for fine-tuning. [archive/openalex/text/W7119235243.txt]
- **Stated properties / implications**
  - Claims HISTOGRAPH can **mitigate over-smoothing** by assigning nonzero attention mass to early layers so final embeddings retain discriminative information; formalized as **Proposition 1**. [archive/openalex/text/W7119235243.txt]
  - Interprets layer attention as an **adaptive trajectory filter** (low-pass / high-pass / general FIR filter behavior depending on weights). [archive/openalex/text/W7119235243.txt]
- **Quantitative results (available in extraction)**
  - TU dataset table shows large gains in some cases (e.g., IMDB-B: HISTOGRAPH 87.2±1.7 vs best baseline ~80.9±2.3; multiple datasets listed). [archive/openalex/text/W7119235243.txt]

---

### 2) GNN surrogate models for LIGO interferometer optical simulations (arXiv)
**Source**: *Graph Neural Networks for Interferometer Simulations* (Kannan et al., arXiv:2512.16051, 2025-12-18). PDF URL: https://arxiv.org/pdf/2512.16051  [archive/openalex/text/W4417529673.txt]

- **Core claim / motivation**
  - Proposes GNNs for **instrumentation design** as a new physical-sciences application; as a case study, simulates LIGO-like interferometers and reports **“runtimes 815 times faster”** than state-of-the-art simulators, while capturing “complex optical physics.” [archive/openalex/text/W4417529673.txt]
  - Emphasizes design optimization requires “thousands of costly high-fidelity optical simulations” in “high-dimensional, non-convex” landscapes. [archive/openalex/text/W4417529673.txt]
- **Dataset contribution**
  - Provides “a dataset of high-fidelity optical physics simulations for **three interferometer topologies**” as a benchmarking suite. [archive/openalex/text/W4417529673.txt]
  - Dataset sampling: start from “ideal” configuration, then “stochastically perturb” parameters and run **FINESSE** simulations as ground truth. [archive/openalex/text/W4417529673.txt]
- **Graph construction / features (technical)**
  - Each mirror split into **four nodes** (two per side; incoming/outgoing fields separate); edges represent spatial field connections (reflected/transmitted links, propagation to next optic). [archive/openalex/text/W4417529673.txt]
  - Node features include optic properties (described as reflectivity/radius of curvature; later also mentions wavefront curvature, reflectivity, angle). Edge features include **length** and **index of refraction**. [archive/openalex/text/W4417529673.txt]
- **Models**
  - **Power prediction**: predicts **log P** (due to kW vs mW scale separation). Architecture: **20 GATv2 layers + 6 feed-forward layers**, residuals between layers. [archive/openalex/text/W4417529673.txt]
  - Uses a **physics-inspired regularization term** enforcing approximate **power conservation** via adjacency matrix penalty: loss includes MAE + λ‖ŷ − Aᵀŷ‖₁. [archive/openalex/text/W4417529673.txt]
  - **Intensity distribution prediction**: graph embedding via **15 GAT layers**, then **Deep Kolmogorov–Arnold Network (KAN)** to predict radial intensity distribution; rotated to full 2D to enforce azimuthal symmetry and reduce DOF from O(n²) to O(n). [archive/openalex/text/W4417529673.txt]
- **Results / evidence**
  - Reports L1 losses by topology and architecture; notes **GNN models outperform MLP/KAN without graph structure**, especially for generalization to unseen topologies. [archive/openalex/text/W4417529673.txt]
  - Intensity model: L1 loss **27.2 W/m²** vs MLP replacement **58.4 W/m²** (same parameter count). [archive/openalex/text/W4417529673.txt]
  - Speed table: single simulation times FINESSE **2.857 s**, SIS **14.932 s**, GNN power **0.018 s**, GNN intensity **0.011 s** (GPU: NVIDIA A30). [archive/openalex/text/W4417529673.txt]
- **Limitations / open problems explicitly stated**
  - Key limitation: **generalization**—does not achieve as low loss on **unseen optical topologies** as on training topologies; improving topology-agnostic understanding of field propagation is future work. [archive/openalex/text/W4417529673.txt]
  - Suggests exploring better physics encoding / alternative representations (e.g., “mesh based approach similar to Pfaff et al. (2021)”). [archive/openalex/text/W4417529673.txt]

---

### 3) ATLAS jet flavour tagging with GNNs (PoS proceedings PDF)
**Source**: *Flavour-Tagging with Graph Neural Network with the ATLAS Detector* (Helena Santos on behalf of ATLAS, PoS(DIS2025)080, 2025-12-05). PDF URL: https://pos.sissa.it/512/080/pdf  [archive/openalex/text/W4417330266.txt]

- **Problem + impact**
  - b-jet identification is “key” for Higgs/top analyses and BSM searches; performance improvements come from “state-of-the-art machine learning algorithms based on graph neural networks.” [archive/openalex/text/W4417330266.txt]
- **Architecture evolution / methods**
  - Moves from Run-2 DNN taggers (DL1 series) to graph approaches:
    - **GN1**: based on **Graph Attention Network** aggregating neighbor information. [archive/openalex/text/W4417330266.txt]
    - **GN2**: “transformer-inspired attention mechanism” + improved training strategies (one-cycle LR schedule, layer norm, dropout) for convergence/stability. [archive/openalex/text/W4417330266.txt]
  - Models are **multimodal** (jets + tracks + vertices) and **multitask** (jet flavour classification + track origin prediction + vertex finding); includes **auxiliary losses** for track and vertex tasks. [archive/openalex/text/W4417330266.txt]
- **Quantitative performance claims**
  - In t-tbar sample at **70% working point**, GN2 improves **light-jet rejection ~2×** and **c-jet rejection ~3×** vs DL1d. [archive/openalex/text/W4417330266.txt]
  - In Z′ sample at **30% working point**, improvements are larger: **light-jet rejection ~4×** and **c-jet rejection ~3.5×** vs DL1d. [archive/openalex/text/W4417330266.txt]
- **Ablation insight**
  - Removing auxiliary objectives significantly reduces rejection performance; “combined auxiliary objectives yield optimal performance.” [archive/openalex/text/W4417330266.txt]
- **Generalization / deployment context (HL-LHC)**
  - HL-LHC conditions (⟨μ⟩ up to 200) motivate robustness; GN1 trained on simulated HL-LHC + new ITk geometry and shows ability to “generalize to a completely new detector geometry.” [archive/openalex/text/W4417330266.txt]

---

## Metadata / coverage audit (OpenAlex index)
**Source**: OpenAlex works metadata for this run (duplicates + extra non-downloaded items). [archive/openalex/works.jsonl]

- **Duplicate work entries** exist for the interferometer paper (multiple OpenAlex IDs for the same arXiv work); the downloaded/full-text one is **W4417529673** with PDF URL https://arxiv.org/pdf/2512.16051. [archive/openalex/works.jsonl]
- **Extra GNN-related items not downloaded**: two Zenodo entries for “chutongjia/CLGNN: Contrastive learning graph neural network” (DOIs https://doi.org/10.5281/zenodo.17935355 and https://doi.org/10.5281/zenodo.17935354), only abstracts present in metadata here. [archive/openalex/works.jsonl]
- HISTOGRAPH also appears duplicated in OpenAlex metadata; downloaded/full-text is **W7119235243** with PDF URL https://arxiv.org/pdf/2601.01123. [archive/openalex/works.jsonl]

---

## Off-topic / tangential sources (captured but not central to GNN technical deep dive)

### arXiv:2101.00001 (bandits, French survey)
**Source**: https://arxiv.org/pdf/2101.00001v1  [archive/arxiv/text/2101.00001v1.txt]

- Survey on **multi-armed bandits**; focuses on sequential decision-making and exploration–exploitation tradeoff; not about GNNs. [archive/arxiv/text/2101.00001v1.txt]

### LinkedIn post (molecular design “Trio” framework)
**Source**: https://www.linkedin.com/posts/fanli_ai-molecular-design-has-some-known-challenges-activity-7406324682192441344-60n3  [archive/tavily_extract/0001_https_www.linkedin.com_posts_fanli_ai-molecular-design-has-some-known-challenges-activity-7406324682192441344-60n3_utm_s.txt]

- Discusses molecular design challenges and a framework using MLM + DPO + MCTS; no direct GNN technical content in extracted snippet (primarily about optimization/interpretability decomposition). [archive/tavily_extract/0001_https_www.linkedin.com_posts_fanli_ai-molecular-design-has-some-known-challenges-activity-7406324682192441344-60n3_utm_s.txt]