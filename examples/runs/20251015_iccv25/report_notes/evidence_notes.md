## Run audit / coverage diagnosis (collection gaps)

- **Run inventory shows no web URLs were ingested beyond Tavily summaries (URLs: 0), and no arXiv IDs were explicitly harvested (arXiv IDs: 0)**, despite Tavily discovering key ICCV hubs. This indicates FEATHER did not follow/parse those hub pages to collect individual paper/project/code URLs.  
  - Evidence: run index shows “Queries: 4 | URLs: 0 | arXiv IDs: 0” and only OpenAlex PDFs/texts downloaded. [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/20251015_iccv25-index.md]

- **OpenAlex download drift + access failures**: the OpenAlex query “international conference on computer vision 2025” pulled multiple off-scope PDFs (education, oncology, e-commerce retrieval) and hit 403s for some publishers (MIT Press, MDPI).  
  - Evidence (403 examples): MIT Press “direct.mit.edu … 403 Forbidden”; MDPI PDFs repeatedly 403. [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/_log.txt]

- **Conclusion:** The local OpenAlex PDFs are *not* representative of “key ICCV 2025 main-conference papers”; they are mostly (i) ICCV 2025 workshop/challenge reports on arXiv plus (ii) unrelated journal articles.  
  - Evidence: OpenAlex list includes Nature Cancer, TechTrends, IJFMR, etc., alongside ICCV workshop/challenge arXiv PDFs. [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/20251015_iccv25-index.md]

---

## Canonical ICCV 2025 landscape entry points (authoritative hubs found in Tavily)

- **ICCV official site (dates + venue)**: ICCV 2025 in Honolulu, Oct 19–23, 2025.  
  - Source: https://iccv.thecvf.com/ (captured in tavily results) [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/tavily_search.jsonl]

- **CVF Open Access “All Papers” page exists and exposes per-paper links ([pdf]/[supp]/[arXiv])** and BibTeX blocks for ICCV 2025 proceedings entries.  
  - Source: https://openaccess.thecvf.com/ICCV2025?day=all (captured in tavily results) [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/tavily_search.jsonl]

- **Curated accepted-paper list with “Project Page” links (useful for code links)**: MMLab@NTU’s ICCV 2025 accepted papers page includes entries with “[arXiv] [Project Page]”.  
  - Source: https://www.mmlab-ntu.com/conference/iccv2025/index.html (captured in tavily results) [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/tavily_search.jsonl]

- **OpenReview group exists for ICCV 2025 conference** (useful for metadata and discussion, but code links vary).  
  - Source: https://openreview.net/group?id=thecvf.com/ICCV/2025/Conference (captured in tavily results) [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/tavily_search.jsonl]

- **Community “papers with code” aggregators surfaced** (high coverage of GitHub links, but not primary sources):
  - https://github.com/amusi/ICCV2025-Papers-with-Code (captured in tavily results) [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/tavily_search.jsonl]

---

## Locally downloaded OpenAlex items (what *is* relevant to ICCV 2025)

### A) Dataset / code releases (practically impactful)

- **R-LiViT: A LiDAR-Visual-Thermal Dataset**  
  - Claims: “first dataset to combine LiDAR, RGB, and thermal imaging from a roadside perspective, with a strong focus on VRUs”; includes “10,000 LiDAR frames and 2,400 … aligned RGB and thermal images across 150 traffic scenarios.”  
  - Public artifacts: dataset DOI + GitHub code to reproduce evaluation.  
  - Evidence: dataset DOI `https://doi.org/10.5281/zenodo.16356714` and code repo `https://github.com/XITASO/r-livit` explicitly listed in the paper text.  
  - Sources: https://arxiv.org/pdf/2503.17122 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4417156065.txt] (also OpenAlex metadata: https://openalex.org/W4417156065 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/works.jsonl])

### B) Workshop/challenge benchmarks + code links

