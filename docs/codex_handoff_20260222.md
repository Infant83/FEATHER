# Codex Unified Handoff - 2026-02-22

Last updated: 2026-02-22 16:35:46 +09:00  
Source set: `docs/codex_handoff_20260220.md`, `docs/run_site_publish_strategy.md`, `docs/federnett_roadmap.md`, `docs/federnett_remaining_tasks.md`, `docs/federhav_deepagent_transition_plan.md`, `docs/ppt_writer_strategy.md`, `docs/capability_governance_plan.md`, `docs/artwork_agent_and_deepagents_0_4_plan.md`, `docs/federlicht_report.md`, `docs/playwright_mcp_troubleshooting.md`

## 1) 목적
- 기존 문서의 상태를 하나로 통합해, 앞으로 이 문서를 단일 기준으로 업데이트한다.
- 항목을 `DONE / TODO / 결정 필요`로 고정하고 문서 간 정책 충돌을 추적한다.

## 2) 현재 적용도 요약
- Federlicht 보고서 파이프라인: **고도화 진행 중 (부분완료)**
- Federnett 실행/운영 UI: **핵심 기능 완료 + UX 정리 잔여**
- FederHav deepagent 전환: **Phase A + Phase B-2(액션 handoff/preflight/trace) 반영, Phase B-3~D 미완**
- Run/Hub 분리 및 publish: **엔진 완료, 협업/승인 UI 미완**
- LLM 정책 일원화: **전역 정책 중심으로 완료**
- Playwright 검증체계: **로컬 스모크 안정, CI E2E 미완**
- PPT Writer 확장: **전략/설계 단계, 구현 착수 전**

## 3) DONE 리스트 (문서 교차확인 완료)
- Run root / site 분리 정책 운영 반영 (`runs,site/runs` + `site/report_hub`).
- Report Hub publish 모듈 구현 (`python -m federlicht.hub_publish`).
- Federnett Run Studio publish 버튼 + API 브릿지 구현.
- LLM Settings 전역 일원화(backend/model 정책 단일 진입점).
- Federlicht prompt 경로 불일치(`site/runs` vs `runs`) 해결.
- Codex 모델명 정규화(대문자 토큰 이슈 완화).
- Live Logs/Workflow Studio 주요 가독성 개선 및 white theme 보정 반복 적용.
- Run Picker(Choose Run Folder) UI 안정화:
  - white theme 선택 상태 강조 복구(Selected badge + high-contrast active card).
  - workspace settings/리스트 겹침 현상 제거(모달 grid/overflow/z-index 보정).
  - 모달 반응형 정리(좁은 화면 footer/actions stacking).
- Run Picker 접근성/선택 인지성 2차 강화:
  - 선택 카드 `aria-selected=true` + left accent rail 고정.
  - white/black theme에서 active background 색 대비 재보정.
- Sidebar-Logs splitter 제거 및 2열 레이아웃 전환.
- Live Logs/Sidebar 높이 결합 완화:
  - control panel 최대높이/내부스크롤 적용(Logs 길이에 따른 불필요한 사이드 패널 확장 억제).
  - Live Logs idle 상태(대화 비어있는 경우) 높이 compact 규칙 추가.
- Live Logs 구조 개선 2차:
  - topbar non-sticky 동작 고정(스크롤 시 자연 이탈).
  - workflow strip을 대화 스레드 하단으로 이동해 Q/A 가시영역 확대.
  - composer 높이 상한/입력창 높이 상한 도입으로 thread 가시성 확대.
  - 소형 해상도(540w 포함) 수평 overflow 제거.
- Live Logs 구조 개선 3차:
  - idle 상태에서 workflow strip 자동 compact(높이 54px) 적용.
  - 1024/1280 폭에서 thread 높이 추가 확보(약 229~247px).
- Live Logs compact polishing 4차:
  - turn/process 로그 fold를 전면 1-line compact 카드로 통일(요약 접기/펼치기 유지).
  - 요약 라벨 길이 제한 + command 미리보기 축약으로 카드 줄바꿈/높이 낭비 감소.
- Live Logs compact polishing 5차:
  - 대화 turn 내부 배치 조정: 로그 브릿지 카드가 답변 블록 바깥을 가리지 않도록 assistant message 내부로 이동.
  - sources(근거확인) 다음에 process fold가 오도록 렌더 순서 정리.
  - 대화가 이미 존재할 때는 global log card를 별도 삽입하지 않도록 조건 변경(중복 스택/스크롤 혼잡 완화).
- Live Logs compact polishing 6차:
  - 실행 중 상태줄에 로그 위치 힌트 노출(`로그: 타임라인 + 로그 브릿지`) + tooltip 안내 추가.
  - composer 슬림화(입력창 최소높이 44px, 상태/도구행 밀도 축소, runtime fold pill 기본화).
  - white theme 대비 보정(텍스트/배경/워크플로우 노드 대비 강화, 과도한 밝은톤+밝은글자 조합 완화).
- Theme 기본값 정책 정리:
  - 최초 로드/저장값 미존재/legacy `default` 저장값 모두 `white`로 정규화.
  - Theme selector 기본 선택값도 `white`로 일치화.
