# Federlicht Platform

Author: Hyun-Jung Kim (angpangmokjang@gmail.com, Infant@kias.re.kr)

Version: 1.9.20

## Core Idea
Federlicht is an agentic research and reporting platform designed around one principle:
collect evidence carefully, then illuminate decisions clearly.

In short: individual evidence fragments are lightweight, but when curated and composed with
the right structure, they become actionable insight.

## Platform Overview
- `Feather`: source intake and archival (web, arXiv, local docs).
- `Federlicht`: multi-stage report generation and quality pipeline.
- `Federnett`: operational studio (UI) to run, inspect, and iterate workflows.
- `FederHav`: operator chat + profile-guided revision flow for persona-aware report refinement.

Federlicht focuses on process-first report operations: gather evidence in Feather, preserve context/artifacts in run archives, and assemble explainable outputs in Federlicht. FederHav is designed as an operator-side guide that helps clarify questions, organize arguments, and refine tone/structure, rather than acting as a rigid one-shot answer gate.

Federlicht is the base platform package name. It includes four operational components:
- `feather`: external evidence intake and source archival (RAG collector).
- `federlicht`: report generation pipeline (agentic synthesis, quality loop, rendering).
- `federnett`: web studio for workflow control and artifact inspection.
- `federhav`: operator chat and profile-guided update/revision workflow for report refinement.

Feather-light knowledge intake is one component of this package. The collector ingests text instructions (`.txt` files), runs Tavily search/extract, fetches arXiv papers, and builds an offline-friendly archive of everything it collected. Input can be a single `.txt` file or a folder of `.txt` files.

Feather and Federlicht are designed as a deliberate two-step flow. Feather is about gathering: knowledge floats in the air like feathers, and only the right collection can form a meaningful whole. It also plays on “feeder” — the collected knowledge is fed into language models, so the intake must be curated through well‑designed queries in the instruction file. Federlicht is about illumination and curation: “feder + licht” (feather + light) — a German word pairing. The separation is intentional: collection and synthesis need different knobs. The way you combine input arguments (sources, limits, language, templates, prompts) shapes not just coverage but the narrative voice and report style, so tuning both steps together is essential for high-quality output. That tuning is done by the user — typically domain experts — and even in the GenAI/agentic era, the decision maker and director remain essential for choosing what matters, what to trust, and how to frame the story. 
“Knowledge is light; ignorance is darkness.”

## Package Identity
- Distribution/package name: `federlicht`
- Repository name: `FEATHER`
- Primary CLI commands shipped by this package:
  - `feather` (collector)
  - `federlicht` (report engine)
  - `federnett` (studio UI)
  - `federhav` (interactive operator chat + revision runner)

## Features
- Parse natural-language instructions from `.txt` files.
- Tavily search and content extraction (requires `TAVILY_API_KEY`).
- Optional arXiv metadata fetch; optional PDF download and text extraction.
- Optional arXiv source download (TeX + figure manifests).
- Optional YouTube search and transcript capture.
- Writes a reproducible archive per instruction file with logs and an `index.md` summary.
- List and review existing run folders.
- Federlicht report synthesis: multi-step agentic review with templates, citations, and HTML/TeX output.

## Requirements
- Python 3.10+ recommended (3.12 verified).
- Required package: `requests` (declared in `pyproject.toml`).
- Optional packages (extra features, declared as extras):
  - `arxiv` for arXiv metadata/search.
  - `pymupdf` (imported as `fitz`) for PDF-to-text extraction.
  - `youtube-transcript-api` for YouTube transcript capture.
  - `python-docx` / `python-pptx` / `beautifulsoup4` for local file ingestion (docx/pptx/html).
