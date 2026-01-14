## Archive map (what’s in this run)

**Run / query context**
- **Query ID:** 20260105_arxiv-gnn  
- **Focus prompt:** *Analyze main ideas, methods, and implications. Highlight trends and open problems.*
- **Instruction file:** `instruction/20260105_arxiv-gnn.txt`  
  - Inputs: `graph neural networks`, **arXiv:2101.00001**, plus a LinkedIn post URL.

**High-level index**
- `archive/20260105_arxiv-gnn-index.md` (overview of all captured sources and downloaded artifacts)

**Metadata indices (JSONL) — must-use for coverage**
- `archive/tavily_search.jsonl` (web search results for “graph neural networks”; mostly general explainers)
- `archive/openalex/works.jsonl` (OpenAlex works metadata; includes abstracts, DOIs, OA status; note duplicates)
- `archive/arxiv/papers.jsonl` (arXiv metadata for explicitly provided arXiv ID)

**Primary technical sources (downloaded papers)**
OpenAlex texts/PDFs (GNN-related and recent):
- `archive/openalex/pdf/W7119235243.pdf` + `archive/openalex/text/W7119235243.txt`  
  - **Learning from Historical Activations in Graph Neural Networks** (Galron et al., arXiv:2601.01123, 2026-01-03)
- `archive/openalex/pdf/W4417529673.pdf` + `archive/openalex/text/W4417529673.txt`  
  - **Graph Neural Networks for Interferometer Simulations** (Kannan et al., arXiv:2512.16051, 2025-12-18)
- `archive/openalex/pdf/W4417330266.pdf` + `archive/openalex/text/W4417330266.txt`  
  - **Flavour Tagging with Graph Neural Network with the ATLAS Detector** (PoS(DIS2025)080, 2025-12-15)

arXiv texts/PDFs (explicit arXiv ID from instruction; **not GNN-focused**):
- `archive/arxiv/pdf/2101.00001v1.pdf` + `archive/arxiv/text/2101.00001v1.txt`  
  - **Etat de l'art sur l'application des bandits multi-bras** (Bouneffouf, 2021) — multi-armed bandits review; likely off-focus.

**Web extraction**
- `archive/tavily_extract/0001_https_www.linkedin.com_posts_fanli_ai-molecular-design-has-some-known-challenges-activity-7406324682192441344-60n3_utm_s.txt`  
  - LinkedIn post content (appears tangential; likely about AI molecular design challenges)

**Run logs / provenance**
- `archive/_job.json` (job config/provenance)
- `archive/_log.txt` (run log)

---

## Notable coverage gaps / quirks
- The instruction includes **arXiv:2101.00001** which is about **bandits**, not GNNs → treat as an input mismatch/off-topic unless your report wants “adjacent methods.”
- `openalex/works.jsonl` contains **duplicate entries** for the same work (e.g., “Graph Neural Networks for Interferometer Simulations” appears multiple times with different OpenAlex IDs). Prefer the one with an actual downloaded PDF (`W4417529673`) and the most complete metadata.
- Tavily search results are **general introductions** (DataCamp, GeeksforGeeks, IBM, Wikipedia, XenonStack). Useful only for brief definitions, not for the technical deep dive.

---

## Prioritized reading plan (max 12 files)

1) **`archive/openalex/text/W7119235243.txt`**  
   *Core methods paper for the report focus.* Introduces **HISTOGRAPH**: layer-wise attention over intermediate activations + node-wise attention; directly addresses deep GNN issues (over-smoothing, information loss). Great for “main ideas/methods/open problems”.

2) **`archive/openalex/pdf/W7119235243.pdf`**  
   Use for figures, experimental tables, ablations, and precise formulation details that may be lost/truncated in text extraction.

3) **`archive/openalex/text/W4417529673.txt`**  
   Strong “implications” paper: GNN surrogate modeling for **instrumentation design** (LIGO interferometer simulations), claims **~815× speedup**; includes dataset contribution and domain-specific challenges.

4) **`archive/openalex/pdf/W4417529673.pdf`**  
   For technical specifics: graph construction for optical systems, loss definitions, baselines vs. simulators, dataset specs.

5) **`archive/openalex/text/W4417330266.txt`**  
   Application trend paper: **GNNs in HEP** (ATLAS flavour tagging), evolution from DNN taggers to **GN1/GN2** (GAT/transformer-inspired attention), plus multimodal/multitask setup.

6) **`archive/openalex/pdf/W4417330266.pdf`**  
   For architecture diagrams, performance numbers (light/c-jet rejection factors), and HL-LHC perspective details.

7) **`archive/openalex/works.jsonl`**  
   Coverage audit: abstracts, dates, duplication, and any additional works (e.g., Zenodo CLGNN entries not downloaded). Use to ensure the report accurately reflects what’s in-scope and recent.

8) **`archive/tavily_search.jsonl`**  
   Only if you need a short, sourced background paragraph defining GNNs/message passing; otherwise low priority.

9) **`archive/tavily_extract/0001_https_www.linkedin.com_posts_fanli_ai-molecular-design-has-some-known-challenges-activity-7406324682192441344-60n3_utm_s.txt`**  
   Likely tangential; scan quickly for any concrete claims about GNNs in molecular design that could motivate “implications/open problems,” but don’t anchor the report on it.

10) **`archive/arxiv/text/2101.00001v1.txt`**  
   Off-focus (multi-armed bandits). Read only if you decide to discuss exploration–exploitation as a recurring theme in design optimization / active learning around GNN surrogates.

11) **`archive/arxiv/pdf/2101.00001v1.pdf`**  
   Same as above; consult only if you keep the bandits thread.

12) **`archive/20260105_arxiv-gnn-index.md`**  
   Quick navigation/provenance reference while writing; not content-heavy, but helpful for citations and file mapping.

--- 

If you want, I can also propose a **section-by-section report outline** (technical_deep_dive style) keyed to these three main papers (HISTOGRAPH, LIGO surrogate, ATLAS tagging) and map “trends/open problems” to concrete quotes/sections to extract.