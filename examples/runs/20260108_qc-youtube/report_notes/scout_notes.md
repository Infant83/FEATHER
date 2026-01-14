## Archive map (20260108_qc-youtube)

### Top-level contents (archive/)
- `archive/20260108_qc-youtube-index.md` — run summary/index (queries, URLs, tool flags)
- `archive/tavily_search.jsonl` — main web-search index with per-result `summary` and `query_summary` (largest source coverage)
- `archive/youtube/videos.jsonl` — YouTube metadata index (1 video)
- `archive/youtube/transcripts/youtu.be-sQSQBYHR0ms-Quantum_Computing_and_AI.txt` — the single transcript (primary “narrative” source)
- `archive/arxiv/papers.jsonl` — arXiv metadata index (2 IDs; **both appear off-topic** to quantum/AI)
- `archive/_job.json` — run configuration + parameters (provenance)
- `archive/_log.txt` — execution log (debug/provenance)

### Instruction / scope signals
- `instruction/20260108_qc-youtube.txt` focuses on: “quantum computing + AI industry use cases (last 30 days)”, plus “Nature/Science/IEEE Spectrum/PRX Quantum” prompts, and one YouTube URL.
- The archive, however, contains **only**: Tavily web results, **one** YouTube transcript, and **no** OpenAlex data. arXiv IDs included are **not** quantum/AI papers.

---

## Key source indices (JSONL) — what they cover

### 1) `archive/tavily_search.jsonl` (web coverage)
Contains multiple queries and top web results per query with short summaries. From the first query block visible, prominent hits include:
- Quantum Computing Report news page (industry news; mentions photonics reservoir computing system “Neurawave”; Aramco–Pasqal deployment)  
- Network World “Top quantum breakthroughs of 2025” (enterprise framing; includes claims/quotes about timelines and market value)
- QED-C / SRI report page: “Quantum Computing and Artificial Intelligence Use Cases” (March 2025; structured use-case framing)
- Various vendor/blog-style explainers (likely lower authority; use cautiously)

This JSONL is the **main place to select credible citations** for a narrative review.

### 2) `archive/youtube/videos.jsonl`
Single item:
- “Quantum Computing and AI” — Caleb Writes Code (2025-10-19), ~10m40s; transcript available.

### 3) `archive/arxiv/papers.jsonl`
Two records:
- `2401.01234v1` — survival analysis (stat.ME), unrelated
- `2311.12345v1` — Stable Diffusion for aerial object detection (cs.CV), unrelated  
=> Treat as **noise/mis-specified IDs** for this report focus.

---

## Prioritized reading list (max 12) with rationale

1) **`archive/tavily_search.jsonl`**  
   *Rationale:* Primary coverage of “industry use cases” and recent discussions; contains many candidate citations with summaries. Start here to identify the best authoritative outlets (Nature/Science/IEEE Spectrum etc., if present later in the file).

2) **`archive/youtube/transcripts/youtu.be-sQSQBYHR0ms-Quantum_Computing_and_AI.txt`**  
   *Rationale:* The only long-form narrative source in the run; useful for explaining concepts and capturing popular claims to fact-check against stronger sources.

3) **`archive/youtube/videos.jsonl`**  
   *Rationale:* Metadata (date, channel, description, tags) for citing the video properly and contextualizing the transcript.

4) **`archive/20260108_qc-youtube-index.md`**  
   *Rationale:* Quick run scoping (queries count, days window, which collectors ran) and a pointer list of what exists/missing.

5) **`archive/_job.json`**  
   *Rationale:* Provenance: confirms flags like `--days 30 --max-results 5 --youtube --yt-transcript`; helpful for method writeup/limitations.

6) **`archive/_log.txt`**  
   *Rationale:* Checks for collection errors/omissions (e.g., why Nature/Science didn’t appear, whether some steps failed).

7) **`archive/arxiv/papers.jsonl`**  
   *Rationale:* Only to document that the arXiv IDs are off-topic and should not be used as evidence in the narrative review.

(Only 7 files exist in the archive; the list above is exhaustive.)

---

## Suggested reading plan (to support a narrative review w/ clear explanations + citations)

1. **Scan `20260108_qc-youtube-index.md` + `_job.json`** to understand constraints (30-day window, max results, limited sources).  
2. **Mine `tavily_search.jsonl` systematically**:  
   - Extract the most credible sources first (peer-reviewed journals, major tech journalism, industry consortia like QED-C).  
   - Down-rank vendor blogs/marketing pages unless they provide unique, verifiable details.  
3. **Read the YouTube transcript** and mark: (a) definitions/analogies worth reusing, (b) any strong claims (speedups, timelines, “QPU replaces GPU”, etc.) that need validation.  
4. **Cross-check YouTube claims against the strongest web sources** found in Tavily before using them in the narrative.  
5. **Use `_log.txt`** to note collection gaps/limitations in the final report methods (e.g., missing OpenAlex/Nature links despite being requested in instructions).

If you want, I can also (next step) extract a “best-citation shortlist” from `tavily_search.jsonl` (top ~10 URLs) optimized for authority and narrative flow.