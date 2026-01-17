# Run Overview

## Instruction
Source: ./instruction/20260117_arxiv-template.txt

```
https://arxiv.org/abs/2511.00922
https://arxiv.org/abs/2512.06029
https://arxiv.org/abs/1901.01201
```

## Archive Index
Source: ./archive/20260117_arxiv-template-index.md

# Archive 20260117_arxiv-template

- Query ID: `20260117_arxiv-template`
- Date: 2026-01-17 (range: last 30 days)
- Queries: 0 | URLs: 3 | arXiv IDs: 3

## Run Command
- `python -m feather --input examples\instructions\20260117_arxiv-template.txt --output examples\runs --days 30 --max-results 8 --download-pdf --arxiv-src --openalex --oa-max-results 8`

## Instruction
- `../instruction/20260117_arxiv-template.txt`

## Tavily Extract
- `./tavily_extract/0001_https_arxiv.org_abs_2511.00922.txt`
- `./tavily_extract/0002_https_arxiv.org_abs_2512.06029.txt`
- `./tavily_extract/0003_https_arxiv.org_abs_1901.01201.txt`

## arXiv
- `./arxiv/papers.jsonl`
- PDFs: 3
- PDF file: `./arxiv/pdf/1901.01201v1.pdf` | Title: General Approach To Compute Phosphorescent OLED Efficiency | Source: https://arxiv.org/pdf/1901.01201v1 | Citations: 88
- PDF file: `./arxiv/pdf/2511.00922v1.pdf` | Title: Validation of Semi-Empirical xTB Methods for High-Throughput Screening of TADF Emitters: A 747-Molecule Benchmark Study | Source: https://arxiv.org/pdf/2511.00922v1 | Citations: -
- PDF file: `./arxiv/pdf/2512.06029v1.pdf` | Title: From orbital analysis to active learning: an integrated strategy for the accelerated design of TADF emitters | Source: https://arxiv.org/pdf/2512.06029v1 | Citations: -
- Extracted texts: 3

- Text file: `./arxiv/text/1901.01201v1.txt` | Title: General Approach To Compute Phosphorescent OLED Efficiency | Source: https://arxiv.org/pdf/1901.01201v1 | Citations: 88
- Text file: `./arxiv/text/2511.00922v1.txt` | Title: Validation of Semi-Empirical xTB Methods for High-Throughput Screening of TADF Emitters: A 747-Molecule Benchmark Study | Source: https://arxiv.org/pdf/2511.00922v1 | Citations: -
- Text file: `./arxiv/text/2512.06029v1.txt` | Title: From orbital analysis to active learning: an integrated strategy for the accelerated design of TADF emitters | Source: https://arxiv.org/pdf/2512.06029v1 | Citations: -

## arXiv Source
- `./arxiv/src_manifest.jsonl`
- Source archives: 3
- Source tar: `./arxiv/src/1901.01201.tar.gz`
- Source tar: `./arxiv/src/2511.00922.tar.gz`
- Source tar: `./arxiv/src/2512.06029.tar.gz`
- Extracted TeX texts: 2
- TeX text: `./arxiv/src_text/2511.00922.txt`
- TeX text: `./arxiv/src_text/2512.06029.txt`