- Optional packages: `deepagents` for report scripts and `markdown` for HTML output (LLM API key required).
- Optional packages: `langchain-openai` for OpenAI-compatible endpoints (e.g., local Qwen hosting).
- Environment: `TAVILY_API_KEY` must be set for search/extract steps.
- Environment: `YOUTUBE_API_KEY` must be set for YouTube search.
- Optional env: `YOUTUBE_PROXY` or `YOUTUBE_PROXY_HTTP` / `YOUTUBE_PROXY_HTTPS` for transcript access when YouTube blocks direct requests.
- Optional env: `OPENALEX_API_KEY` (used if set) and `OPENALEX_MAILTO` (polite contact string).
- Optional env: `FEATHER_USER_AGENT` to set a polite `User-Agent` for PDF downloads and OpenAlex requests.
- Optional env: `OPENAI_BASE_URL` / `OPENAI_API_BASE` for OpenAI-compatible endpoints (used when `--model` is not an OpenAI model like `gpt-*`/`o*`).
- Optional env: `OPENAI_BASE_URL_VISION` / `OPENAI_API_KEY_VISION` for vision-only models (used with `--model-vision`).
- `requirements.txt` is a convenience bundle for local runs/tests and includes optional deps + pytest.

### License and Dependency Notice
- This repository is licensed under MIT (`LICENSE`).
- Some optional extras may install dependencies under different licenses.
- In particular, `pymupdf` is distributed under AGPL/commercial terms, so using extras that include it (`pdf`, `report`, `all`) requires your own compliance review.
- If your organization requires permissive-only dependencies, use `report-lite` and avoid extras that include `pymupdf`.

## Installation
```bash
# PyPI install (distribution name):
python -m pip install federlicht

# Recommended: install the package (editable during development)
python -m pip install -e .
# For a regular install, use: python -m pip install .

# With optional features (arXiv + PDF text):
python -m pip install -e ".[all]"
python -m pip install "federlicht[all]"

# Federlicht report stack without pymupdf (permissive-leaning default):
python -m pip install -e ".[report-lite]"
python -m pip install "federlicht[report-lite]"

# Local file ingestion only:
python -m pip install -e ".[local]"

# Only YouTube transcripts:
python -m pip install -e ".[youtube]"

# Deepagents report script:
python -m pip install -e ".[agents]"
python -m pip install -e ".[report]"
python -m pip install "federlicht[report]"

# Dependency-only install for run.py / local scripts:
python -m pip install -r requirements.txt
```

### Diagram Tooling (Mermaid / D2 / diagrams)
- Mermaid artifact rendering uses Mermaid CLI (`mmdc`):
  - `npm i -g @mermaid-js/mermaid-cli`
- D2 artifact rendering uses D2 CLI:
  - install: `winget install -e --id Terrastruct.D2`
  - if PATH is not refreshed, set `D2_BIN` to full executable path (e.g., `C:\Program Files\D2\d2.exe`).
- Python `diagrams` rendering requires:
  - python deps: `python -m pip install diagrams graphviz`
  - Graphviz CLI (`dot`): `winget install -e --id Graphviz.Graphviz`
  - if PATH is not refreshed, set `GRAPHVIZ_DOT` to full path (e.g., `C:\Program Files\Graphviz\bin\dot.exe`).

## Usage
```bash
feather --input ./instructions --output ./archive --download-pdf --max-results 8

# Inline query mode (separate items with ';' or newlines):
feather --query "what is quantum computer; recent 30 days; arXiv:2401.01234; https://aaa.blog" --output ./runs --lang en

# Open-access papers via OpenAlex (optional):
feather --input ./instructions --output ./archive --openalex --download-pdf

# YouTube search with transcripts:
feather --input ./instructions --output ./archive --youtube --yt-transcript

# Agentic iterative expansion (LLM-guided):
feather --input ./instructions --output ./archive --agentic-search --model gpt-4o-mini --max-iter 3

# List or review existing runs:
feather --list ./runs
feather --review ./runs/20260104
feather --review ./runs/20260104 --review-full
feather --list ./runs --filter ai
feather --review ./runs/20260104 --format json
feather --review ./runs/20260104/archive/tavily_search.jsonl

# Or:
python -m feather --input ./instructions --output ./archive --download-pdf --max-results 8

# Or without installing (local runner):
python run.py --input ./instructions --output ./archive --download-pdf --max-results 8

# Federlicht report generation (requires deepagents + LLM key):
federlicht --run ./examples/runs/20260104_oled --output ./examples/runs/20260104_oled/report_full.md --lang ko --prompt-file ./examples/instructions/20260104_prompt_oled.txt
# HTML output:
federlicht --run ./examples/runs/20260104_oled --output ./examples/runs/20260104_oled/report_full.html --lang ko --prompt-file ./examples/instructions/20260104_prompt_oled.txt
# Structure/creativity controls:
federlicht --run ./examples/runs/20260104_oled --output ./examples/runs/20260104_oled/report_full.html --template-rigidity balanced --temperature-level balanced
# See docs/federlicht_report.md for detailed options.

# Windows wrappers (no install):
# .\feather.ps1 --input .\instructions --output .\archive --max-results 8
# .\feather.cmd --input .\instructions --output .\archive --max-results 8
```

