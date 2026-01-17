# Run Overview

## Instruction
Source: ./instruction/20260116_arxiv-materials.txt

```
https://arxiv.org/abs/2601.05567
```

## Archive Index
Source: ./archive/20260116_arxiv-materials-index.md

# Archive 20260116_arxiv-materials

- Query ID: `20260116_arxiv-materials`
- Date: 2026-01-16 (range: last 30 days)
- Queries: 0 | URLs: 1 | arXiv IDs: 1

## Run Command
- `python -m feather --input examples\instructions\20260116_arxiv-materials.txt --output examples\runs --days 30 --max-results 8 --download-pdf --arxiv-src --openalex --oa-max-results 8 --update-run`

## Instruction
- `../instruction/20260116_arxiv-materials.txt`

## Tavily Extract
- `./tavily_extract/0001_https_arxiv.org_abs_2601.05567.txt`

## arXiv
- `./arxiv/papers.jsonl`
- PDFs: 1
- PDF file: `./arxiv/pdf/2601.05567v1.pdf` | Title: WildSci: Advancing Scientific Reasoning from In-the-Wild Literature | Source: https://arxiv.org/pdf/2601.05567v1 | Citations: -
- Extracted texts: 1

- Text file: `./arxiv/text/2601.05567v1.txt` | Title: WildSci: Advancing Scientific Reasoning from In-the-Wild Literature | Source: https://arxiv.org/pdf/2601.05567v1 | Citations: -

## arXiv Source
- `./arxiv/src_manifest.jsonl`
- Source archives: 1
- Source tar: `./arxiv/src/2601.05567.tar.gz`
- Extracted TeX texts: 1
- TeX text: `./arxiv/src_text/2601.05567.txt`
