## 수집/아카이브 범위(메타)
- 수집 대상 URL 3개(Instruction 명시)  
  - LinkedIn 포스트: https://www.linkedin.com/feed/update/urn:li:activity:7399939023072358401/ [/instruction/20260113_linkedin-review.txt]  
  - arXiv: https://arxiv.org/abs/2511.16652 [/instruction/20260113_linkedin-review.txt]  
  - 블로그(tistory): https://muni-dev.tistory.com/entry/Evolution-Strategies-at-the-Hyperscale [/instruction/20260113_linkedin-review.txt]
- 아카이브 인덱스에 “Tavily Extract 3개 텍스트 스냅샷”만 존재한다고 명시(= PDF 다운로드 커맨드가 인덱스에 보이지만, 실제 PDF 파일은 아카이브에 없음)  
  - `--download-pdf` 옵션이 커맨드에 포함되어 있으나 결과물 목록은 tavily_extract txt 3개만 기재됨 [/archive/20260113_linkedin-review-index.md]
- 아카이브 내 버전 파일 존재: final, final-v2~v5, 초안 md, 로그/잡 파일  
  - 파일 목록: [/archive] (ls 결과)

---

## 1차 근거(원문/발췌) — arXiv
출처 URL: https://arxiv.org/abs/2511.16652  
근거 파일: [/archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt]

- EGGROLL의 정식 명칭/정의
  - “Evolution Guided General Optimization via Low-rank Learning (EGGROLL)”로 소개하며, “backprop-free optimization”을 “large population sizes”로 스케일시키는 ES 알고리즘이라고 설명. [/archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt]
- 기존(naïve) ES의 병목
  - 전통적 ES가 대규모에서 비싸지는 이유로, 섭동 행렬 \(E \in \mathbb{R}^{m \times n}\) 생성 비용/메모리와 per-member forward pass를 위한 batched matmul 비용을 명시. [/archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt]
- 핵심 아이디어: low-rank perturbation
  - full-rank \(E\) 대신, \(A\in\mathbb{R}^{m\times r}, B\in\mathbb{R}^{n\times r}\) (단 \(r \ll \min(m,n)\))를 생성해 \(AB^\top\) 형태의 low-rank perturbation을 사용한다고 서술. [/archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt]
- 계산/메모리 절감 주장(복잡도/저장공간)
  - 보조 저장(auxiliary storage): \(mn\) → \(r(m+n)\) (per layer)  
  - forward pass 비용: \(\mathcal{O}(mn)\) → \(\mathcal{O}(r(m+n))\)  
  - 위 비교가 “full-rank ES 대비”라고 명시. [/archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt]
- 이론적 수렴률 주장
  - low-rank update가 full-rank update로 “fast \(\mathcal{O}(1/r)\)” rate로 수렴한다는 “theoretical analysis”를 언급. [/archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt]
- 실험 결과(초록 수준의 주장)
  - (1) tabula-rasa RL에서 ES 성능을 해치지 않으면서 더 빠르다  
  - (2) LLM reasoning 개선에서 GRPO와 경쟁력  
  - (3) “purely in integer datatypes”로 동작하는 nonlinear recurrent language model의 stable pre-training을 가능케 함  
  - 모두 초록에 요약 형태로 제시. [/archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt]

---

## 1차 근거(원문/발췌) — LinkedIn 포스트(실무자 주장)
출처 URL: https://www.linkedin.com/feed/update/urn:li:activity:7399939023072358401/  
근거 파일: [/archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt]

- “미분/backprop 없이도 거대 모델 훈련 가능”이라는 강한 메시지
  - “미분 없이도, backprop 없이도, 거대한 모델을 충분히 잘 훈련”할 수 있다는 취지로 서술. [/archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt]
- ES가 과거에 주류가 되지 못한 이유(비용/스케일링)
  - ES가 “너무 비싸고, 너무 느리고, 스케일링이 되지” 않았다는 설명과, population 평가 방식으로 인해 개체 수 증가 시 계산량이 폭증한다고 서술. [/archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt]
- low-rank perturbation(‘A와 B를 곱해 low-rank’)
  - 기존 ES의 full-rank perturbation 대신 “두 개의 얇은(skinny) 행렬 A와 B를 곱해 low-rank perturbation”을 만든다고 요약. [/archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt]