- Live Logs interaction UX 7차:
  - 질문실행 버튼을 소형 아이콘형(arrow)으로 축소하고, 실행 중에는 spinner 기반 진행 표시로 전환.
  - Plan/Act 버튼을 질문창 우측 세로 스택으로 재배치(질문 입력 옆 1열 action rail).
  - FederHav runtime/log fold를 Live Logs에서 제거하고, Global LLM Settings 모달로 이관.
  - Workflow strip 헤더의 `Workflow Studio 열기` 버튼 제거, 상단 글로벌 버튼(`Workflow Studio`)으로 이동.
  - Workflow Pipeline을 composer 바로 아래 위치로 고정하고 패널 톤을 white/black 테마 기준으로 재정렬.
- Live Logs interaction UX 11차:
  - Plan/Act 버튼 잘림 이슈를 작업계획에 반영하고 action rail 폭/버튼 높이를 재조정해 클리핑을 해소.
  - `파일쓰기` 토글을 side action rail에서 입력창 foot로 이동해 버튼 영역 충돌을 제거.
- Popup 접근성/조작성 9차:
  - 주요 팝업 모달(`instruction/run-picker/model-policy/jobs/template/save-as/help/ask-action`)에 공통 드래그 이동(헤더 드래그) 적용.
  - popup instant panel(`workspace panel`, `workflow studio`)도 드래그 이동 가능하도록 통일.
  - 전역 `Esc` close 정책 적용(최상위 popup/panel 우선 닫기)으로 닫기 동작 일관화.
  - 모달 레이어(z-index)와 배경 불투명도 보강으로 뒤 프레임 텍스트 bleed/가독성 저하 완화.
- Workflow Studio Stage UX 개선 2차:
  - stage 선택 액션 추가(활성 stage로 맞춤, 선택 stage override 초기화).
  - stage context에 override 우선순위 고정 표기(`global settings → stage override → runtime temp`).
  - 기본값 상태 override는 저장에서 자동 제거(불필요한 stage override 잔여 최소화).
- GitLab Pages 기본 CI 파이프라인 추가(`.gitlab-ci.yml`).
- Capability registry/API/기본 런타임 가시화(Phase 1).
- FederHav action 과잉유도 완화(의도 기반 실행 가드 1차).
- FederHav 명시 실행의도(`작업하자/진행해/실행해`) 즉시 실행 경로 강화:
  - Live Logs 질문 처리 시 최근 제안 action 재사용 shortcut 추가(확인 질문 루프 방지).
  - Help-Agent safe action 추론의 실행의도 판별 확장(작업/진행 표현 인식).
  - 실행의도 질문 턴에서는 임시 `execution_mode=act` 승격(전역 Plan 유지)으로 확인 루프 완화.
- Feather run-folder nesting 버그 수정:
  - 기존 동작: `--output`이 이미 run 폴더여도 `output/query_id` 하위 run을 다시 생성.
  - 수정 동작: `archive + instruction`이 있는 기존 run 폴더를 출력으로 받으면 해당 폴더를 직접 갱신(중첩 생성 금지).
- DeepAgents 0.4 런타임 분기 준비(파이썬 버전 조건부 의존성 반영).

## 4) TODO 리스트 (우선순위)

### P0 (즉시)
- Report Hub 협업 UI 완성(comment/followup/link 실제 submit 흐름).
- 승인 워크플로우 UI 완성(초안 -> 검토 -> 발행 상태모델).
- Live Logs 최종 시각 polish(모바일/저해상도에서 카드 밀도·여백·시선흐름 미세 조정).
- Workflow Studio 고급 Stage 설정 최종 polish(초기 사용자용 설명/경고 문구 정제 + 오입력 가드 추가).
- 테마별 semantic chip 대비 점검 상시화(Run Studio/Workflow/Runtime warning chip 포함, white/black 우선).

### P1 (단기)
- FederHav DeepAgent Phase B-3 진행(LLM fallback 축소 + CLI 품질 회귀셋 + planner 계약 테스트 확장).
- 계정/권한 운영 문서화(root/admin/user, bootstrap, session revoke 정책).
- Agent profile ownership UI 명시화(built-in/private/org-shared).
- Stage 비용/시간 대시보드(run 단위 elapsed/token/cache 집계).
- Ad-hoc 규칙 축소 리팩터링(문구/토큰 하드코딩 기반 라우팅 제거 -> tool/state 기반 의사결정으로 이관).

### P2 (중기)
- Playwright E2E CI 고정(질문->제안->실행->결과 시나리오 자동화).
- PPT Writer Phase 1~2 구현(slide schema/contract + minimal renderer).
- Quality evaluator 도메인별 가중치 세분화(산업/의학/정책).
- 장문 deep quality timeout 저감(runtime budget/loop policy).

## 5) 정책 충돌/중복 지점

### 충돌 A: Run root 이원(`runs` + `site/runs`) vs 단일 root 지향
- 현상: 문서들은 점진 이관을 전제로 이원을 허용한다.
- 리스크: 경로 혼동, prompt/output 위치 불일치 재발 가능.
- 권고: 운영 기본값은 `runs` 단일로 고정하고 `site/runs`는 읽기 전용 호환 모드로 단계 축소.

### 충돌 B: FederHav read-only 기본(roadmap) vs Act 실행 허용(handoff)
- 현상: 로드맵 Phase 1은 read-only 기본, 최근 구현은 bounded Act 실행을 허용.
- 리스크: 권한 경계/감사 정책 불명확.
- 권고: 정책 문구를 "default=plan(read-only), act=bounded write scope"로 통일하고 UI/문서 동기화.

