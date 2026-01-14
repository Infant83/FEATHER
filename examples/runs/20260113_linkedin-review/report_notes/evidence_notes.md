## 1) 1차/2차 소스(웹 텍스트 추출본)

### A. arXiv 논문(초록/서지 페이지) — 1차 근거
- **핵심 제안**: “Evolution Guided General Optimization via Low-rank Learning (EGGROLL)”을 소개하며, **billions of parameters** 규모의 현대 신경망에서 **backprop-free(gradient-free) 최적화**를 대규모 population으로 스케일링하기 위한 ES 알고리즘이라고 설명함. [https://arxiv.org/abs/2511.16652] [archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt]
- **비용 병목 진단**: 나이브 ES는 각 레이어에서 **full-rank perturbation 행렬** 생성 및 배치 행렬곱 때문에 계산/메모리 비용이 커져 스케일에서 “prohibitively expensive”해진다고 명시. [https://arxiv.org/abs/2511.16652] [archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt]
- **핵심 메커니즘(저랭크 섭동)**: full-rank \(E \in R^{m\times n}\) 대신 \(A \in R^{m\times r}, B \in R^{n\times r}\)를 샘플링해 \(AB^T\) 형태의 **low-rank perturbation**을 사용하며 \(r \ll \min(m,n)\)라고 명시. [https://arxiv.org/abs/2511.16652] [archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt]
- **복잡도/메모리 절감 claim**: 보조 저장공간을 **\(mn \rightarrow r(m+n)\) per layer**로 줄이고, forward pass 비용을 **\(O(mn) \rightarrow O(r(m+n))\)**로 줄인다고 서술. [https://arxiv.org/abs/2511.16652] [archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt]
- **이론적 수렴 claim**: 저랭크 업데이트가 full-rank 업데이트로 **\(O(1/r)\)** 속도로 빠르게 수렴한다고 밝힘. [https://arxiv.org/abs/2511.16652] [archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt]
- **실험 결과(요약)**: (1) tabula-rasa RL에서 **더 빠르면서도 ES 성능을 compromise하지 않음**, (2) LLM reasoning 개선에서 **GRPO와 competitive**, (3) **purely integer datatypes**로 동작하는 nonlinear recurrent language model의 **stable pre-training**을 가능하게 했다고 요약. [https://arxiv.org/abs/2511.16652] [archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt]

### B. LinkedIn 포스트(한국어) — 실무자 내러티브/2차 주장 포함
- **문제의식/프레이밍**: “대규모 AI 모델 훈련에는 backpropagation과 미분 가능 구조가 필수”라는 믿음을 전제로 삼아왔으나, EGGROLL이 “미분 없이도, backprop 없이도” 거대 모델을 훈련할 수 있다고 주장하는 톤으로 서술. [https://www.linkedin.com/feed/update/urn:li:activity:7399939023072358401/] [archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt]
- **ES가 주류가 아니었던 이유**: ES는 “너무 비싸고, 너무 느리고, 스케일링이 되지 않았다”는 설명을 제시. [https://www.linkedin.com/feed/update/urn:li:activity:7399939023072358401/] [archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt]
- **핵심 아이디어 요약(저랭크)**: full-rank perturbation 대신 “두 개의 skinny 행렬 A와 B를 곱해 low-rank perturbation”을 만든다고 요약. [https://www.linkedin.com/feed/update/urn:li:activity:7399939023072358401/] [archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt]
- **(2차 주장) 평균 시 full-rank처럼 작동**: population 전체에서 low-rank 업데이트를 평균 내면 결과가 “full-rank ES 업데이트처럼 작동”한다고 강조. [https://www.linkedin.com/feed/update/urn:li:activity:7399939023072358401/] [archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt]
- **(2차 주장) 통신비용/대규모 population 수치**: “counter-based RNG”로 워커가 perturbation을 재현해 “통신 비용이 사실상 0”, population이 “262,144명”까지 확장 가능 등의 수치를 언급. *단, 이는 본 런에서 논문 PDF 본문이 없어 1차 검증 불가.* [https://www.linkedin.com/feed/update/urn:li:activity:7399939023072358401/] [archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt]

### C. 블로그 리뷰(한국어) — 2차 소스(논문 요약/해설)
- **요약 포지션**: EGGROLL이 “Backpropagation 방식이 아닌 ES를 거대 모델에 효과적으로 적용”하기 위한 방법이며, 기존 ES가 “거대한 노이즈 행렬 생성” 때문에 메모리/연산 비용 문제로 대형 모델에 적용이 어려웠다고 정리. [https://muni-dev.tistory.com/entry/Evolution-Strategies-at-the-Hyperscale] [archive/tavily_extract/0003_https_muni-dev.tistory.com_entry_Evolution-Strategies-at-the-Hyperscale.txt]
- **저랭크 아이디어를 LoRA와 연결**: 거대한 노이즈 행렬 \(E\)를 직접 만들지 않고 작은 행렬 \(A,B\)를 만들어 \(AB^T\)로 노이즈를 표현한다고 설명하며 LoRA 아이디어 차용으로 해설. [https://muni-dev.tistory.com/entry/Evolution-Strategies-at-the-Hyperscale] [archive/tavily_extract/0003_https_muni-dev.tistory.com_entry_Evolution-Strategies-at-the-Hyperscale.txt]
- **하드웨어 최적화 관점 설명**: \(AB^T\)를 명시적으로 만들기보다 입력 \(x\)에 대해 “(xB)A^T 순서로 연산 순서를 최적화”해 GPU에서 빠르고 메모리 효율적으로 계산되도록 설계했다고 소개. [https://muni-dev.tistory.com/entry/Evolution-Strategies-at-the-Hyperscale] [archive/tavily_extract/0003_https_muni-dev.tistory.com_entry_Evolution-Strategies-at-the-Hyperscale.txt]
- **이론 요약(O(1/r))**: 노이즈 분포의 대칭성 등으로 인해 수렴 속도가 “\(O(1/r)\)”로 빠르다고 해설. [https://muni-dev.tistory.com/entry/Evolution-Strategies-at-the-Hyperscale] [archive/tavily_extract/0003_https_muni-dev.tistory.com_entry_Evolution-Strategies-at-the-Hyperscale.txt]
- **(2차) 실험 디테일/수치**: LLM 추론 미세조정에서 “1,024개 생성 vs 32개” 등 탐색 병렬성 수치를 언급. *본 런에서는 논문 PDF 본문 미포함으로 1차 검증 불가(블로그 주장으로 취급 필요).* [https://muni-dev.tistory.com/entry/Evolution-Strategies-at-the-Hyperscale] [archive/tavily_extract/0003_https_muni-dev.tistory.com_entry_Evolution-Strategies-at-the-Hyperscale.txt]

---

## 2) 실행/수집 메타(범위·누락 확인용; 근거 인용은 ‘원문’ 대신 운영 로그로만 활용 권장)

### A. 수집 범위 고정(입력 URL 3개)
- 입력은 LinkedIn 1, arXiv 1, 블로그 1의 **3개 URL**로 구성됨. [archive/_job.json]
- 로그상 LinkedIn은 “LINKEDIN EMBED EXTRACT”, 나머지 2개는 “TAVILY EXTRACT”로 추출됨. [archive/_log.txt]

### B. 기존 산출물(초안) 점검 — 참고 수준
- 기존 `final.md`는 **영문**이며, 소스의 구체 문장 인용/“supported vs inferred” 라벨링이 약하고, 블로그에 없는 “community adoption/early implementations positive feedback” 등 **근거 불명 문장**이 포함됨(추출본 근거로 뒷받침 어려움). [archive/20260113_linkedin-review-final.md]