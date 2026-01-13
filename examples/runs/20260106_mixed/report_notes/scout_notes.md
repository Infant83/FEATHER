## Archive map (coverage + what’s inside)

**Run / Query**
- **Query ID:** `20260106_mixed` (date 2026-01-06; lookback window: last 30 days)
- **Report focus prompt:** “Identify cross-source trends and notable signals; cite sources.”
- **Input instruction:** `instruction/20260106_mixed.txt` (contains: `linkedin`, `quantum computing`, a URL, and `arXiv:2101.00001`)

**Key index / metadata**
- `archive/20260106_mixed-index.md` — high-level inventory: 1 query, 1 URL, 1 arXiv ID; where to find each artifact.
- `archive/_job.json` — run configuration (days=30, max_results=5, citations enabled; YouTube/OpenAlex disabled).
- `archive/_log.txt` — execution log (useful only if debugging missing sources).

**Collected sources**
- `archive/tavily_search.jsonl` — **main cross-source signal set** for this run (actually multiple LinkedIn results for “quantum computing site:linkedin.com”, up to 5).
  - Includes LinkedIn Pulse articles and LinkedIn Learning resource page; also one LinkedIn post referencing external news (e.g., Fast Company).
- `archive/tavily_extract/0001_https_example.com_blog_post.txt` — extraction attempt for the provided URL; **failed (404)**, so no usable content.
- `archive/arxiv/papers.jsonl` — 1 arXiv record:
  - **2101.00001v1** “Etat de l'art sur l'application des bandits multi-bras” (Djallel Bouneffouf), a survey on multi-armed bandits (cs.LG/cs.AI). Not directly aligned with “quantum computing”, but could serve as an adjacent AI/optimization signal.

**Not present in this run**
- No OpenAlex (`openalex_enabled: false`)
- No YouTube (`youtube_enabled: false`)
- No PDFs downloaded from arXiv (`download_pdf: false`), so only metadata/abstract available.

---

## Notable cross-source themes/signals visible *from the indices*
(Useful for orienting your trend scan; validate/quote precisely when drafting by citing the exact records in `tavily_search.jsonl`.)

1. **Quantum computing framed as cross-industry “transformer”** (healthcare/drug discovery, finance/risk, logistics/optimization, AI/ML).
   - Appears in multiple LinkedIn items (Pulse + Learning).  
   - Source to cite: `archive/tavily_search.jsonl` (LinkedIn Pulse results + LinkedIn Learning page).

2. **Cybersecurity narrative: “breaks current crypto” + “quantum-safe/quantum-based encryption needed”**
   - Repeated across LinkedIn Learning and Pulse-style explainers.
   - Source to cite: `archive/tavily_search.jsonl` (e.g., LinkedIn Learning resource + Pulse posts).

3. **Commercialization / “near-term” milestones** (claims about commercial quantum computers in 2025; chip announcements; performance milestones like “AQ 64”).
   - This is a *signal* rather than validated fact in-archive; treat as “what people are saying” and attribute carefully.
   - Source to cite: `archive/tavily_search.jsonl` (LinkedIn post content referencing Microsoft + Atom Computing, Google “Willow” chip, IonQ AQ 64).

4. **Access model trend: “quantum cloud computing” as the bridge to adoption**
   - Explicitly discussed in LinkedIn Learning resource.
   - Source to cite: `archive/tavily_search.jsonl` (LinkedIn Learning page).

5. **Off-axis academic signal: bandits/online learning survey (2021)**
   - Not quantum, but can support a broader “optimization under uncertainty / exploration-exploitation” thread if your trend scan compares adjacent compute paradigms.
   - Source to cite: `archive/arxiv/papers.jsonl`.

---

## Prioritized reading plan (max 12 files) with rationale

1. **`archive/tavily_search.jsonl`**  
   *Rationale:* Primary multi-result corpus. Needed to extract cross-source trends and cite multiple independent items (LinkedIn Pulse, LinkedIn Learning, LinkedIn posts).

2. **`archive/arxiv/papers.jsonl`**  
   *Rationale:* Only scholarly source. Even if tangential, it’s the only non-LinkedIn source-type artifact; helps avoid a single-platform trend scan.

3. **`archive/tavily_extract/0001_https_example.com_blog_post.txt`**  
   *Rationale:* Confirms the provided URL is unusable (404). Important to note source gaps/failed retrieval in methodology.

4. **`archive/20260106_mixed-index.md`**  
   *Rationale:* Quick “table of contents” for what the archive is supposed to contain; useful to cite in audit trail / coverage section.

5. **`archive/_job.json`**  
   *Rationale:* Documents constraints shaping the evidence (LinkedIn site hint; max_results=5; OpenAlex/YouTube disabled; no PDFs). Use for transparency in report limitations.

6. **`archive/_log.txt`**  
   *Rationale:* Only if you need to explain missing PDFs/extract failures or verify that all steps executed.

(There are only 6 files total in the archive; the list above is effectively the complete reading set.)

---

## Practical note for your trend_scan draft
Because the archive is **heavily LinkedIn-weighted** and the only URL extract failed, your “cross-source” framing will mostly mean **cross-item within Tavily results** (different authors/pages on LinkedIn) plus **one arXiv metadata entry**. If you want stronger cross-source triangulation (news, vendor blogs, standards bodies), you’d need another run with broader site hints / OpenAlex/YouTube enabled or additional URLs.