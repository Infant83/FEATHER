## 0) 범위/제약 확인(스카우트 단계)
- 목적: **아카이브 매핑 + 핵심 소스 파일 식별 + 우선 읽기(딥리드) 계획 제안**
- 제약 준수: 긴 문서 전체 읽기 금지, 필요 최소 범위만 확인
- 현재 상태: 아카이브는 **tavily_extract 5개 URL 스냅샷** 중심이며, 지정된 **메타데이터 JSONL 인덱스들(tavily_search/openalex/arxiv/youtube/local manifest)** 은 **이번 run 폴더에 존재하지 않음**(패턴 매칭 실패로 확인). 따라서 `archive/openclaw-index.md`가 사실상 1차 인덱스 역할.

---

## 1) 아카이브 인벤토리(구조화)
### A. 실행/인덱스/로그
1. `archive/openclaw-index.md` (946B)  
   - 본 run에서 수집된 URL 5개와 tavily_extract 파일 매핑 제공(핵심 인덱스).
2. `instruction/openclaw.txt`  
   - 수집 대상 URL 목록(5개)만 포함(스카우트용 입력).
3. `archive/_job.json` / `archive/_log.txt` / `archive/_feather_log.txt`  
   - 수집 작업 메타/로그(추가 소스 확장 시 참고).

### B. 본문 스냅샷(1차 소스 풀)
(모두 `archive/tavily_extract/*.txt` 형태, 각 파일은 JSON 구조 안에 `url/title/raw_content` 포함)
1. `archive/tavily_extract/0002_https_openclaw.ai.txt` (49KB)  
   - OpenClaw 공식 사이트 랜딩/기능/설치/문서 링크 요약(제품 주장·기능 범위).
2. `archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt` (17KB)  
   - Dark Reading 기사: “OpenClaw AI Runs Wild in Business Environments”(보안 이슈·리스크 내러티브).
3. `archive/tavily_extract/0001_https_twofootdog.tistory.com_555.txt` (11KB)  
   - 한국어 설치/연동 실습 가이드(로컬 설치 전제, Gemini 연동 등 운영 관점 단서).
4. `archive/tavily_extract/0003_https_dev.to_czmilo_moltbot-the-ultimate-personal-ai-assistant-guide-for-2026-d4e.txt` (77KB)  
   - Dev.to 장문 가이드(변경 전 명칭 MoltBot 관련, 기술/사용법 가능성 높음). *이번 단계에서 예산 한도로 헤더만 확인됨.*
5. `archive/tavily_extract/0004_https_skywork.ai_skypage_en_moltbot-proactive-ai-assistants_2016342203473260544.txt` (29KB)  
   - Skywork 페이지(요약/해설 성격 가능, 2차 컨텐츠일 확률). *이번 단계에서 내용 확인 실패(예산 한도).*

### C. 보고서 노트
- `report_notes/source_index.jsonl`: **빈 파일**(현재 인용 번호 체계/소스 등록이 안 된 상태)
- `report_notes/source_triage.md`: `(no sources ranked)` (트리아지 미수행)

---

## 2) 리포트 포커스(CTO/보안 리더 의사결정) 관점의 소스 적합도
의사결정 리포트에 필요한 축:
- **(1) 제품/아키텍처/권한 범위**: 무엇에 접근하고 무엇을 실행하는지(메일/파일/메신저/쉘/브라우저 등)
- **(2) 위협모델/공격면**: BYO-agent, 비인간 ID, IAM 밖의 지속 세션/메모리, 기본 포트 스캐닝 등
- **(3) 운영 통제 옵션**: 샌드박스, 권한 제한, 로깅/감사, 비밀관리, 네트워크 제어
- **(4) 도입 의사결정**: “허용/부분 허용/금지” 정책과 가드레일

현재 아카이브 내에서 (2)를 직접 다루는 건 **Dark Reading(0005)** 가 가장 강함. (1)은 **공식 사이트(0002)** 가 1차 근거. (3)은 공식 docs 링크로 추가 확장 필요(현 아카이브에는 docs 본문 스냅샷이 없음). (4)는 위 1~3 근거로 작성.

---

## 3) 우선순위 산정(읽기 계획: 최대 12개)
아래는 “스카우트 → 다음 단계(딥리드/인용 구축)”로 넘어갈 때의 **우선 읽기 목록**이며, 각 항목은 **인용 [n]으로 쓰기 적합한가** 기준으로 선정했습니다.

1) `archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt`  
- 이유: 보안 리스크/우려를 가장 직접적으로 정리한 기사. 위협모델 섹션의 핵심 근거 후보.