### 충돌 C: 승인 후 발행 원칙 vs 즉시 publish 버튼 제공
- 현상: 전략 문서는 승인 후 publish를 권장하지만 UI는 즉시 실행 버튼 중심.
- 리스크: 검토 없는 게시.
- 권고: publish 버튼 앞에 승인 상태 체크 또는 확인단계(Review Gate) 추가.

### 충돌 D: 설정 일원화 목표 vs 일부 패널의 잔여 고급 설정
- 현상: LLM은 일원화됐지만 stage override/툴 매핑 등은 분산 체감.
- 리스크: 사용자가 어디서 무엇이 우선인지 혼동.
- 권고: 우선순위 체계를 고정 표기(global > stage override > runtime temp)하고 UI에 항상 노출.

### 충돌 E: 대화기록 저장 위치
- 현상: roadmap은 run 내 파일 저장을 명시, 현재는 scope/local 중심 흐름이 혼재.
- 리스크: 감사 추적/재현성 불일치.
- 권고: 최소한 실행 액션 관련 대화는 run artifact로 append 저장(옵션화 가능).

## 6) 결정 필요 항목 (Owner 지정 필요)
- 결정 1: Pages 배포 모델
  - 선택지: 단일 repo vs 이원 repo(product + hub-publish).
  - 권고: 이원 repo.
- 결정 2: run 산출물 git 추적 정책
  - 선택지: 기본 ignore vs 샘플 run 선별 추적.
  - 권고: 기본 ignore + 샘플/검증 run만 추적.
- 결정 3: Run root 장기 정책
  - 선택지: 이원 유지 vs `runs` 단일화.
  - 권고: `runs` 단일화 로드맵 명시(읽기 호환 기간 포함).
- 결정 4: FederHav 실행 권한 기본값
  - 선택지: 항상 read-only vs Plan 기본 + Act 승인 실행.
  - 권고: Plan 기본 + Act 승인 실행.

## 7) 다음 개발 사이클 권장 순서
1. Report Hub 승인/협업 UI를 먼저 완성해 publish 안전성 확보.
2. FederHav DeepAgent Phase B를 착수해 구조적 실행 일관성 확보.
3. Playwright E2E CI를 고정해 회귀 자동검증 체계 확보.
4. PPT Writer Phase 1 계약(schema/AST)부터 구현 착수.

## 8) 운영 규칙 (앞으로 이 파일 기준)
- 모든 작업 후 이 파일의 `DONE/TODO/결정 필요`를 먼저 갱신한다.
- `Last updated`는 반드시 절대시간으로 기록한다.
- 기존 `docs/codex_handoff_20260220.md`는 상세 로그 아카이브로 유지하고, 상태 기준은 본 파일을 우선한다.

## 8.1) Ad-hoc 정리 백로그 (우선 제거 대상)
- `src/federnett/help_agent.py`
  - `_extract_run_hint(...)`: 긴 정규식/토큰 기반 run 추론 규칙이 과도하여 오탐 가능.
  - `_is_invalid_run_hint(...)`: blocklist 중심 판별 규칙(언어/표현 변화에 취약).
  - `_needs_agentic_action_planning(...)`: 키워드 기반 trigger 분기가 많아 유지보수 비용 증가.
  - `_infer_safe_action(...)`: 규칙 분기 규모가 커서 deepagent 경로와 이중 정책이 생김.
- 개선 목표:
  - 질문 의도 판별은 `state_memory + run_context + tool_result` 기반으로 우선.
  - 규칙은 최소한의 안전 가드(파괴적 동작 차단, 경로 범위 제한)만 유지.
  - 실행 제안은 deepagent planner 결과를 기본으로 하고, safe-rule fallback은 완전 opt-in 유지.

## 9) 최근 Iteration 기록 (2026-02-22)
- 작업 초점:
  - Run Picker 모달 품질 복구(선택 인지성/겹침/테마별 대비)
  - Live Logs 가시영역 확대(대화 스레드 우선) + topbar 스크롤 동작 확정
- 적용 파일:
  - `site/federnett/app.css`
  - `site/federnett/app.js`
  - `site/federnett/index.html`
