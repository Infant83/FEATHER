# Archive 20260105_arxiv

- Query ID: `20260105_arxiv`
- Date: 2026-01-05 (range: last 30 days)
- Queries: 1 | URLs: 1 | arXiv IDs: 1

## Run Command
- `python -m hidair_feather --input C:\Users\angpa\myProjects\HiDair-feather\examples\instructions\20260105.txt --output runs --days 30 --max-results 8 --download-pdf --openalex --oa-max-results 8 --set-id arxiv`

## Instruction
- `../instruction/20260105.txt`

## Tavily Search
- `./tavily_search.jsonl`
- Includes per-result `summary` and `query_summary`

## Tavily Extract
- `./tavily_extract/0001_https_www.linkedin.com_posts_fanli_ai-molecular-design-has-some-known-challenges-activity-7406324682192441344-60n3_utm_s.txt`

## OpenAlex (OA)
- `./openalex/works.jsonl`
- PDFs: 2
- PDF file: `./openalex/pdf/W4417195415.pdf` | Title: Fraud Detection in Financial Transactions Using Graph Neural Networks | Source: https://ijsrem.com/download/fraud-detection-in-financial-transactions-using-graph-neural-networks/?wpdmdl=62268&refresh=6939fdc439b5e1765408196
- PDF file: `./openalex/pdf/W7116584439.pdf` | Title: Graph Neural Networks for Interferometer Simulations | Source: https://arxiv.org/pdf/2512.16051
- Extracted texts: 2
- Text file: `./openalex/text/W4417195415.txt` | Title: Fraud Detection in Financial Transactions Using Graph Neural Networks | Source: https://ijsrem.com/download/fraud-detection-in-financial-transactions-using-graph-neural-networks/?wpdmdl=62268&refresh=6939fdc439b5e1765408196
- Text file: `./openalex/text/W7116584439.txt` | Title: Graph Neural Networks for Interferometer Simulations | Source: https://arxiv.org/pdf/2512.16051

## arXiv
- `./arxiv/papers.jsonl`
- PDFs: 1
- PDF file: `./arxiv/pdf/2101.00001v1.pdf` | Title: Etat de l'art sur l'application des bandits multi-bras | Source: https://arxiv.org/pdf/2101.00001v1
- Extracted texts: 1

- Text file: `./arxiv/text/2101.00001v1.txt` | Title: Etat de l'art sur l'application des bandits multi-bras | Source: https://arxiv.org/pdf/2101.00001v1

