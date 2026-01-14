## What’s available in this run (evidence audit)

- Only **3 archive files** exist: `archive/tavily_search.jsonl`, `archive/_job.json`, `archive/_log.txt` (no OpenAlex/arXiv/YouTube/local manifests were produced in this run). [`archive/_job.json`, `archive/_log.txt`]
- The job configuration *enabled* OpenAlex (`openalex_enabled: true`) but **no OpenAlex outputs** are present in the archive. [`archive/_job.json`]
- The runtime log shows Tavily searches ran for:
  - “AI trends 2025 (English)”
  - “AI trends 2026 (English)”
  - “emerging AI technologies 2026 (English)” → **failed** with `OSError(22, 'Invalid argument')` (so evidence coverage is truncated). [`archive/_log.txt`]
- Instruction scope asked for **linkedin / arxiv / github** plus many venue-specific queries (Technology Review, IEEE, VentureBeat, CES 2026, conference “best papers”). None of those collectors/results appear in the archive; only Tavily results for the first two queries are captured. [`instruction/20260107_ai-trends.txt`, `archive/_log.txt`, `archive/tavily_search.jsonl`]

---

## Web sources captured (Tavily results) — salient facts to reuse as “breakthrough” evidence

### 1) Spencer Stuart (AI trends 2025 framing)
Source: https://www.spencerstuart.com/research-and-insight/the-top-three-ai-trends-of-2025-according-to-ai  [`archive/tavily_search.jsonl`]
- Claims “rapid rise of **autonomous agents**” by 2025; “beyond chatbots” agents will proactively manage calendar, negotiate, co-create content, triage email. [`archive/tavily_search.jsonl`]
- Notes enterprise scaling of AI agent pilots and governance/accountability risks if agents make erroneous decisions. [`archive/tavily_search.jsonl`]
- Also frames “quantum-powered AI” as enabling materials discovery, climate modeling precision, and cryptography/security advances. [`archive/tavily_search.jsonl`]

### 2) Microsoft Source (6 AI trends for 2025)
Source: https://news.microsoft.com/source/features/ai/6-ai-trends-youll-see-more-of-in-2025/  [`archive/tavily_search.jsonl`]
- Predicts AI tools will have “measurable impact on the **throughput**” of researchers tackling sustainable materials and drug development (quote attributed to Microsoft Research leadership). [`archive/tavily_search.jsonl`]
- Highlights AI infrastructure efficiency/sustainability investments (low-carbon materials; carbon-free energy sources such as wind/geothermal/nuclear/solar). [`archive/tavily_search.jsonl`]

### 3) McKinsey (Technology trends outlook 2025)
Source: https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-top-trends-in-tech  [`archive/tavily_search.jsonl`]
- Positions AI as a “foundational amplifier” across domains (robot training, bioengineering discovery, energy optimization). [`archive/tavily_search.jsonl`]
- Notes McKinsey updated its trend taxonomy: replaces multiple AI categories with an overarching AI category, and **adds “agentic AI” and “application-specific semiconductors”** as new trends. [`archive/tavily_search.jsonl`]
- Executive implication: success requires identifying high-impact domains, investing in talent/infrastructure, and addressing regulatory/ecosystem readiness. [`archive/tavily_search.jsonl`]

### 4) Cisco (Six AI predictions for 2025)
Source: https://blogs.cisco.com/partner/six-ai-predictions-for-2025-that-will-reshape-how-we-think-about-enterprise-technology  [`archive/tavily_search.jsonl`]
- Predicts a shift away from “massive GPU clusters” toward **smaller, specialized models** due to unsustainable LLM costs; cites training costs of **$4.6M–$12M per run** and “thousands of high-end GPUs.” [`archive/tavily_search.jsonl`]
- Argues organizations will prefer bespoke models for control/compliance/cost efficiency as dissatisfaction grows around accuracy/confidence of general-purpose models. [`archive/tavily_search.jsonl`]
- Predicts accelerated reskilling and internal talent conversion pathways as AI talent scarcity intensifies. [`archive/tavily_search.jsonl`]
- Predicts partnerships become core to AI deployment due to operational complexity and talent scarcity. [`archive/tavily_search.jsonl`]