### Federnett (Web UI)
Federnett is a lightweight HTML5 interface that wraps the existing Feather and
Federlicht CLIs via subprocess. It does not replace core behavior.

Key points:
- It serves the static UI from `./site/federnett/`.
- All paths are resolved under `--root` (guardrail against path escape).
- It scans run folders from `--run-roots` (default: `runs,site/runs`).
- Default policy is `runs/*` for working run artifacts and `site/report_hub/*` for publishable hub pages (legacy `site/runs/*` is still compatible).
- Logs stream live via SSE and jobs can be stopped from the UI.
- Live Logs ask context uses `state-memory` + optional recent-execution-log auxiliary summary (for example `1.2k` chars).
  - `state-memory`: run/workflow/artifact/dialogue 상태 요약 메모리
  - `recent-log tail summary`: 직전 실행 로그 끝부분 보조 컨텍스트 요약 (길이 선택값 기준)
- FederHav action policy defaults to agentic runtime (`auto/deepagent`) and does not use safe-rule fallback unless explicitly enabled with `FEDERNETT_HELP_RULE_FALLBACK=1`.
- FederHav deepagent runtime uses run-scoped tools (`memory_snapshot`, `run_artifacts`, `read_run_file`, `source_digest`) and action preflight tool (`execution_preflight`) to ground answers/actions in current run artifacts.
- FederHav action proposal path now runs deepagent planner-first with structured handoff metadata (`confidence`, `intent_rationale`, `execution_handoff.preflight`) and keeps legacy LLM planner as migration fallback.
- Ask trace includes structured `action_plan` step details so planner intent/confidence/preflight can be audited in logs.
- Path/file questions are handled with run-context source selection + tool grounding (not per-phrase hardcoded reply templates).
- Run-internal file/folder summary requests are treated as content-analysis tasks by default (no automatic Feather/Federlicht run action suggestion unless explicit execution intent exists).
- If `run` is omitted in help payload, FederHav recovers run context from `state_memory.scope.run_rel`/`state_memory.run.run_rel` to keep run-scoped analysis stable.
- Forward roadmap for account/profile/hub collaboration: `docs/federnett_roadmap.md`.
- Account/권한 운영(root/admin/user/bootstrap/revoke) 가이드: `docs/federnett_auth_operations.md`.
- Playwright MCP troubleshooting and fallback validation path: `docs/playwright_mcp_troubleshooting.md`.

Optional auth env:
- `FEDERNETT_ROOT_PASSWORD`: enables root unlock for built-in profile editing.
- `FEDERNETT_AUTH_ACCOUNTS_JSON`: enables session login API (JSON list/map of username/password/role/display_name).
  - Example: `[{"username":"root","password":"change-me","role":"root","display_name":"Root Admin"}]`
  - Session `role` in `root/admin/owner/superuser` grants built-in profile edit permission even when root token unlock is not active.

```bash
# Start the UI server (defaults to ./site/federnett):
federnett --root . --port 8765

# Share on the local network:
federnett --root . --host 0.0.0.0 --port 8765

# Module entrypoint (equivalent):
python -m federnett.app --root . --port 8765

# Customize run discovery roots:
federnett --root . --run-roots runs,site/runs,data/runs

# Serve from a different static directory:
federnett --root . --static-dir site/federnett --site-root site
```

Then open `http://127.0.0.1:8765/`.

### FederHav (CLI Chat + Update Runner)
`federhav` now has two modes:
- `chat`: interactive operator dialog backed by the same `federnett.help_agent` core used in Live Logs.
- `update`: legacy profile-guided report revision runner.

```bash
# One-shot question
federhav --question "현재 run 폴더 구조를 요약해줘"

# Interactive chat
federhav chat --root . --run runs/my_run --profile-id default

# Legacy revision runner
federhav update \
  --run runs/my_run \
  --base-report report_full.html \
  --update "요약 섹션을 더 간결하게 수정해줘" \
  --agent-profile federhav
```