- **VQualA 2025 ISRGC-Q (SR Generated Content Quality Assessment) challenge report**  
  - Scope: SR-IQA emphasizing artifacts from modern generative SR (GAN + diffusion), addressing lag of older SR-IQA datasets.  
  - Public artifact: project GitHub repo explicitly provided: `https://github.com/Lighting-YXLI/ISRGen-QA`.  
  - Sources: https://arxiv.org/pdf/2509.06413 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4414756887.txt] (OpenAlex metadata: https://openalex.org/W4414756887 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/works.jsonl])

- **VQualA 2025 Engagement Prediction for Short Videos (SnapUGC) challenge report**  
  - Practical problem: engagement prediction for short-form UGC; highlights cold-start issues and mismatch between MOS-based VQA and real popularity.  
  - Dataset/metrics: introduces engagement metrics derived from real user interactions; defines **NAWP** and **ECR** (ECR: probability viewer watches beyond first 5 seconds).  
  - Public artifact: project page GitHub link shown in text: `https://github.com/dasongli1/SnapUGC_Engagement/tree/main/ECR_inference`.  
  - Sources: https://arxiv.org/pdf/2509.02969 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4417409712.txt] (OpenAlex metadata: https://openalex.org/W4417409712 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/works.jsonl])

- **SAMSON (LSVOS 2025 VOS Challenge, MOSE track) solution report**  
  - Method: SAM2-based framework with long-term memory for re-identification; uses SAM2Long post-processing to reduce error accumulation.  
  - Reported result: final performance **J&F = 0.8427** on test-set leaderboard; also gives J=0.8182 and F=0.8671 on MOSEv1 track.  
  - Practical issue highlighted: trade-off between memory length and computational cost; memory overload/distractor interference in long sequences.  
  - Sources: https://arxiv.org/pdf/2509.17500 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4415254644.txt] (OpenAlex metadata: https://openalex.org/W4415254644 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/works.jsonl])

- **DRL4Real workshop summary (disentangled representation learning in realistic scenarios)**  
  - Stated motivation: DRL progress has “largely remained confined to synthetic datasets”; transition to realistic scenarios hindered by “lack of robust benchmarks and unified evaluation metrics.”  
  - Themes in accepted papers include: diffusion models + inductive biases (e.g., language), 3D-aware disentanglement, applications to autonomous driving and EEG.  
  - Sources: https://arxiv.org/pdf/2509.10463 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4415090288.txt] (OpenAlex metadata: https://openalex.org/W4415090288 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/works.jsonl])

### C) Survey-style “gaps” synthesis (not ICCV-specific, but useful for research gaps)

- **Vision-Language Modeling Meets Remote Sensing (survey)**  
  - Provides taxonomy: contrastive learning, visual instruction tuning, text-conditioned image generation; emphasizes two-stage paradigm (pre-train on massive image-text then fine-tune).  
  - Explicit future directions listed: cross-modal representation alignment; vague requirement comprehension; explanation-driven model reliability; continually scalable capabilities; large-scale datasets with richer modalities and greater challenges.  
  - Sources: https://arxiv.org/pdf/2505.14361 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4411143162.txt] (OpenAlex metadata: https://openalex.org/W4411143162 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/works.jsonl])

---

## “Key papers + code links” evidence surfaced in Tavily (examples; not downloaded locally)

- **Example official code repo explicitly labeled for an ICCV 2025 paper**: “One Trajectory, One Token…” codebase.  
  - Source: https://github.com/RAIVNLab/trajvit (captured in tavily results) [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/tavily_search.jsonl]

- **Example official code repo with award note**: RayZer repo states “ICCV’2025 (Best student paper honorable mention)” and provides implementation details + known issues.  
  - Source: https://github.com/hwjiang1510/RayZer (captured in tavily results) [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/tavily_search.jsonl]

- **Example ICCV 2025 code repo (video coding)**: HyTIP repo says “accepted to ICCV 2025” and contains source code + citation.  
  - Source: https://github.com/NYCU-MAPL/HyTIP (captured in tavily results) [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/tavily_search.jsonl]

