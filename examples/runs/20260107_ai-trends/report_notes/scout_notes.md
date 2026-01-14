## Archive map (what’s in this run)

**Archive root:** `.../20260107_ai-trends/archive`  
Only **3 files** are present:

1. **`archive/tavily_search.jsonl` (53 KB)**  
   JSONL index of web search results (Tavily). Contains multiple queries and top results summaries/snippets. This is the *core source inventory* for the report.

2. **`archive/_job.json` (4.1 KB)**  
   Run/job metadata (configuration, parameters). Useful for provenance and reproducibility, not for content.

3. **`archive/_log.txt` (407 B)**  
   Minimal runtime log; mostly operational.

**Instruction file (outside archive):** `instruction/20260107_ai-trends.txt`  
Contains target source types (“linkedin/arxiv/github”) and a query list (AI trends 2025/2026, agentic AI, physical AI robotics, CES 2026, venue-specific queries like Technology Review/IEEE/VentureBeat).

---

## Coverage snapshot (from `tavily_search.jsonl`)

The JSONL currently shows at least two main queries captured:

### Query: “AI trends 2025 (English)”
Representative sources found:
- Spencer Stuart: “The top three AI trends of 2025 — according to AI…”
- Microsoft Source: “6 AI trends you’ll see more of in 2025”
- McKinsey: “technology trends outlook 2025”
- Cisco blog: “Six AI Predictions For 2025…”
- “State of AI Report 2025” (stateof.ai)

Themes visible in snippets:
- **Agentic AI / autonomous agents**
- **AI for scientific discovery**
- **Shift to smaller/specialized models + cost/efficiency**
- **Compute/power constraints + industrial-scale data centers**
- **Governance/safety moving from abstract x-risk to reliability/security**

### Query: “AI trends 2026 (English)”
Representative sources found:
- Gartner: “Top 10 Strategic Technology Trends for 2026”
- MIT Sloan Management Review: “Five Trends in AI and Data Science for 2026” (Davenport, Bean)
- Microsoft Source: “What’s next in AI: 7 trends to watch in 2026”
- Harvard Business School Working Knowledge: “AI Trends for 2026…”

Themes visible in snippets:
- **AI platforms/infrastructure maturation**
- **Agents as “digital colleagues” with security implications**
- **GenAI shifting from individual tool → organizational capability**
- **AI becoming central in research workflows (hypothesis generation, tool use)**
- **Hype cycle / “trough of disillusionment” framing for agents**

---

## Key source files (inventory + what they’re good for)

### Must-use content index
- **`archive/tavily_search.jsonl`** — primary content source; includes URLs, titles, snippets, and scores. Use to extract the “10 breakthroughs + implications” bullets quickly.

### Provenance / debugging
- **`archive/_job.json`** — confirms what collectors ran and with what settings.
- **`archive/_log.txt`** — confirms run completed; rarely adds substance.

### Scope definition
- **`instruction/20260107_ai-trends.txt`** — clarifies intended topical coverage (agentic AI, physical AI robotics, CES 2026, major venues).

---

## Prioritized reading plan (max 12), with rationale

1. **`archive/tavily_search.jsonl`**  
   Rationale: Contains *all* captured sources and is the only substantive archive artifact. Extract candidate “breakthroughs” and attach implications.

2. **`instruction/20260107_ai-trends.txt`**  
   Rationale: Ensures the synthesis matches intended scope (agentic AI, physical AI robotics, CES angle, venue queries).

3. **`archive/_job.json`**  
   Rationale: Check whether other collectors (arxiv/openalex/youtube/local manifests) were expected but not produced; helps explain coverage gaps.

4. **`archive/_log.txt`**  
   Rationale: Quick sanity check for errors that might explain why only Tavily results exist.

Then, within `tavily_search.jsonl`, prioritize reading/clicking (as “virtual sub-sources”) in this order for short, sharp MIT Tech Review–style breakthroughs:

5. **Gartner — “Top 10 Strategic Technology Trends for 2026”**  
   Rationale: Clean “top 10” packaging; ideal for short sections + implications.

6. **MIT Sloan Management Review — “Five Trends in AI and Data Science for 2026”**  
   Rationale: Executive framing + hype-cycle realism; strong for “implications.”

7. **State of AI Report 2025 — stateof.ai**  
   Rationale: Macro signals (compute, geopolitics, safety posture, adoption metrics).

8. **McKinsey — “technology trends outlook 2025”**  
   Rationale: Enterprise/strategy lens; includes “agentic AI” and “application-specific semiconductors.”

9. **Microsoft Source — “What’s next in AI: 7 trends to watch in 2026”**  
   Rationale: Specific applied claims (research copilots, security, infrastructure).

10. **Microsoft Source — “6 AI trends you’ll see more of in 2025”**  
   Rationale: Complements 2026; strong science/throughput narrative.

11. **Cisco blog — “Six AI Predictions for 2025…”**  
   Rationale: Cost/efficiency + move toward specialized models; good “breakthrough implication” framing for 2025.

12. **Harvard Business School Working Knowledge — “AI Trends for 2026…”**  
   Rationale: Leadership/organizational implications (scaling, trade-offs, “change fitness”).

---

## Notable gap vs. expected coverage

The instruction file mentions **arxiv/github/linkedin** and venue-specific queries (Technology Review, IEEE, CES 2026, CVPR/NeurIPS/etc.), but the archive contains **only Tavily web results** and no `archive/arxiv/...`, `archive/openalex/...`, `archive/youtube/...`, or `archive/local/manifest.jsonl`.  
Reading `_job.json` should clarify whether those pipelines didn’t run or produced no outputs.