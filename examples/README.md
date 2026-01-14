Example inputs you can run quickly.

```bash
python -m pip install -e .
feather --input ./examples/instructions --output ./examples/runs

# Or use module form:
python -m feather --input ./examples/instructions --output ./examples/runs

# Or without installing:
python run.py --input ./examples/instructions --output ./examples/runs

# Run all curated examples:
python examples/test_run.py --output ./examples/runs
```

## Running test_run.py
```bash
python examples/test_run.py --output ./examples/runs
python examples/test_run.py --only oled-basic --only iccv25 --output ./examples/runs
python examples/test_run.py --skip-download-pdf --output ./examples/runs
python examples/test_run.py --no-openalex --output ./examples/runs
python examples/test_run.py --no-youtube --output ./examples/runs
python examples/test_run.py --dry-run
```

Notes:
- Run folder names default to the instruction file stem (e.g., `20260104_oled.txt` -> `examples/runs/20260104_oled`). If it already exists, `_01` is appended.

## Example cases

### 1) Simple keyword queries (no PDFs)
Uses `examples/instructions/20260104_oled.txt`.

```bash
feather --input ./examples/instructions/20260104_oled.txt --output ./examples/runs
```

### 1b) Open-access papers via OpenAlex (PDF download)
Uses the same file and adds OA search across journals (including open access in Nature when available).

```bash
feather --input ./examples/instructions/20260104_oled.txt --output ./examples/runs --download-pdf
```

Note:
- If you already ran Example 1, the output folder will be `examples/runs/20260104_oled_01` (or higher).

Outputs of interest for LLM inputs:
- `examples/runs/<queryID>/archive/openalex/works.jsonl` (open-access metadata)
- `examples/runs/<queryID>/archive/openalex/pdf/*.pdf` (PDFs, when available)
- `examples/runs/<queryID>/archive/openalex/text/*.txt` (PDF text, when `pymupdf` is available)
- `examples/runs/<queryID>/archive/<queryID>-index.md` (relative paths to all outputs)

### 1c) ICCV 2025 + GitHub code (OpenAlex + Tavily)
Uses `examples/instructions/20251015_iccv25.txt`. Consider expanding the date range to capture the conference window.

```bash
feather --input ./examples/instructions/20251015_iccv25.txt --output ./examples/runs --download-pdf --days 180
```

Notes:
- `github` as a hint will bias code-related queries toward `site:github.com`.
- OpenAlex only returns open-access works; some ICCV papers may not have OA PDFs.

### 2) arXiv metadata + PDF/text extraction
Uses `examples/instructions/20260105_arxiv-gnn.txt`. Requires optional deps.

```bash
python -m pip install -e ".[all]"
feather --input ./examples/instructions/20260105_arxiv-gnn.txt --output ./examples/runs --download-pdf
```

Outputs of interest for LLM inputs:
- `examples/runs/<queryID>/archive/arxiv/papers.jsonl` (metadata)
- `examples/runs/<queryID>/archive/arxiv/text/*.txt` (PDF text, when `--download-pdf`)
- `examples/runs/<queryID>/archive/<queryID>-index.md` (relative paths to all outputs)

### 3) Mixed queries + URLs + arXiv IDs
Uses `examples/instructions/20260106_mixed.txt`.

```bash
feather --input ./examples/instructions/20260106_mixed.txt --output ./examples/runs --max-results 5
```

Outputs of interest for LLM inputs:
- `examples/runs/<queryID>/archive/tavily_search.jsonl` (includes per-result `summary` and `query_summary`)
- `examples/runs/<queryID>/archive/tavily_extract/*.txt`
- `examples/runs/<queryID>/archive/<queryID>-index.md` (relative paths to all outputs)

### 4) AI trends + CES 2026 + conferences (multi-source)
Uses `examples/instructions/20260107_ai-trends.txt`. This is a heavier run; consider lowering result caps.

```bash
feather --input ./examples/instructions/20260107_ai-trends.txt --output ./examples/runs --days 30 --max-results 5 --oa-max-results 2 --download-pdf --lang en
```

### 5) Quantum computing + AI + industry + YouTube (with journals)
Uses `examples/instructions/20260108_qc-youtube.txt`. This includes queries that work well for YouTube, plus arXiv IDs and major journal searches.

