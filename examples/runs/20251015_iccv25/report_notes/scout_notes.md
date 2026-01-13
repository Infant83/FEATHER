## Archive map (what’s in this run)

**Root indices / run bookkeeping**
- `archive/20251015_iccv25-index.md` — run summary + what got downloaded (OpenAlex PDFs/text).
- `archive/_job.json` — FEATHER job config (queries, params like max-results/days).
- `archive/_log.txt` — execution log; useful for diagnosing missing sources.
- `instruction/20251015_iccv25.txt` — seed queries (“github”, “iccv 2025 open access”, “paper code”, etc.).

**Search index (broad web results)**
- `archive/tavily_search.jsonl` — Tavily results for queries like “iccv 2025”; includes key hubs:
  - ICCV official site: `https://iccv.thecvf.com/`
  - CVF Open Access ICCV 2025 all papers: `https://openaccess.thecvf.com/ICCV2025?day=all`
  - OpenReview group: `https://openreview.net/group?id=thecvf.com/ICCV/2025/Conference`
  - Curated accepted-paper list (MMLab@NTU): `https://www.mmlab-ntu.com/conference/iccv2025/index.html`
  - (These are critical for *practical impact + code links*, because many entries include “Project Page” / GitHub.)

**OpenAlex corpus (local PDFs + extracted text)**
- `archive/openalex/works.jsonl` — metadata for the OA-selected works (title/authors/abstract/doi/pdf_url).
- PDFs (11) + extracted text (11) under:
  - `archive/openalex/pdf/*.pdf`
  - `archive/openalex/text/*.txt`

**Important coverage note (gap)**
- The OpenAlex selection is **not a representative “ICCV 2025 key papers” set**; it includes several workshop/challenge reports and even off-topic items (e.g., “OpenCV for Computer Vision Applications”, oncology agent, education review). For the requested report (“key papers, code links, gaps, practical impact”), you’ll rely heavily on **CVF Open Access + curated accepted-paper pages**, then only use OpenAlex PDFs that truly map to ICCV 2025.

---

## Key source files (prioritized reading list, max 12)

1) **`archive/tavily_search.jsonl`**  
   *Why:* Fastest way to extract the canonical ICCV 2025 paper listing endpoints (CVF Open Access “All Papers”), plus curated pages that often include **GitHub/project links**. Also reveals what the run *didn’t* download.

2) **`archive/openalex/works.jsonl`**  
   *Why:* Your master metadata table for the downloaded PDFs/text. Use it to filter what’s truly ICCV-related (many are “ICCV 2025 Workshops/Challenge”) and to capture **DOIs/arXiv IDs/dataset links**.

3) **`archive/openalex/text/W4411143162.txt`** — *Vision-Language Modeling Meets Remote Sensing: Models, datasets, and perspectives*  
   *Why:* Likely the most “survey-like” and practically useful for identifying **research gaps, datasets, and open problems** (and typically cites many codebases).

4) **`archive/openalex/text/W4417156065.txt`** — *R-LiViT: A LiDAR-Visual-Thermal Dataset*  
   *Why:* Direct practical impact via **dataset release** (Zenodo DOI in metadata). Good for “what to build next” gaps (multimodal roadside perception).

5) **`archive/openalex/text/W4414756887.txt`** — *VQualA 2025 Challenge on Image Super-Resolution Generated Content Quality Assessment*  
   *Why:* Contains at least one explicit GitHub link in metadata: `https://github.com/Lighting-YXLI/ISRGen-QA` (strong for “code links + benchmark gaps”).

6) **`archive/openalex/text/W4417409712.txt`** — *VQualA 2025 Challenge on Engagement Prediction for Short Videos*  
   *Why:* Practical focus: real-world UGC engagement prediction; helps identify gaps in **multimodal + metadata modeling** and evaluation leakage/robustness.

7) **`archive/openalex/text/W4415254644.txt`** — *SAMSON: 3rd Place Solution of LSVOS 2025 VOS Challenge*  
   *Why:* Implementation-centric report (SAM2-based framework, memory modules). Useful for summarizing **what worked in practice** and remaining failure modes.

8) **`archive/openalex/text/W4415090288.txt`** — *DRL4Real workshop methods & results*  
   *Why:* Explicitly about moving disentanglement beyond synthetic benchmarks—good for “research gaps” and practical constraints.

9) **`archive/20251015_iccv25-index.md`**  
   *Why:* Quick inventory of what you already have locally; ensures you don’t miss a downloaded PDF/text pair.

10) **`archive/_log.txt`**  
   *Why:* Helps explain why **URLs=0** and why CVF Open Access papers weren’t downloaded as PDFs. Useful if you’ll rerun collection to pull actual ICCV papers + code links.

11) **`archive/openalex/text/W4409578551.txt`** — *Trajectory prediction via proposal guided transformer…*  
   *Why:* Practical-ish CV topic (trajectory prediction), but verify conference relevance (it’s *Scientific Reports*). Include only if you need a non-workshop method paper.

12) **(Optional sanity check)** `archive/openalex/text/W4410841160.txt` — *OpenCV for Computer Vision Applications*  
   *Why:* High-citation but likely **not ICCV**; read only to exclude as off-scope or to use as background for practical tooling sections.

---

## Proposed reading plan (optimized for “key papers + code + gaps + practical impact”)

**Phase 1 — Reconstruct the true ICCV 2025 landscape (30–45 min)**
- Read `archive/tavily_search.jsonl` to capture:
  - CVF Open Access “All Papers” page (primary)
  - any curated “Accepted papers + [Project Page]/[GitHub]” lists (e.g., MMLab@NTU)
- Outcome: shortlist of *actual* ICCV 2025 papers with accessible code/project pages.

**Phase 2 — Mine your locally downloaded PDFs/text for concrete assets (60–90 min)**
- Use `archive/openalex/works.jsonl` to tag each local work as:
  - ICCV main / ICCV workshop / non-ICCV
  - has code? dataset? benchmark?
- Read the 6–7 most relevant OpenAlex text files (items 3–8 above) to extract:
  - GitHub/project links, datasets, evaluation protocols
  - stated limitations and future work (for research gaps)
  - practical deployment notes (compute, data collection, failure cases)

**Phase 3 — Fill gaps / decide rerun needs (15–30 min)**
- Check `archive/_log.txt` + index to confirm you didn’t actually fetch CVF Open Access PDFs.
- If needed, rerun FEATHER with targeted queries like:
  - `site:openaccess.thecvf.com ICCV 2025 github`
  - specific topic clusters (e.g., “diffusion”, “3D”, “VLM”, “tracking”) to get representative “key papers”.

If you want, I can next produce a *coverage diagnosis* (what percentage of the archive is truly ICCV 2025 and where the biggest missing clusters are) and a concrete “Top X ICCV 2025 papers to include” shortlist based on the CVF Open Access hub.