Interactive commands:
- `/run <path>`: switch run context
- `/profile <id>`: switch history/profile scope
- `/agent <id>`: set operator agent label (or `/agent default` to clear override)
- `/plan [질문]`: switch to plan-confirm mode (optionally send question immediately)
- `/act [질문]`: switch to act mode (optionally send question immediately)
- `/clear`: clear run/profile-scoped chat history
- `/exit`: leave chat

### Report Hub API Skeleton (Federnett)
Federnett now exposes report-hub conversation/link primitives for post-id based loading and run linkage:
- `GET /api/report-hub/posts?q=&run=&limit=&offset=`
- `GET /api/report-hub/posts/{post_id}`
- `GET /api/report-hub/posts/{post_id}/comments?limit=`
- `GET /api/report-hub/posts/{post_id}/followups?limit=`
- `GET /api/report-hub/posts/{post_id}/link`
- `POST /api/report-hub/comments` (`post_id`, `text`, optional `author/run_rel/profile_id/metadata`)
- `POST /api/report-hub/followups` (`post_id`, `prompt`, optional `status/author/run_rel/profile_id/metadata`)
- `POST /api/report-hub/link` (`post_id`, `run_rel`, optional `linked_by/metadata`)

Session auth endpoints:
- `GET /api/auth/session/status`
- `POST /api/auth/session/login` (`username`, `password`)
- `POST /api/auth/session/logout` (`session_token` or `X-Federnett-Session-Token`)

When report-hub writes are made with an authenticated session token, Federnett auto-stamps `metadata.signed_by` and `metadata.signed_role`.

### Agent Profile Author Metadata
Agent profiles can carry report byline metadata:
- `author_name`: author label to show in the report header.
- `organization` (optional): appended as `author_name / organization`.

Author resolution order in Federlicht:
1) `--author` (and optional `--organization`)  
2) selected agent profile `author_name`/`organization`  
3) `Author:` line in report prompt  
4) fallback `Federlicht Writer`

Notes:
- Built-in profiles stay read-only.
- Site profile IDs are auto-assigned as random 6-digit numbers for new profiles.
- `author_name` / `organization` are metadata only and do not grant any memory/DB permissions.

### Auth-Gated Memory/DB (TODO)
- Add certificate/SSO-based access control for profile-bound memory connectors.
- Add API-key token option for controlled vector DB or knowledge-base access.
- Enforce explicit permission policies (who can query which memory source, and when).
- Keep report generation presets separate from identity/permission profiles for reproducibility.

### Python API (Federlicht)
```python
from federlicht import create_reporter

reporter = create_reporter(
    run="./examples/runs/20260110_qc-oled",
    output="./examples/runs/20260110_qc-oled/report_full.html",
    template="review_of_modern_physics",
    lang="ko",
    prompt_file="./examples/instructions/20260110_prompt_qc-oled.txt",
    no_figures=True,
)

# Full run (ReportOutput)
result = reporter.run()
print(result.output_path)

# Partial run -> state -> finish
state = reporter.run(stages="scout,plan,evidence")
final = reporter.write(state, output="./examples/runs/20260110_qc-oled/report_full.html")
print(final.output_path)

# Stage registry
print(reporter.stage_info())                # all stages
print(reporter.stage_info(["scout", "web"]))  # subset
```

### Federlicht context/tool limits
Federlicht uses multiple guardrails to prevent context overflows and preserve evidence quality:
- `--max-chars` / `--max-pdf-pages`: per-read limits for `read_document` (single file load).
- `--max-tool-chars`: cumulative cap for all `read_document` outputs in a run; overflow triggers reducer summaries.
- Reducer summaries store original chunks under `report_notes/tool_cache/` and mark `NEEDS_VERIFICATION` items.
- For PDF follow-ups, `read_document` supports `start_page` to read later pages without raising global limits.

### Figures (PDF extraction & selection)
Federlicht can extract figures from referenced PDFs and insert them into the report. Candidates are derived from
PDFs cited in the report body (e.g., `./archive/.../pdf/...`); it does **not** scan the entire archive.

Default behavior (`--figures-mode auto`) inserts all candidates. For manual curation, switch to `select` mode:
1) Run once to generate candidates and the preview (`report_views/figures_preview.html`).
2) Add selected IDs to `report_notes/figures_selected.txt` and rerun.

