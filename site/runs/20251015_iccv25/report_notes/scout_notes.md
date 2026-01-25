## Archive map (what’s in this run)

### Top-level
- `instruction/20251015_iccv25.txt` (keywords only)
  - Queries: “github”, “iccv 2025”, “international conference on computer vision 2025”, “iccv 2025 open access”, “iccv 2025 paper code”.
- `archive/20251015_iccv25-index.md` (run index + what was downloaded)
- `archive/tavily_search.jsonl` (web search results + summaries; main gateway to CVF Open Access / listings)
- `archive/openalex/works.jsonl` (OpenAlex metadata index; includes titles, abstracts, DOIs, URLs, citation counts)
- `archive/openalex/pdf/*.pdf` (11 PDFs downloaded)
- `archive/openalex/text/*.txt` (11 extracted text files; faster to scan than PDFs)
- `archive/_job.json`, `archive/_log.txt` (run provenance / debug)

### Expected but missing indices (coverage gaps)
- `archive/local/manifest.jsonl` **missing**
- `archive/arxiv/papers.jsonl` **missing**
- `archive/youtube/videos.jsonl` **missing**
  - Practical implication: this run is *not* a comprehensive ICCV’25 paper crawl; it’s primarily (a) a Tavily pointer to CVF Open Access, and (b) a small OpenAlex sample that includes several **ICCV 2025 workshop/challenge reports** plus off-topic items.

---

## What sources are actually about ICCV 2025 (high-signal subset)

### From Tavily (primary “ICCV 2025 paper universe” entry points)
- CVF ICCV 2025 Open Access:
  - `https://openaccess.thecvf.com/ICCV2025`
  - `https://openaccess.thecvf.com/ICCV2025?day=all` (All Papers listing)
- ICCV site / virtual program:
  - `https://iccv.thecvf.com/`
  - `https://iccv.thecvf.com/virtual/2025/papers.html`
- Third-party accepted paper lists (useful for quickly grabbing project/code links):
  - `https://www.mmlab-ntu.com/conference/iccv2025/index.html`
- Industry pages with “accepted publications” (spot checks; may include project links):
  - `https://www.amazon.science/conferences-and-events/iccv-2025`
  - `https://machinelearning.apple.com/updates/apple-at-iccv-2025`

### From OpenAlex PDFs/texts (downloaded in-archive)
Likely ICCV-related (explicitly says ICCV 2025 / workshops/challenges):
- `archive/openalex/text/W4417156065.txt` — **R-LiViT: A LiDAR-Visual-Thermal Dataset** (mentions accepted at ICCV 2025; dataset on Zenodo)
- `archive/openalex/text/W4417409712.txt` — **VQualA 2025 Challenge on Engagement Prediction for Short Videos: Methods and Results** (ICCV 2025 Workshops)
- `archive/openalex/text/W4414756887.txt` — **VQualA 2025 Challenge on Image Super-Resolution Generated Content Quality Assessment: Methods and Results** (includes GitHub link in abstract)
- `archive/openalex/text/W4415090288.txt` — **DRL4Real workshop summary** (ICCV 2025)
- `archive/openalex/text/W4415254644.txt` — **SAMSON: 3rd Place Solution of LSVOS 2025 VOS Challenge** (ICCV 2025 challenge report)

Probably off-topic for an “ICCV 2025 key papers” report (unless you want broader CV/AI context):
- `W4410841160` OpenCV applications (general)
- `W4411100445` oncology agent (Nature Cancer)
- `W4411166620` genAI in education (systematic review)
- `W4411466105` e-commerce multimodal retrieval
- `W4409578551` trajectory prediction (not clearly ICCV)
(These can be deprioritized unless the report wants “recent CV work” beyond ICCV.)

---

## Prioritized reading plan (max 12 files)

1) **`archive/tavily_search.jsonl`**  
   *Rationale:* Contains the key portals (CVF Open Access “All Papers”, ICCV virtual paper list, MMLab accepted list) and is the best route to “key papers + code/project links” at scale.

2) **`archive/20251015_iccv25-index.md`**  
   *Rationale:* Quick situational awareness: what was queried, what was downloaded, and which PDFs/text correspond to which titles.

3) **`archive/openalex/works.jsonl`**  
   *Rationale:* Metadata index for the 11 works (abstracts, DOIs, URLs, citations). Helps you pick what to actually summarize and extract code/dataset links.

4) **`archive/openalex/text/W4417156065.txt`** — *R-LiViT: A LiDAR-Visual-Thermal Dataset*  
   *Rationale:* Practical impact (dataset), likely to include download/benchmark details; good for “resources + gaps”.

5) **`archive/openalex/text/W4414756887.txt`** — *VQualA 2025 Challenge on Image Super-Resolution Generated Content Quality Assessment*  
   *Rationale:* Contains a concrete GitHub link (`Lighting-YXLI/ISRGen-QA`), challenge framing, metrics—useful for “code links + research gaps”.

6) **`archive/openalex/text/W4417409712.txt`** — *VQualA 2025 Challenge on Engagement Prediction for Short Videos*  
   *Rationale:* Real-world UGC engagement dataset/task; strong “practical impact” and open problems.

7) **`archive/openalex/text/W4415254644.txt`** — *SAMSON: 3rd Place Solution of LSVOS 2025 VOS Challenge*  
   *Rationale:* Implementation-oriented VOS system details; can highlight what works in practice + remaining failure modes.

8) **`archive/openalex/text/W4415090288.txt`** — *DRL4Real workshop summary*  
   *Rationale:* Directly useful for “research gaps”: summarizes themes, pitfalls, and future directions in disentanglement for real-world settings.

9) **`archive/openalex/pdf/W4417156065.pdf`**  
   *Rationale:* If the extracted text is missing tables/figures, the PDF will capture dataset specs, splits, sensors, licensing, and benchmark protocols.

10) **`archive/openalex/pdf/W4414756887.pdf`**  
   *Rationale:* For challenge details (dataset composition, artifacts taxonomy, evaluation protocol) that may be lost in text extraction.

11) **`archive/openalex/pdf/W4417409712.pdf`**  
   *Rationale:* For dataset/task definition and leaderboard methodology (often clearer in figures/tables).

12) **`archive/_log.txt`**  
   *Rationale:* Only if you need to diagnose why arXiv/YouTube/local manifests are missing or why results skew off-topic (useful to fix future runs).

---

## Coverage notes (important for your report framing)

- This archive **does not** contain the actual CVF ICCV 2025 paper PDFs; it mostly contains:
  1) **Pointers** to CVF Open Access and other listings (via Tavily), and  
  2) A small OpenAlex sample skewed toward **workshop/challenge reports** + unrelated 2025 papers.
- If your report must cover *main conference key papers*, you’ll likely need a second crawl that specifically ingests the CVF Open Access “All Papers” page and/or scrapes paper pages for code/project links.