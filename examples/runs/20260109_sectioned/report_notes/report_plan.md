Plan (updated):
- [x] Extract required section headers/order — Read `instruction/20260109_sectioned.txt` and capture the exact section boundaries implied by the separator lines.  
- [x] Inventory evidence per section — Scan `archive/tavily_search.jsonl`, `archive/youtube/videos.jsonl`, and `archive/arxiv/papers.jsonl` to map which records support each section.  
- [x] Define citation anchors & format — Standardize citations as (title + URL) from Tavily, (video title + channel + YouTube URL) from YouTube JSONL, and (arXiv ID + title + entry/pdf URL) from arXiv JSONL.  
- [ ] Draft Section 1 (AI trends for 2026 (agentic AI, physical AI)) — Synthesize across Tavily trend sources; separate facts vs interpretation; attach citations.  
- [ ] Draft Section 2 (youtube / github / agentic AI demos open source code) — Summarize key demos and notable GitHub topic/repo signals using Tavily + YouTube metadata; cite each claim.  
- [ ] Draft Section 3 (youtube / github / industrial AI deployment talks) — Extract industrial deployment themes from relevant Tavily/YouTube items; emphasize deployment constraints; cite.  
- [ ] Draft Section 4 (arXiv:2401.01234) — Summarize metadata, assess relevance to the stated trend focus, and flag mismatch if any; cite arXiv entry.  
- [ ] Add run limitations & gaps — Use `archive/20260109_sectioned-index.md` and `archive/_job.json` to document constraints (no transcripts, no PDFs, 30-day window, max-results=5).  
- [ ] Final consistency pass — Ensure section order matches instruction file verbatim (including sublines like “linkedin/news” and “youtube/github”), every paragraph has supporting citations, and citations are consistent across sections.