You can also add a custom caption by appending `|`:
```
fig-001 | Overview of the model architecture
fig-002 | Dataset distribution summary
```

Preview-only (no report regeneration):
```bash
federlicht --run ./examples/runs/20260104_oled \
  --output ./examples/runs/20260104_oled/report_full.html \
  --figures-preview
```

See `docs/federlicht_report.md` for full figure options and dependencies.

## Hosting the Report Hub (GitHub/GitLab Pages)
Federlicht uses separated roots by default:
- working runs: `./runs/*` (legacy fallback: `./site/runs/*`)
- publish hub: `./site/report_hub/*`

Recommended publish flow:

1) Generate a report under `runs/`:
```bash
federlicht --run ./runs/20260110_qc-oled \
  --output ./runs/20260110_qc-oled/report_full.html \
  --template review_of_modern_physics --lang ko \
  --prompt-file ./examples/instructions/20260110_prompt_qc-oled.txt
```

2) Publish approved output into hub snapshot storage:
```bash
python -m federlicht.hub_publish \
  --report ./runs/20260110_qc-oled/report_full.html \
  --run ./runs/20260110_qc-oled \
  --hub ./site/report_hub
```

3) (Optional) Rebuild hub by scanning run roots:
```bash
federlicht --site-refresh ./site/report_hub
```

4) Commit/push `site/report_hub/*` for static deployment.

### GitLab Pages (internal)
- This repo now includes a baseline `.gitlab-ci.yml` with:
  - `pytest_smoke` test job
  - `pages` deploy job (`site/report_hub -> public/report_hub`)
- Enable Pages in GitLab project settings and deploy from `main`.

### GitHub Pages (enterprise)
Option A: set Pages source to the `site/` folder.  
Option B: copy `site/` to `docs/` and set Pages source to `/docs`.

Notes:
- Default separation is `runs` (artifacts) + `site/report_hub` (published index), with `site/runs` kept as legacy-compatible fallback.
- For on-prem publishing, keep run artifacts internal and expose only `site/report_hub`.
- The hub footer includes an AI transparency and source-rights notice for publication/distribution contexts.
- Detailed policy: `docs/run_site_publish_strategy.md`.

## Workflow (Feather -> Federlicht)
Use Feather to collect sources, then Federlicht to synthesize a report.

1) Prepare an instruction file (and optionally a report prompt file).
```bash
# Example inputs
./instructions/20260110_qc-oled.txt
./instructions/20260110_prompt_qc-oled.txt
```

2) Run Feather to create a run folder under `--output`.
```bash
feather --input ./instructions/20260110_qc-oled.txt --output ./runs --download-pdf
```

3) Inspect the run (optional).
```bash
feather --review ./runs/20260110_qc-oled
```

4) Generate the report with Federlicht.
```bash
federlicht --run ./runs/20260110_qc-oled --output ./runs/20260110_qc-oled/report_full.html --lang ko --prompt-file ./instructions/20260110_prompt_qc-oled.txt
```

Notes:
- Feather only collects data; Federlicht never re-fetches sources.
- The run folder contains `instruction/`, `archive/`, and `*-index.md` used by Federlicht.
- See `examples/README.md` and `docs/federlicht_report.md` for advanced templates and report options.

