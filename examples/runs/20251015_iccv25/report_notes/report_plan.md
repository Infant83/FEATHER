Plan (updated)

- [ ] Scope & success criteria — Confirm report focus (“key ICCV 2025 papers + code links + research gaps + practical impact”) and define what qualifies as “key” (main conference vs workshops/challenges; evidence thresholds; how many papers/which clusters).  
- [x] Audit the run archive — Read `archive/20251015_iccv25-index.md` + `archive/_log.txt` to diagnose collection gaps and document coverage limits.  
- [x] Reconstruct the canonical ICCV 2025 landscape — Mine `archive/tavily_search.jsonl` to extract authoritative hubs (CVF Open Access “All Papers”, OpenReview group, MMLab@NTU accepted-papers list, etc.) and how they would be used to build a key-paper list.  
- [ ] Build a source-of-truth table from OpenAlex — Parse `archive/openalex/works.jsonl` to classify each downloaded work (ICCV main / workshop / non-ICCV) and extract structured fields (title, venue signal, DOI/arXiv, PDF/text paths, dataset/code URLs).  
- [ ] Enumerate + extract URLs from local texts — List `archive/openalex/text/*.txt`, deep-read prioritized items (remote-sensing VLM survey, R-LiViT, VQualA reports, SAMSON, DRL4Real) and extract methods/datasets/results/limitations + all embedded links (GitHub/Zenodo/project pages) into an “assets” table.  
- [ ] Cross-link with ICCV hubs for “key papers” — Use CVF/OpenReview/MMLab to select representative ICCV 2025 *main-conference* papers across clusters and attach paper/project/code links; **if not locally ingested, explicitly mark as “requires rerun crawl”**.  
- [ ] Synthesize research gaps & practical impact — Aggregate recurring limitations and translate into actionable R&D opportunities + deployment considerations (compute/latency, data collection, eval protocol, robustness/domain shift).  
- [ ] Assemble the technical_deep_dive report — Write per template sections with citations to archive files and clear separation of empirical findings vs inference.  
- [ ] Finalize deliverables & rerun recommendations — Produce (1) “Key papers & links” table, (2) gap/practical-impact summary, (3) concrete FEATHER rerun queries/params (including CVF OA page crawl + GitHub/topic search + OpenReview scraping).

Missing step(s) to finish the report that weren’t explicit before
- [ ] Define output format constraints up front (target length, number of “key papers”, required clusters, citation style, and whether workshops/challenges count as “key” or “supporting evidence”).