Updated plan (with completions + missing steps added):

- [x] Review instruction/20260107_ai-trends.txt — scope/constraints check  
  - Note: this “instruction” file is only a **query list** (no tone/template constraints embedded).

- [x] Extract sources from archive/tavily_search.jsonl — pull all distinct titles/URLs/snippets and note credibility/limitations  
  - Note: tavily_search.jsonl contains **only 2 lines** (two executed queries) and sources are mostly **vendor/consulting** + State of AI.

- [x] Confirm whether any CES/conference/robotics-specific evidence exists in tavily_search.jsonl beyond the two executed queries; if not, mark as gap  
  - Confirmed: **no CES/conference/robotics-specific** results captured in the archive; “emerging AI technologies 2026” query failed per _log.txt.

- [ ] Add missing step: locate/confirm the **report template/format expectations** elsewhere (since instruction file has none); if none, define a minimal consistent template and note the assumption in Provenance

- [ ] Cluster evidence into 6–8 trend buckets — group sources into buckets and identify strongest evidence per bucket

- [ ] Select the “Top 10” breakthroughs — ensure coverage across agents, physical AI/robotics, chips/infra, governance/safety; avoid “10 variants of agents” given limited evidence

- [ ] Draft the report in template structure — Executive Summary + How We Chose + 10 numbered H3 entries (What/Why/Key players/Availability)

- [ ] Synthesize cross-cutting insights — 3–5 themes tied back to specific archived snippets/sources

- [ ] Add decision-focused sections — Industry Implications + Risks & Gaps (explicitly call out missing CES/conference/robotics capture and the failed query)

- [ ] Provenance + quality pass — use archive/_job.json and archive/_log.txt to document run limits; edit for clarity, consistency, traceability; MIT Tech Review-style tone