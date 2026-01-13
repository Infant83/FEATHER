## Run scope / corpus confirmation (manifests + logs)
- **Run configuration**: FEATHER invoked with `--days 30 --max-results 8 --download-pdf --openalex --oa-max-results 8` for query **“graph neural networks”**, plus explicit arXiv ID **2101.00001** and one LinkedIn URL. Source instruction lines confirm the same. [archive/_job.json]
- **What was actually archived (primary research PDFs/text)**: 3 OpenAlex PDFs (with extracted text) + 1 arXiv PDF (with extracted text). [archive/20260105_arxiv-gnn-index.md]
- **Retrieval notes / issues**
  - OpenAlex duplicates / reuse happened for the interferometer paper (PDF reuse logged). [archive/_log.txt]
  - Citation lookup failed for arXiv ID 2101.00001 due to OpenAlex API request error. [archive/_log.txt]
- **Primary research sources and URLs (as archived)**
  - *Learning from Historical Activations in Graph Neural Networks* — arXiv PDF: https://arxiv.org/pdf/2601.01123 [archive/20260105_arxiv-gnn-index.md], content in [archive/openalex/text/W7119235243.txt]
  - *Graph Neural Networks for Interferometer Simulations* — arXiv PDF: https://arxiv.org/pdf/2512.16051 [archive/20260105_arxiv-gnn-index.md], content in [archive/openalex/text/W4417529673.txt]
  - *Flavour Tagging with Graph Neural Network with the ATLAS Detector* — PoS PDF: https://pos.sissa.it/512/080/pdf [archive/20260105_arxiv-gnn-index.md], content in [archive/openalex/text/W4417330266.txt]
  - *Etat de l’art sur l’application des bandits multi-bras* — arXiv PDF: https://arxiv.org/pdf/2101.00001v1 [archive/20260105_arxiv-gnn-index.md], content in [archive/arxiv/text/2101.00001v1.txt]

## OpenAlex metadata (coverage / deduplication evidence)
- **Duplicate entries exist** for:
  - *Graph Neural Networks for Interferometer Simulations* under multiple OpenAlex IDs (e.g., W7116276642, W4417529673, W7116584439) with same abstract/landing page; one record includes `pdf_url=https://arxiv.org/pdf/2512.16051`. [archive/openalex/works.jsonl]
  - *Learning from Historical Activations in Graph Neural Networks* appears as W7119235243 and W7119230132 (one with DOI landing page). [archive/openalex/works.jsonl]
- **Additional non-paper / software artifacts surfaced** (Zenodo “chutongjia/CLGNN”) without PDFs in this run; likely out-of-scope for “main ideas/methods” synthesis unless explicitly included. [archive/openalex/works.jsonl]

## Evidence from primary GNN research papers (key ideas/methods/results)
### 1) HISTOGRAPH (historical activations for readout/pooling) — arXiv:2601.01123
Source: https://arxiv.org/pdf/2601.01123 ; extracted text [archive/openalex/text/W7119235243.txt]
- **Problem statement (pooling underuses intermediate layers)**: prior pooling schemes “rely on the last GNN layer features… under-utilizing important activations of previous layers… historical graph activations,” with the gap worsened by deep-layer representation drift and “over-smoothing.” [archive/openalex/text/W7119235243.txt]
- **Core method**: **HISTOGRAPH** is a “two-stage attention-based final aggregation layer”:
  - stage 1: “unified layer-wise attention over intermediate activations”
  - stage 2: “node-wise attention.” [archive/openalex/text/W7119235243.txt]
- **Mechanistic framing**: models “the evolution of node representations across layers” and uses both “activation history of nodes and the graph structure” to refine features for prediction. [archive/openalex/text/W7119235243.txt]
- **Usage modes**:
  - (1) “end-to-end joint training with the backbone”
  - (2) “post-processing as a lightweight head on a frozen pretrained GNN” where only the head is trained for “substantial gains with minimal overhead.” [archive/openalex/text/W7119235243.txt]
- **Claimed empirical outcome (high level)**: “consistently outperforms strong GNN and pooling baselines on TU and OGB benchmarks… with particularly strong robustness in deep GNNs.” [archive/openalex/text/W7119235243.txt]
- **Positioning vs prior pooling**: Table asserts HISTOGRAPH is the only listed method combining “intermediate representations” + “structural considerations” + “Layer-Node modeling.” [archive/openalex/text/W7119235243.txt]

### 2) GNN surrogate simulation for LIGO interferometers — arXiv:2512.16051
Source: https://arxiv.org/pdf/2512.16051 ; extracted text [archive/openalex/text/W4417529673.txt]
- **Application framing**: proposes GNNs for **instrumentation design** (new application area) as a case study on LIGO interferometer simulation. [archive/openalex/text/W4417529673.txt]
- **Runtime claim**: GNN surrogate achieves “runtimes **815 times faster** than state of the art simulation packages.” [archive/openalex/text/W4417529673.txt]
- **Dataset contribution**: releases “a dataset of high-fidelity optical physics simulations for **three interferometer topologies**” as a benchmark suite. [archive/openalex/text/W4417529673.txt]
- **Graph construction details**:
  - “each mirror is split into four nodes, two for each side… incoming and outgoing fields treated as separate nodes”
  - edges represent spatial connections between fields (reflected/transmitted and propagation between optics). [archive/openalex/text/W4417529673.txt]
