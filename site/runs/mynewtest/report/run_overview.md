# Run Overview

## Instruction
Source: ./instruction/generated_prompt_mynewtest.txt

```
Language: Korean

Template: acs_review
Depth: deep

목적/범위: “what is quantum computing” 질문에 답하는 ACS 스타일 리뷰 프롬프트를 작성하라. 재료·화학 연구자 독자를 대상으로, 양자컴퓨팅의 정의(고전 대비), 핵심 물리 개념(큐비트, 중첩, 얽힘, 간섭), 계산 모델(게이트형/어닐링 등)과 하드웨어-소재 관점(초전도·이온트랩·포토닉 등)을 연결해 설명하고, 응용·한계·검증 과제를 균형 있게 정리하라. 합의된 내용과 추정/전망을 명확히 분리하고, 모든 약어는 최초 1회 정의하라.

필수 섹션 산출물(섹션명 유지): Abstract(5–7문장), Introduction, Current Landscape(접근법/플랫폼을 범주화하고 근거 수준을 비교), Mechanistic Insights(큐비트 상태, 게이트/측정, 오류·디코히런스, 오류정정 개념), Applications(암호/소재과학·화학 시뮬레이션/최적화 등과 현실적 격차), Challenges(스케일링, 결함/소자 변동성, cryo/통합, 컴파일·연결성 제약), Outlook(검증 필요 실험·표준화·벤치마크), Risks & Gaps(누락된 증거·제약·불확실성 명시), Critics(반대 견해/과장 비판: “short headline” + 짧은 문단 + 불릿), Appendix(용어집, 비교표, 참고문헌 목록).

증거/인용 정책: 로컬 전문 텍스트/PDF(특히 “Cryptography & Quantum Computing: Why it matters and what comes next?”, “Quantum Leap: A Look at Google’s and China’s Quantum Computing Efforts…”, 필요 시 “Full Characterization of the Depth Overhead…”)에서 핵심 주장에는 문장 단위 인용(저자/연도/제목) 또는 파일ID를 붙여라. Tavily 웹 검색 결과는 현재 본문 추출이 없어 직접 인용 대신 “개념 정합성 점검/정의 프레이밍” 참고로만 사용하라. 하드웨어/소재별 성능 수치, 최신 로드맵 등 추가 근거가 없으면 “공개정보 한계”로 표시하고 단정적 수치를 피하라.

언어/문체: 한국어로 학술적으로 작성하되, 고유명사·논문 제목은 원문 유지. 단락 중심, 표/불릿은 최소화(Challenges, Risks & Gaps, Critics, Appendix에서만 적극 활용).
```

## Archive Index
Source: ./archive/mynewtest-index.md

# Archive mynewtest

- Query ID: `mynewtest`
- Date: 2026-02-02 (range: last 365 days)
- Queries: 1 | URLs: 0 | arXiv IDs: 0

## Run Command
- `python -m feather --input C:\Users\angpa\myProjects\FEATHER\site\runs\mynewtest\instruction\mynewtest.txt --output C:\Users\angpa\myProjects\FEATHER\site\runs --days 365 --max-results 8 --download-pdf --lang en --openalex --oa-max-results 8 --youtube --update-run`

## Instruction
- `../instruction/mynewtest.txt`

## Tavily Search
- `./tavily_search.jsonl`
- Includes per-result `summary` and `query_summary`

## OpenAlex (OA)
- `./openalex/works.jsonl`
- PDFs: 4
- PDF file: `./openalex/pdf/W4391590997.pdf` | Title: Full Characterization of the Depth Overhead for Quantum Circuit Compilation with Arbitrary Qubit Connectivity Constraint | Source: https://quantum-journal.org/papers/q-2025-05-28-1757/pdf/ | Citations: 2
- PDF file: `./openalex/pdf/W4409149714.pdf` | Title: Nonlocality in photonic materials and metamaterials: roadmap | Source: https://arxiv.org/pdf/2503.00519 | Citations: 15
- PDF file: `./openalex/pdf/W4413877234.pdf` | Title: Cryptography &amp; Quantum Computing: Why it matters and what comes next? | Source: https://www.scholarlyreview.org/article/143824.pdf | Citations: 0
- PDF file: `./openalex/pdf/W7116737831.pdf` | Title: Quantum Leap: A Look at Google’s and China’s Quantum Computing Efforts and What They Mean for the Future of the Industry | Source: https://ijircst.org/DOC/1417_pdf.pdf | Citations: 0
- Extracted texts: 4
- Text file: `./openalex/text/W4391590997.txt` | Title: Full Characterization of the Depth Overhead for Quantum Circuit Compilation with Arbitrary Qubit Connectivity Constraint | Source: https://quantum-journal.org/papers/q-2025-05-28-1757/pdf/ | Citations: 2
- Text file: `./openalex/text/W4409149714.txt` | Title: Nonlocality in photonic materials and metamaterials: roadmap | Source: https://arxiv.org/pdf/2503.00519 | Citations: 15
- Text file: `./openalex/text/W4413877234.txt` | Title: Cryptography &amp; Quantum Computing: Why it matters and what comes next? | Source: https://www.scholarlyreview.org/article/143824.pdf | Citations: 0
- Text file: `./openalex/text/W7116737831.txt` | Title: Quantum Leap: A Look at Google’s and China’s Quantum Computing Efforts and What They Mean for the Future of the Industry | Source: https://ijircst.org/DOC/1417_pdf.pdf | Citations: 0
