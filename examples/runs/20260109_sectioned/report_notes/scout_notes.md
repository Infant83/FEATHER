## Archive map (what’s in this run)

**Run / query context**
- **Instruction**: `instruction/20260109_sectioned.txt`  
  Focus: *AI trends for 2026 (agentic AI, physical AI)* + *YouTube/GitHub demos* + *industrial AI deployment talks*; includes an arXiv ID.  
- **Index**: `archive/20260109_sectioned-index.md`  
  Confirms: 3 queries, 0 URLs explicitly listed, 1 arXiv ID, YouTube enabled, no transcripts, no PDFs downloaded.

**Key source indices (JSONL)**
- **Web search results**: `archive/tavily_search.jsonl`  
  Contains 3 query blocks with per-result `summary` and `query_summary`. This is the main evidence base for web/news/GitHub/YouTube (via “site:” queries).
- **YouTube metadata**: `archive/youtube/videos.jsonl`  
  Contains YouTube video metadata and short summaries (but **no transcripts**).
- **arXiv metadata**: `archive/arxiv/papers.jsonl`  
  Contains metadata for **arXiv:2401.01234v1** (note: appears unrelated to AI trends; it’s a survival analysis/statistics paper).
- **Job/log**
  - `archive/_job.json` (run configuration, queries, flags)
  - `archive/_log.txt` (execution log)

**All files detected (6 total)**
1. `archive/20260109_sectioned-index.md`
2. `archive/_job.json`
3. `archive/_log.txt`
4. `archive/tavily_search.jsonl`
5. `archive/youtube/videos.jsonl`
6. `archive/arxiv/papers.jsonl`

---

## Coverage notes (relevant to “Respect section structure and summarize each section with citations”)

The instruction file is implicitly “sectioned” using separator lines:
1) **AI trends for 2026 (agentic AI, physical AI)** (hints: linkedin, news)  
2) **YouTube/GitHub: agentic AI demos open source code**  
3) **YouTube/GitHub: industrial AI deployment talks**  
4) **arXiv:2401.01234**

Citations will primarily come from:
- Tavily results (web pages like Deloitte, MIT SMR, Forbes, HealthVerity, plus GitHub topic pages)
- YouTube video URLs/metadata (titles, channels, descriptions—no transcript quotes)
- arXiv metadata entry

---

## Prioritized reading plan (max 12 files; here only 6 exist)

1) **`instruction/20260109_sectioned.txt`**  
   *Rationale:* Defines the required section structure to preserve in the report.

2) **`archive/tavily_search.jsonl`**  
   *Rationale:* Core citation source for each section (AI trends pages; GitHub “agentic-ai” topic; YouTube “site:youtube.com” results; includes per-result summaries).

3) **`archive/youtube/videos.jsonl`**  
   *Rationale:* Needed to cite and summarize the YouTube section(s) accurately (video titles, channels, descriptions). Important because Tavily’s YouTube “site:” results may differ from the dedicated YouTube search output.

4) **`archive/20260109_sectioned-index.md`**  
   *Rationale:* Quick run metadata and confirms what was/wasn’t collected (no transcripts, no PDFs), helping set expectations for citations.

5) **`archive/arxiv/papers.jsonl`**  
   *Rationale:* Required to handle the arXiv section with a citation; also reveals likely off-topic inclusion (stat.ME paper), which should be noted in the section summary.

6) **`archive/_job.json`**  
   *Rationale:* Confirms query specs and settings (days=30, max_results=5, youtube_transcript=false), useful for explaining limitations.

*(Optional / low priority)*  
- **`archive/_log.txt`**: only if you need debugging context or to explain missing artifacts (e.g., why no transcripts/PDFs).

---

## Key sources found inside the indices (for awareness)

**AI trends (agentic/physical/sovereign AI)**
- “Three new AI breakthroughs shaping 2026: AI trends | Deloitte US” (web) — in `tavily_search.jsonl`
- “Five Trends in AI and Data Science for 2026” (MIT Sloan Management Review) — in `tavily_search.jsonl`
- “AI trends shaping healthcare in 2026: agentic, physical & sovereign AI” (HealthVerity blog) — in `tavily_search.jsonl`
- “Agentic AI Takes Over — 11 Shocking 2026 Predictions” (Forbes) — in `tavily_search.jsonl`

**Agentic AI demos (open source / GitHub)**
- GitHub topic page `https://github.com/topics/agentic-ai` (lists projects like `google/adk-python`, `Fosowl/agenticSeek`, etc.) — in `tavily_search.jsonl`
- Example repos: `rh-aiservices-bu/agentic-examples`, `nibzard/awesome-agentic-patterns`, etc. — in `tavily_search.jsonl`

**Industrial AI deployment talks (YouTube)**
- DNV “Veracity AI Talks…” (accountability, assurance) — in `tavily_search.jsonl`
- AWS re:Invent 2025 talk on agentic AI at the edge — in `tavily_search.jsonl`
- Siemens CES 2026 keynote / Bloomberg Talks on “Industrial AI Operating System” — in `tavily_search.jsonl`

**arXiv**
- `2401.01234v1` “Mixture cure semiparametric additive hazard models…” — in `arxiv/papers.jsonl` (likely not aligned to AI-trends focus)

If you want, I can also propose a section-by-section citation strategy (which file/fields to cite per section) based on these indices.