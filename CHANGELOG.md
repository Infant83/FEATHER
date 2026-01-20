# Changelog

## 0.5.1
- Add configurable max input token guardrails for models without profile limits (env/CLI/agent-config) and expose values in `--agent-info`.
- Apply max input token overrides across agents, including quality/evaluation stages and template adjuster.
- Add writer output validation/retry to prevent placeholder/meta responses and enforce required H2 headings in free-format.

## 0.5.0
- Add agent streaming output with debug logging and optional Markdown echo (`--stream`, `--stream-debug`, `--echo-markdown`).
- Add separate check model selection for alignment/plan checks (`--check-model`, default gpt-4o).
- Add free-form report mode that lets the model choose structure while still requiring Risks & Gaps/Critics (`--free-format`).
- Harden structural repair and writer output (append/replace/off modes, debug logs, heading coercion, placeholder retry, no-status-output guardrails).
- Ensure Risks & Gaps/Critics are present across all templates with “Not applicable/해당없음” guidance.
- Default template adjuster to risk-only behavior and improve template adjustment logging.
- Fix filesystem path resolution for report viewers/supporting data under deepagents to avoid outside-root errors.
- Localize alignment-check prompt for Korean.

## 0.4.0
- Treat arXiv abstract URLs as arXiv IDs when `--download-pdf` is enabled (auto PDF download).
- Add optional arXiv source download with TeX/figure manifests (`--arxiv-src`).
- arXiv-derived templates now generate per-section `.tex` files and guidance Markdown files.
- Add `--update-run` to reuse existing run folders and merge new outputs in place.
- Added optional vision model support in Federlicht (`--model-vision`) for figure analysis.
- Documentation updates for installation, workflow, and publishing.
