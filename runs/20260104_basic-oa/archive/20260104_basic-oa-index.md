# Archive 20260104_basic-oa

- Query ID: `20260104_basic-oa`
- Date: 2026-01-04 (range: last 30 days)
- Queries: 3 | URLs: 2 | arXiv IDs: 0

## Run Command
- `python -m hidair_feather --input examples\instructions\20260104.txt --output runs --days 30 --max-results 8 --download-pdf --openalex --oa-max-results 8 --set-id basic-oa`

## Instruction
- `../instruction/20260104.txt`

## Tavily Search
- `./tavily_search.jsonl`
- Includes per-result `summary` and `query_summary`

## Tavily Extract
- `./tavily_extract/0001_https_www.linkedin.com_posts_fanli_ai-molecular-design-has-some-known-challenges-activity-7406324682192441344-60n3_utm_s.txt`
- `./tavily_extract/0002_https_www.nature.com_articles_s41467-025-67312-4_reference.pdf.txt`

## Web PDFs
- PDFs: 1
- PDF file: `./web/pdf/s41467-025-67312-4_reference.pdf` | Source: https://www.nature.com/articles/s41467-025-67312-4_reference.pdf
- Extracted texts: 1
- Text file: `./web/text/s41467-025-67312-4_reference.txt` | Source: https://www.nature.com/articles/s41467-025-67312-4_reference.pdf

## OpenAlex (OA)
- `./openalex/works.jsonl`
- PDFs: 1
- PDF file: `./openalex/pdf/W7117787413.pdf` | Title: Recent Progress in Stretchable OLED Design and Applications | Source: https://drpress.org/ojs/index.php/ajst/article/download/33002/32289 | Citations: 0
- Extracted texts: 1
- Text file: `./openalex/text/W7117787413.txt` | Title: Recent Progress in Stretchable OLED Design and Applications | Source: https://drpress.org/ojs/index.php/ajst/article/download/33002/32289 | Citations: 0

