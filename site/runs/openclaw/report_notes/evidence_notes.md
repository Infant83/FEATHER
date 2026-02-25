현재 단계(파일 read budget 제한으로 추가 열람 불가)에서 **실제 원문 텍스트를 확인해 근거를 추출**할 수 있었던 소스는 `0002(openclaw.ai)`와 `0005(Dark Reading)` 2개뿐입니다. 따라서 아래 “핵심 사실(관찰)”은 **이 2개 소스에서만** 뽑았고, 나머지 3개(0001/0003/0004)는 이번 응답에서 근거 추출/인용을 하지 않습니다(원문 확인 불가).

---

## 1) 근거 기반 핵심 사실 추출 (관찰/명시된 내용만)

### A. OpenClaw(공식 사이트) — 제품/배치/기능(주장)
- OpenClaw는 “Personal AI Assistant”로 자신을 소개하며, “Clears your inbox, sends emails, manages your calendar, checks you in for flights” 같은 업무를 “WhatsApp, Telegram, or any chat app”을 통해 수행한다고 설명합니다. (https://openclaw.ai/ ; [/archive/tavily_extract/0002_https_openclaw.ai.txt])
- 설치/실행 방식으로 **CLI 설치(npm)** 및 **GitHub 리포지토리 클론 후 빌드(pnpm)** 경로를 제시합니다(예: `npm i -g openclaw`, `git clone https://github.com/openclaw/openclaw.git`). (https://openclaw.ai/ ; [/archive/tavily_extract/0002_https_openclaw.ai.txt])
- “Runs on Your Machine”을 전면에 내세우며, “Mac, Windows, or Linux… Private by default—your data stays yours.”라고 주장합니다. (https://openclaw.ai/ ; [/archive/tavily_extract/0002_https_openclaw.ai.txt])
- “Full System Access”로 **파일 읽기/쓰기, 쉘 커맨드 실행, 스크립트 실행**을 할 수 있다고 명시하면서 “Full access or sandboxed—your choice.”라고 옵션을 언급합니다. (https://openclaw.ai/ ; [/archive/tavily_extract/0002_https_openclaw.ai.txt])
- 기능 링크로 문서 도메인(`docs.openclaw.ai`)의 여러 항목을 노출합니다(예: getting-started, session, browser, bash, skills). 즉, 공식 사이트 자체 텍스트에서 **문서/기능 영역(세션/메모리, 브라우저, bash, skills)**을 제품 범위로 제시합니다. (https://openclaw.ai/ ; [/archive/tavily_extract/0002_https_openclaw.ai.txt])

### B. Dark Reading 기사 — 보안 우려/리스크(2차 + 인용 포함)
- Dark Reading은 OpenClaw를 “popular open source AI assistant”로 소개하며, “privileged, autonomous control within users' computers”에 대한 보안 우려가 제기된다고 서술합니다. (https://www.darkreading.com/application-security/openclaw-ai-runs-wild-business-environments ; [/archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt])
- 기사 본문은 Token Security의 평가를 인용해 OpenClaw가 **email/files/messaging platforms/system tools에 직접 연결**되며, 그 결과 **traditional IAM 및 secrets controls 밖에 놓이는 persistent non-human identities / access paths**를 만든다고 주장합니다. (https://www.darkreading.com/application-security/openclaw-ai-runs-wild-business-environments ; [/archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt])
- 같은 인용 구간에서 OpenClaw가 수행 가능한 행위로 **terminal commands 실행, scripts 실행, web browse, read/write files, control browsers, retain memory across sessions, proactively act on a user's behalf**가 열거됩니다. (https://www.darkreading.com/application-security/openclaw-ai-runs-wild-business-environments ; [/archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt])
- Dark Reading은 “bring-your-own-AI systems”가 로컬 애플리케이션 및 사용자의 채팅 채널에 privileged access를 갖는 것이 “significant security risks”를 동반한다고 일반화해 경고합니다. (https://www.darkreading.com/application-security/openclaw-ai-runs-wild-business-environments ; [/archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt])
- Pillar Security 경고를 인용/요약하며, 공격자가 “default MoltBot—now, OpenClaw—port”를 스캔하고 있다는 맥락을 언급합니다(단, 이번 스냅샷에서는 링크 URL이 본문 중간에서 잘려 있어 1차 원문 추적은 미완). (https://www.darkreading.com/application-security/openclaw-ai-runs-wild-business-environments ; [/archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt])

---

## 2) 의사결정(intent: decision) 기준에 직접 매핑되는 “근거 포인트”
(아래는 **근거가 있는 것만**)

- **로컬 실행/데이터 위치 주장(벤더 주장)**: “Runs on Your Machine”, “Private by default—your data stays yours.” (https://openclaw.ai/ ; [/archive/tavily_extract/0002_https_openclaw.ai.txt])
- **권한/툴 실행 범위(벤더 주장)**: 파일/쉘/스크립트 실행 + “Full access or sandboxed—your choice.” 옵션 존재 (https://openclaw.ai/ ; [/archive/tavily_extract/0002_https_openclaw.ai.txt])
- **IAM/Secrets 통제 리스크(2차 인용)**: “persistent non-human identities… outside traditional IAM and secrets controls”라는 위험 프레이밍 (https://www.darkreading.com/application-security/openclaw-ai-runs-wild-business-environments ; [/archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt])
- **지속 메모리/세션(리스크 연결고리)**: “retain memory across sessions” (Dark Reading 인용) + 공식 사이트의 “Persistent Memory” 기능 제시가 서로 맞물려, “지속성”이 핵심 특성임을 뒷받침 (https://openclaw.ai/ , https://www.darkreading.com/application-security/openclaw-ai-runs-wild-business-environments ; [/archive/tavily_extract/0002_https_openclaw.ai.txt] ; [/archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt])

---

## 3) 이번 단계의 한계(근거 관점)
- `docs.openclaw.ai` 및 `github.com/openclaw/openclaw` **원문(추출본/PDF)이 아카이브에 포함되어 있지 않아**, “sandboxed—your choice”가 의미하는 정확한 격리 수준, 토큰/시크릿 저장 위치, 감사로그/권한 프롬프트 정책 등은 **근거로 확정할 수 없습니다.** (https://openclaw.ai/ ; [/archive/tavily_extract/0002_https_openclaw.ai.txt])
- Dark Reading이 인용한 Token Security / Pillar Security의 **1차 출처 원문을 본 run에서 열람하지 못해**, 해당 주장(지속 non-human ID, 포트 스캔 등)을 **재인용/정량화**할 수는 없습니다(현 단계에선 “Dark Reading이 이렇게 인용했다”까지만 근거). (https://www.darkreading.com/application-security/openclaw-ai-runs-wild-business-environments ; [/archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt])

---

## Evidence Ledger (요약 표)

| Claim | Evidence summary | Source URL/path | Strength | Limits | Recency |
|---|---|---|---|---|---|
| OpenClaw는 채팅앱을 통해 이메일/캘린더 등 작업을 수행한다고 주장 | 랜딩에 “Clears your inbox… manages your calendar…” + “All from WhatsApp, Telegram…” 명시 | https://openclaw.ai/ ; [/archive/tavily_extract/0002_https_openclaw.ai.txt] | medium | 벤더 마케팅 주장, 검증/구현 세부 없음 | 2026-02-03 스냅샷(인덱스 날짜) |
| OpenClaw는 로컬 머신에서 동작하며 “Private by default”를 주장 | “Runs on Your Machine… Private by default—your data stays yours.” | https://openclaw.ai/ ; [/archive/tavily_extract/0002_https_openclaw.ai.txt] | medium | “data stays yours”의 범위/예외/텔레메트리 불명 | 동 |
| 파일/쉘/스크립트 실행 등 “Full system access”와 “sandboxed 옵션”을 언급 | “Read and write files, run shell commands, execute scripts… Full access or sandboxed—your choice.” | https://openclaw.ai/ ; [/archive/tavily_extract/0002_https_openclaw.ai.txt] | medium | 샌드박스 정의/경계/구현 근거(문서/코드) 부재 | 동 |
| OpenClaw가 IAM·secrets 통제 밖 persistent non-human identity/access path를 만든다는 우려(인용) | Dark Reading이 Token Security 평가를 따옴표로 인용 | https://www.darkreading.com/application-security/openclaw-ai-runs-wild-business-environments ; [/archive/tavily_extract/0005_…txt] | low~medium | 2차 기사 인용이며 1차 출처 원문 검증 불가 | 기사 2026-01-30 |
| OpenClaw가 다양한 강력 행위(터미널/파일/브라우저/세션 메모리/프로액티브)를 수행 가능하다는 우려(인용) | Dark Reading이 Token Security 인용으로 행위 목록 열거 | https://www.darkreading.com/application-security/openclaw-ai-runs-wild-business-environments ; [/archive/tavily_extract/0005_…txt] | low~medium | 2차 인용, 실제 제품 설정/권한 프롬프트/로깅은 미확인 | 2026-01-30 |

---