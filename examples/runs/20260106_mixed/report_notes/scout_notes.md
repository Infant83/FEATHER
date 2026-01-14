## Archive map (Query ID: `20260106_mixed`)

### What’s in this run (coverage)
- **Instruction**: `instruction/20260106_mixed.txt`  
  Inputs: `linkedin` (site hint), query = “quantum computing”, URL = `https://example.com/blog/post` (extract failed), arXiv ID = `2101.00001`.
- **Tavily search results (JSONL index)**: `archive/tavily_search.jsonl`  
  Contains one search query: `quantum computing site:linkedin.com` with **5 LinkedIn results** and per-result summaries.
- **Tavily extract**: `archive/tavily_extract/0001_https_example.com_blog_post.txt`  
  **404 page not found** (no extracted content).
- **arXiv metadata (JSONL index)**: `archive/arxiv/papers.jsonl`  
  1 record: `2101.00001v1` (“Etat de l'art sur l'application des bandits multi-bras”, cs.LG/cs.AI). No PDF/text downloaded.
- **Run metadata/logs**: `archive/_job.json`, `archive/_log.txt`

### Key source “channels” present
- LinkedIn (via Tavily search index): multiple posts/articles on quantum computing (jobs, use cases, cloud access, “trends” framing).
- arXiv (metadata only): unrelated to quantum computing (multi-armed bandits review).
- Direct URL extraction: failed (404).

---

## Notable cross-source trends & signals (what this archive can support)
From the **LinkedIn cluster** (multiple independent results), recurring signals you can cite:
- **Quantum computing framed as near-term business impact** (optimization/data analysis, finance, healthcare/drug discovery).  
  Source examples in `archive/tavily_search.jsonl`: LinkedIn Pulse articles and LinkedIn Learning resource.
- **Cybersecurity/cryptography risk + “quantum-safe” transition narrative** appears repeatedly (QC breaks classical encryption; push to quantum-resistant methods).  
  Source examples: multiple LinkedIn results including the LinkedIn Learning page and a LinkedIn post referencing commercialization timelines.
- **Commercialization / timeline signaling** (e.g., “commercial quantum computers starting in 2025”, chip milestones) used as hype/market readiness indicators.  
  Source example: LinkedIn post content captured in `archive/tavily_search.jsonl`.
- **Access model trend: “quantum cloud computing”** as the pragmatic adoption path (IT teams learning, using remote QC resources).  
  Source example: LinkedIn Learning “Quantum Cloud Computing Tools, Tips and Tech”.

Counter-signal / data quality note:
- The included **arXiv item is off-topic** relative to “quantum computing” (bandits survey), suggesting the arXiv ID was manually provided rather than discovered by query relevance.
- The only explicit URL provided **failed extraction (404)**, reducing non-LinkedIn triangulation.

---

## Prioritized reading plan (max 12 files), with rationale

1) **`archive/tavily_search.jsonl`**  
   Primary evidence base. Contains all captured LinkedIn result snippets + summaries; best for extracting “cross-source” repeated themes and notable signals.

2) **`archive/20260106_mixed-index.md`**  
   Quick orientation: confirms intended scope, counts, and where each dataset lives.

3) **`instruction/20260106_mixed.txt`**  
   Confirms what was asked for vs. what was returned (site hint “linkedin”, one URL, one arXiv ID). Useful for explaining coverage limitations.

4) **`archive/tavily_extract/0001_https_example.com_blog_post.txt`**  
   Important negative result (404). Cite as a gap/failed source when discussing confidence and triangulation.

5) **`archive/arxiv/papers.jsonl`**  
   Only arXiv metadata; verify mismatch/off-topic and decide whether to exclude from “trend” synthesis or mention as irrelevant.

6) **`archive/_job.json`**  
   Reproducibility + configuration (days=30, max_results=5, citations enabled, OpenAlex/YouTube disabled). Helps interpret why coverage is narrow.

7) **`archive/_log.txt`**  
   Spot any additional warnings/errors (e.g., extraction failures) that affect source completeness.

(Only 7 files exist; the rest of the “max 12” slots are unused.)

---

## Suggested workflow to produce the trend-scan report (from this archive)
- Extract and cluster repeated claims across the **5 LinkedIn results** (business use cases, crypto risk, cloud access, commercialization timelines).
- Treat the **404 extract** as an explicit missing corroboration.
- Either exclude the **arXiv bandits survey** from quantum trends (recommended) or mention it as “out-of-scope source present in run inputs.”