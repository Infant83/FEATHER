## Source inventory (what’s available to cite)

- **LinkedIn (5 results, snippets + summaries; no full-page extraction)** from Tavily search output for query `quantum computing site:linkedin.com`  
  Evidence file: [archive/tavily_search.jsonl]  
  Underlying URLs:
  - https://www.linkedin.com/pulse/quantum-computing-future-technology-jobs-create-morgan-feldman-i8sje
  - https://www.linkedin.com/pulse/quantum-computing-what-how-its-being-used-gerges-dit-m-sc--o1k4c
  - https://learning.linkedin.com/resources/learning-tech/quantum-cloud-computing-tools-tips-tech
  - https://www.linkedin.com/pulse/7-quantum-computing-trends-shape-every-industry-2026-bernard-marr-efwke
  - https://www.linkedin.com/posts/bernardmarr_5-game-changing-quantum-computing-use-cases-activity-7318155678542385152-1t1v

- **Direct URL extract attempt: failed (404)**  
  Evidence file: [archive/tavily_extract/0001_https_example.com_blog_post.txt]  
  Underlying URL: https://example.com/blog/post

- **arXiv (metadata only; appears off-topic vs “quantum computing”)**  
  Evidence file: [archive/arxiv/papers.jsonl]  
  Underlying URL: http://arxiv.org/abs/2101.00001v1 (PDF: https://arxiv.org/pdf/2101.00001v1)

- **Run configuration / limitations** (why coverage is narrow: LinkedIn-only hint; OpenAlex/YouTube disabled; PDFs not downloaded)  
  Evidence files: [archive/_job.json], [archive/20260106_mixed-index.md], [archive/_log.txt]


## Salient trend signals (grouped by source type)

### A) LinkedIn cluster (recurring signals across multiple independent LinkedIn URLs)
- **Near-term business framing: optimization, data analysis, AI/ML, and industry use cases (healthcare/drug discovery, finance, logistics).**  
  - Morgan Feldman article claims QC could “transform industries… ranging from healthcare to finance, logistics, and AI,” and highlights “Healthcare and Drug Discovery” plus “Finance and Risk Analysis.” [archive/tavily_search.jsonl] (https://www.linkedin.com/pulse/quantum-computing-future-technology-jobs-create-morgan-feldman-i8sje)  
  - LinkedIn Learning page frames “Quantum Computing in Modern Business” with “Data analysis and optimization” and “Artificial intelligence and machine learning.” [archive/tavily_search.jsonl] (https://learning.linkedin.com/resources/learning-tech/quantum-cloud-computing-tools-tips-tech)

- **Cybersecurity/cryptography risk + “quantum-safe” transition narrative.**  
  - Morgan Feldman article: QC “could crack traditional encryption codes” while enabling “quantum-based encryption methods.” [archive/tavily_search.jsonl] (https://www.linkedin.com/pulse/quantum-computing-future-technology-jobs-create-morgan-feldman-i8sje)  
  - LinkedIn Learning page: “Current encryption methods… could become obsolete… New quantum-safe encryption methods are in development.” [archive/tavily_search.jsonl] (https://learning.linkedin.com/resources/learning-tech/quantum-cloud-computing-tools-tips-tech)  
  - Bernard Marr LinkedIn post excerpt: systems “could break current encryption methods, prompting the need for quantum-resistant alternatives.” [archive/tavily_search.jsonl] (https://www.linkedin.com/posts/bernardmarr_5-game-changing-quantum-computing-use-cases-activity-7318155678542385152-1t1v)

- **Adoption model signal: “quantum cloud computing” as the pragmatic access path (skills + remote access vs owning hardware).**  
  - LinkedIn Learning page defines “Cloud-based quantum computing” as access “over the internet,” eliminating the need to “own a physical quantum computer,” and argues IT teams should build working knowledge. [archive/tavily_search.jsonl] (https://learning.linkedin.com/resources/learning-tech/quantum-cloud-computing-tools-tips-tech)

- **Commercialization / timeline signaling used as market-readiness indicator.**  
  - Bernard Marr LinkedIn post excerpt states: “Microsoft and Atom Computing… intention to provide commercially available quantum computers starting in 2025.” [archive/tavily_search.jsonl] (https://www.linkedin.com/posts/bernardmarr_5-game-changing-quantum-computing-use-cases-activity-7318155678542385152-1t1v)

### B) Direct URL extraction (negative signal / gap)
- **The only explicitly provided non-LinkedIn URL failed extraction (404), limiting triangulation beyond LinkedIn.**  
  - Extract log shows `error: "404 page not found"` for https://example.com/blog/post. [archive/tavily_extract/0001_https_example.com_blog_post.txt]

### C) arXiv channel (off-topic artifact + missing full text)
- **arXiv record is about multi-armed bandits (cs.LG/cs.AI), not quantum computing; only metadata is present (no PDF/text downloaded).**  
  - Title: “Etat de l'art sur l'application des bandits multi-bras”; summary describes bandit algorithms (epsilon-greedy, UCB, Thompson Sampling). [archive/arxiv/papers.jsonl] (http://arxiv.org/abs/2101.00001v1)  
  - Run index confirms “PDFs: 0; Extracted texts: 0.” [archive/20260106_mixed-index.md]

## Run constraints / quality notes that affect confidence
- **Single-platform skew**: query was forced to `site:linkedin.com` (seen in logs), so “cross-source” is effectively “cross-result within LinkedIn,” not cross-platform. [archive/_log.txt]  
- **OpenAlex/YouTube disabled; PDFs not downloaded**, reducing independent corroboration. [archive/_job.json]  
- **Citations lookup failed** for arXiv ID via OpenAlex API (HTTP 400), further reducing usable scholarly linkage. [archive/_log.txt]