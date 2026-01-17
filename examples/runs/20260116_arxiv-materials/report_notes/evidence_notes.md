## 런 스코프/지시(Instruction & Index)
- **수집 대상 URL(단일 논문)**: arXiv abs 링크만 포함됨 — https://arxiv.org/abs/2601.05567  [instruction/20260116_arxiv-materials.txt]  
- **아카이브 범위**: PDF 1개 다운로드, PDF 텍스트 추출 1개, arXiv 소스(TeX) 및 src_text 포함 [archive/20260116_arxiv-materials-index.md]  
- **근거로 사용 가능한 “원문 계열” 파일**: arXiv PDF(`archive/arxiv/pdf/2601.05567v1.pdf`), PDF 텍스트(`archive/arxiv/text/2601.05567v1.txt`), TeX 섹션 파일들(`archive/arxiv/src/2601.05567/*.tex`), 참고문헌 bbl(`archive/arxiv/src/2601.05567/neurips_2025.bbl`) [archive/20260116_arxiv-materials-index.md]

---

## 논문 원문(TeX)에서의 핵심 사실 발췌 (arXiv:2601.05567v1, “WildSci”)
### 문제의식/기여(Introduction)
- 과학 도메인은 **RLVR(reinforcement learning with verifiable rewards)** 맥락에서 상대적으로 미개척이며, 과학 질문은 복잡하고 도메인지식이 필요하다고 서술 [archive/arxiv/src/2601.05567/ch_intro.tex]  
- 기존 데이터셋이 물리/화학/생물에 치우쳐 있고 **materials science, medicine 같은 학제 분야가 과소대표**라고 명시 [archive/arxiv/src/2601.05567/ch_intro.tex]  
- 과학 질문의 “검증 가능 보상” 문제를 완화하기 위해 **open-ended 질문을 MCQ(객관식)**로 구조화한다고 설명 [archive/arxiv/src/2601.05567/ch_intro.tex]  
- 핵심 기여 요약:
  - **“fully automated data synthesis pipeline”** (논문 기반 QA 생성→정제→모델 보팅) [archive/arxiv/src/2601.05567/ch_intro.tex]
  - **WildSci: 56K 질문, 9 disciplines, 26 subdomains** [archive/arxiv/src/2601.05567/ch_intro.tex]
  - WildSci로 RLVR을 과학으로 전이했으며 GPQA/SuperGPQA/MMLU-Pro 등에서 개선 주장 [archive/arxiv/src/2601.05567/ch_intro.tex]

### 데이터 생성 파이프라인/설계 선택(Method: WildSci 섹션)
- 데이터 소스: **Nature Communications의 공개(open-access) 논문**을 사용한다고 명시 [archive/arxiv/src/2601.05567/ch_method.tex]
- 분류 체계: Nature Communications의 다수 카테고리를 **SuperGPQA taxonomy를 따라 9개 discipline으로 재구성** [archive/arxiv/src/2601.05567/ch_method.tex]
- 멀티모달 배제: 논문에 텍스트+비주얼이 있으나 **title/abstract/main body만 사용하고 figures/tables는 제외**(텍스트 기반 추론에 집중) [archive/arxiv/src/2601.05567/ch_method.tex]
- QA 생성 요구사항: **figure/table/정밀 수치에 의존하지 않는 “context-independent questions”**를 생성하도록 프롬프트 설계 [archive/arxiv/src/2601.05567/ch_method.tex]
- 필터링:
  - 섹션/실험 디테일/그림·표 참조 등 **휴리스틱·키워드 기반 필터**로 제거 [archive/arxiv/src/2601.05567/ch_method.tex]
  - **13-gram dedup**을 GPQA, SuperGPQA, MMLU-Pro에 대해 수행, **overlap 0.0%**로 보고 [archive/arxiv/src/2601.05567/ch_method.tex]