- 검증:
  - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `57 passed`
  - `node --check site/federnett/app.js` -> passed
  - Playwright audits:
    - `test-results/run-picker-modal-ui-audit-20260222-v2.json`
      - white overlap=False, black overlap=False
      - badge contrast: white 5.62 / black 6.73
    - `test-results/modal-layout-audit-20260222.json` (page_errors=0)
    - `test-results/layout-balance-audit-20260222-v2.json`
    - `test-results/ui-iter2e-audit-20260222.json`
      - topbar non-sticky=true, run-picker overlap=false(white/black/default)
      - responsive overflow=false at `1280x800`, `1024x768`, `768x1024`, `540x960`
      - thread height: 200.95px(1280x800), 182.95px(1024x768), 415px(768x1024), 252.95px(540x960)
    - `test-results/ui-iter2d-layout-20260222.json` (composer cap + mobile overflow 회귀 확인)
    - `test-results/ui-popup-audit-20260222.json`
      - workspace/instruction/run-picker/model/help 팝업 모두 viewport 내 가시영역 확인
      - page_errors=0
    - `test-results/ui-iter3-audit-20260222.json`
      - workflow strip idle compact=true (all tested viewports)
      - responsive thread height: 246.95px(1280x800), 228.95px(1024x768), 461px(768x1024), 326.95px(540x960)
      - topbar non-sticky=true, run-picker overlap=false(white/black/default), page_errors=0
    - `test-results/ui-iter4-audit-20260222.json`
      - workflow studio open + stage action buttons visible=true
      - live logs order: `mainOrder=1`, `workflowOrder=2` 유지
      - compact process style: `summaryMinHeight=20px`, `white-space=nowrap`, `text-overflow=ellipsis`
      - page_errors=0
    - `test-results/ui-iter4b-runpicker-20260222.json`
      - white theme run-picker selected card 강조 유지(background/border-left/title color 확인)
      - modal overlap probe ok=true
      - page_errors=0
    - `test-results/ui-iter5b-global-log-hide-20260222.json`
      - assistant_count=1 상태에서 global_log_card_count=0 확인
      - 대화 스택 존재 시 별도 global log card 비표시 정책 확인
      - page_errors=0
    - `test-results/ui-iter7-live-logs-20260222.json`
      - white theme 대비: message 15.28 / input 12.38 / workflow-node 11.63
      - scrollable container 수 1개(`workflow-track`)로 유지
      - `runtimeSummary=Runtime / Log`, `inputMinHeight=50px`, `page_errors=0`
    - `test-results/ui-iter7b-live-logs-20260222.json`
      - composer 추가 슬림화 확인: `composerHeight=175.09px`, `inputMinHeight=44px`, `inputMaxHeight=120px`
      - thread 높이 311.86px, `workflowHeight=54px`, `page_errors=0`
    - `test-results/ui-iter8-live-ask-layout-20260222.json`
      - run button size: `52x52` (소형 action button)
      - workflow button in strip=false, global workflow button=true
      - runtime fold in live ask=false, runtime control in modal=true
      - workflowBelowComposer=true, `page_errors=0`
    - `test-results/ui-iter8b-popup-consistency-20260222.json`
      - run-picker/model-policy/workspace-panel/workflow-studio open state 정상
      - modal/panel aria-hidden 전환 정상, `page_errors=0`
    - `test-results/ui-iter9-popup-escape-drag-20260222.json`
      - popup drag 이동 확인: run-picker/workspace-panel/workflow-studio 모두 `ok=true`
      - `Esc` 닫기 확인: run-picker/model-policy/workspace-panel/workflow-studio 모두 `true`
      - `page_errors=0`
- 추가 수정(11:09 KST):
  - `site/federnett/app.js`
    - 명시 실행 의도 감지 시 최근 제안 액션 즉시 실행 shortcut (`tryRunExplicitExecutionShortcut`) 추가.
    - 실행 가능한 최근 액션 탐색기(`latestExecutableLiveAskAction`) 추가.
  - `src/federnett/help_agent.py`
    - `_has_explicit_execution_intent` 추가 및 safe action 추론 경로에 공통 적용.
    - `작업하자/진행해` 계열이 실행 intent로 인식되도록 보강.
  - `tests/test_help_agent.py`
    - 실행의도 판별/후속 실행 추론 회귀 테스트 추가.
  - 검증:
    - `node --check site/federnett/app.js` -> passed
    - `pytest -q tests/test_help_agent.py tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `103 passed`
    - `test-results/ui-iter10b-live-ask-act-intent-20260222.json`
      - run button `38x38` compact=true
      - workflow_below_composer=true
      - page load ok=true (`http://127.0.0.1:8765`)
- 추가 수정(11:16 KST):
  - `site/federnett/app.css`
    - Live Logs composer 우측 액션 레일 폭 확장(`44px -> 58px`) + 질문창 폭 소폭 축소.
    - `Plan/Act` 버튼을 `width:100%` + ellipsis-safe로 고정해 잘림/클리핑 방지.
    - side action rail `overflow: visible`/`min-width` 보강으로 테마/배율 환경에서 버튼 텍스트 가시성 안정화.
  - 검증:
    - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `57 passed`
- 추가 수정(12:15 KST):
  - `site/federnett/index.html`
    - Workflow Studio > Pipeline 선택 영역에 `Quality Iterations (x1~x10)` 명시 설정 필드 추가(`wf-quality-iterations`).
  - `site/federnett/app.js`
    - Workflow Studio 품질 반복 설정 필드와 런타임 상태 동기화(quality stage 비활성 시 disabled/tooltip 처리).
    - `setWorkflowStudioOpen` 재호출 시 open 상태에서 drag offset을 불필요하게 초기화하지 않도록 보정(위치 튐 완화).
  - `site/federnett/app.css`
    - Workflow Studio 패널을 `position: fixed`로 전환해 Live Logs 프레임 클리핑 영향 제거.
    - viewport 기준 너비/높이 제한으로 drag 시 패널이 화면 기준으로 자연스럽게 이동하도록 보정.
  - 검증:
    - `node --check site/federnett/app.js` -> passed
    - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `57 passed`