```bash
feather --input ./examples/instructions/20260108_qc-youtube.txt --output ./examples/runs --youtube --yt-transcript --yt-order date --max-results 5 --yt-max-results 5
```

Notes:
- Requires `YOUTUBE_API_KEY` in your environment.
- `--yt-transcript` needs `youtube-transcript-api`. Omit it if you only want metadata.

### 6) Sectioned instructions with per-section hints
Uses `examples/instructions/20260109_sectioned.txt`. Each section has its own hints (e.g., `linkedin`, `news`, `youtube`, `github`).

```bash
feather --input ./examples/instructions/20260109_sectioned.txt --output ./examples/runs --max-results 5 --youtube
```

Notes:
- Hints only apply within the section they appear in.
- Repeat hint lines across sections if you want them to apply broadly.

### 6b) Federlicht in-depth report (multi-step)
Runs a scout + evidence + writer pipeline and optionally saves notes.

```bash
python -m pip install -e ".[agents]"
feather --input ./examples/instructions/20260104_oled.txt --output ./examples/runs --download-pdf
federlicht --run ./examples/runs/20260104_oled --output ./examples/runs/20260104_oled/report_full.md --notes-dir ./examples/runs/20260104_oled/report_notes --lang ko --prompt-file ./examples/instructions/20260104_prompt_oled.txt --quality-iterations 5
federlicht --run ./examples/runs/20260104_oled --output ./examples/runs/20260104_oled/report_full.html --lang ko --prompt-file ./examples/instructions/20260104_prompt_oled.txt --quality-iterations 5
federlicht --run ./examples/runs/20260104_oled --output ./examples/runs/20260104_oled/report_full.html --lang ko --prompt-file ./examples/instructions/20260104_prompt_oled.txt --quality-iterations 2 --web-search

Notes:
- The no-install wrapper is `python scripts/federlicht_report.py ...`.
- `--web-search` will create `./examples/runs/20260104_oled/supporting/<timestamp>` and store `web_search.jsonl`, `web_fetch.jsonl`, and extracted texts.
- Requires `TAVILY_API_KEY` in the environment.
- Reports now include a `Critics` section and numbered citations with a `References` list.
- You can set the report byline with `--author "Name / Team"` or add `Author: Name / Team` inside the prompt file.

### 7) Quantum computing for materials + OLED emitters (industry + academia)
Uses `examples/instructions/20260110_qc-oled.txt` and a report prompt at `examples/instructions/20260110_prompt_qc-oled.txt`.

```bash
feather --input ./examples/instructions/20260110_qc-oled.txt --output ./examples/runs --download-pdf --days 365 --max-results 5 --oa-max-results 5 --lang en
federlicht --run ./examples/runs/20260110_qc-oled --output ./examples/runs/20260110_qc-oled/report_full.html --lang ko --prompt-file ./examples/instructions/20260110_prompt_qc-oled.txt --quality-iterations 2 --web-search
```

Notes:
- Requires `TAVILY_API_KEY` for web search support.

### 8) LinkedIn-style practitioner review
Uses `examples/instructions/20260113_linkedin-review.txt` and the `linkedin_review` template.

```bash
feather --input ./examples/instructions/20260113_linkedin-review.txt --output ./examples/runs --download-pdf
federlicht --run ./examples/runs/20260113_linkedin-review --output ./examples/runs/20260113_linkedin-review/report_full.html --template linkedin_review --lang en --prompt-file ./examples/instructions/20260113_prompt_linkedin-review.txt --figures --figures-mode select
```

Notes:
- First run creates `report_views/figures_preview.html` and `report_notes/figures_selected.txt`.
- Add candidate IDs to `figures_selected.txt`, then rerun Federlicht to insert figures.

### 7b) QC-OLED report in LaTeX (compile to PDF)
```bash
federlicht --run ./examples/runs/20260110_qc-oled --output ./examples/runs/20260110_qc-oled/report_full.tex --template review_of_modern_physics --lang ko --prompt-file ./examples/instructions/20260110_prompt_qc-oled.txt
```

Notes:
- If `latexmk` or `pdflatex` is installed, the PDF is compiled automatically.

## Federlicht template suggestions per example
Use the actual run folder (e.g., `20260104_oled`, `20260104_oled_01`, ...). Add `--figures --figures-renderer pdfium --figures-dpi 200` to embed cropped figures.

- `20260104_oled` (simple keywords): `executive_brief`
  ```bash
  federlicht --run ./examples/runs/20260104_oled --output ./examples/runs/20260104_oled/report_full.html --template executive_brief --lang ko --prompt-file ./examples/instructions/20260104_prompt_oled.txt
  ```
- `20260104_oled` (open-access PDFs): `nature_reviews`
  ```bash
  federlicht --run ./examples/runs/20260104_oled --output ./examples/runs/20260104_oled/report_full.html --template nature_reviews --lang ko --prompt-file ./examples/instructions/20260104_prompt_oled.txt
  ```
- `20251015_iccv25` (ICCV + GitHub): `technical_deep_dive`
  ```bash
  federlicht --run ./examples/runs/20251015_iccv25 --output ./examples/runs/20251015_iccv25/report_full.html --template technical_deep_dive --lang en --prompt "Summarize key papers, code links, and research gaps. Emphasize practical impact."
  ```
- `20260105_arxiv-gnn` (arXiv GNN): `technical_deep_dive`
  ```bash
  federlicht --run ./examples/runs/20260105_arxiv-gnn --output ./examples/runs/20260105_arxiv-gnn/report_full.html --template technical_deep_dive --lang en --prompt "Analyze main ideas, methods, and implications. Highlight trends and open problems."
  ```
- `20260106_mixed` (mixed sources): `trend_scan`
  ```bash
  federlicht --run ./examples/runs/20260106_mixed --output ./examples/runs/20260106_mixed/report_full.html --template trend_scan --lang en --prompt "Identify cross-source trends and notable signals; cite sources."
  ```
- `20260107_ai-trends` (AI trends): `mit_tech_review_10_breakthroughs`
  ```bash
  federlicht --run ./examples/runs/20260107_ai-trends --output ./examples/runs/20260107_ai-trends/report_full.html --template mit_tech_review_10_breakthroughs --lang en --prompt "Synthesize top breakthroughs and implications. Keep sections short and sharp."
  ```
- `20260108_qc-youtube` (quantum + YouTube): `quanta_magazine`
  ```bash
  federlicht --run ./examples/runs/20260108_qc-youtube --output ./examples/runs/20260108_qc-youtube/report_full.html --template quanta_magazine --lang en --prompt "Write a narrative review with clear explanations and source citations."
  ```
- `20260109_sectioned` (sectioned instructions): `default`
  ```bash
  federlicht --run ./examples/runs/20260109_sectioned --output ./examples/runs/20260109_sectioned/report_full.html --template default --lang en --prompt "Respect section structure and summarize each section with citations."
  ```
- `20260110_qc-oled` (deep research review): `review_of_modern_physics`
  ```bash
  federlicht --run ./examples/runs/20260110_qc-oled --output ./examples/runs/20260110_qc-oled/report_full.html --template review_of_modern_physics --lang ko --prompt-file ./examples/instructions/20260110_prompt_qc-oled.txt
  ```
- `20260112_ms-ai-diffusion` (industry report): `annual_review`
  ```bash
  federlicht --run ./examples/runs/20260112_ms-ai-diffusion --output ./examples/runs/20260112_ms-ai-diffusion/report_full.html --template annual_review --lang ko --prompt-file ./examples/instructions/20260112_prompt_ms-ai-diffusion2025.txt
  ```
  ```bash
  federlicht --run ./examples/runs/20260112_ms-ai-diffusion --output ./examples/runs/20260112_ms-ai-diffusion/report_full.tex --template annual_review --lang ko --prompt-file ./examples/instructions/20260112_prompt_ms-ai-diffusion2025.txt
  ```
- `20260113_linkedin-review` (LinkedIn practitioner review): `linkedin_review`
  ```bash
  federlicht --run ./examples/runs/20260113_linkedin-review --output ./examples/runs/20260113_linkedin-review/report_full.html --template linkedin_review --lang en --figures --figures-mode select
  ```
```
