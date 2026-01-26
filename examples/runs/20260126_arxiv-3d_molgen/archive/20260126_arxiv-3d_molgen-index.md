# Archive 20260126_arxiv-3d_molgen

- Query ID: `20260126_arxiv-3d_molgen`
- Date: 2026-01-26 (range: last 30 days)
- Queries: 1 | URLs: 1 | arXiv IDs: 1

## Run Command
- `python -m feather --input examples\instructions\20260126_arxiv-3d_molgen.txt --output examples\runs --days 30 --max-results 8 --download-pdf --arxiv-src --openalex --oa-max-results 8`

## Instruction
- `../instruction/20260126_arxiv-3d_molgen.txt`

## Tavily Search
- `./tavily_search.jsonl`
- Includes per-result `summary` and `query_summary`

## Tavily Extract
- `./tavily_extract/0001_https_arxiv.org_pdf_2601.16955.txt`

## arXiv
- `./arxiv/papers.jsonl`
- PDFs: 1
- PDF file: `./arxiv/pdf/2601.16955v1.pdf` | Title: 3D Molecule Generation from Rigid Motifs via SE(3) Flows | Source: https://arxiv.org/pdf/2601.16955v1 | Citations: -
- Extracted texts: 1

- Text file: `./arxiv/text/2601.16955v1.txt` | Title: 3D Molecule Generation from Rigid Motifs via SE(3) Flows | Source: https://arxiv.org/pdf/2601.16955v1 | Citations: -

## arXiv Source
- `./arxiv/src_manifest.jsonl`
- Source archives: 1
- Source tar: `./arxiv/src/2601.16955.tar.gz`
- Extracted TeX texts: 1
- TeX text: `./arxiv/src_text/2601.16955.txt`