- 추가 수정(12:25 KST):
  - `site/federnett/app.js`
    - Workflow Studio 패널을 body로 포털 이동해(Live Logs 내부 좌표 종속 완화) drag 시 위치 꼬임을 줄임.
    - Stage tool mapping 입력 정규화/오입력 가드 추가:
      - 쉼표/줄바꿈 분리, 소문자 정규화, 중복 제거, 토큰 형식 검사.
      - invalid token은 자동 제외하고 stage context 경고 배지로 노출.
    - Workflow Studio `Quality Iterations`를 quality stage OFF 상태에서도 미리 설정 가능하도록 완화(실행 중에만 비활성).
  - `site/federnett/app.css`
    - stage context warning 스타일(white/dark) 추가.
  - 검증:
    - `node --check site/federnett/app.js` -> passed
    - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `57 passed`
- 추가 수정(12:50 KST):
  - `site/federnett/app.js`
    - Live Logs/Ask 공통으로 명시 실행의도(`작업하자/진행해/실행해` 계열) 감지 시 해당 턴에 한해 `execution_mode`를 임시 `act`로 승격.
    - 최근 제안 action shortcut이 없더라도, 실행 의도 질문은 계획 확인 루프에 갇히지 않도록 실행 우선 경로를 강화.
    - 임시 `act` 승격 시 `allow_artifacts`도 동일 턴 기준으로 함께 계산해 실행 가능성 일관화.
  - `site/federnett/index.html`
    - 정적 자원 캐시 버전 `v44`로 상향(`app.css`, `app.js`)해 브라우저 캐시로 인한 구버전 UI/동작 잔존 방지.
  - 검증:
    - `node --check site/federnett/app.js` -> passed
    - `pytest -q tests/test_help_agent.py tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `103 passed`
- 추가 수정(12:59 KST):
  - `site/federnett/index.html`
    - `#live-ask-artifact-policy`를 side action rail에서 입력창 foot로 이동.
    - 정적 자원 캐시 버전 `v45`로 상향(`app.css`, `app.js`).
  - `site/federnett/app.css`
    - Live Ask action rail 폭을 `58px -> 68px`로 조정.
    - Plan/Act 버튼 높이를 `24px`로 통일하고 중앙 정렬로 잘림 방지.
    - run 버튼을 `40x40`으로 재조정하고 side-action gap/정렬을 보정.
  - 검증:
    - `node --check site/federnett/app.js` -> passed
    - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `57 passed`
    - `test-results/ui-iter11-plan-act-clip-20260222.json`
      - `plan_inside_side=true`, `act_inside_side=true`, `run_inside_side=true`
      - `plan_height=24`, `act_height=24`, `side_width=68`
- 추가 수정(13:15 KST):
  - 원인 분석:
    - `src/feather/collector.py`의 `build_job`이 항상 `root_dir = out_root / query_id`를 사용하여,
      Federnett가 전달한 run 폴더(`runs/<run_name>`) 아래에 동일 run명을 재생성하는 구조적 버그 확인.
    - 결과적으로 상위 run의 `archive`는 비고, 하위 중첩 run에 산출물이 기록되는 비정상 상태 발생.
  - 코드 수정:
    - `src/feather/collector.py`
      - `is_existing_run_folder(path)` 추가(`archive` + `instruction` 존재 시 run 폴더로 판별).
      - `build_job`에서 기존 run 폴더 출력은 `root_dir=out_root`로 처리하도록 변경(중첩 생성 차단).
    - `tests/test_collector.py`
      - 기존 run 폴더 출력에 대해 `root_dir == run_dir`, `out_dir == run_dir/archive`를 보장하는 회귀 테스트 추가.
  - 데이터 정비(실행 환경 보정):
    - `runs/양자컴퓨터_관련_자료_정리/양자컴퓨터_관련_자료_정리` 중첩 폴더를 상위 run으로 이관.
    - `runs/QC_ppt/QC_ppt` 중첩 폴더도 동일 방식으로 상위 run으로 이관.
    - archive 파일 이동 후 두 중첩 폴더 제거(`no_self_nested_runs` 확인).
  - 검증:
    - `pytest -q tests/test_collector.py` -> `12 passed`
    - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `57 passed`
    - `prepare_jobs(...)` 스모크 확인:
      - `root_dir = runs/양자컴퓨터_관련_자료_정리`
      - `out_dir = runs/양자컴퓨터_관련_자료_정리/archive`
    - Feather 실행 스모크(`--output runs/<run> --update-run`) 확인:
      - 중첩 폴더 미생성(`nested_removed_or_not_created`)
      - 산출물은 상위 run의 `archive`에 직접 기록
- 추가 수정(13:42 KST, Iter-1):
  - `site/federnett/app.js`
    - Live Logs 로그브릿지 fold 내부에 빠른 `접기` 버튼(상단/하단) 추가.
    - 긴 로그를 펼친 뒤 스크롤 하단에서도 즉시 fold close 가능하도록 이벤트 바인딩 추가(`data-process-fold-close`).
  - `site/federnett/app.css`
    - White theme `Recent Jobs` 모달 카드(`.job-item/.job-pill/.ghost`) 대비 보정.
    - Live Ask 액션 레일 1차 재조정(질문 실행/Plan/Act 비율 정리) + 로그브릿지 접기 버튼 스타일 추가.
  - 검증:
    - `node --check site/federnett/app.js` -> passed
    - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `57 passed`
    - `pytest -q tests/test_help_agent.py` -> `46 passed`
    - `test-results/ui-iter12-live-logs-jobs-audit-20260222.json`
      - run button `36x36`, plan/act `62x20`, tail close 동작 `true`
      - jobs modal white-theme card contrast 적용 확인