- “population 평균 내면 full-rank처럼 동작” 주장
  - population 전체에서 low-rank update를 평균내면 “full-rank ES 업데이트처럼 작동”한다는 취지의 설명. [/archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt]
- 통신/전달 비용 관련 강한 주장 + 구현 아이디어 언급
  - “perturbation을 아예 전달하지 않는다”, “counter-based RNG”로 각 worker가 인덱스만으로 perturbation을 재현하도록 설계, “통신 비용도 사실상 0”이라는 표현. [/archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt]
- 스케일 수치 주장(예: population 262,144)
  - “population 규모 262,144명”까지 확장, “기존 ES 스케일링의 200배 이상” 등의 수치/비교를 제시. [/archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt]
  - (주의) 이 수치/비교는 LinkedIn 글의 주장으로만 확인되며, 현재 아카이브의 arXiv 초록 텍스트에서는 동일 수치가 직접 확인되지 않음. [/archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt]

---

## 2차 근거(해설/리뷰) — Tistory 블로그
출처 URL: https://muni-dev.tistory.com/entry/Evolution-Strategies-at-the-Hyperscale  
근거 파일: [/archive/tavily_extract/0003_https_muni-dev.tistory.com_entry_Evolution-Strategies-at-the-Hyperscale.txt]

- 원문/코드 링크 제시
  - “원문: https://arxiv.org/pdf/2511.16652”, “코드: https://eshyperscale.github.io/”를 명시. [/archive/tavily_extract/0003_https_muni-dev.tistory.com_entry_Evolution-Strategies-at-the-Hyperscale.txt]
- EGGROLL 요지(ES를 hyperscale에 적용하기 위한 low-rank 대체)
  - ES가 거대 모델에서 “거대한 노이즈 행렬” 때문에 메모리/연산 비용 문제가 있고, 이를 “두 개의 작은 저랭크 행렬의 곱”으로 대체하는 아이디어라고 요약. [/archive/tavily_extract/0003_https_muni-dev.tistory.com_entry_Evolution-Strategies-at-the-Hyperscale.txt]
- 수렴/근사 분석 요약
  - low-rank 근사가 “매우 빠른 속도 \(O(1/r)\)”로 full-rank 업데이트와 동일해짐이 증명되었다고 설명. [/archive/tavily_extract/0003_https_muni-dev.tistory.com_entry_Evolution-Strategies-at-the-Hyperscale.txt]
- 구현 관점의 설명(연산 순서 최적화)
  - \(AB^\top\)를 직접 만들지 않고 입력 \(x\)에 대해 \((xB)A^\top\) 순서로 계산해 GPU에서 빠르고 메모리 효율적으로 만든다고 서술. [/archive/tavily_extract/0003_https_muni-dev.tistory.com_entry_Evolution-Strategies-at-the-Hyperscale.txt]
- 실험 항목(블로그 요약)
  - “Pure Integer Pretraining”, RL 비교(OpenES, PPO), LLM 추론(Countdown & GSM8K), 병렬 탐색(한 번에 1,024개 vs 32개 생성) 등의 서술이 포함. [/archive/tavily_extract/0003_https_muni-dev.tistory.com_entry_Evolution-Strategies-at-the-Hyperscale.txt]
  - (주의) 위 수치(예: 1,024 vs 32)는 블로그의 재서술이며, 현재 아카이브에는 논문 PDF 본문이 없어 원문 표/실험 세팅의 직접 대조는 불가. [/archive/20260113_linkedin-review-index.md]

---

## 2차 산출물(아카이브 내 작성된 리뷰 문서) — 내용 성격
근거 파일: [/archive/20260113_linkedin-review-final.md]

- 문서 목적/포맷(서두)
  - “LinkedIn practitioner review”로서 EGGROLL 관련 논의를 분석하고 “claims, evidence-backed insights, implications, risks, actions”를 제공한다고 명시. [/archive/20260113_linkedin-review-final.md]
- 핵심 내용 중 근거 연결이 약한(일반화된) 진술의 예
  - “Community Adoption: Early implementations … positive feedback”, “businesses can deploy …” 등은 현재 아카이브의 1차/2차 근거 텍스트에서 직접 인용/근거 문장으로 확인되기 어려운 일반론 형태로 서술됨. [/archive/20260113_linkedin-review-final.md]