- 정제(refinement): 질문 패러프레이즈, 표면 단서 제거, **선택지 수를 4→10 등으로 확장**하여 난이도/다양성 증가 [archive/arxiv/src/2601.05567/ch_method.tex]
- 모델 보팅(voting): 앙상블 모델들이 풀게 하고 **추가 선택지 “None of the above / unanswerable”**를 넣어 다수 모델이 unanswerable이면 폐기 [archive/arxiv/src/2601.05567/ch_method.tex]
- 데이터 난이도/명확성 프록시: 모델 합의 수준으로 **All Aligned / Majority Aligned / Majority Divergent / All Divergent**로 그룹화 [archive/arxiv/src/2601.05567/ch_method.tex]
- RLVR 보상: synthetic label \(y_{syn}\)과 모델 예측 \(\hat y\)의 **단순 정답 일치(맞으면 1, 아니면 0)**로 reward 정의 [archive/arxiv/src/2601.05567/ch_method.tex]
- 과적합 완화(옵션 위치 암기 방지): **각 epoch마다 선택지 셔플** [archive/arxiv/src/2601.05567/ch_method.tex]
- 학습 알고리즘: 수학 추론에서 쓰인 **GRPO(Group Relative Policy Optimization)** 채택 [archive/arxiv/src/2601.05567/ch_method.tex]

### 정량 결과/분석(Results and Analysis)
- 메인 성능표(일부):
  - Qwen2.5-1.5B-Instruct 기준, WildSci All Aligned로 학습 시 WildSci-Val **46.70→80.48** [archive/arxiv/src/2601.05567/ch_results.tex]
  - OOD 벤치마크 평균(“Average”, GPQA-Aug/SuperGPQA/MMLU-Pro 평균) **24.52→31.78**로 증가 [archive/arxiv/src/2601.05567/ch_results.tex]
  - Qwen2.5-3B-Instruct도 평균 **31.80→36.25**로 증가 [archive/arxiv/src/2601.05567/ch_results.tex]
- 학습 다이내믹스: **validation set에서 overfitting 이후에도 OOD test 성능이 계속 향상**되는 현상을 보고 [archive/arxiv/src/2601.05567/ch_results.tex]
- 도메인 커버리지와 성능 동학: WildSci 커버리지가 많은 영역(chemistry/physics/engineering)은 **학습이 진행될수록 더 안정적으로 증가**, 커버리지가 적은 영역(law/history/philosophy)은 변동이 더 큼 [archive/arxiv/src/2601.05567/ch_results.tex]
- “format alignment vs reasoning” 분해:
  - 답안 형식(extractability)은 **초기(수십 step 내) 빠르게 95% 근처로 수렴**
  - 그 이후에도 정확도가 계속 오르므로 **후반 성능 향상은 단순 포맷 적응만으로 설명되지 않는다**고 해석 [archive/arxiv/src/2601.05567/ch_results.tex]
- refinement 어블레이션:
  - refinement 없이도 평균 성능이 오르지만(예: 평균 28.83), **10-option valid set에서 66.63**으로 낮아지고, 옵션 확장이 랜덤 추측을 줄여 더 견고한 학습을 유도한다고 주장 [archive/arxiv/src/2601.05567/ch_results.tex]
- WildSci의 추론유형 분포(자동 분류 결과):
  - numerical calculation 40.00%
  - causal inference 37.59%
  - model/method/concept analysis 22.41% [archive/arxiv/src/2601.05567/ch_results.tex]

### 실험/재현성 정보(Experiments & Appendix: settings)
- WildSci-Val 구성: **9 disciplines에서 각 100문항 샘플링(총 900), 각 문항 10 options** [archive/arxiv/src/2601.05567/ch_experiments.tex]
- GPQA-Aug: GPQA-Diamond 198문항에 대해 정답 위치가 4개 포지션에 오도록 **4-way permutation으로 792 예시** [archive/arxiv/src/2601.05567/ch_experiments.tex]
- 데이터 생성에 사용한 LLM: **Qwen2.5-32B-Instruct, Qwen3-32B**, 보팅에 **Mistral-Small-24B-Instruct-2501** 등 사용; 보팅은 모델당 4샘플(temperature 0.8)로 총 8응답을 사용 [archive/arxiv/src/2601.05567/ch_experiments.tex]
- 학습 설정(appendix):
  - GRPO(verl 프레임워크), max response 8192 토큰, rollout 8응답/프롬프트 temperature 1.0, lr \(5\times10^{-7}\), AdamW [archive/arxiv/src/2601.05567/ch_appendix.tex]
  - 컴퓨트: **8× NVIDIA A100 40GB**, 1.5B 700step=1일(4 GPU), 3B 700step=2일(8 GPU) [archive/arxiv/src/2601.05567/ch_appendix.tex]

