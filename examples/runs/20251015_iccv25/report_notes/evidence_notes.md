## Authoritative ICCV 2025 entry points (web portals discovered via Tavily)

- **CVF Open Access – ICCV 2025 landing page** (official OA hub; day-by-day + “All Papers”)  
  - Evidence: “These ICCV 2025 papers are the Open Access versions, provided by the Computer Vision Foundation… [All Papers…]”  
  - URL: https://openaccess.thecvf.com/ICCV2025  [archive/tavily_search.jsonl]

- **CVF Open Access – ICCV 2025 “All Papers” listing** (bulk list with bibtex + pdf/supp/arXiv links; best scaling surface for paper→code mining)  
  - Evidence snippet shows paper entries with “\[pdf] \[supp] \[arXiv]” links and bibtex blocks.  
  - URL: https://openaccess.thecvf.com/ICCV2025?day=all  [archive/tavily_search.jsonl]

- **ICCV 2025 conference site** (conference metadata; schedule/videos; confirms dates/location)  
  - Evidence: “Oct 19 – 23th, 2025, Honolulu, Hawai’i”  
  - URL: https://iccv.thecvf.com/  [archive/tavily_search.jsonl]

- **ICCV 2025 virtual papers page** (paper list by session/time; useful secondary index)  
  - URL: https://iccv.thecvf.com/virtual/2025/papers.html  [archive/tavily_search.jsonl]

- **MMLab@NTU “ICCV 2025 Accepted Papers” list** (third-party curated list that explicitly includes **\[arXiv]** and **\[Project Page]** links)  
  - Evidence snippet shows rows with “in Proceedings of IEEE/CVF… (ICCV) \[arXiv] \[Project Page]”.  
  - URL: https://www.mmlab-ntu.com/conference/iccv2025/index.html  [archive/tavily_search.jsonl]

- **Amazon Science – ICCV 2025** (industry accepted-publications page; may include project links per item)  
  - URL: https://www.amazon.science/conferences-and-events/iccv-2025  [archive/tavily_search.jsonl]

---

## In-archive OpenAlex sample (what this run actually downloaded)

This run is **not a full ICCV’25 main-conference crawl**; it includes (a) the portal URLs above, plus (b) **11 OpenAlex PDFs/texts**, many being **ICCV 2025 workshop/challenge reports** rather than main-conference papers. Evidence: run index enumerates the 11 PDFs/texts and their sources (mostly arXiv PDFs for ICCV 2025 workshop/challenge items). [archive/20251015_iccv25-index.md]

---

## ICCV-2025-relevant “key items” from the OpenAlex PDFs/texts (with practical links)

### Datasets / resources

- **R-LiViT: A LiDAR-Visual-Thermal Dataset Enabling Vulnerable Road User Focused Roadside Perception** (accepted at ICCV 2025; dataset + code released)  
  - Evidence: “accepted at the ICCV 2025… The dataset1 and the code for reproducing our evaluation results2 are made publicly available.”  
  - Dataset (Zenodo DOI): https://doi.org/10.5281/zenodo.16356714  
  - Code: https://github.com/XITASO/r-livit  
  - Additional dataset specs from text: “10,000 LiDAR frames and 2,400… aligned RGB and thermal images across 150 traffic scenarios” and VRU focus.  
  - Sources: http://arxiv.org/abs/2503.17122 ; https://arxiv.org/pdf/2503.17122  [archive/openalex/text/W4417156065.txt], [archive/openalex/works.jsonl]

### Challenges / benchmarks + code

- **VQualA 2025 Challenge on Image Super-Resolution Generated Content Quality Assessment: Methods and Results** (ICCV 2025 Workshops; repo provided)  
  - Evidence: “organized as part of the… VQualA… at the ICCV 2025 Workshops… The project is publicly available at: https://github.com/Lighting-YXLI/ISRGen-QA.”  
  - Code/dataset hub: https://github.com/Lighting-YXLI/ISRGen-QA  
  - Sources: http://arxiv.org/abs/2509.06413 ; https://arxiv.org/pdf/2509.06413  [archive/openalex/text/W4414756887.txt], [archive/openalex/works.jsonl]

