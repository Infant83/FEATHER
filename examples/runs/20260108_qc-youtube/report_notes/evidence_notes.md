## Run scope & provenance (what this archive actually contains)

- **Run parameters (coverage constraints):** last **30 days**, **10** Tavily queries, **max 5 results/query**; **YouTube enabled** with **transcript extraction**; **OpenAlex disabled**; **no PDF downloads**. Source: run config JSON. [archive/_job.json]  
- **Collected artifacts:** Tavily web search results (JSONL), **1 YouTube video + transcript**, arXiv metadata for **2 IDs** (but **no PDFs/texts**). Source: run index. [archive/20260108_qc-youtube-index.md]  
- **Known collection gaps / issues:** YouTube search was skipped because there were **no `site:youtube.com` query hints**; transcript was gathered via the **direct URL**. OpenAlex citation lookups for arXiv IDs failed with HTTP 400. Source: execution log. [archive/_log.txt]

---

## Web sources (Tavily results → salient evidence snippets + URLs)

- **Quantum Computing Report — “News” (industry news roundup page)**
  - Mentions **Quantum Computing Inc. (QCi) “Neurawave”** as a **photonics-based reservoir computing** system, described as **compact/room-temperature**, using **PCIe**, positioned for **edge-AI use cases** (e.g., “signal processing” and “time-series forecasting”), “leveraging optical computing with digital electronics for energy-efficient performance.”  
    URL: https://quantumcomputingreport.com/news/  [archive/tavily_search.jsonl]
  - Mentions **Aramco + Pasqal** deploying “Saudi Arabia’s first quantum computer for industrial applications,” described as a **neutral-atom** system “capable of controlling **200 qubits** in programmable two-dimensional arrays,” installed at **Aramco’s data center** to “accelerate the development of quantum applications across the energy, materials, and industrial sectors.”  
    URL: https://quantumcomputingreport.com/news/  [archive/tavily_search.jsonl]

- **Network World — “Top quantum breakthroughs of 2025” (enterprise/tech journalism framing)**
  - Claims a **SAS survey of 500 global business leaders** found **60%** “actively investing in, or exploring opportunities, in quantum AI.”  
  - Cites a **Bain** estimate: quantum could unlock “up to **$250B** of market value” (pharma/finance/logistics/materials science), while stating the “total market for quantum computing is **less than $1B today**.”  
  - Includes an attribution that **Nvidia CEO Jensen Huang** said quantum is “**15 to 30 years** from being truly useful” (as reported in the article).  
    URL: https://www.networkworld.com/article/4088709/top-quantum-breakthroughs-of-2025.html  [archive/tavily_search.jsonl]

- **Quantum Economic Development Consortium (QED‑C) / SRI International — “Quantum Computing and Artificial Intelligence Use Cases” (report page)**
  - Frames QC and AI as “complement[ing] each other… in multidirectional ways,” including: **AI assisting QC** (circuit design, applications, error correction, generating test data) and **QC assisting AI** by solving “certain types of problems more efficiently, such as **optimization and probabilistic tasks**,” with an emphasis on **hybrid approaches** that “reduce algorithmic complexity” and improve “resource allocation.”  
  - Provides a formal citation line indicating: “SRI International, **March 2025**.”  
    URL: https://quantumconsortium.org/publication/quantum-computing-and-artificial-intelligence-use-cases/  [archive/tavily_search.jsonl]

---

## YouTube source (primary narrative transcript evidence)

- **Caleb Writes Code — “Quantum Computing and AI” (video metadata)**
  - Video title/channel/date/duration and topic framing: “Quantum Computers are approaching a turning point…” with chapters including “LLM Training,” “CPU to GPU to QPU,” “Quantum Computing Industry,” etc.  
    URL: https://www.youtube.com/watch?v=sQSQBYHR0ms  (direct URL in archive: https://www.youtube.com/watch?v=sQSQBYHR0ms&t=374s)  [archive/youtube/videos.jsonl]

- **Transcript — key definitional/claim passages (needs external corroboration if used as factual claims)**
  - Claims about LLM training scale: uses Meta “Llama 3.1 (405B)” and asserts training on “just one GPU” would take “around **4,486 years**,” while “16,000 GPUs” brings it to “**3 months**.” [archive/youtube/transcripts/youtu.be-sQSQBYHR0ms-Quantum_Computing_and_AI.txt]
  - Conceptual explanation: argues LLM training cost is dominated by **matrix multiplication** / FLOPs, gives a figure of “**10^25 flops**” for training, and questions whether quantum can “do all that math simultaneously.” [archive/youtube/transcripts/youtu.be-sQSQBYHR0ms-Quantum_Computing_and_AI.txt]
  - Encoding/friction point: describes a key challenge as mapping classical deterministic bits (“zeros and ones”) into **probabilistic quantum states**; suggests naïvely encoding classical bits deterministically into qubits removes the point of quantum speedups. [archive/youtube/transcripts/youtu.be-sQSQBYHR0ms-Quantum_Computing_and_AI.txt]

---

## arXiv metadata (off-topic / should be excluded from QC+AI use-case evidence)

- **arXiv:2401.01234v1** — survival analysis additive hazard model under censoring (stat.ME), not about quantum/AI use cases.  
  URL: http://arxiv.org/abs/2401.01234v1  [archive/arxiv/papers.jsonl]
- **arXiv:2311.12345v1** — Stable Diffusion for aerial object detection (cs.CV/cs.AI), not about quantum computing.  
  URL: http://arxiv.org/abs/2311.12345v1  [archive/arxiv/papers.jsonl]

---

## Method/limitations notes you can reuse in the report

- Evidence base here is **(a)** Tavily-result snippets (not full-page extractions) and **(b)** one YouTube transcript; **no peer-reviewed full texts** were downloaded; OpenAlex was **disabled**, and arXiv citation lookup **failed**. [archive/_job.json] [archive/_log.txt]