### 한계(Limitations)
- 일부 수치 문제는 **상대적으로 단순**하며, 과학지식+더 깊은 정량 추론 결합이 미래 과제 [archive/arxiv/src/2601.05567/ch_conclusion.tex]
- MCQ 포맷 자체가 **spurious heuristics 악용 위험**이 있고, open-ended research 질문(인과/분석)의 평가·검증은 여전히 도전과제 [archive/arxiv/src/2601.05567/ch_conclusion.tex]

### 재료과학(materials) 관련 “직접 근거”
- 26개 subdomain 분포 설명에서 **Materials Science가 journal에서 더 prevalent**하여 더 많은 papers/questions가 생성된다고 명시 [archive/arxiv/src/2601.05567/ch_appendix.tex]
- 관련 벤치마크 언급(관련 work 맥락): “only a few domains… mainly chemistry, biology, materials science, and physics”라고 적시 [archive/arxiv/src/2601.05567/ch_appendix.tex]

---

## 그림(figure) 기반 근거(파이프라인/분포/해석에 유용)
- **Figure: pipeline** — “Literature → QA Generation → Filtering → Refinement → Model Voting → Data Selection(Discard/Refined)” 흐름을 도식화(질문 예시와 ‘Discard’ 포함) [archive/arxiv/src/2601.05567/figs/pipeline.pdf]  
- **Figure: format_align** — 학습 step에 따른 **Accuracy**와 **Extractable Answer Rate**를 함께 표시(포맷 적응이 빠르게 수렴함을 시사) [archive/arxiv/src/2601.05567/figs/format_align.pdf]  
- **Figure: domain_combined_mean_std** — (a) chemistry/physics/engineering과 (b) history/law/philosophy의 **도메인별 accuracy 추세 차이**를 분리 제시 [archive/arxiv/src/2601.05567/figs/domain_combined_mean_std.pdf]  
- **Figure: subdomain_dist** — 26개 subdomain(예: **Materials science**, Energy science and technology, Drug discovery 등)별 **질문 수 분포 막대 그래프** [archive/arxiv/src/2601.05567/figs/subdomain_dist.pdf]

---

## PDF 텍스트(표현/요약 재확인용)
- 초록에서 **materials science/medicine의 데이터 부족**을 문제로 들고 WildSci(9 disciplines/26 subdomains), MCQ로 reward 신호 정의, RL finetune 및 training dynamics 분석을 요약 [archive/arxiv/text/2601.05567v1.txt]

---

## 인접 접근/벤치마크 “아카이브 내 근거로만” 연결 가능한 포인트(참고문헌 bbl/본문 언급 기반)
- WildSci가 개선을 보고한 OOD 벤치마크로 **GPQA / SuperGPQA / MMLU-Pro**를 명시 [archive/arxiv/src/2601.05567/ch_intro.tex; archive/arxiv/src/2601.05567/ch_results.tex]
- 관련 데이터셋 비교 테이블에서 WildSci를 “Peer-reviewed papers”, “Multiple (research focused)”, “56K”, “Avg Len 82±19”, “New? Yes”로 기재 [archive/arxiv/src/2601.05567/ch_intro.tex]
- materials science QA 벤치마크로 **MaScQA**가 참고문헌에 포함(인접 비교의 ‘존재’ 근거) [archive/arxiv/src/2601.05567/neurips_2025.bbl]