- 추가 수정(13:49 KST, Iter-2):
  - `site/federnett/app.css`
    - 질문 실행 버튼을 정사각형에서 가로형(`64x30`)으로 변경하고 Plan/Act(`64x20`)와 폭/비율 통일.
    - side action rail 폭을 `64px`로 미세 조정해 버튼 균형/가독성 향상.
  - `site/federnett/index.html`
    - 정적 자원 캐시 버전을 `v46`으로 상향해 브라우저에 최신 UI 패치가 즉시 반영되도록 조정.
  - 검증:
    - `node --check site/federnett/app.js` -> passed
    - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `57 passed`
    - `test-results/ui-iter13-live-logs-jobs-audit-20260222.json`
      - run button `64x30`, plan/act `64x20`, side rail `64px`
      - process fold tail close `true`, jobs modal white-theme contrast 유지
- 추가 수정(14:03 KST, Iter-3):
  - 요청 반영: Run Studio `Run Map` 하위 chip 대비 개선(white theme 기준 가독성 문제 해결).
  - `site/federnett/app.css`
    - `run-file-required/scope/tree`, `file-group-kind`의 white theme 전용 고대비 색상 팔레트 적용.
    - `file-group-title` white theme 텍스트 색 강화.
  - 검증:
    - `test-results/ui-iter14-runmap-contrast-white-20260222.json`
      - `Instruction: ok`, `Report: missing` 등 핵심 chip 대비 최소 `7.38` 확보.
      - pink/green 계열 배경+연한글자 조합 해소 확인.
- 추가 수정(14:08 KST, Iter-4):
  - 요청 확장 반영: 다른 패널 유사 이슈 동시 보정(Runtime/Workflow warning chip).
  - `site/federnett/app.css`
    - white theme 경고 chip 통일:
      - `.runtime-summary-pill.is-warning`
      - `.runtime-summary-chip.is-warning`
      - `.workflow-runtime-chip.is-warning`
      - `.ask-action-run-target-box.is-warning`
    - 경고 텍스트를 진한 amber tone으로 변경해 밝은 배경 대비 보장.
  - 검증:
    - `node --check site/federnett/app.js` -> passed
    - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `57 passed`
    - `test-results/ui-iter15-theme-contrast-runmap-runtime-20260222.json`
      - white theme: `minRunMap=7.38`, `minRuntime=7.90`
      - black theme: `minRunMap=11.76`, `minRuntime=12.13`
    - white/black 모두 경고/상태 chip 대비 기준 충족.
- 추가 수정(14:44 KST, Iter-5):
  - Run Studio file preview 버그 수정(필터 분기 재현/해결):
    - 원인: `renderRunFiles(...)`에서 `visibleGroups=0` 분기(파일 필터 적용 시)에서
      `button[data-file-open]` 클릭 바인딩이 누락되어 preview popup이 열리지 않음.
  - `site/federnett/app.js`
    - `bindRunFileOpenButtons()`, `bindRunFileDeleteButtons()`로 바인딩 루틴 정리.
    - `!visibleGroups` 분기에서도 `bindRunFileOpenButtons()` 호출하도록 보정.
  - 검증:
    - `node --check site/federnett/app.js` -> passed
    - `test-results/ui-iter17-preview-theme-after-fix.json`
      - `filtered_preview_open: true`
      - `filtered_preview_path: runs/QC_ppt/instruction/QC_ppt.txt`
    - `test-results/ui-iter17-preview-theme-after-fix.png`
- 추가 수정(14:58 KST, Iter-6):
  - FederHav run 파일 요약 정확도 개선(archive/youtube/videos.jsonl 질문 대응):
    - `.jsonl/.csv/.tsv` 텍스트 소스 허용.
    - run-context 수집에서 archive 경로를 질문 의도 기반으로 포함.
    - 질문 경로 힌트(`archive/...`, `*.jsonl`) 추출/매칭 로직 추가.
    - 파일/경로 컨텍스트 질문은 action-planning으로 우회하지 않고 직접 분석 응답 경로로 처리.
  - `src/federnett/help_agent.py`
    - `_extract_path_hints`, `_matches_path_hints`, `_is_file_context_question` 추가.
    - `_iter_run_context_files(..., question=...)`로 archive 조건부 포함.
    - `_score_run_context_sources`에 explicit path hint bonus 반영.
    - `_needs_agentic_action_planning`에서 file-context 질문 early-skip.
    - `_help_user_prompt`는 조건분기 없이 단일 규칙(경로 포함 질문 시 경로 우선 분석)을 유지.
  - `src/federhav/agentic_runtime.py`
    - governor prompt에 `read_run_file` 우선 사용 지침 추가(파일/경로 질문 시 finding-first 응답).
  - `tests/test_help_agent.py`
    - path-first 지침/의도 판별/action-planning 회피 테스트 추가.
    - run-context에서 `archive/youtube/videos.jsonl` 포함 회귀 테스트 추가.
    - explicit path hint 시 해당 archive 파일 우선 선택 테스트 추가.
    - `answer_help_question(..., run_rel=...)`가 archive 소스를 실제로 전달하는 테스트 추가.
  - 검증:
    - `pytest -q tests/test_help_agent.py -k \"archive or run_context or path_hint or question_asks or needs_agentic_action_planning or prompt_demands\"`
      -> `8 passed`
    - `pytest -q tests/test_federnett_routes.py -k \"preview or run_map or run_files or live\"` -> `2 passed`
    - `pytest -q tests/test_federnett_commands.py -k \"run or prompt or preview\"` -> `10 passed`
  - 후속 반영(15:02 KST):
    - `site/federnett/index.html` 정적 자원 캐시 버전 `v48`로 상향(`app.css/app.js`)해 브라우저 캐시로 인한 미반영 가능성 차단.