### 5) State of AI Report 2025 (stateof.ai)
Source: https://www.stateof.ai/  [`archive/tavily_search.jsonl`]
- Reports survey stats: **95%** of professionals use AI at work/home; **76%** pay out of pocket; respondents report sustained productivity gains. [`archive/tavily_search.jsonl`]
- Claims “industrial era of AI” with **multi‑GW data centers**; “power supply emerging as the new constraint.” [`archive/tavily_search.jsonl`]
- Notes geopolitics: “America-first AI,” EU AI Act issues, China expanding open-weights ecosystem and domestic silicon ambitions. [`archive/tavily_search.jsonl`]
- Notes safety discourse shift: existential risk debate cooled; focus moving to reliability, cyber resilience, governance of more autonomous systems; “models can now imitate alignment under supervision.” [`archive/tavily_search.jsonl`]

---

## 2026-focused sources captured — salient facts

### 6) Gartner (Top 10 Strategic Technology Trends for 2026)
Source: https://www.gartner.com/en/articles/top-technology-trends-2026  [`archive/tavily_search.jsonl`]
- Groups trends under “AI platforms and infrastructure,” including:
  - **AI-Native Development Platforms** (genAI-assisted software building)
  - **AI Supercomputing Platforms** (training/analytics with governance + cost control needs)
  - **Confidential Computing** (protect data “while in use,” enabling secure AI/analytics). [`archive/tavily_search.jsonl`]
- Also frames “AI application and orchestration” as combining specialized models, agents, and physical-digital systems. [`archive/tavily_search.jsonl`]

### 7) MIT Sloan Management Review (Five Trends in AI and Data Science for 2026)
Source: https://sloanreview.mit.edu/article/five-trends-in-ai-and-data-science-for-2026/  [`archive/tavily_search.jsonl`]
- Summarizes five trends:
  - deflation of an “AI bubble”
  - growth of “factory” infrastructure for “AI adapters”
  - genAI as an **organizational resource** (not individual)
  - progression toward value from **agentic AI** despite hype
  - questions around who should manage data and AI. [`archive/tavily_search.jsonl`]
- Predicts agents fall into Gartner’s “trough of disillusionment” in 2026 (after being highly hyped). [`archive/tavily_search.jsonl`]

### 8) Microsoft Source (7 trends to watch in 2026)
Source: https://news.microsoft.com/source/features/ai/whats-next-in-ai-7-trends-to-watch-in-2026/  [`archive/tavily_search.jsonl`]
- Frames 2026 as AI moving “from instrument to partner,” emphasizing collaboration and real-world impact. [`archive/tavily_search.jsonl`]
- Notes that as agents become “digital colleagues,” organizations strengthen security to keep pace with new risks; infrastructure is “maturing” with more efficient systems. [`archive/tavily_search.jsonl`]
- Predicts AI becomes central to research: beyond summarizing/writing reports, AI will “generate hypotheses,” use tools/apps controlling experiments, and collaborate with human + AI colleagues. [`archive/tavily_search.jsonl`]

### 9) Harvard Business School Working Knowledge (AI trends for 2026)
Source: https://www.library.hbs.edu/working-knowledge/ai-trends-for-2026-building-change-fitness-and-balancing-trade-offs  [`archive/tavily_search.jsonl`]
- Emphasizes leaders seeking more value from AI in 2026; advises focusing on solving “real problem” with “verifiable customer pain” as product barriers drop and development speeds up. [`archive/tavily_search.jsonl`]
- Notes autonomous agents absorb analytical/modeling tasks; differentiation shifts toward human judgment/insight and client relationships in professional services. [`archive/tavily_search.jsonl`]

### 10) IBM (AI/tech trends predictions 2026)
Source: https://www.ibm.com/think/news/ai-tech-trends-predictions-2026  [`archive/tavily_search.jsonl`]
- Predicts AI shifts from individual usage to **team/workflow orchestration**; and from passive assistant to active collaborator as reasoning improves. [`archive/tavily_search.jsonl`]
- Highlights **multimodal (“multisensory”) AI** bridging language/vision/action; anticipates “multimodal digital workers” that can autonomously complete tasks and interpret complex cases (e.g., healthcare). [`archive/tavily_search.jsonl`]
- Predicts efficiency/compute evolution: GPUs remain dominant, but ASIC accelerators, chiplets, analog inference, and possibly quantum-assisted optimizers mature; mentions possible new chip class for “agentic workloads.” [`archive/tavily_search.jsonl`]
- Notes enterprise focus on trust/security and “AI sovereignty.” [`archive/tavily_search.jsonl`]