## 아카이브 커버리지 빠른 요약 (Query ID: 20260116_arxiv-materials)
- **핵심 대상 arXiv 논문(1편)**: *WildSci: Advancing Scientific Reasoning from In-the-Wild Literature* (arXiv:2601.05567v1, 2026-01-09)  
  - PDF: `archive/arxiv/pdf/2601.05567v1.pdf`  
  - 텍스트 추출본: `archive/arxiv/text/2601.05567v1.txt`  
  - 소스(TeX) 및 분할 챕터: `archive/arxiv/src/2601.05567/*.tex` + 참고문헌 `.bbl`
- **외부 검색/인용 메타 인덱스(JSONL)**: 이 런에는 **openalex/works.jsonl 등은 없음**.  
  - 존재하는 JSONL 인덱스: `archive/arxiv/papers.jsonl`, `archive/arxiv/src_manifest.jsonl`
- **추가 웹 발췌**: arXiv abs 페이지 텍스트 1개  
  - `archive/tavily_extract/0001_https_arxiv.org_abs_2601.05567.txt`
- **그림(figure) 리소스 존재**: 파이프라인/분포/UMAP 등 PDF 그림 다수  
  - `archive/arxiv/src/2601.05567/figs/*.pdf` (예: `pipeline.pdf`, `umap.pdf` 등)

---

## 구조적 인벤토리 (중요 파일/폴더 맵)

### 1) 런/지시/인덱스
- `instruction/20260116_arxiv-materials.txt`  
  - 대상 URL이 `https://arxiv.org/abs/2601.05567` 단일로 지정됨
- `archive/20260116_arxiv-materials-index.md`  
  - 수집 범위 요약(1 arXiv, 1 PDF, src 포함), 실행 커맨드 기록

### 2) arXiv 메타데이터(인덱스 역할)
- `archive/arxiv/papers.jsonl`  
  - 논문 title/author/summary/pdf_url 등 1레코드
- `archive/arxiv/src_manifest.jsonl`  
  - 소스 패키지 내 파일 목록/매핑(TeX/fig 경로 찾기용)

### 3) 논문 본문(리뷰의 1차 근거)
- `archive/arxiv/pdf/2601.05567v1.pdf`  
  - Nature-style 리뷰용 최종 원문(그림/표 포함)
- `archive/arxiv/text/2601.05567v1.txt`  
  - 빠른 검색/인용에 유리(단, PDF 레이아웃 손실 가능)
- `archive/arxiv/src_text/2601.05567.txt`  
  - TeX에서 추출된 텍스트(appendix/related work/실험세팅 등 구조적으로 읽기 쉬움)

### 4) 소스(TeX) 챕터 단위(정확한 서술/구조 파악용)
- `archive/arxiv/src/2601.05567/ch_intro.tex`
- `archive/arxiv/src/2601.05567/ch_method.tex`
- `archive/arxiv/src/2601.05567/ch_results.tex`
- `archive/arxiv/src/2601.05567/ch_experiments.tex`
- `archive/arxiv/src/2601.05567/ch_conclusion.tex`
- `archive/arxiv/src/2601.05567/ch_appendix.tex`  
  - 실험 세부/관련연구/데이터 품질 분석 등(리밋/보틀넥 논의에 직접적)

### 5) 참고문헌(“인접 접근 비교”를 아카이브 근거로 처리하기 위한 핵심)
- `archive/arxiv/src/2601.05567/neurips_2025.bbl`  
  - 본문에서 언급하는 인접 데이터셋/벤치마크/RLVR 계열을 **정확한 서지정보로** 확인 가능  
  - (예: GPQA, SuperGPQA, MMLU-Pro, SciInstruct, Natural Reasoning 등과 연결)

### 6) 그림(보고서에 “figure가 있을 때 통합” 요구 대응)
- `archive/arxiv/src/2601.05567/figs/pipeline.pdf`  (데이터 생성 파이프라인 도식)
- `archive/arxiv/src/2601.05567/figs/umap.pdf` (도메인/임베딩 분포 시각화로 추정)
- `archive/arxiv/src/2601.05567/figs/domain_dist.pdf`, `subdomain_dist.pdf` (커버리지/분포)
- `archive/arxiv/src/2601.05567/figs/data_type_split.pdf`, `format_align.pdf`
- `archive/arxiv/src/2601.05567/figs/valid_test_allaligned*.pdf` (subset별 valid/test 관련 도표로 추정)

