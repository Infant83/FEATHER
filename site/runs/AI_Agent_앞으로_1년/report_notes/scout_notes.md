아카이브 인벤토리(구조화)

1) 핵심 1차·2차 근거(우선 검토 대상)
- OpenAlex 텍스트(로컬)
  - ./archive/openalex/text/W4412877164.txt — “Evaluation and Benchmarking of LLM Agents: A Survey” (KDD’25, DOI: https://doi.org/10.1145/3711896.3736570)
  - ./archive/openalex/text/W4412787296.txt — “AI-driven disinformation: policy recommendations for democratic resilience” (Frontiers in AI’25, DOI: https://doi.org/10.3389/frai.2025.1569115)
- OpenAlex PDF(참고)
  - ./archive/openalex/pdf/W4412877164.pdf — 위 KDD’25 논문 PDF
  - ./archive/openalex/pdf/W4412787296.pdf — 위 Frontiers 논문 PDF

2) 웹/블로그·산업 리소스(보조 근거)
- Orchestration/Tooling/Evals
  - AI Agent Orchestration Flows — Comet (https://www.comet.com/site/blog/agent-orchestration/)
  - ReliabilityBench: Evaluating LLM Agent Reliability Under Production … (arXiv HTML, https://arxiv.org/html/2601.06112v1)
  - Evaluating LLM Agents in Multi-Step Workflows — CodeAnt (https://www.codeant.ai/blogs/evaluate-llm-agentic-workflows)
  - 9 Best LLM Orchestration Frameworks — ZenML (https://www.zenml.io/blog/best-llm-orchestration-frameworks)
  - Top 15 Amazing LLM Observability Tools … — LinkedIn (https://www.linkedin.com/pulse/top-15-amazing-llm-observability-tools-catch-agent-failures-before-u5yzf) [홍보성 가능성]
- 동향/맥락(국문 위주, 보조)
  - IBM Think: “2025년 AI 에이전트: 기대치 vs. 현실” (https://www.ibm.com/kr-ko/think/insights/ai-agents-2025-expectations-vs-reality) [홍보성 가능성]
  - Samsung SDS: “버티컬 AI 에이전트 …” (https://www.samsungsds.com/kr/insights/vertical-ai-agents-part1.html) [홍보성 가능성]
  - Dfinite: “AI agent 종합 가이드 …” (https://blog.dfinite.ai/ai-agent-enterprise-guide) [홍보성 가능성]
  - GeekNews/브런치/행사 페이지(국문 트렌드 맥락, 선택적)

3) 내부 지시·산출물(작성 기준 정합)
- 지시 파일: ./instruction/AI_Agent_앞으로_1년.txt
- 베이스라인 리포트: ./report.md
- 인덱스/메타(커버리지 파악용, 본문 인용 제외)
  - ./archive/AI_Agent_앞으로_1년-index.md
  - ./archive/tavily_search.jsonl
  - ./archive/openalex/works.jsonl
  - ./report_notes/source_index.jsonl
  - ./report_notes/source_triage.md

4) 커버리지 한계(증거 공백)
- arXiv JSONL 부재: arXiv 원문 로컬 메타/텍스트 아카이브가 없어 HTML 원문(외부 링크)로 대체 확인. 공개정보 한계: 로컬 보존·버전 동결 미보장.
- YouTube 원문 아카이브 부재: 영상 원문·자막의 로컬 사본 없음. 공개정보 한계로 2차 요약에 의존.
- 1차 보안/침해 시연 자료 제약: 에이전트 보안 실증(공격/방어) 1차 데이터 부재. 산업 블로그·홍보성 글 비중 증가.


우선 읽기 목록(최대 12) + 선정 이유

1) Evaluation and Benchmarking of LLM Agents: A Survey (OpenAlex 텍스트)
- 경로/식별: ./archive/openalex/text/W4412877164.txt, DOI
- 이유: 에이전트 평가·신뢰성·안전의 체계적 분류와 엔터프라이즈 요구(신뢰보장·컴플라이언스)를 직접 다룸. 본 보고서의 “evals/reliability” 정의·프레임 설계의 근간.

2) ReliabilityBench: Evaluating LLM Agent Reliability Under Production … (arXiv HTML)
- 링크: https://arxiv.org/html/2601.06112v1
- 이유: 반복성/강건성/장애 허용 등 “프로덕션 신뢰성”을 계량화하는 개념(신뢰성 표면, fault injection 등) 제공. 오퍼레이션 관점의 지표·벤치 설계 근거.
- 주석: 공개정보 한계(로컬 보존 없음).

3) AI Agent Orchestration Flows — Comet
- 링크: https://www.comet.com/site/blog/agent-orchestration/
- 이유: “LLM이 제어 흐름을 결정하면 그게 에이전트”라는 실무적 오케스트레이션 정의와 트레이싱/테레메트리/드리프트 탐지 권고가 명확. 운영(Observability) 섹션의 실무 예시로 적합.
- 주석: 블로그 출처. 홍보성 가능성 있음.

4) Evaluating LLM Agents in Multi-Step Workflows — CodeAnt
- 링크: https://www.codeant.ai/blogs/evaluate-llm-agentic-workflows
- 이유: Tool selection/parameter correctness/효율 등 “툴 사용 평가” 체크리스트가 실무에 바로 쓰일 수준. 내부 평가 절차·메트릭 템플릿화에 유용.
- 주석: 블로그 출처. 홍보성 가능성.

5) 9 Best LLM Orchestration Frameworks — ZenML
- 링크: https://www.zenml.io/blog/best-llm-orchestration-frameworks
- 이유: 프레임워크 지형도(워크플로 그래프·체크포인트·오픈텔레메트리·A2A/MCP 등) 파악. 도구 선정·거버넌스 통합 포인트 정리.
- 주석: 블로그 출처. 홍보성 가능성.

6) Top 15 Amazing LLM Observability Tools … — LinkedIn
- 링크: https://www.linkedin.com/pulse/top-15-amazing-llm-observability-tools-catch-agent-failures-before-u5yzf
- 이유: 트레이싱/루트코즈 클러스터링/실시간 경보 등 에이전트 관측성 도구 목록과 기능 비교. 운영 체계·도구 도입 체크리스트에 활용.
- 주석: LinkedIn. 홍보성 가능성: 높음. 참고용 보조 근거로 제한.

7) AI-driven disinformation … — Frontiers in AI (OpenAlex 텍스트)
- 경로/식별: ./archive/openalex/text/W4412787296.txt, DOI
- 이유: 보안·거버넌스 장에서 “생성형 도구의 악용/정보 무결성 리스크”를 다루는 외연 근거. 조직 정책·감사 요구사항의 맥락 제공.

