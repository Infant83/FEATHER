## Archive map (Query ID: `20260105_arxiv-gnn`)

**Run intent / focus:** “Analyze main ideas, methods, and implications. Highlight trends and open problems.”  
**Instruction input:** `arxiv`, query “graph neural networks”, explicit arXiv ID `2101.00001`, plus 1 LinkedIn URL.

### 1) Top-level indices & logs
- `archive/20260105_arxiv-gnn-index.md` — Run manifest: what was fetched (Tavily, arXiv, OpenAlex), PDFs/text paths.
- `archive/_job.json` — Job configuration + parameters (useful to understand retrieval scope/limits).
- `archive/_log.txt` — Execution log (helps diagnose missing sources / why some weren’t downloaded).

### 2) JSONL metadata indices (coverage overview)
- `archive/tavily_search.jsonl` — Web search results for “graph neural networks” (mostly general/tutorial content; not research-primary).
- `archive/arxiv/papers.jsonl` — arXiv metadata for the single requested ID.
- `archive/openalex/works.jsonl` — OpenAlex works harvested for the query; includes abstracts + links; duplicates exist for same work.

### 3) Primary documents (full text / PDFs)
**OpenAlex PDFs + extracted text (3 research items):**
- `archive/openalex/pdf/W7119235243.pdf` + `archive/openalex/text/W7119235243.txt`  
  **Learning from Historical Activations in Graph Neural Networks** (arXiv:2601.01123, 2026-01-03)
- `archive/openalex/pdf/W4417529673.pdf` + `archive/openalex/text/W4417529673.txt`  
  **Graph Neural Networks for Interferometer Simulations** (arXiv:2512.16051, 2025-12-18)
- `archive/openalex/pdf/W4417330266.pdf` + `archive/openalex/text/W4417330266.txt`  
  **Flavour Tagging with Graph Neural Network with the ATLAS Detector** (PoS(DIS2025)080, 2025-12-05)

**arXiv PDF + extracted text (1 item, likely off-focus vs “GNN”):**
- `archive/arxiv/pdf/2101.00001v1.pdf` + `archive/arxiv/text/2101.00001v1.txt`  
  **Etat de l'art sur l'application des bandits multi-bras** (multi-armed bandits survey, 2021)

### 4) Web extraction (non-archival commentary)
- `archive/tavily_extract/0001_https_www.linkedin.com_posts_fanli_ai-molecular-design-has-some-known-challenges-activity-...txt`  
  LinkedIn post summarizing a molecular design framework (“Trio”); not clearly GNN-centric.

---

## Relevance triage (to your report focus)

### Highly relevant (GNN research contributions)
1) **HISTOGRAPH (historical activations + attention readout)** — directly methodological; clear implications for deep GNNs, pooling, oversmoothing.
2) **GNN surrogate simulation for LIGO interferometers** — applied GNNs for physics simulation + dataset release; implications for AI-for-science + surrogate modeling.
3) **ATLAS flavour tagging GNNs (GN1/GN2)** — applied GNNs/transformer-style attention at scale; trends in multimodal + multitask training and robustness to HL-LHC conditions.

### Medium/low relevance (context/background)
- Tavily search results (DataCamp/GeeksforGeeks/Wikipedia/IBM etc.) — general intros; can be used only for lightweight framing/definitions.
- LinkedIn “Trio” molecular design — likely off-topic unless your report also discusses graph methods in chemistry; as-is it’s about LM + MCTS + DPO.

### Off-topic vs query (“graph neural networks”)
- arXiv:2101.00001 (bandits survey) — mismatch with GNN focus; only include if you explicitly want a “retrieval error / query drift” note.

---

## Prioritized reading plan (max 12 files)

1) `archive/openalex/text/W7119235243.txt`  
   **Why:** Core new GNN method (HISTOGRAPH). Best for “main ideas/methods/implications” + open problems (deep GNNs, oversmoothing, pooling).

2) `archive/openalex/pdf/W7119235243.pdf`  
   **Why:** Figures/method details, experiments, ablations; use if the text extraction misses equations/diagrams.

3) `archive/openalex/text/W4417529673.txt`  
   **Why:** Clear applied-method paper: graph construction for interferometers, model choice (deep GATv2 stack), dataset design; highlights trends in surrogate simulation.

4) `archive/openalex/pdf/W4417529673.pdf`  
   **Why:** Pipeline figures + dataset tables + architectural diagrams; better for technical deep dive.

5) `archive/openalex/text/W4417330266.txt`  
   **Why:** Practical large-experiment GNN use (ATLAS). Useful for implications/trends: transformer-inspired attention, multitask objectives, robustness/generalization.

6) `archive/openalex/pdf/W4417330266.pdf`  
   **Why:** Plots of rejection vs efficiency, HL-LHC discussion; ensures you capture quantitative claims correctly.

7) `archive/openalex/works.jsonl`  
   **Why:** Fast scan of abstracts + metadata; helps ensure no key OA work is missed and reveals duplicates to ignore.

8) `archive/20260105_arxiv-gnn-index.md`  
   **Why:** High-level inventory; cite exactly what corpus the report is based on.

9) `archive/tavily_search.jsonl`  
   **Why:** Only for brief “what is a GNN” framing or to note that web results were mostly general-audience.

10) `archive/tavily_extract/0001_https_www.linkedin.com_posts_fanli_ai-molecular-design-...txt`  
   **Why:** Optional “adjacent trend” (closed-loop discovery + search/optimization); include only if you broaden implications beyond strict GNNs.

11) `archive/arxiv/papers.jsonl`  
   **Why:** Confirms the arXiv item mismatch; can document scope/limitations of the run.

12) `archive/arxiv/text/2101.00001v1.txt` (or PDF if needed)  
   **Why:** Likely exclude from the final GNN deep dive; read only if you need to verify it’s irrelevant or mention as retrieval noise.

---

## Notable gaps / issues to be aware of
- **Query drift:** The explicitly provided arXiv ID `2101.00001` is about **bandits**, not GNNs; the run nonetheless pulled strong GNN material via OpenAlex.
- **Small research corpus:** Only **3** research PDFs clearly about GNNs; trends/open problems will need to be synthesized across these plus your own framing, rather than a broad literature sweep.
- **OpenAlex duplicates:** `openalex/works.jsonl` contains repeated entries for the interferometer and HISTOGRAPH items (same title, different OA IDs/DOIs). Deduplicate when citing.