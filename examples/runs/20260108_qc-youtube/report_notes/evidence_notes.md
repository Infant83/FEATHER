## Run provenance / scope (what evidence exists and what’s missing)

- **Run scope & parameters**
  - Run covers **“last 30 days”**, **10 queries**, **max-results=5**, YouTube enabled w/ transcript extraction; **PDF download disabled**. Source: run index + job config.  
    Evidence: [archive/20260108_qc-youtube-index.md], [archive/_job.json]
- **What was actually captured**
  - **YouTube**: **1 video + 1 transcript** (primary long-form text).  
    Evidence: [archive/20260108_qc-youtube-index.md], [archive/youtube/videos.jsonl], [archive/youtube/transcripts/youtu.be-sQSQBYHR0ms-Quantum_Computing_and_AI.txt]
  - **arXiv**: 2 IDs recorded but **no PDFs/texts extracted**.  
    Evidence: [archive/20260108_qc-youtube-index.md]
- **Extraction / lookup limitations**
  - OpenAlex citation lookups for the arXiv IDs failed with HTTP 400 errors.  
    Evidence: [archive/_log.txt]

---

## YouTube (primary narrative source)

- **Video metadata**
  - Title: **“Quantum Computing and AI”**; Channel: **Caleb Writes Code**; Published: **2025-10-19**; Duration: **10m40s**; URL: https://www.youtube.com/watch?v=sQSQBYHR0ms  
    Evidence: [archive/youtube/videos.jsonl], [archive/youtube/transcripts/youtu.be-sQSQBYHR0ms-Quantum_Computing_and_AI.txt]
- **Key claims / explanations in transcript (quotable narrative points)**
  - Frames the common expectation that quantum computers will train AI models “significantly faster,” then asks what would make that true.  
    Evidence: [archive/youtube/transcripts/youtu.be-sQSQBYHR0ms-Quantum_Computing_and_AI.txt]
  - Describes LLM training scaling through classical **parallel computing** (example: many GPUs reduce training time dramatically).  
    Evidence: [archive/youtube/transcripts/youtu.be-sQSQBYHR0ms-Quantum_Computing_and_AI.txt]
  - Identifies **matrix multiplication** and FLOPs as the core computational burden in modern neural networks / LLM training.  
    Evidence: [archive/youtube/transcripts/youtu.be-sQSQBYHR0ms-Quantum_Computing_and_AI.txt]
  - Argues “GPU → QPU” is not seamless because classical data are deterministic bits while qubits are probabilistic superpositions; highlights the **data encoding** problem (classical tokens must be encoded into quantum states).  
    Evidence: [archive/youtube/transcripts/youtu.be-sQSQBYHR0ms-Quantum_Computing_and_AI.txt]
  - Raises the skeptical question: if classical parallelism already works well for training, **where exactly do quantum computers fit** for AI/ML?  
    Evidence: [archive/youtube/transcripts/youtu.be-sQSQBYHR0ms-Quantum_Computing_and_AI.txt]
  - Notes market dynamics/hype: AI is a huge capital magnet and could fund quantum progress; references Jensen Huang remarks in this context (as presented by the speaker).  
    Evidence: [archive/youtube/transcripts/youtu.be-sQSQBYHR0ms-Quantum_Computing_and_AI.txt]

---

## Web sources discovered via Tavily (URLs + salient extracted snippets)

### Consortium / white paper (more “authoritative framing” than blogs/news)
- **QED-C (Quantum Economic Development Consortium)** — *Quantum Computing and Artificial Intelligence Use Cases* (March 2025)  
  - States QC and AI “can complement each other… in many significant and multidirectional ways”; examples include **AI assisting QC** (circuit design, applications, error correction, generating test data) and **QC assisting AI** via efficiency for “optimization and probabilistic tasks,” often in **hybrid approaches**.  
  URL: https://quantumconsortium.org/publication/quantum-computing-and-artificial-intelligence-use-cases/  
  Evidence: [archive/tavily_search.jsonl]

- **Quantum Flagship / qt.eu white paper (PDF)** — *Artificial intelligence and quantum computing white paper*  
  - Discusses hybrid approaches including: quantum data preprocessing feeding classical AI; accelerating training using **NISQ variational algorithms** and future **fault-tolerant** devices; “quantum-enhanced AI” focused on subroutines like **optimization, sampling, high-dimensional data processing**; references near-term device scales (e.g., “100 to 200 physical qubits”) and longer-term “over 50 logical qubits” (as quoted in extracted snippet).  
  URL: https://qt.eu/media/pdf/Artificial_Intelligence_and_Quantum_Computing_white_paper.pdf  
  Evidence: [archive/tavily_search.jsonl]

### Major lab / tooling hub
- **Google Quantum AI — Educational Resources**
  - Points to **TensorFlow Quantum tutorials** and other labs/tutorials; positioned as resources to “learn how to use quantum computing to accelerate machine learning workloads.”  
  URL: https://quantumai.google/resources  
  Evidence: [archive/tavily_search.jsonl]

### Industry/news roundups (useful but treat as secondary / claims-by-announcement)
- **Network World** — *Top quantum breakthroughs of 2025*  
  - Mentions enterprise interest in “quantum and AI”; cites a **SAS survey** statistic (“60% … investing in, or exploring opportunities, in quantum AI”) and mentions market-sizing language attributed to Bain; also references public discourse contrasting AI hype vs quantum timelines (including Jensen Huang’s “15 to 30 years” remark, per the article excerpt).  
  URL: https://www.networkworld.com/article/4088709/top-quantum-breakthroughs-of-2025.html  
  Evidence: [archive/tavily_search.jsonl]

- **Quantum Computing Report — News page**
  - Contains industry announcements, e.g., photonics-based reservoir computing “Neurawave” and a Pasqal/Aramco deployment claim (neutral-atom system “capable of controlling 200 qubits… for industrial applications”), per extracted snippet.  
  URL: https://quantumcomputingreport.com/news/  
  Evidence: [archive/tavily_search.jsonl]

### General overviews / lower-authority sources (use cautiously)
- **MDPI paper (overview)** — *Quantum Machine Learning—An Overview*  
  - Overview framing and comparison of classical SVM vs quantum SVM; discusses challenges/limitations; useful as background but still a secondary overview.  
  URL: https://www.mdpi.com/2079-9292/12/11/2379  
  Evidence: [archive/tavily_search.jsonl]

- Additional results in the run include vendor blogs / developer posts (SpinQ, dev.to, etc.) that describe QML benefits and applications; these are generally **promotional or non-peer-reviewed** and should be treated as illustrative rather than authoritative.  
  Evidence: [archive/tavily_search.jsonl]

---

## arXiv metadata (audit: appears off-topic vs QC+AI focus)

- **arXiv:2401.01234v1** — “Mixture cure semiparametric additive hazard models…” (survival analysis; stat.ME)  
  URL: http://arxiv.org/abs/2401.01234v1 (PDF: https://arxiv.org/pdf/2401.01234v1)  
  Evidence: [archive/arxiv/papers.jsonl]
- **arXiv:2311.12345v1** — “Stable Diffusion For Aerial Object Detection” (computer vision; not quantum computing)  
  URL: http://arxiv.org/abs/2311.12345v1 (PDF: https://arxiv.org/pdf/2311.12345v1)  
  Evidence: [archive/arxiv/papers.jsonl]

These arXiv entries don’t support “quantum computing + AI” directly and—per the run—no full texts were downloaded anyway.