Arguments:
- `--input` (required): Folder containing one or more `.txt` instruction files, or a single `.txt` file.
- `--query` (required if `--input` is not set): Inline instructions separated by `;` or newlines.
- `--list`: List run folders under a path (default: current directory).
- `--filter`: Filter list entries by queryID substring (case-insensitive). Use with `--list`.
- `--review`: Show outputs for a single run folder or its `archive` path.
- `--review <file.jsonl>`: Show a compact summary of a JSONL file (e.g., `tavily_search.jsonl`).
- `--review-full`: Show full outputs when reviewing a run or JSONL file.
- `--format`: Output format for `--review` (`text` or `json`).
- `--output` (required): Archive root; each run creates `output/<queryID>/`.
- `--update-run`: Reuse an existing run folder and update outputs in place (skip existing files/entries).
- `--days` (default 30): Lookback window for the "recent" arXiv search heuristic.
- `--max-results` (default 8): Max Tavily/arXiv results per query.
- `--agentic-search`: Enable iterative LLM-guided source expansion on top of the standard Feather run.
- `--model`: Model for `--agentic-search` (OpenAI-compatible; falls back to `OPENAI_MODEL` when omitted).
- `--max-iter` (default 3): Max planning iterations in `--agentic-search` mode.
- `--download-pdf`: If set, arXiv PDFs are downloaded and converted to text.
- `--arxiv-src`: Download arXiv source tarballs (TeX + figures) and create source manifests.
- `--no-citations`: Disable citation enrichment for papers (OpenAlex is used by default when available).
- `--lang`: Preferred language for search results (`en`/`eng` or `ko`/`kor`). This is a soft preference only.
- `--no-stdout-log`: Disable console logging (write to `_log.txt` only).
- `--openalex` / `--oa`: Also search OpenAlex for open-access papers (optional; default on when `--download-pdf` is set).
- `--no-openalex`: Disable OpenAlex search (overrides the default when `--download-pdf` is set).
- `--oa-max-results`: Max OpenAlex results per query (defaults to `--max-results`).
- `--youtube`: Enable YouTube search.
- `--no-youtube`: Disable YouTube search.
- `--yt-max-results`: Max YouTube results per query (defaults to `--max-results`).
- `--yt-order`: YouTube search ordering (`relevance`, `date`, `viewCount`, `rating`).
- `--yt-transcript`: Fetch YouTube transcripts (requires `youtube-transcript-api`).

QueryID rules:
- Default: `safe_filename(file_stem)` (or `safe_filename(first_query_line)` for `--query`).
- If the output folder already exists: suffix `_01`, `_02`, ...
- With `--update-run`: reuse the existing folder (no suffix) and merge new outputs in place.
- To control run folder names, rename the instruction file (e.g., `ai_trends.txt`).

## Instruction File Format
- File name can be anything as long as it ends with `.txt`. If the stem starts with `YYYYMMDD`, that date is used for the run; otherwise today's date is used.
- Lines are grouped into sections; blank lines or separator-only lines (`-_=*#`) split sections.
- Site hints apply only to queries in the same section; repeat hints across sections if needed.
- Multiple hint lines in a section are combined.
- Lines detected as URLs are treated as direct extract targets.
- arXiv abstract URLs (`https://arxiv.org/abs/...`) are also treated as arXiv IDs when `--download-pdf` or `--arxiv-src` is enabled.
- Local file directives are supported:
  - `file: <path>` for a single file
  - `dir: <path>` for a directory (recursive)
  - `glob: <pattern>` for explicit file patterns
  - Optional metadata: `| title="..." | tags=a,b | lang=en`
- Supported local file types: `pdf`, `docx`, `pptx`, `txt`, `md`, `html`, `htm`.
- YouTube URLs (watch/shorts/embed) are handled by the YouTube collector when `--youtube` is enabled.
- YouTube search only runs if a `youtube` hint is present or the query includes `site:youtube.com`/`youtu.be`.
- LinkedIn post URLs are extracted via LinkedIn's public embed page (no comments; includes post text and image URLs).
- Lines containing an arXiv ID (e.g., `arXiv:2401.01234`) are fetched directly.
- Simple site hints: lines equal to `linkedin`, `arxiv`, `news`, or `github` may be used to bias search.
  - `linkedin`: short queries may add `site:linkedin.com`.
  - `github`: code-related queries (e.g., containing "code" or "repo") may add `site:github.com`.
- Everything else is treated as a search query.
- Inline `--query` supports the same section splitters (use blank lines or `---`) and `;` separators.

Example (`instructions/20250101.txt`):
```
LLM evaluation frameworks
linkedin
news

-----
youtube
agentic AI demos for manufacturing

arXiv:2401.01234
https://example.com/blog/post
file: ./local/report.pdf | title="Local report"
dir: ./local/briefings
glob: ./local/**/*.md
```