---

## Extracted research gaps / limitations (grounded in the local texts)

- **Roadside multimodal perception gap (LiDAR+RGB+Thermal, VRU-centric)**  
  - Thermal is “underrepresented in datasets” despite benefits in extreme lighting; few datasets integrate all three modalities; existing LiDAR-RGB-T datasets offer “little to no support for object detection and tracking.”  
  - Source: https://arxiv.org/pdf/2503.17122 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4417156065.txt]

- **Engagement prediction vs. MOS-based quality assessment mismatch**  
  - Prior VQA datasets rely on small-scale subjective MOS; paper states MOS correlates poorly with popularity; engagement depends on more than visuals (audio, category, titles/metadata).  
  - Source: https://arxiv.org/pdf/2509.02969 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4417409712.txt]

- **Modern SR artifacts outpace SR-IQA datasets**  
  - SR-IQA datasets/metrics lag behind modern GAN/diffusion SR; need subjective datasets reflecting current generative SR artifacts (hallucinated textures, unnatural patterns).  
  - Source: https://arxiv.org/pdf/2509.06413 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4414756887.txt]

- **Long-video segmentation: occlusion/reappearance + memory/compute trade-offs**  
  - SAM2’s fixed short memory limits long-term analysis; long sequences suffer memory overload and distractor interference; method reports exploring trade-off between memory length and computational cost.  
  - Source: https://arxiv.org/pdf/2509.17500 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4415254644.txt]

- **Disentanglement in realistic settings lacks benchmarks/metrics**  
  - DRL remains “confined to synthetic datasets”; realistic data complexity + lack of robust benchmarks and unified evaluation metrics block progress.  
  - Source: https://arxiv.org/pdf/2509.10463 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4415090288.txt]

- **Remote-sensing VLM gaps (explicit future directions)**  
  - Calls out: cross-modal alignment, vague requirement comprehension, explanation-driven reliability, scalable capabilities, richer/larger multimodal datasets.  
  - Source: https://arxiv.org/pdf/2505.14361 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4411143162.txt]

---

## Practical impact highlights (grounded)

- **Directly usable assets to build on now**
  - R-LiViT dataset (Zenodo DOI) + reproducibility code (GitHub).  
    - Source: https://arxiv.org/pdf/2503.17122 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4417156065.txt]
  - ISRGen-QA benchmark + GitHub repo.  
    - Source: https://arxiv.org/pdf/2509.06413 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4414756887.txt]
  - SnapUGC engagement prediction task + inference code link.  
    - Source: https://arxiv.org/pdf/2509.02969 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4417409712.txt]

- **Operationalizable method insights**
  - SAMSON: concrete architecture components (SAM2 + long-term memory + SAM2Long post-processing) and reported leaderboard metric.  
    - Source: https://arxiv.org/pdf/2509.17500 [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/openalex/text/W4415254644.txt]

---

## Rerun recommendations (evidence-based from what’s missing)

- Because the archive did not ingest CVF/OpenReview/MMLab links into a paper-level URL list (URLs: 0), you likely need a targeted crawl to build a “key papers + code links” table:
  - Start from CVF All Papers: https://openaccess.thecvf.com/ICCV2025?day=all (paper-level pdf/supp/arXiv links) [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/tavily_search.jsonl]
  - Add curated “Project Page” sources: https://www.mmlab-ntu.com/conference/iccv2025/index.html [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/tavily_search.jsonl]
  - Include GitHub topic search for `iccv2025` and/or known aggregators (secondary): https://github.com/topics/iccv2025?o=desc&s=updated [/C:/Users/angpa/myProjects/FEATHER/examples/runs/20251015_iccv25/archive/tavily_search.jsonl]

If you want, I can now (1) enumerate all locally available OpenAlex PDFs/texts and label each as “ICCV workshop/challenge vs off-topic,” and (2) extract every URL (GitHub/Zenodo/etc.) mentioned inside each local PDF text for a consolidated “assets” table.