2) `archive/tavily_extract/0002_https_openclaw.ai.txt`  
- 이유: 제품이 주장하는 기능(“Runs on your machine”, “Full system access”, “Persistent memory”, “Any chat app”)을 1차 소스로 고정해야 함. “통제 옵션(샌드박스 선택)” 언급도 있어 정책 권고에 필요.

3) `archive/tavily_extract/0001_https_twofootdog.tistory.com_555.txt`  
- 이유: 한국어 운영/설치 맥락(Windows/WSL, Node 버전, API 키 등)으로 **실제 도입 마찰·현장 운영 포인트**를 보강 가능. (단, 2차 블로그이므로 사실 주장 인용은 신중)

4) `archive/tavily_extract/0003_https_dev.to_czmilo_moltbot-the-ultimate-personal-ai-assistant-guide-for-2026-d4e.txt`  
- 이유: 장문 가이드일 가능성이 높아 기능/설정/통합 지점(메일/캘린더/슬랙 등)과 위험을 체계적으로 정리했을 수 있음. 단, 2차 컨텐츠 → 교차검증 필요.

5) `archive/tavily_extract/0004_https_skywork.ai_skypage_en_moltbot-proactive-ai-assistants_2016342203473260544.txt`  
- 이유: “proactive assistants” 관점에서 요약/프레이밍 제공 가능. 다만 마케팅/재가공 위험이 있어 낮은 우선순위.

6) (아카이브 밖 확장 후보) `https://docs.openclaw.ai/getting-started` 및 하위: `/bash`, `/browser`, `/skills`, `/session`, `/integrations`  
- 이유: CTO/보안 리더 의사결정에는 **공식 문서의 권한 모델/보안 옵션/로깅/설계**가 필수. 현재 run에 미수집이므로, 다음 수집에서 최우선으로 추가해야 함.

7) (아카이브 밖 확장 후보) GitHub repo: `https://github.com/openclaw/openclaw` (특히 security, permissions, sandbox, telemetry 관련 문서/코드)  
- 이유: “오픈소스 에이전트” 리스크 판단은 repo의 기본 설정, 통신, 비밀/토큰 처리, 샌드박스 구현을 확인해야 함.

8) (아카이브 밖 확장 후보) Token Security / Pillar Security 언급 원문(0005에 간접 인용된 리서치/블로그)  
- 이유: Dark Reading이 인용한 “IAM/Secrets 통제 밖 지속 ID” 주장에 대해 1차 자료로 강화 필요.

> 참고: `report_notes/source_index.jsonl`가 비어 있어, 다음 단계에서는 위 1~5를 **[1]~[5] 인용 번호로 먼저 등록**하는 작업이 선행돼야 합니다(리포트 요구사항: 문장 끝 inline 인용).

---

## 4) “필수 섹션/비교표/다이어그램”을 위한 소스 커버리지 갭
- 비교표(최소 1개):  
  - 축 예시: **OpenClaw 도입 옵션(로컬/원격/샌드박스) vs 통제수단(IAM 연계, secrets, 네트워크, 로깅)**  
  - 근거는 (0002) 기능/옵션 + (0005) 리스크로 구성 가능하나, **공식 docs/repo 근거가 부족**.
- 다이어그램(mermaid):  
  - “사용자/채팅앱 ↔ OpenClaw(에이전트) ↔ 로컬 시스템(파일/쉘/브라우저) ↔ 외부 SaaS(메일/캘린더)” 데이터/권한 흐름 그림이 필요. (0002, 0005)로 초안 가능하지만 **세부 경계(샌드박스/권한 프롬프트/토큰 저장 위치)** 는 docs/repo로 보강 권장.

---

## 5) 다음 액션 제안(스카우트 종료 후)
1. `report_notes/source_index.jsonl`를 비어있는 상태에서 **최소 5개 소스(0001~0005)를 등록**(인용 번호 체계 확보).
2. 추가 수집(권장): OpenClaw 공식 docs 주요 페이지 + GitHub repo의 security/permissions 관련 문서.
3. 그 다음에만 딥리드: (0005)→(0002)→(docs)→(repo) 순으로, “주장-근거-통제” 체계를 세워 의사결정 리포트 본문 작성.

원하면, 제가 다음 단계에서 **소스 트리아지 템플릿(신뢰도/1차성/의사결정 기여도/인용 가능 문장 후보 필드)** 를 `report_notes/source_triage.md`에 맞춰 제안할 수 있습니다.