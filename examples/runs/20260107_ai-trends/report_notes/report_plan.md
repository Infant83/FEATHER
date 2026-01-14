- [x] Confirm scope & success criteria — read `instruction/20260107_ai-trends.txt` (it defines the query set + hints: linkedin/arxiv/github; implies a “10 breakthroughs”-style output).  
- [x] Audit available evidence — read `archive/_job.json` + `archive/_log.txt` (only Tavily ran; “emerging AI technologies 2026” failed; OpenAlex enabled but produced no artifacts; no linkedin/arxiv/github/CES/site-specific outputs present).  
- [x] Extract source inventory from Tavily — parsed `archive/tavily_search.jsonl` (2 queries captured; 10 total results; needs dedupe if near-identical, but current set is already distinct).  
- [x] Build candidate breakthrough pool (10–15) — can be clustered only from the limited 10 sources (agents; AI-for-science; AI infra/energy; specialized models; chips; confidential computing; AI-native dev; org-level genAI; multimodal; sovereignty/trust).  
- [ ] Select final Top 10 — **blocked by evidence thinness** (current archive likely can’t credibly support 10 distinct “breakthroughs” with 1–2 strong URLs each without re-collecting missing query outputs).  
- [ ] Draft each breakthrough entry — pending (requires final Top 10 selection + per-item template fields: What/Why/Players/Availability).  
- [ ] Synthesize cross-cutting sections — pending (Exec Summary, How We Chose, Themes, Implications, Risks & Gaps; must explicitly note evidence limits).  
- [ ] Add provenance & QA pass — pending (breakthrough→URLs→origin query; redundancy/hype/template compliance).  

Missing step to finish the report:
- [ ] **Rebuild/refresh evidence**: re-run the failed/missing collectors/queries requested in the instruction file (agentic AI; physical AI/robotics; recent 30 days; CES 2026; TechReview/IEEE/VentureBeat; NeurIPS/ICLR/ICML/CVPR/etc.; plus linkedin/arxiv/github and OpenAlex outputs). If re-collection isn’t possible, add an explicit constraint section and **reduce scope/claims** accordingly.