### 7) 웹 발췌(보조)
- `archive/tavily_extract/0001_https_arxiv.org_abs_2601.05567.txt`  
  - arXiv abstract 페이지 기반 요약/링크(핵심은 PDF/TeX가 더 강함)

---

## 우선순위 읽기 계획 (최대 12개, 근거 포함)

1) `archive/arxiv/pdf/2601.05567v1.pdf`  
- 최종 원문. Nature-style 리뷰의 “코어 기술 아이디어/워크플로/실험결과/그림”을 한 번에 확보.

2) `archive/arxiv/src/2601.05567/ch_intro.tex`  
- 문제정의(과학 추론 데이터 부족), 왜 literature-grounded MCQ+RLVR이 중요한지의 논리 전개를 정확히 인용하기 좋음.

3) `archive/arxiv/src/2601.05567/ch_method.tex`  
- WildSci 데이터 생성 파이프라인(논문→QA 생성→필터링→refinement→model voting→subset) 기술의 디테일 확보(보틀넥/한계 평가 근거).

4) `archive/arxiv/src/2601.05567/ch_results.tex`  
- 벤치마크 성능/도메인별 변화/일반화 경향 등 “효과가 무엇인지”를 수치 기반으로 정리하는 1순위.

5) `archive/arxiv/src/2601.05567/ch_experiments.tex`  
- 모델/학습 절차(RL finetune 등) 설정과 평가 프로토콜의 핵심을 빠르게 확인.

6) `archive/arxiv/src/2601.05567/ch_appendix.tex`  
- 데이터 품질 검증(예: Gemini 기반 라벨 합치율), redundancy/validity/difficulty 분석 등 “한계·누락·리스크”를 논증할 근거가 많음.

7) `archive/arxiv/src/2601.05567/ch_conclusion.tex`  
- 저자들이 스스로 주장하는 의의/한계/향후 과제 정리(리뷰 결론과 ‘next-step 질문’ 설계에 직접적).

8) `archive/arxiv/src/2601.05567/figs/pipeline.pdf`  
- 데이터 생성 워크플로를 리뷰 본문에 그림으로 통합하기 가장 좋은 자원(요구사항의 figure 통합 충족).

9) `archive/arxiv/src/2601.05567/figs/domain_dist.pdf`  
- 9 disciplines/26 subdomains 커버리지 분포를 시각적으로 보여줘 “재료과학 관점에서 데이터 커버리지” 논의에 유용.

10) `archive/arxiv/src/2601.05567/figs/subdomain_dist.pdf`  
- materials science가 ‘long-tail’로 취급될 때 세부 분포를 논할 근거(도메인 편향/불균형 문제 제기 가능).

11) `archive/arxiv/src/2601.05567/figs/umap.pdf`  
- 데이터/도메인 표현 공간의 분리/혼합 등을 통해 “범분야 일반화 vs 도메인 특이성” 논의에 도움(그림 해석은 본문 설명과 함께 확인 필요).

12) `archive/arxiv/src/2601.05567/neurips_2025.bbl`  
- “인접 접근/베이스라인 비교”를 **아카이브 근거로만** 수행해야 하므로, 관련 데이터셋·벤치마크·RLVR 선행연구를 정확한 레퍼런스로 묶는 데 필수.

---

## 메모(재료과학 관점으로 읽을 때 체크할 포인트)
- WildSci는 **materials science 자체를 새 데이터로 직접 확장**하기보다는, *peer-reviewed literature 기반의 자동 문제 생성+MCQ화+RLVR 학습 신호*라는 “연구 자동화 인프라” 제안임. 재료 R&D 관점에서는  
  - (i) 문헌 기반 지식/추론을 모델이 얼마나 잘 내재화하는지,  
  - (ii) 실제 discovery 워크플로(가설→실험→검증)와의 간극(특히 **그림/표 배제**, 정량 데이터/구조 정보 부재),  
  - (iii) 도메인 편향/용어/단위/재료 데이터 형식(조성, 결정구조, 공정-미세조직-물성 연계) 반영 여부  
  를 “한계/보틀넥”으로 짚을 근거가 있는지 확인하는 게 중요함.

원하시면 위 우선순위 1–7(본문/부록)에서 **재료과학·R&D 리더 관점으로 직접 인용 가능한 문장/수치/그림 캡션 위치**까지 뽑는 2단계 리딩 플랜(섹션별 체크리스트)도 잡아드릴 수 있습니다.