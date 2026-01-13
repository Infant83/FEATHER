## Archive map (what’s in this run)

### Top-level archive inventory
1. **`archive/tavily_search.jsonl`** (53 KB)  
   *Role:* Primary source index for this run. Contains the web search results/snippets used to ground “AI trends 2025/2026” and related subtopics (agentic AI, robotics/physical AI, chips, governance, infrastructure, etc.).  
2. **`archive/_job.json`** (4 KB)  
   *Role:* Run/job metadata (likely config: query id, timestamps, tool settings). Useful for provenance/reproducibility, not for report substance.  
3. **`archive/_log.txt`** (407 B)  
   *Role:* Minimal execution log; use only if debugging what ran/failed.

### Instruction / scope inputs
- **`instruction/20260107_ai-trends.txt`**  
  *Role:* Query list and target sites/topics (linkedin, arxiv, github; plus prompts like “agentic AI”, “physical AI robotics”, “CES 2026 …”, “NeurIPS/ICLR/ICML/CVPR/ACL/AAAI trends”). This defines intended coverage, even if not all were retrieved.

### Coverage reality check (based on reading `tavily_search.jsonl`)
- The index currently shows **a small set of high-level “AI trends 2025” sources** (e.g., Spencer Stuart, Microsoft Source, McKinsey, Cisco) and **State of AI Report 2025** snippet text.
- I **do not** see separate JSONL indices for arXiv/OpenAlex/YouTube in the archive (none present), and the “supporting folder” isn’t available—so this run appears **web-snippet heavy** and **light on primary research papers**.

---

## Key source files (what to read first for the report)

### Prioritized reading list (max 12)
1. **`archive/tavily_search.jsonl`**  
   *Why:* It’s the only substantive source container; you’ll extract the “10 breakthroughs” candidates + implications from its URLs/snippets.

2. **`instruction/20260107_ai-trends.txt`**  
   *Why:* Use as a checklist to ensure your “10 breakthroughs” aren’t skewed (it signals desired angles: agents, robotics, conferences, CES 2026, etc.).

3. **`archive/_job.json`**  
   *Why:* Confirms what tools/queries were actually executed; helps explain gaps (e.g., why no arXiv/OpenAlex outputs exist).

4. **`archive/_log.txt`**  
   *Why:* Only to confirm whether any collection steps failed (low value for synthesis).

### Highest-value external sources *referenced inside* `tavily_search.jsonl` (open via their URLs if your pipeline fetches full text later)
These are not separate files in the archive, but they are the *anchors* you’ll likely base short “breakthrough + implication” sections on:
- **State of AI Report 2025** (`stateof.ai`) — broad, synthesis-ready (infra, policy, safety pragmatism, adoption).
- **McKinsey technology trends outlook 2025** — structured taxonomy (agentic AI, app-specific semiconductors, intersections).
- **Microsoft Source: “6 AI trends you’ll see more of in 2025”** — mainstream framing + science acceleration + infra sustainability.
- **Cisco blog predictions for 2025** — enterprise angle: smaller/specialized models, cost, compliance, reskilling.
- **Spencer Stuart “top three AI trends of 2025”** — agent framing + governance/privacy/ethics implications.

---

## Proposed reading plan (optimized for “short and sharp” breakthroughs + implications)

1. **Scan `tavily_search.jsonl` end-to-end** and list all distinct URLs/titles; cluster into buckets:  
   *Agents & autonomy; Compute/semis & data centers; Science/biomed/materials; Robotics/physical AI; Security/safety/governance; Enterprise adoption/workforce.*

2. **Pick 10 “breakthrough statements”** (1 sentence each) from the strongest buckets, ensuring diversity (not 10 variants of “agents”). Use Instruction file topics as balancing constraints.

3. **For each breakthrough, draft 2 implications** (one technical/industry, one societal/policy), keeping each bullet tight.

4. **Use `_job.json` only to annotate limitations** (e.g., “no direct arXiv paper ingestion in this run”) so the report is honest about evidence depth.

If you want, I can also extract a clean table of all URLs/titles found in `tavily_search.jsonl` and propose a concrete “Top 10 breakthroughs” candidate list aligned to the MIT Tech Review-style template.