- 추가 수정(15:06 KST, Iter-7):
  - 사용자 피드백 반영: 문구 의존(if-then) ad-hoc 프롬프트 분기 제거.
  - `src/federnett/help_agent.py`
    - `_help_user_prompt`의 `content_summary_request/execution_rule` 조건분기 삭제.
    - 단일 규칙으로 일반화: 파일/경로 포함 질문은 경로 우선 분석.
    - `_question_asks_run_content_summary` 제거, `_is_file_context_question`으로 대체.
  - 검증:
    - `pytest -q tests/test_help_agent.py -k \"archive or run_context or path_hint or needs_agentic_action_planning\"` -> passed
    - `test-results/ui-iter18-preview-post-ad-hoc-removal.json`
      - `preview_open=true`, `preview_path=runs/QC_ppt/instruction/QC_ppt.txt`
      - white theme markdown preview (`md_bg=rgba(255,255,255,0.95)`) 유지 확인
- 추가 수정(15:16 KST, Iter-8):
  - 안정성 회귀검증(문구분기 제거 이후):
    - `pytest -q tests/test_help_agent.py` -> `52 passed`
    - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `57 passed`
    - `pytest -q tests/test_federhav_core.py tests/test_federhav_cli.py` -> `7 passed`
    - `node --check site/federnett/app.js` -> passed
- 추가 수정(15:28 KST, Iter-9):
  - `src/federnett/help_agent.py`
    - run-콘텐츠 요약 의도 감지기 추가:
      - `_has_run_content_path_reference(...)`
      - `_is_run_content_summary_request(...)`
    - 파일/폴더 해석 요청은 실행 액션 제안으로 승격되지 않도록 가드 추가:
      - `_infer_agentic_action(...)` early return
      - `_infer_governed_action(...)` early return
      - `_infer_safe_action(...)` early return
    - `_is_file_context_question(...)`를 path-hint 전용에서 folder/path 문맥까지 확장.
  - 의도:
    - `archive/youtube`, `archive 폴더` 같은 run 내부 자료 해석 요청에 대해
      Feather/Federlicht 실행 제안(run 생성 포함)이 뜨지 않도록 정책 고정.
- 추가 수정(15:31 KST, Iter-10):
  - `src/federnett/help_agent.py`
    - `run_rel` 누락 시 `state_memory.scope.run_rel` / `state_memory.run.run_rel`에서 자동 복구:
      - `_extract_run_rel_from_state_memory(...)`
      - `_effective_run_rel(...)`
    - `answer_help_question(...)`, `stream_help_question(...)`에서
      web research / source select / action inference 모두 `effective_run_rel` 사용.
  - 의도:
    - UI payload에서 run 값이 누락돼도 현재 선택 run 컨텍스트를 유지해
      archive 파일 질의가 코드 전역 소스로 새는 문제를 완화.
- 추가 수정(15:34 KST, Iter-11):
  - `src/federnett/help_agent.py`
    - `_extract_run_hint(...)` 강화:
      - `runs/<run>/archive/...`처럼 artifact 경로가 들어와도 run hint는 첫 세그먼트(run 이름)만 사용.
      - 중첩 경로 전체가 run 이름으로 오인되는 문제 방지.
  - 의도:
    - 과도한 run 힌트/액션 오탐을 줄여 "파일 해석 요청 -> 실행 제안"으로 튀는 확률 축소.