- **VQualA 2025 Challenge on Engagement Prediction for Short Videos: Methods and Results** (ICCV 2025; SnapUGC dataset + project link)  
  - Evidence: “held in conjunction with ICCV 2025… uses a new short-form UGC dataset… metrics derived from… real-world user interactions.”  
  - Project page (explicit GitHub): “https://github.com/dasongli1/SnapUGC_Engagement/tree/main/ECR_inference”  
  - Defines engagement metrics: **NAWP** and **ECR**; ECR described as \(P(\mathrm{watch}>5s)\).  
  - Sources: http://arxiv.org/abs/2509.02969 ; https://arxiv.org/pdf/2509.02969  [archive/openalex/text/W4417409712.txt], [archive/openalex/works.jsonl]

- **SAMSON: 3rd Place Solution of LSVOS 2025 VOS Challenge** (ICCV 2025 challenge track report; practical system details)  
  - Evidence: “3rd place solution in the MOSE track of ICCV 2025… incorporate a long-term memory module… adopt SAM2Long as a post-processing strategy…”  
  - Reported result: “final performance of 0.8427 in terms of J & F… (J=0.8182, F=0.8671)”  
  - Source: http://arxiv.org/abs/2509.17500 ; https://arxiv.org/pdf/2509.17500  [archive/openalex/text/W4415254644.txt], [archive/openalex/works.jsonl]

### Workshop summary (gap-setting / research directions)

- **The 1st International Workshop on Disentangled Representation Learning for Controllable Generation (DRL4Real): Methods and Results** (ICCV 2025 workshop overview + competition link)  
  - Evidence: workshop goal “bridge the gap… beyond synthetic benchmarks… lack of robust benchmarks and unified evaluation metrics.”  
  - Workshop website: https://drl-for-real.github.io/DRL-for-Real/index.html  
  - Competition (EvalAI): https://eval.ai/web/challenges/challenge-page/2527/overview  
  - Source: http://arxiv.org/abs/2509.10463 ; https://arxiv.org/pdf/2509.10463  [archive/openalex/text/W4415090288.txt], [archive/openalex/works.jsonl]

---

## Research gaps & limitations (evidence-based from the archived texts)

- **Tri-modal roadside perception gaps (RGB+LiDAR+Thermal, aligned)**  
  - Gap stated: thermal “remains underrepresented in datasets” and aligned RGB-T data is “currently available in only a limited number of datasets.”  
  - Source: https://arxiv.org/pdf/2503.17122  [archive/openalex/text/W4417156065.txt]

- **Engagement prediction vs MOS-based VQA mismatch**  
  - Evidence: VQA models trained on MOS datasets “struggle to predict the popularity of short videos… MOS… show a poor correlation with… popularity levels.”  
  - Implication gap: need learning targets grounded in large-scale real interactions; multi-modal inputs beyond visuals (audio, titles, metadata).  
  - Source: https://arxiv.org/pdf/2509.02969  [archive/openalex/text/W4417409712.txt]

- **Long-term VOS: occlusions/reappearance + memory–compute trade-off**  
  - Evidence: SAM2 “fixed 8-frame memory restricts its effectiveness in long-term video analysis” and greedy strategies are “vulnerable” under occlusion/reappearance; SAMSON discusses exploring “trade-off between memory length and computational cost”.  
  - Source: https://arxiv.org/pdf/2509.17500  [archive/openalex/text/W4415254644.txt]

- **Disentanglement in real-world settings lacks benchmarks/metrics**  
  - Evidence: field “confined to synthetic datasets… lack of robust benchmarks and unified evaluation metrics.”  
  - Source: https://arxiv.org/pdf/2509.10463  [archive/openalex/text/W4415090288.txt]

---

## Practical implication for “key ICCV 2025 papers + code” coverage (run constraint)

- The archive contains **portals** to the full ICCV 2025 paper universe (CVF OA “All Papers”, ICCV virtual list, MMLab accepted list), but **does not include the actual CVF ICCV 2025 paper PDFs**—only an **11-paper OpenAlex sample** (largely workshop/challenge reports).  
  - Evidence: index lists only those 11 PDFs/texts; Tavily results include the CVF OA links.  
  - Sources: [archive/20251015_iccv25-index.md], [archive/tavily_search.jsonl]