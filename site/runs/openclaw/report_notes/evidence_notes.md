아래는 주어진 런 폴더(./archive)에 있는 핵심 추출물들을 정독해 각 소스별로 보고서 작성에 쓸 만한 핵심 사실(사실·설정 스니펫·보안 쟁점)을 추출·정리한 결과입니다. 파일 우선순위·검증 상태는 스카우트 노트 계획을 반영했습니다. 각 문장 끝에 출처(원문 URL)와 읽은 로컬 추출파일 경로를 함께 표기했습니다.

1) 열람한 핵심 파일(요약)
- OpenClaw 공식 페이지(Quick Start · 기능 요약) — https://openclaw.ai/ [./archive/tavily_extract/0002_https_openclaw.ai.txt] (공식)  
- Dark Reading 보안 기사(기업 환경 리스크·‘lethal trifecta’ 등) — https://www.darkreading.com/application-security/openclaw-ai-runs-wild-business-environments [./archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt] (보안기사)  
- Dev.to 심층 가이드(아키텍처, gateway 포트·ws, config 예시, 보안 권장) — https://dev.to/czmilo/moltbot-the-ultimate-personal-ai-assistant-guide-for-2026-d4e [./archive/tavily_extract/0003_https_dev.to_czmilo_moltbot-the-ultimate-personal-ai-assistant-guide-for-2026-d4e.txt] (커뮤니티 가이드)  
- Twofootdog 한글 설치 튜토리얼(Windows/WSL, Gemini 연동, onboarding 워크플로) — https://twofootdog.tistory.com/555 [./archive/tavily_extract/0001_https_twofootdog.tistory.com_555.txt] (현장 튜토리얼)  
- Skywork.ai 기술보고(2차 요약/분석 — 일부 주장 교차검증 필요) — https://skywork.ai/skypage/en/moltbot-proactive-ai-assistants/2016342203473260544 [./archive/tavily_extract/0004_https_skywork.ai_skypage_en_moltbot-proactive-ai-assistants_2016342203473260544.txt] (2차 요약, 미검증 항목 존재)

