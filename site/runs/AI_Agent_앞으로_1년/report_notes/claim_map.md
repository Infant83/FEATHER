Claim | Evidence | Strength | Flags
--- | --- | --- | ---
`archive/openalex/works.jsonl` : 존재(LLM agent eval/benchmark, PdM, human-AI 협업, DevOps self-healing, RPA 테스트, personalized federated intelligence, multimodal AER 등 8 works) | (none) | none | no_evidence
`archive/tavily_search.jsonl` : 존재(한국어 트렌드/가이드/오케스트레이션/평가/관측성/유튜브 링크 등 다수) | (none) | none | no_evidence
`archive/arxiv/papers.jsonl` : **없음** | (none) | none | no_evidence
`archive/youtube/videos.jsonl` : **없음** | (none) | none | no_evidence
`archive/local/manifest.jsonl` : **없음** | (none) | none | no_evidence
보고서/지침 | (none) | none | no_evidence
`instruction/AI_Agent_앞으로_1년.txt` (포커스: *LLM agent orchestration, tool use, reliability, evals, security*) | (none) | none | no_evidence
`report.md` (베이스라인 보고서) | (none) | none | no_evidence
`archive/AI_Agent_앞으로_1년-index.md` (아카이브 요약/메타) | (none) | none | no_evidence
OpenAlex | (none) | none | no_evidence
PDFs 2개 + 추출 텍스트 2개 | (none) | none | no_evidence
`archive/openalex/pdf/W4412787296.pdf`, `archive/openalex/text/W4412787296.txt` | (none) | none | no_evidence
`archive/openalex/pdf/W4412877164.pdf`, `archive/openalex/text/W4412877164.txt` | (none) | none | no_evidence
Tavily | (none) | none | no_evidence
`archive/tavily_search.jsonl` (검색 결과 본문/요약 포함) | (none) | none | no_evidence
기타 | (none) | none | no_evidence
`archive/_job.json`, `archive/_log.txt` 등 실행 로그류 | (none) | none | no_evidence
**** *Evaluation and Benchmarking of LLM Agents: A Survey* (2025) — https://doi.org/10.1145/3711896.3736570 | OpenAlex; full text + PDF; https://doi.org/10.1145/3711896.3736570 | high | -
파일: `archive/openalex/text/W4412877164.txt`, `archive/openalex/pdf/W4412877164.pdf` | (none) | none | no_evidence
이유: “evals/reliability/safety”를 직접 다루는 **정리형 서베이**(베이스라인 보고서의 기술 포커스와 정합) | (none) | none | no_evidence
**** *AI Agent Orchestration Flows - Comet* — https://www.comet.com/site/blog/agent-orchestration/ | Tavily; https://www.comet.com/site/blog/agent-orchestration/ | low | -
이유: 실무 관점 orchestration 패턴/플로우(관측/실험 플랫폼 관점도 포함 가능성) | (none) | none | no_evidence
**** *ReliabilityBench: Evaluating LLM Agent Reliability Under Production ...* — https://arxiv.org/html/2601.06112v1 | Tavily; https://arxiv.org/html/2601.06112v1 | high | -
이유: “reliability under production”에 초점(운영 신뢰성 벤치마크/방법론 단서) | (none) | none | no_evidence
**** *Evaluating LLM Agents in Multi-Step Workflows (2026 Guide)* — https://www.codeant.ai/blogs/evaluate-llm-agentic-workflows | Tavily; https://www.codeant.ai/blogs/evaluate-llm-agentic-workflows | low | -
이유: 멀티스텝 워크플로우 평가(실무 체크리스트/메트릭/프로세스 관점 보완) | (none) | none | no_evidence
**** *Top 15 Amazing LLM Observability Tools to Catch Agent Failures ...* — https://www.linkedin.com/pulse/top-15-amazing-llm-observability-tools-catch-agent-failures-before-u5yzf | Tavily; https://www.linkedin.com/pulse/top-15-amazing-llm-observability-tools-catch-agent-failures-before-u5yzf | low | -
이유: agent failure 탐지/관측성 툴링(다만 LinkedIn 글이라 **홍보성/선별 필요**) | (none) | none | no_evidence
**** *AI-driven disinformation: policy recommendations for democratic resilience* (2025) — https://doi.org/10.3389/frai.2025.1569115 | OpenAlex; full text + PDF; https://doi.org/10.3389/frai.2025.1569115 | high | -
파일: `archive/openalex/text/W4412787296.txt`, `archive/openalex/pdf/W4412787296.pdf` | (none) | none | no_evidence
이유: “security”를 직접 다루진 않지만, **AI 악용/리스크 거버넌스** 축에서 참고 가능 | (none) | none | no_evidence
**** *Scaling Generative AI for Self-Healing DevOps Pipelines: Technical Analysis* (2025) — https://doi.org/10.20944/preprints202506.1436.v1 | OpenAlex; https://doi.org/10.20944/preprints202506.1436.v1 | high | -
이유: 멀티에이전트 오케스트레이션/거버넌스(블라스트 레디우스, 정책엔진 등) 언급 가능성이 높음(단, preprint 성격) | (none) | none | no_evidence
**** *A Unified Framework for Automated Testing of Robotic Process Automation Workflows...* (2025) — https://doi.org/10.3390/machines13060504 | OpenAlex; https://doi.org/10.3390/machines13060504 | high | -
이유: agent 테스트/검증을 “워크플로우 테스트” 관점으로 확장할 때 아이디어 소스(직접 LLM agent는 아님) | (none) | none | no_evidence
Predictive maintenance, 금융권 human-AI 협업, 감정조절 AER, personalized federated intelligence 등: “AI 에이전트” 일반론에는 도움 되지만, 지침의 핵심축(orchestration/tool use/reliability/evals/security)과는 거리가 있어 후순위. | (none) | none | no_evidence
**선정 이유:** 평가/벤치마킹 taxonomy, reliability·safety·enterprise challenges를 한 번에 커버하는 “기준 문서”. | (none) | none | no_evidence
**선정 이유:** 텍스트 추출본에서 누락될 수 있는 표/그림/정의/분류체계를 확인. | (none) | none | no_evidence
**선정 이유:** “운영 환경 신뢰성”을 벤치마크로 다루는 경우가 드물어, next-12-month 대비 항목으로 유용. | (none) | none | no_evidence
**선정 이유:** orchestration 흐름/패턴을 실무적으로 정리했을 가능성이 높아, 기술 로드맵/아키텍처 섹션에 바로 사용 가능. | (none) | none | no_evidence
**선정 이유:** 학술 서베이(1번)를 **프로덕션 평가 프로세스**로 번역하는 데 도움. | (none) | none | no_evidence
**선정 이유:** 보안/안전(safety)과 연결되는 “악용·사회적 리스크” 프레이밍과 정책 권고를 확보. | (none) | none | no_evidence
**선정 이유:** 사례/권고사항 디테일(표/박스)을 확인해 거버넌스 섹션을 탄탄하게. | (none) | none | no_evidence
**선정 이유:** observability 툴 맵을 빠르게 훑어볼 때 유용. 단, **마케팅성 리스트**이므로 핵심 도구만 추려 사용. | (none) | none | no_evidence
**선정 이유:** 현재 수집된 OA 작업의 전체 범위/메타(연도, 인용, PDF 링크)를 재확인해 빈 구간(보안/agent tool-use 안전 등) 파악. | (none) | none | no_evidence
**선정 이유:** 웹 소스 후보들의 원문/요약이 들어 있어 “추가 읽을 URL”을 선별하기 좋음(특히 orchestration/evals/observability). | (none) | none | no_evidence
**선정 이유:** 최종 산출물이 흔들리지 않게 **포커스 키워드**를 계속 기준점으로 삼기 위해. | (none) | none | no_evidence
**선정 이유:** 현재 보고서가 어떤 주장/출처 구조를 이미 갖고 있는지 확인 후, 부족한 근거(특히 reliability/evals/security의 직접 근거)를 위 소스로 보강. | (none) | none | no_evidence
**Phase 1 (기준 잡기):** 11 → 1(+2) | (none) | none | no_evidence
**Phase 2 (프로덕션 신뢰성/평가 구체화):** 3 → 5 → 4 | (none) | none | no_evidence
**Phase 3 (보안/거버넌스 리스크 축 보강):** 6(+7) | (none) | none | no_evidence
**Phase 4 (툴링/시장 맵 & 공백 점검):** 10 → 8 → 9 → 12 | (none) | none | no_evidence