## Outputs (per instruction file)
Created under `--output/<queryID>/`:
- `instruction/`: Copy of the input instruction file.
- `archive/`: All run outputs:
  - `_job.json`: Parsed job inputs (queries, URLs, arXiv IDs, options) for reproducibility.
  - `_log.txt`: Timestamped log of all actions and errors.
  - `agentic_trace.jsonl`: Structured turn-by-turn planner/executor trace (only when `--agentic-search` is enabled).
  - `agentic_trace.md`: Human-readable summary of the agentic trace (only when `--agentic-search` is enabled).
  - `tavily_search.jsonl`: One JSON object per query with Tavily search results; each result includes a short `summary` plus a `query_summary`.
  - `tavily_extract/`: Per-URL extraction JSON (pretty-printed).
  - `local/manifest.jsonl`: One JSON object per local document (path, title, tags, text path).
  - `local/raw/`: Copied local source files.
  - `local/text/`: Extracted text from local files.
  - `web/pdf/`: PDFs downloaded directly from URL instructions (when the URL ends in `.pdf` and `--download-pdf` is set).
  - `web/text/`: Extracted text from `web/pdf` (when `pymupdf` is available).
  - `openalex/works.jsonl`: OpenAlex open-access metadata including `cited_by_count` (when `--openalex` is set).
  - `openalex/pdf/`: OpenAlex PDFs (when `--download-pdf`).
  - `openalex/text/`: Extracted text from OpenAlex PDFs (when `pymupdf` is available).
  - `youtube/videos.jsonl`: YouTube video metadata (when `--youtube` is set).
  - `youtube/transcripts/`: YouTube transcripts named `youtu.be-<id>-<title>.txt` (title truncated to 80 chars) with header metadata (title, URL, tags, summary).
  - `arxiv/papers.jsonl`: arXiv metadata (includes `cited_by_count` when available); includes heuristic recent search entries when applicable.
  - `arxiv/pdf/`: Downloaded arXiv PDFs (when `--download-pdf`).
  - `arxiv/text/`: Extracted text from PDFs (when `--download-pdf` and `pymupdf` available).
  - `arxiv/src/`: arXiv source tarballs (`*.tar.gz`) and extracted source folders (when `--arxiv-src`).
  - `arxiv/src_text/`: Extracted TeX text (when `--arxiv-src`).
  - `arxiv/src_manifest.jsonl`: TeX/figure manifests per paper (when `--arxiv-src`).
  - `<queryID>-index.md`: Human-friendly summary with relative file paths for downstream ingestion.

## Project Layout
- `src/feather/`: Core package code.
- `tests/`: Unit tests (pytest).
- `examples/`: Sample instruction files.
- `docs/`: Detailed CLI/report references and operational notes.
- `.backup/`: Archived files moved out of the main tree.
- `run.py`: Local CLI runner without installation.
- `feather.ps1` / `feather.cmd`: Convenience wrappers for Windows.

## Testing
```bash
python -m pip install -r requirements.txt
pytest
```

## Lint
```bash
python -m pip install -r requirements.txt
ruff check .
```

## List Output Columns
- `Date`: From `archive/_job.json` if present.
- `Q/U/A`: Query, URL, and arXiv ID counts.
- `Tavily`: `S` if `tavily_search.jsonl` exists; `+E#` for extracted text count.
- `arXiv`: `pdf/txt` counts if `arxiv/papers.jsonl` exists.
- `OpenAlex`: `pdf/txt` counts if `openalex/works.jsonl` exists.
- `YouTube`: `videos/transcripts` counts if `youtube/videos.jsonl` exists.
- `Local`: `raw/text` counts for ingested local files.
- `WebPDF`: `pdf/txt` counts from direct PDF downloads.
- `Index`: `Y` if a `*-index.md` exists.

## JSONL Review Output
- `tavily_search.jsonl` prints one line per query with query text, result counts, result type counts (pdf/arXiv/web), a top result summary, and the query summary.
- Other JSONL files show a short preview with detected keys and limited lines.
- Use `--review-full` to print full JSONL entries or full text outputs.

## Notes and Tips
- Set `TAVILY_API_KEY` in your environment before running.
- Set `YOUTUBE_API_KEY` in your environment before running YouTube search.
- If transcripts fail with `IpBlocked`, set `YOUTUBE_PROXY` (or `YOUTUBE_PROXY_HTTP`/`YOUTUBE_PROXY_HTTPS`) or omit `--yt-transcript`.
- Tavily and arXiv calls include short sleeps to be polite; heavy batches may take time.
- If `arxiv` or `pymupdf` are missing, those features are skipped with runtime errors logged per item.
- The program stops early if no `.txt` files are found in `--input`.