- 추가 수정(15:39 KST, Iter-12):
  - 테스트 추가/강화:
    - `tests/test_help_agent.py`
      - run-content summary 판별 테스트
      - folder-query(file path 미포함) 판별 테스트
      - safe/governed action이 run-content summary에서 `None`을 반환하는 회귀 테스트
      - nested artifact path run-hint trim 테스트
      - `state_memory` 기반 run_rel 복구 소스선택 테스트
  - 검증:
    - `python -m py_compile src/federnett/help_agent.py src/federnett/capabilities.py` -> passed
    - `pytest -q tests/test_help_agent.py tests/test_capabilities.py` -> `63 passed`
    - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py tests/test_federhav_core.py tests/test_federhav_cli.py` -> `64 passed`
    - `node --check site/federnett/app.js` -> passed
- 추가 수정(15:45 KST, Iter-13):
  - 정책 동작 스모크 확인(로컬):
    - `archive/youtube 의 videos.jsonl 을 정리해줘` -> suggested action `None`
    - `archive 폴더에 있는 파일들을 정리해서 알려줘` -> suggested action `None`
    - `archive/youtube 기반으로 feather 실행해줘` -> suggested action `run_feather`
  - 결론:
    - run 내부 파일 해석/요약 요청과 실행 요청의 경계를 분리해,
      FederHav가 불필요한 run 생성/Feather 실행으로 흐르는 현상을 1차 차단.
- 추가 수정(15:54 KST, Phase B Iter-1):
  - `src/federhav/agentic_runtime.py`
    - DeepAgent action planner 경로 추가:
      - `try_deepagent_action_plan(...)`
      - governor+executor subagent 조합으로 JSON action object 산출.
    - planner 보조 유틸 추가:
      - `_extract_first_json_object(...)`
      - `_build_action_planner_messages(...)`
      - `_capability_digest(...)`, `_normalize_history(...)`
  - 목적:
    - 답변 생성 경로뿐 아니라 실행 제안(action planning) 경로도 deepagent 런타임으로 승격 시작.
- 추가 수정(15:56 KST, Phase B Iter-2):
  - `src/federnett/help_agent.py`
    - `_try_agentic_runtime_action_plan(...)` 추가.
    - `_infer_agentic_action(...)`에서 deepagent planner를 우선 사용하고,
      실패/미사용 시 기존 LLM JSON planner로 fallback 유지.
  - 목적:
    - 기존 규칙/LLM planner를 완전 제거하지 않고 안전하게 점진 이관.
- 추가 수정(15:58 KST, Phase B Iter-3):
  - 정책 확인:
    - run-content summary 질문 early-guard(`_is_run_content_summary_request`) 유지.
    - deepagent planner 도입 후에도 파일요약 질의가 실행 제안으로 튀지 않도록 경계 유지.
- 추가 수정(16:00 KST, Phase B Iter-4):
  - 테스트 보강:
    - `tests/test_help_agent.py`
      - deepagent planner 우선 사용 테스트 추가.
      - deepagent planner 미응답 시 LLM planner fallback 테스트 추가.
  - 검증:
    - `pytest -q tests/test_help_agent.py tests/test_federhav_core.py tests/test_federhav_cli.py` -> `67 passed`
    - `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `57 passed`
    - `node --check site/federnett/app.js` -> passed
- 추가 수정(16:02 KST, Phase B Iter-5):
  - Phase B 진행도/추정:
    - 현재: **Phase B-1 완료** (governor+executor planner 연결 + fallback 이중화).
    - 다음 필요 작업(예상 3~5 iter):
      1) planner action confidence/intent rationale를 trace에 구조화 저장
      2) action execution preflight(run/instruction 확인)을 deepagent executor 도구로 이관
      3) safe-rule fallback 기본 off 고정 + emergency fallback 플래그 최소화
      4) planner->UI action preview 스키마 안정화(테스트/계약서화)
      5) federhav CLI(`chat --runtime-mode deepagent`)에서 action 제안 품질 회귀셋 추가
- 추가 수정(16:35 KST, Phase B-2 Complete):
  - `src/federhav/agentic_runtime.py`
    - action planner 스키마 확장: `confidence`, `intent_rationale`, `execution_handoff`.
    - `execution_preflight` deepagent tool 추가(런/인스트럭션 준비상태 검사).
    - planner 결과 정규화:
      - `_normalize_action_planner_payload(...)`
      - `_sanitize_execution_handoff(...)`
      - `_build_action_preflight(...)`
    - state-memory JSON 문자열 입력도 deepagent 메모리 툴에서 파싱하도록 보정.
  - `src/federnett/help_agent.py`
    - action 정규화에 planner 메타/신뢰도/intent rationale/handoff 스키마 반영.
    - trace에 `action_plan` 단계를 구조화(details 포함)로 저장.
    - stream 경로에서도 `action_plan` activity 이벤트 추가.
    - safe-rule fallback은 emergency opt-in(`FEDERNETT_HELP_RULE_FALLBACK=1|true|on|yes|emergency`)에서만 허용.
  - `site/federnett/app.js`
    - action preview에 planner meta + execution_handoff(preflight) 반영.
    - run-target 추론 시 planner preflight(`resolved_run_rel/run_hint`)를 우선 반영.
    - action preview schema를 실행 전 확인 데이터로 일관화.
  - 테스트:
    - `tests/test_help_agent.py`
      - deepagent handoff metadata 보존 회귀
      - answer trace의 `action_plan` structured details 회귀
      - emergency fallback opt-in 정책 회귀
  - 검증:
    - `python -m py_compile src/federhav/agentic_runtime.py src/federnett/help_agent.py tests/test_help_agent.py` -> passed
    - `node --check site/federnett/app.js` -> passed
    - `pytest -q tests/test_help_agent.py tests/test_federhav_core.py tests/test_federhav_cli.py tests/test_federnett_routes.py tests/test_federnett_commands.py` -> `127 passed`
- Phase B 진행도 갱신:
  - 현재: **Phase B-2 완료**
    - action proposal -> execution handoff 경로를 deepagent planner 중심으로 이관.
    - handoff preflight(run/instruction 확인) + trace 구조화 + UI preview 연계 완료.
  - 다음: **Phase B-3**
    1) rule fallback 제거/격리(운영 긴급 플래그 외 기본 경로 완전 차단)
    2) federhav CLI deepagent action 품질 회귀셋 확장
    3) planner/output 계약 테스트를 federnett route 계층까지 확장