2) 소스 유형별 핵심 추출 — 간결 불릿 (한국어, 원문명·출처는 유지)
- 공식 / 제품 페이지 (OpenClaw)
  - 설치/Quick Start 명령어(복제·온보드 스크립트): curl -fsSL https://openclaw.ai/install.sh | bash 및 npm i -g openclaw 그리고 openclaw onboard 같은 원-라이너·CLI 온보드 절차가 공식 안내에 포함되어 있다 (공식: https://openclaw.ai/ [./archive/tavily_extract/0002_https_openclaw.ai.txt]).  
  - 제품 주장(기능 요약): persistent memory(지속 메모리), browser control(브라우저 제어), full system access(파일 읽기/쓰기·셸 명령 실행), skills/plugins(확장 가능한 스킬), 다중 채널 통합(WhatsApp·Telegram 등)을 제품 핵심 기능으로 명시하고 있다 (공식: https://openclaw.ai/ [./archive/tavily_extract/0002_https_openclaw.ai.txt]).  
  - 배포·빌드 경로: Git 설치(소스 빌드) 안내(pnpm/pnpm run build)와 Companion App(macOS 릴리스) 링크가 포함되어 있다 (공식: https://openclaw.ai/ [./archive/tavily_extract/0002_https_openclaw.ai.txt]).  

- 커뮤니티/사용자 가이드 (Dev.to)
  - 아키텍처 요약: 중앙 제어면(Gateway)이 존재하고 웹소켓 기본 바인딩 주소/포트 예시로 ws://127.0.0.1:18789(또는 gateway --port 18789) 같은 설정이 문서화되어 있어 로컬 게이트웨이 + 에이전트(“Pi Agent”) 구조를 설명하고 있다 (커뮤니티: https://dev.to/.../moltbot-the-ultimate-personal-ai-assistant-guide-for-2026-d4e [./archive/tavily_extract/0003_https_dev.to_czmilo_moltbot-the-ultimate-personal-ai-assistant-guide-for-2026-d4e.txt]).  
  - 네트워크/접속 모드: Loopback(127.0.0.1), Tailscale Serve/Funnel, SSH 터널 등 원격 액세스 옵션을 제시하며, 보안 권고로 "포트 18789을 공용에 노출하지 말 것"을 강조한다 (커뮤니티: https://dev.to/... [./archive/tavily_extract/0003_https_dev.to_czmilo_moltbot-the-ultimate-personal-ai-assistant-guide-for-2026-d4e.txt]).  
  - 구성·샘플: ~/.clawdbot/moltbot.json 예시(agents.model 설정, channels.whatsapp.allowFrom 등)과 Node.js ≥ 22 요구사항, moltbot onboard 및 moltbot gateway 명령 예시가 포함되어 있어 재현 가능한 초기 설정 스니펫으로 활용 가능하다 (커뮤니티: https://dev.to/... [./archive/tavily_extract/0003_https_dev.to_czmilo_moltbot-the-ultimate-personal-ai-assistant-guide-for-2026-d4e.txt]).  
  - 보안 권장: DM pairing(미승인 송신자 차단), Docker sandbox 권장, allowlists·moltbot doctor 진단 사용 권고, "expose port 18789 하지 마라" 등 실무 권고가 명시되어 있다 (커뮤니티: https://dev.to/... [./archive/tavily_extract/0003_https_dev.to_czmilo_moltbot-the-ultimate-personal-ai-assistant-guide-for-2026-d4e.txt]).  

- 실전/현장 설치 가이드 (twofootdog.tistory.com, 한글)
  - Windows 용 설치 주의: WSL 또는 Git Bash/Cmder 사용 권장 및 Node ≥ 22 요구를 분명히 함으로써 Windows 환경에서의 재현 절차(명령어: npm i -g openclaw; openclaw onboard)를 단계별로 제공한다 (현장 튜토리얼: https://twofootdog.tistory.com/555 [./archive/tavily_extract/0001_https_twofootdog.tistory.com_555.txt]).  
  - 모델/API 연동 예시: Google Gemini API 키를 발급 받아 onboarding에서 Google → Gemini API key 방식으로 연결하는 절차(키 입력, 모델 선택 예: google/gemini-3-flash-preview)를 실습형으로 서술하고 있다 (현장 튜토리얼: https://twofootdog.tistory.com/555 [./archive/tavily_extract/0001_https_twofootdog.tistory.com_555.txt]).  
  - 온보드 훅(hooks) 예시: boot-md(부팅 시 Markdown 불러오기), command-logger(명령 기록), session-memory(세션 문맥 저장) 등 온보드에서 활성화 가능한 훅과 그 의미를 구체적으로 설명한다 — 이 항목은 실험적 환경설계(로그·메모리 항목 확보)에 유용하다 (현장 튜토리얼: https://twofootdog.tistory.com/555 [./archive/tavily_extract/0001_https_twofootdog.tistory.com_555.txt]).  

- 보안 기사 / 업계 분석 (Dark Reading)
  - 기업 환경 리스크 요지: OpenClaw(ClawdBot/MoltBot)은 이메일·파일·메시징·시스템 도구에 직접 연결되는 권한 모델을 갖고 있어 전통적 IAM·시크릿 관리 체계를 우회할 수 있으며, 터미널 실행·웹브라우징·파일쓰기도 가능하다고 분석된다 (보안기사: https://www.darkreading.com/.../openclaw-ai-runs-wild-business-environments [./archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt]).  
  - 탐지된 위협·사례: 보안업체(Pillar Security) 보고에 따라 기본 MoltBot 게이트웨이 포트(보고서 내 언급)가 스캔·공격 대상으로 관찰되었고, Token Security는 조직 내 약 22% 직원이 ClawdBot을 사용한다는 조사치를 인용해 섀도우 IT 리스크를 제기했다 (보안기사: https://www.darkreading.com/... [./archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt]).  
  - 공급망·vibe-coding 위험: Ox Security 보고서(요약 인용)에서는 vibe-coded(자동 생성/에이전트 보조) 풀 리퀘스트와 다수 기여자의 빠른 병합이 단일 악성 커밋으로 대규모 백도어·공급망 사건을 야기할 수 있음을 지적했다(공급망 리스크) (보안기사: https://www.darkreading.com/... [./archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt]).  
  - 'Lethal trifecta' 개념: 외부 untrusted 입력 + 민감 데이터 접근 + 외부 통신(즉, “데이터를 처리·전송·행동”하는 조합)이 위험을 극대화한다고 전문가들이 지적하고 있다 (보안기사: https://www.darkreading.com/... [./archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt]).  

- 2차 요약·분석 (Skywork.ai)
  - 종합적 해석: Moltbot을 “local-first, proactive agent”로 분류하고, 비용·운영 모델(월 $25–$95 추정), 성장·재브랜딩(Clawdbot→Moltbot)과 보안 사건들을 요약·정리하고 있다 — 다만 많은 수치·사례는 2차 출처를 조합한 것이므로 1차 자료(예: GitHub, Ox Security 리포트)로 교차검증이 필요하다 (2차 요약: https://skywork.ai/... [./archive/tavily_extract/0004_https_skywork.ai_skypage_en_moltbot-proactive-ai-assistants_2016342203473260544.txt]).  
  - 권고·전망: 로컬 에이전트의 확산과 함께 보안·운영 표준(네트워크 노출 통제·권한 최소화 등)을 조속히 마련해야 한다고 결론을 제시하고 있다(단, 일부 예측은 분석가 관점임) (2차 요약: https://skywork.ai/... [./archive/tavily_extract/0004_https_skywork.ai_skypage_en_moltbot-proactive-ai-assistants_2016342203473260544.txt]).  

3) 재현 가능한 설정·스니펫(보고서용 바로쓰기)
- 설치 명령(공식 Quick Start): curl -fsSL https://openclaw.ai/install.sh | bash; npm i -g openclaw; openclaw onboard — 온보드 마법사에서 모델·채널·hooks를 설정하도록 안내되어 있음 (공식: https://openclaw.ai/ [./archive/tavily_extract/0002_https_openclaw.ai.txt]).  
- Gateway 기본 바인딩/포트(실무상 주목): ws://127.0.0.1:18789 또는 moltbot gateway --port 18789 같은 로컬 웹소켓 게이트웨이 예시가 문서화되어 있어 네트워크 노출·방화벽 규칙에서 우선 확인해야 함 (커뮤니티: https://dev.to/... [./archive/tavily_extract/0003_https_dev.to_czmilo_moltbot-the-ultimate-personal-ai-assistant-guide-for-2026-d4e.txt]).  
- 샘플 구성(~/.clawdbot/moltbot.json 요약): agent.model(예: anthropic/claude-opus-4-5), channels.whatsapp.allowFrom, browser.enabled:true 등 재현 가능한 필드 예시가 제공됨 (커뮤니티: https://dev.to/... [./archive/tavily_extract/0003_https_dev.to_czmilo_moltbot-the-ultimate-personal-ai-assistant-guide-for-2026-d4e.txt]).  
- 온보드 훅(운영·감사 관련): boot-md(부팅시 마크다운 로드), command-logger(명령어 로그), session-memory(대화 세션 메모리) 활성화 추천 — 실험·감사 설계 시 반드시 체크할 항목(두깨씨 튜토리얼에 상세) (현장 튜토리얼: https://twofootdog.tistory.com/555 [./archive/tavily_extract/0001_https_twofootdog.tistory.com_555.txt]).  

4) 보안·거버넌스 관점에서 즉시 유의할 점 (증거 근거 포함)
- 기본 포트/노출 탐지: 게이트웨이 포트(보고상 18789)가 인터넷에서 스캔·공격 표적이 됐다는 보고가 있으므로 조직 네트워크에서의 탐지·차단이 필요하다 (Dark Reading 인용, Pillar Security 사례) (보안기사: https://www.darkreading.com/... [./archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt]).  
- 권한 최소화·샌드박스 기본화: 에이전트가 셸·파일·브라우저를 제어할 수 있으므로 기본 신뢰권한을 낮추고 그룹/비주류 채널은 도커·sandbox로 격리해야 한다(Dev.to 권고) (커뮤니티: https://dev.to/... [./archive/tavily_extract/0003_https_dev.to_czmilo_moltbot-the-ultimate-personal-ai-assistant-guide-for-2026-d4e.txt]).  
- 공급망·기여자 리스크: 빠른 턴오버·다수 기여 환경에서 단일 악성 커밋·악성 스킬이 대규모 확산을 초래할 수 있으므로 공개 스킬·PR은 별도审査(코드 리뷰·SBOM·서명) 필요(공급망 경고: Dark Reading → Ox Security 요지) (보안기사: https://www.darkreading.com/... [./archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt]).  
- 데이터 유출·프롬프트 인젝션 가능성: 에이전트가 외부 입력(이메일·웹페이지)을 처리하고 LLM에 전달하므로 prompt injection·비의도적 키·시크릿 노출 경로가 존재함(전문가 인용) (보안기사: https://www.darkreading.com/... [./archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt]).  

5) 교차검증 필요·미검증 항목(우선 수집 권장)
- Ox Security 원문(공급망 상세 분석) — Dark Reading이 요약 인용하므로 원문 확인 필요(미검증 상세: https://www.ox.security/... 원문 확인 권장) (미검증·교차검증 필요).  
- Token Security·Pillar Security 블로그/보고서 원문 — Dark Reading 인용 수치(예: 22% 사용 비율, 스캔 사례) 원문 확인 필요(미검증·교차검증 필요).  
- GitHub 소스코드(설정 스키마·gateway 구현·기본 auth) — 제품 주장(예: 포트·auth 기본값·auto-update 동작)을 정확히 문서화한 리포지토리 파일(예: gateway 코드, default config)을 직접 확인해야 함(미검증·교차검증 필요).  

6) 권장 다음 단계(간단)
- 우선순위: (1) 공식 openclaw.ai의 docs(세부 섹션: docs.openclaw.ai/getting-started, docs/openclaw gateway/security)와 GitHub 소스코드 → (2) Ox Security·Token Security 원문 보고서 → (3) Dev.to / twofootdog의 config 예시로 재현 스크립트 작성 → (4) Dark Reading의 보안 쟁점 근거 보강. (참고: 위 파일들은 현재 아카이브에 일부만 포함되어 있어 추가 수집 권장) (권장액션: 내부 메모).  

7) 부가메모(보고서 작성 시 표기 지침)
- 본 런의 공개자료는 주로 웹 문서·커뮤니티 가이드·보안 기사에 한정되어 있어 화학·재료 분야의 실증적 벤치마크·정량 성능 데이터는 부재함 — 보고서 본문에서 “공개정보 한계”로 명시할 것(스카우트 노트와 일치).  
- Skywork.ai 등 2차 요약의 단정적 수치·전망은 1차 근거로 교차검증 불가 시 “미검증”으로 표기할 것(출처 표기 필요).  

원하시면 지금 바로 (A) 공식 문서·Dev.to에서의 아키텍처·설정 스니펫을 정밀 발췌(문장별 인용 스니펫 포함)하거나, (B) Dark Reading·Ox Security 관련 보안 근거를 우선 정독해 'Risks & Gaps' 섹션용 인용을 준비하겠습니다. 어느 항목부터 진행할까요?