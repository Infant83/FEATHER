Claim | Evidence | Strength | Flags
--- | --- | --- | ---
본 런(20260116_arxiv-materials)은 **arXiv 1편(“WildSci: Advancing Scientific Reasoning from In-the-Wild Literature”)**만 수집된 미니 아카이브입니다. | (none) | none | no_evidence
목표: 아카이브를 매핑하고(커버리지 확인), **핵심 소스/파일을 식별**한 뒤, **읽기 계획(우선순위 최대 12개)**을 제안. | (none) | none | no_evidence
-- | (none) | none | no_evidence
`archive/arxiv/papers.jsonl` : 1개 arXiv 레코드(2601.05567v1) | (none) | none | no_evidence
`archive/arxiv/src_manifest.jsonl` : 소스 tar 및 tex 구성/메인 tex/figure 목록 | (none) | none | no_evidence
(요청된 기본 인덱스 중) `archive/tavily_search.jsonl` **없음** | (none) | none | no_evidence
(요청된 기본 인덱스 중) `archive/openalex/works.jsonl` **없음** | (none) | none | no_evidence
(요청된 기본 인덱스 중) `archive/youtube/videos.jsonl` **없음** | (none) | none | no_evidence
(요청된 기본 인덱스 중) `archive/local/manifest.jsonl` **없음** | (none) | none | no_evidence
`archive/20260116_arxiv-materials-index.md` : 이번 런이 무엇을 수집했는지 요약(텍스트/소스/추출물 경로) | (none) | none | no_evidence
`archive/tavily_extract/0001_https_arxiv.org_abs_2601.05567.txt` : arXiv 랜딩 페이지 추출(초록/메타) | (none) | none | no_evidence
`/instruction/20260116_arxiv-materials.txt` : 입력 instruction(이번 런이 arXiv URL 1개를 대상으로 했음) | (none) | none | no_evidence
`/archive/20260116_arxiv-materials-index.md` : 수집 범위(1 URL, 1 arXiv ID, PDF 1, 텍스트 1, 소스 1)와 경로 안내 | /archive/20260116_arxiv-materials-index.md` | low | -
`archive/arxiv/text/2601.05567v1.txt` : PDF에서 추출된 텍스트(페이지 단위로 들어있음) | (none) | none | no_evidence
`archive/arxiv/pdf/2601.05567v1.pdf` : 원문 PDF | (none) | none | no_evidence
`archive/arxiv/src_manifest.jsonl` : main tex, tex file list, figures | (none) | none | no_evidence
`archive/arxiv/src_text/2601.05567.txt` : 여러 tex를 합쳐 텍스트화한 파일(appendix/related work/프롬프트 등 세부가 잘 보임) | (none) | none | no_evidence
`archive/arxiv/src/2601.05567/neurips_2025.tex` : 메인 엔트리(tex include 구조의 시작점) | (none) | none | no_evidence
`archive/arxiv/src/2601.05567/ch_intro.tex` | (none) | none | no_evidence
`archive/arxiv/src/2601.05567/ch_method.tex` | (none) | none | no_evidence
`archive/arxiv/src/2601.05567/ch_experiments.tex` | (none) | none | no_evidence
`archive/arxiv/src/2601.05567/ch_results.tex` | (none) | none | no_evidence
`archive/arxiv/src/2601.05567/ch_conclusion.tex` | (none) | none | no_evidence
`archive/arxiv/src/2601.05567/ch_appendix.tex` | (none) | none | no_evidence
`archive/arxiv/src/2601.05567/figs/*.pdf` : 파이프라인/분포/학습곡선 등 도표 | (none) | none | no_evidence
`archive/tavily_extract/0001_https_arxiv.org_abs_2601.05567.txt` : arXiv 페이지 스냅샷(초록/링크) | (none) | none | no_evidence
`/report_notes/source_index.jsonl` : 소스 1개 레코드 | (none) | none | no_evidence
`/report_notes/source_triage.md` : “WildSci” 1개가 높은 점수로 triage | (none) | none | no_evidence
**논문 내용을 빠르게 파악**: `archive/arxiv/text/2601.05567v1.txt` (PDF 추출본) | (none) | none | no_evidence
**재현/디테일(프롬프트/하이퍼파라미터/부록 분석)을 정확히 파악**: `archive/arxiv/src_text/2601.05567.txt` + 개별 tex(ch_*.tex) | (none) | none | no_evidence
**구조 내비게이션**: `archive/arxiv/src/2601.05567/neurips_2025.tex` (include 관계 확인) | (none) | none | no_evidence
**핵심 그림 확인**: `archive/arxiv/src/2601.05567/figs/pipeline.pdf`, `figs/umap.pdf`, `figs/valid_test_allaligned*.pdf` | (none) | none | no_evidence
이유: 논문 전체 스토리(문제의식→데이터셋 WildSci→RL( GRPO )→벤치마크 결과)를 **가장 빠르게 훑는 1차 원문**. | (none) | none | no_evidence
이유: PDF 추출본보다 **부록/프롬프트/세부 실험 설정**이 깔끔하게 잡히는 경우가 많고, 특히 WildSci의 **QA generation prompt**/품질분석(Gemini 평가 등)이 들어있음. | (none) | none | no_evidence
이유: 본문이 여러 `ch_*.tex`로 쪼개져 있어 **문서 구조를 잡는 앵커 파일**. | (none) | none | no_evidence
이유: WildSci가 겨냥하는 갭(수학/코딩 대비 과학 도메인 RLVR 데이터 부족)과 핵심 기여를 **압축적으로 확인**. | (none) | none | no_evidence
이유: 데이터 생성 파이프라인(논문 소스: Nature Communications, 필터링/중복제거, refinement로 옵션 10개 확장, model voting, subset 정의 등)과 **reward 설계(정답 매칭) 핵심**. | (none) | none | no_evidence
이유: 사용 모델(Qwen2.5-32B-Instruct, Qwen3-32B, Mistral-Small-24B-Instruct-2501 등), 생성/투표 설정, 평가셋 구성(WildSci-Val, GPQA-Aug 등) 같은 **실험 프로토콜**. | (none) | none | no_evidence
이유: 성능 향상, 도메인별 트렌드, “post-saturation generalization” 같은 **분석 주장**이 결과 파트에 집중. | (none) | none | no_evidence
이유: 재현에 중요한 학습 세팅(verl 프레임워크, max response length 8192, rollout 8, lr 5e-7, A100 8장 등)과 데이터 품질 분석(라벨 신뢰도/난이도 평가/유사도 분석)이 상세. | (none) | none | no_evidence
이유: 어떤 tex/figure가 있는지, main tex가 무엇인지 등 **소스 탐색 내비게이션**(본문 인용용이 아니라 “지도”로 유용). | (none) | none | no_evidence
이유: 논문 Figure 1에 해당. 데이터 생성 파이프라인을 **한 장으로 요약**. | (none) | none | no_evidence
이유: WildSci가 기존 벤치마크(SuperGPQA, MMLU-Pro) 대비 **커버리지/분포 차이**를 주장하는 시각적 근거. | (none) | none | no_evidence
이유: validation 과적합 이후에도 OOD 성능이 오르는 “post-saturation generalization”을 **직관적으로 확인**. | (none) | none | no_evidence
**1단계(20~30분, 스토리 파악)**: 1 → 4 → 5 → 7 | (none) | none | no_evidence
**2단계(재현/디테일, 30~60분)**: 6 → 8 (특히 prompts/quality analysis/학습 세팅) | (none) | none | no_evidence
**3단계(구조/근거 보강, 10~20분)**: 10 → 11 → 12 | (none) | none | no_evidence
**막히면 내비게이션**: 3, 9를 열어 “어디에 뭐가 있는지” 확인 후 필요한 tex로 점프 | (none) | none | no_evidence
이번 아카이브에는 OpenAlex/YouTube/Tavily Search JSONL이 없어서, **외부 인용망/관련영상/추가 문헌 확장**은 커버되지 않습니다(현재는 논문 1편 중심으로만 읽기 계획을 세우는 게 맞음). | (none) | none | no_evidence
“materials”라는 쿼리명과 달리, 수집된 것은 **materials science 자체 논문이 아니라 scientific reasoning dataset/RL 논문**입니다. 따라서 보고서 포커스가 “materials science”라면 추가 수집이 필요합니다(현재 아카이브 범위 밖). | (none) | none | no_evidence