8) 내부 지시 파일 — 보고서 요구사항 재확인
- 경로: ./instruction/AI_Agent_앞으로_1년.txt
- 이유: 문체·라벨(관찰/추정/권고)·섹션 필수 요건 준수 점검. 산출물 일관성 확보.

9) 베이스라인 리포트 — 기존 주장/인용 점검
- 경로: ./report.md
- 이유: 기존 근거 연결·중복 제거·업데이트 포인트 식별. 최종 리포트 편집 동선 최적화.

10) 인덱스/트리아지 — 커버리지 확인(인용 금지)
- 경로: ./archive/AI_Agent_앞으로_1년-index.md, ./report_notes/source_triage.md
- 이유: 누락 소스/중복 파악, 읽기 우선순위 보정. 본문 인용은 금지.

11) Samsung SDS: Vertical AI Agents (국문)
- 링크: https://www.samsungsds.com/kr/insights/vertical-ai-agents-part1.html
- 이유: 국내 독자 대상 “버티컬/산업 적용” 서술 레퍼런스. 조직 변화/역량 측면 서술에 보조 인용 가능.
- 주석: 기업 콘텐츠. 홍보성 가능성.

12) IBM Think: 2025년 AI 에이전트 — 기대 vs 현실
- 링크: https://www.ibm.com/kr-ko/think/insights/ai-agents-2025-expectations-vs-reality
- 이유: 경영진 관점의 도입 포인트·ROI 논의 보완. “트렌드 스캔” 서두 메시지(앱→운영 워크플로우 전환)에 보조 인용.
- 주석: 기업 콘텐츠. 홍보성 가능성.


읽기·작성 운영 메모

- 포커스 엄수: LLM agent orchestration, tool use, reliability, evals, security에 직접 관련된 소스만 본문에 인용. 산업/동향 글은 보조 근거로 제한하고 “홍보성 가능성” 주석 표기.
- 증거 라벨링: 각 주장에 (관찰/추정/권고) 라벨 부여. 관찰은 상기 1차·2차 근거에서 직접 인용, 추정은 합리적 일반화, 권고는 조직·거버넌스 실행항목으로 단문화.
- 가이드라인 반영: “에이전트=앱”이 아니라 “에이전트=운영되는 워크플로우” 전환을 트렌드 스캔의 핵심 메시지로 명시. 오케스트레이션·에이전트 평가의 실무적 정의를 제시.
- 한계 명시(필수): arXiv JSONL·YouTube 로컬 아카이브 부재, 1차 보안 실증자료 제약은 “공개정보 한계”로 본문 ‘위험 및 결핍’ 섹션에 명기.


빠른 작성 순서 제안

- 1차 근거 정리: (1) Mohammadi et al. KDD’25, (2) ReliabilityBench HTML
- 오케스트레이션·관측성: Comet, ZenML, LinkedIn(주석)
- 툴 사용·평가 메트릭: CodeAnt
- 보안·리스크 맥락: Frontiers disinformation(필요 부분 최소 인용)
- 내부 지시·베이스라인 동기화 후 본문 작성 및 인용 삽입

끝.