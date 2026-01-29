# Run Overview

## Instruction
Source: ./instruction/mytest.txt

```
다운받은 논문을 요약해줘.
```

## Archive Index
Source: ./archive/mytest_01-index.md

# Archive mytest_01

- Query ID: `mytest_01`
- Date: 2026-01-30 (range: last 365 days)
- Queries: 0 | URLs: 1 | arXiv IDs: 1

## Run Command
- `python -m feather --input C:\Users\angpa\myProjects\FEATHER\site\runs\mytest\instruction\mytest.txt --output C:\Users\angpa\myProjects\FEATHER\site\runs --days 365 --max-results 8 --download-pdf --lang ko --openalex --oa-max-results 8`

## Instruction
- `../instruction/mytest.txt`

## Tavily Extract
- `./tavily_extract/0001_https_arxiv.org_abs_2412.10149.txt`

## arXiv
- `./arxiv/papers.jsonl`
- PDFs: 1
- PDF file: `./arxiv/pdf/2412.10149v2.pdf` | Title: Learning Radical Excited States from Sparse Data | Source: https://arxiv.org/pdf/2412.10149v2 | Citations: 0
- Extracted texts: 1

- Text file: `./arxiv/text/2412.10149v2.txt` | Title: Learning Radical Excited States from Sparse Data | Source: https://arxiv.org/pdf/2412.10149v2 | Citations: 0