- **Recorded physical quantities**: at each node, records “complex field amplitudes, beam parameter and powers of the even HG modes, up to sixth order,” with helper functions to convert to “2D spatial intensity distribution.” [archive/openalex/text/W4417529673.txt]
- **Data generation**:
  - sampling by starting at an “ideal” configuration then “stochastically perturb” parameters and run FINESSE each step for ground truth; “30,000 samples” collected (per setup statement). [archive/openalex/text/W4417529673.txt]
- **Modeling choices (power prediction)**:
  - predicts **log P** due to scale separation (kW inside cavities vs mW exiting). [archive/openalex/text/W4417529673.txt]
  - architecture: “**20 GATv2 layers** … followed by **6 feed-forward layers**” with LeakyReLU and residual connections between consecutive message passing layers and between linear layers. [archive/openalex/text/W4417529673.txt]

### 3) ATLAS flavour tagging with GNNs (GN1/GN2) — PoS(DIS2025)080
Source: https://pos.sissa.it/512/080/pdf ; extracted text [archive/openalex/text/W4417330266.txt]
- **Task importance and context**: b-jet identification is key for Higgs/top/BMS searches; signature comes from b-hadron lifetime leading to displaced tracks/vertices. [archive/openalex/text/W4417330266.txt]
- **Shift from DNN pipeline to graph-based**: prior two-step paradigm separated low-level reconstruction and high-level classification; ATLAS explores GNNs where jets are graphs (“nodes correspond to tracks and the edges learn the relationships between them”). [archive/openalex/text/W4417330266.txt]
- **Model evolution**:
  - **GN1**: “based on a Graph Attention Network architecture” aggregating neighbor info. [archive/openalex/text/W4417330266.txt]
  - **GN2**: “adopts a transformer-inspired attention mechanism” plus training optimizations (one-cycle LR schedule, layer norm, dropout) for speed/stability. [archive/openalex/text/W4417330266.txt]
- **Multimodal + multitask training**: processes “jets, tracks, and vertices”; jointly optimizes jet flavour classification plus auxiliary objectives (track origin prediction, vertex finding / track-pair compatibility). [archive/openalex/text/W4417330266.txt]
- **Quantitative performance claims**:
  - In a tt̄ sample at 70% WP: GN2 improves **light-jet rejection ~2×** and **c-jet rejection ~3×** vs DL1d. [archive/openalex/text/W4417330266.txt]
  - In a Z′ sample at 30% WP: light-jet rejection **~4×**, c-jet rejection **~3.5×** vs DL1d. [archive/openalex/text/W4417330266.txt]
- **Ablation evidence for auxiliary losses**: removing one/both auxiliary objectives “significantly reduced c- and light-jet rejection”; “combined auxiliary objectives yield optimal performance.” [archive/openalex/text/W4417330266.txt]
- **HL-LHC generalization claims**:
  - describes HL-LHC conditions (⟨μ⟩ up to 200; luminosity up to 7.5×10^34 cm⁻²s⁻¹) and detector upgrade to ITk; GN1 trained on HL-LHC+ITk simulation. [archive/openalex/text/W4417330266.txt]
  - reports b-tagging efficiency vs pT at fixed light-jet rejection 100: ~90% at 250 GeV, ~50% at 5 TeV; stable >75% up to |η|<3.5; “minimal impact” from pile-up contamination; “generalize to a completely new detector geometry.” [archive/openalex/text/W4417330266.txt]

## Off-topic / drift item (arXiv ID explicitly provided)
### arXiv:2101.00001v1 — Multi-armed bandits survey (not GNN)
Source: https://arxiv.org/pdf/2101.00001v1 ; extracted text [archive/arxiv/text/2101.00001v1.txt]
- Paper is explicitly a survey on “bandits multi-bras” (multi-armed bandits), introducing applications and exploration–exploitation taxonomy; not about graph neural networks. [archive/arxiv/text/2101.00001v1.txt]
- Metadata summary confirms bandit focus (epsilon-greedy, UCB, Thompson Sampling) and real-life applications; again not GNN-related. https://arxiv.org/abs/2101.00001v1 [archive/arxiv/papers.jsonl]

## Non-primary web extract (LinkedIn) — adjacent but not clearly GNN-centric
Source: https://www.linkedin.com/posts/fanli_ai-molecular-design-has-some-known-challenges-activity-7406324682192441344-60n3?utm_source=share&utm_medium=member_desktop&rcm=ACoAADrVxc4BEqb4PF0MiiEBRbbQJ7tfp6CkF3Q ; extracted [archive/tavily_extract/0001_https_www.linkedin.com_posts_fanli_ai-molecular-design-has-some-known-challenges-activity-7406324682192441344-60n3_utm_s.txt]
- Post summarizes “Trio” closed-loop molecular design framework decomposing challenges into components: fragment-based molecular language model for validity, DPO for synthesizability alignment, MCTS for multi-objective optimization, and interpretability via the search tree; claims improvements in binding affinity/drug-likeness/synthetic accessibility and “fourfold” diversity. [archive/tavily_extract/0001_https_www.linkedin.com_posts_fanli_ai-molecular-design-has-some-known-challenges-activity-7406324682192441344-60n3_utm_s.txt]
- This is **not** an archived primary GNN source in the run; use only as peripheral context if broadening beyond GNN methods. [archive/tavily_extract/0001_https_www.linkedin.com_posts_fanli_ai-molecular-design-has-some-known-challenges-activity-7406324682192441344-60n3_utm_s.txt]