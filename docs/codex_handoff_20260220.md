# Codex Handoff - 2026-02-20 (Error-stop Recovery)

## 목적
- 긴 세션 진행 중 중단된 상태를 **새 Codex 대화에서 즉시 재개**할 수 있도록,
  - 현재까지 반영된 작업,
  - 검증 상태,
  - 미완/추가 TODO,
  - 다음 실행 순서
  를 한 문서로 정리한다.

---

## 1) 현재 진행 요약

### 1.1 FederHav agentic 전환 축
- `help_agent`가 deepagent 런타임을 우선 시도하고, 실패 시 백엔드 폴백을 적용하는 구조로 강화됨.
- safe-rule fallback은 기본 비활성(명시 opt-in)으로 변경됨.
- instruction 품질 가드(짧은/모호한 실행 요청에 대해 `auto_instruction` 부여)가 들어가 있음.

관련 파일:
- `src/federnett/help_agent.py`
- `src/federhav/agentic_runtime.py`
- `src/federhav/core.py`
- `src/federhav/cli.py`

핵심 포인트:
- `create_deep_agent` 기반 경로 사용
- planner/executor/quality subagent 개념 반영
- `/plan`, `/act`, `/profile`, `/agent`, `/runtime` 운영 명령 흐름 반영

### 1.2 Federnett Live Logs / Ask UI 개편 축
- Live Logs에 FederHav 타임라인 중심 구조를 유지하면서,
  - state-memory 기반 컨텍스트,
  - 보조 로그 요약 길이 정책,
  - 액션 실행 시 run-target 확인 UX
  가 반영됨.
- 액션에서 잘못된 run-target 문자열(예: `Run 전환: 대상에서/에서`)을 차단하는 정규화/검증 로직이 추가됨.
- Workflow pipeline에 `federhav` 노드가 포함됨.
- 테마에 `White`, `Black` 옵션이 추가됨.

관련 파일:
- `site/federnett/index.html`
- `site/federnett/app.js`
- `site/federnett/app.css`

### 1.3 인증/권한 및 프로필 제어 축
- 세션 인증 매니저 및 로그인 API 추가.
- root/admin 계열 세션에 대한 built-in profile 편집 권한 경로 추가.
- Root unlock UI와 session sign-in UI를 Agent Profiles 패널에 연결.

관련 파일:
- `src/federnett/auth.py`
- `src/federnett/routes.py`
- `src/federnett/agent_profiles.py`

### 1.4 Report Hub 연동 축
- report-hub post/comment/followup/link API 골격이 구현됨.
- 인증 세션이 있으면 write payload에 `signed_by`, `signed_role` 자동 스탬핑.

관련 파일:
- `src/federnett/report_hub.py`
- `src/federnett/routes.py`
- `site/report_hub/*`

---

## 2) 검증 스냅샷 (중단 직전 재확인)

### 2.1 테스트
실행 명령:

```bash
pytest -q tests/test_help_agent.py tests/test_federnett_routes.py tests/test_federnett_auth.py tests/test_report_hub_api.py tests/test_federhav_core.py tests/test_federhav_cli.py
```

결과:
- `89 passed` (약 2분 56초)

### 2.2 코드 규모(대략)
- `src/**/*.py`: 약 `31,265` lines
- `site/federnett/*.(js|css|html)`: 약 `27,273` lines
- `tests/**/*.py`: 약 `3,517` lines

### 2.3 워크트리 상태 주의
- 현재 워크트리는 변경 파일이 매우 많음(코드 + run 산출물 + 문서 + 생성 파일 포함).
- 새 세션에서 작업 재개 시 **불필요한 파일 정리 전략을 먼저 확정**해야 안전함.

### 2.4 2026-02-21 추가 검증
- 테스트 재실행:
  - `pytest -q tests/test_help_agent.py tests/test_federnett_routes.py tests/test_federnett_auth.py tests/test_report_hub_api.py tests/test_federhav_core.py tests/test_federhav_cli.py`
  - 결과: `88 passed` (약 3분 36초)
- Playwright 재현(로컬 서버 `http://127.0.0.1:53879/`):
  - 해상도: `1366x768 / 1920x1080 / 2560x1440`
  - Run Studio(`openclaw`, all view): section 4 / group 6 / item 18 확인
  - 계층 칩 overflow: 0건
  - workflow path overflow: 0건(경로 max-width 조정 후)
  - workflow node state 배지 렌더링: 노드 수와 동일(8/8)
- 추가 관찰:
  - 일부 과거 run의 누락 파일(`report_full_1.html`)로 preview 404 콘솔 로그가 남을 수 있음(기능 회귀는 아님).

### 2.5 2026-02-20 재검증 (Instruction Confirm Gate)
- 테스트:
  - `pytest -q tests/test_help_agent.py tests/test_federnett_routes.py tests/test_federnett_auth.py tests/test_report_hub_api.py tests/test_federhav_core.py tests/test_federhav_cli.py`
  - 결과: `88 passed` (약 3분 37초)
- Playwright (로컬 서버 `http://127.0.0.1:8767/`):
  - Action modal에서 `run_feather + require_instruction_confirm=true` payload 주입 케이스 검증
  - `run-target`/`instruction` 체크 전 `확인 후 실행` 버튼 disabled 유지 확인
  - 두 체크 완료 후 버튼 enabled 전환 확인
  - 해상도 `1366x768 / 1920x1080 / 2560x1440`에서 모달 영역/체크박스 렌더링 이상 없음
  - 브라우저 콘솔 error: `0`

### 2.6 2026-02-21 재검증 (Clarify + Governor Trace)
- 테스트:
  - `pytest -q tests/test_help_agent.py tests/test_federnett_routes.py`
  - 결과: `76 passed` (약 2분 55초)
- 추가 스모크:
  - `pytest -q tests/test_help_agent.py tests/test_federnett_routes.py tests/test_federnett_auth.py tests/test_report_hub_api.py tests/test_federhav_core.py tests/test_federhav_cli.py`
  - 결과: `89 passed` (약 2분 56초)
- Playwright (로컬 서버 `http://127.0.0.1:8767/`):
  - 입력 `실행해줘` 후 `질의 보강하기` 버튼 노출 확인
  - Follow-up prompt 자동 삽입 텍스트 확인:
    - `어떤 주제로 실행할까요? 예: '양자컴퓨터 최신 기술 동향을 분석해 보고서 작성해줘'`
  - Live Ask 작업 로그에 tool trace 메타 노출 확인:
    - `trace_id`, `tool_id`, `duration_ms`, `token_est`, `cache_hit`
  - 실행 메타 칩에 `trace=<id>`, `tools=<N>` 노출 확인
  - 브라우저 콘솔 error: `0`

---

## 3) 반영 완료/부분완료/미완 상태표

## 3.1 사용자 요구 대비 상태

1. Codex 모델 옵션 노출
- 상태: **부분완료**
- UI preset 목록 반영됨. 다만 최종 옵션 세트/라벨 정책 고정 필요.

2. 규칙 기반이 아닌 agentic 수행
- 상태: **부분완료**
- deepagent 우선 + rule fallback opt-in 구조 반영됨.
- 아직 "완전한 governing-agent 네트워크" 관점(E2E 오케스트레이션 증명)은 추가 필요.

3. 로그인/서명 기반 책임성
- 상태: **부분완료**
- session auth + report-hub signed metadata 반영.
- 계정 관리 UX/운영 정책 문서화 보강 필요.

4. 워크플로우에 FederHav + tool 가시성
- 상태: **완료(2차)**
- pipeline에 federhav 노드 추가.
- Ask/Live Ask 경로에서 governor tool trace(`trace_id/tool_id/duration/token/cache`)를 실시간/이력 UI와 작업 로그에 노출.
- 후속: stage-level 비용 집계 카드(일/런 단위)는 별도 대시보드화 필요.

5. Run Studio 분리/접근성
- 상태: **완료(1차)**
- 사이드바에서 Run Studio 접근 버튼 분리 + Run Map 계층 필터 반영.
- 계층 칩을 `필수/결과/근거/로그/보조` 톤으로 재분류해 필수/보조 탐색 경로를 축약.
- 후속: 대형 run(수백 파일)에서 스크롤 성능 최적화.

6. Live Logs 답변 잘림/표시 문제
- 상태: **완료(1차)**
- `live-ask-thread` inset 계산을 composer overlay 여부 기준으로 분기해 과도한 하단 inset 누적을 차단.
- 1366x768 / 1920x1080 / 2560x1440에서 마지막 답변/액션 버튼 잘림 재현 케이스 해소.
- 후속: 대화가 수백 turn 이상일 때 auto-follow 성능 관찰.

7. "FederHav에게 요청" 라벨 동적화
- 상태: **부분완료**
- `Agent에게 요청` + active profile/agent 기반 표시 로직 존재.
- 모든 케이스(기존 이력 복원 포함)에서 일관 노출 재검증 필요.

8. 입력창 하단 안내문 UX
- 상태: **부분완료**
- 문구 및 위치가 개편되었으나, 시인성/톤(강조색 과다) 개선 필요.

9. White/Black 테마
- 상태: **완료(기능)**
- 기본 동작 존재. 컴포넌트별 대비/테마별 미세 조정은 후속.

10. Built-in profile 수정 잠금/root unlock
- 상태: **부분완료**
- root unlock + session root 권한 반영.
- 실제 운영 계정 정책(초기 root bootstrap, 비밀번호 갱신 등) 고도화 필요.

11. 사이드바 버튼 비율/균형
- 상태: **완료(반응형)**
- 1024x768 / 900x700 / 820x680 / 768x1024 기준 quick-run/tab 버튼 clipping 미재현 확인.
- 후속: 모바일 세로폭(<=430px)에서 버튼 밀집도 미세 조정.

12. "state-memory + 보조로그 1,200자" 의미 명확화
- 상태: **부분완료**
- README 설명 추가됨.
- UI inline 설명을 더 직관적으로 줄여야 함.

13. deepagent 기반 자동 instruction 보정 + 실행
- 상태: **완료(3차)**
- quality guard + auto_instruction + `require_instruction_confirm` 신호 반영.
- Ask Action modal에 `Instruction 확인` 체크 게이트가 추가되어 미확인 상태 실행이 차단됨.
- `clarify_required + clarify_question` 응답 필드 추가.
- Live Ask 액션 버튼에 `질의 보강하기`를 연결해 보강 질문을 입력창으로 즉시 주입.
- Act 모드 자동실행은 `clarify_required=true`일 때 강제 보류됨.

14. E2E 테스트/반복 개선
- 상태: **부분완료**
- 단위/통합 테스트는 확장됨.
- Playwright 기반 시각/상호작용 E2E 회귀셋은 아직 부족.

---

## 4) 남은 핵심 TODO (새 대화 첫 스프린트 권장)

## P0 (즉시)

- [x] Live Logs 렌더링 안정화 (1차 완료)
  - 목표:
    - 긴 답변, 근거 펼침, 제안 버튼, composer 동시 노출 상황에서 **잘림 0건**
    - 내부 중첩 스크롤 최소화
  - 대상:
    - `site/federnett/app.css`
    - `site/federnett/app.js`
    - `site/federnett/index.html`
  - 검증:
    - 1366x768 / 1920x1080 / 2560x1440 Playwright 재현에서 마지막 메시지 + 제안 액션 버튼 clipping 미재현

- [x] Run Studio 파일 계층 UX 정리 (1차 완료)
  - 목표:
    - 결과물/입력/근거/로그를 계층적으로 구분
    - 긴 파일명 잘림 시 hover/tooltip + 폭 유연화
  - 대상:
    - `site/federnett/app.js` (트리 렌더러)
    - `site/federnett/app.css`
  - 검증:
    - `openclaw`, `agenticAI_recent`, `동영상생성AI` run 기준 all-view에서 입력/결과/근거/로그 계층 분리 확인
    - 계층 칩 필터 + 상단 Latest 항목으로 필수 파일 접근 경로 단축

- [x] Workflow Studio 조작성 재정비 (가시성 1차 완료)
  - 목표:
    - 개별 노드 클릭이 Studio 전체 제어성을 해치지 않도록 정리
    - active/selected/running 상태 색상 3단계 명확 구분
  - 대상:
    - `site/federnett/app.js`
    - `site/federnett/app.css`
  - 검증:
    - workflow 노드별 `state` 배지(`ready/queued/running/done/off/resume/error`) 추가
    - selected/active/complete 시각 구분을 테마 공통 토큰으로 강화

- [x] run-target 확정 UX 최종 마무리 (정책 반영 완료)
  - 목표:
    - 실행 전 대상 run 확인/생성 정책이 항상 일관
    - 힌트 추론 실패 시 자동 fallback 문구/가이드 제공
  - 대상:
    - `site/federnett/app.js`
    - `src/federnett/help_agent.py`
  - 검증:
    - 잘못된 run label/action 미표시
    - `switch_run`은 유효 hint 없으면 서버/클라이언트 모두 액션 생성 차단

## P1 (바로 다음)

- [x] FederHav deepagent governor 고도화 (trace 가시화 1차 완료)
  - 목표:
    - help/executor/planner/evidence/writer/quality subagent 체인을 명확히 분리
    - tool 호출 추적(trace id, tool id, 비용/시간 카운터) 노출
  - 대상:
    - `src/federhav/agentic_runtime.py`
    - `src/federnett/help_agent.py`
    - `site/federnett/app.js` (로그 뷰)
  - 진행(2026-02-21):
    - `/api/help/ask` 및 `/api/help/ask/stream`에 `trace.trace_id/steps` 포함
    - Live Ask process log에 `[run-agent:activity]` 라인 추가
    - Ask trace 패널 + Live Ask inline 로그에 `trace/tool/duration/token/cache` 메타 표시

- [x] instruction 자동작성/보정 흐름 강화 (질의 보강 단계 포함)
  - 목표:
    - 모호한 질문 -> 질의 보강 질문 -> instruction draft -> 사용자 확인 -> 실행
  - 대상:
    - `src/federnett/help_agent.py`
    - `src/federnett/routes.py`
    - `site/federnett/app.js`
  - 수용기준:
    - "실행해줘" 같은 입력에서 저품질 query 직접 실행 금지
  - 진행(2026-02-20):
    - `require_instruction_confirm` / `instruction_confirm_reason` 액션 필드 도입
    - Ask Action modal에 instruction 확인 체크박스 게이트 추가
    - 체크 미완료 시 Confirm 버튼 비활성 + 실행 함수 직접 호출 경로에서도 서버 실행 차단
  - 진행(2026-02-21):
    - `clarify_required` / `clarify_question` 도입
    - `질의 보강하기` 액션 버튼 추가 + follow-up prompt 자동 입력
    - Act 모드에서 clarify-required 액션 자동실행 차단

- [ ] 계정/권한 운영 시나리오 문서화
  - 목표:
    - root/admin/user 역할별 가능 동작 표준화
    - built-in profile 수정/잠금 해제 정책 명문화
  - 대상:
    - `README.md`
    - `docs/*`

## P2 (후속)

- [ ] Report Hub 협업 기능 본 구현
  - comment/followup/link API에 실제 UI write flow 연결
  - 게시물 ID 기반 로딩 + run 연결 + 재생성 제안 흐름 완성

- [ ] Playwright E2E 회귀 세트 상시화
  - 핵심 시나리오:
    - 질문 -> 답변 -> 제안 실행 -> run 전환 -> feather/federlicht 실행 -> 결과/로그 표시

## 4.1 미완 원인 분석 + 다음 핵심 TODO

- 원인 A (해결): FederHav governor 체인의 trace 스키마를 UI까지 고정 포맷으로 노출 완료.
  - 반영: `trace_id/tool_id/duration/token_est/cache_hit`를 `help_agent -> app.js`에 직렬화/렌더링.

- 원인 B (대부분 해결): `질문 보강 -> draft 확인 -> 실행` 중 질문 보강 유도 추가.
  - 반영: `clarify_required + 질의 보강하기`로 모호한 실행요청을 보강 턴으로 유도.
  - 잔여: server-side confirmed-draft 토큰(라우트 레벨) 정책은 문서화/선택 구현 필요.

- 원인 C: Playwright 회귀가 수동 스크립트 중심이라 지속적 회귀 감시가 어려움.
  - 영향: UI 변경 시 재현 시나리오 누락 가능성.
  - 다음 조치: 핵심 시나리오(ask->action->run-switch->workflow)를 CI용 smoke 스크립트로 고정.

- 다음 착수 우선순위(권장):
  1. P1 `계정/권한 운영 시나리오 문서화`
  2. P2 `Playwright 회귀 세트 상시화`
  3. P2 `Report Hub 협업 write-flow 완성`

---

## 5) 새 Codex 대화에서 권장 실행 순서

1. 워크트리 스냅샷 확인

```bash
git status --short
```

2. 핵심 테스트 스모크

```bash
pytest -q tests/test_help_agent.py tests/test_federnett_routes.py tests/test_federnett_auth.py tests/test_report_hub_api.py
```

3. 서버 실행

```bash
federnett --root . --port 8765
```

4. Playwright로 Live Logs + Workflow Studio + Run Studio 재현
- 긴 답변 표시
- 제안 액션(run-target 포함)
- 사이드바 폭/버튼 잘림
- 테마 white/black 전환

5. P0 항목부터 1개씩 패치 -> 테스트 -> Playwright 검증 반복

권장 반복 루프(최소 4회):
- 구현 -> 테스트 -> Playwright 검증 -> 회귀 수정 -> 리팩터링

---

## 6) 현재 블로커/주의사항

- 대화 컨텍스트가 매우 길어졌고, 워크트리 변경량이 큼.
- run 산출물(`site/runs/*`)과 코드 변경이 섞여 있으므로,
  - 기능 패치와 데이터 산출물을 분리해 관리하지 않으면 리뷰 난이도가 급상승함.
- Windows/VS Code/Playwright 세션 락 이슈가 간헐적으로 발생할 수 있으므로,
  - VS Code `Developer: Reload Window`
  - 기존 Playwright 세션 종료 후 재접속
  순서를 우선 적용.

---

## 7) 참고 문서
- `README.md`
- `CHANGELOG.md`
- `docs/federnett_remaining_tasks.md`
- `docs/federhav_deepagent_transition_plan.md`
- `docs/capability_governance_plan.md`

---

## 7.1 Federlicht 철학 반영 점검

- 반영됨:
  - `Feather -> archive(run) -> Federlicht` 흐름이 UI/CLI/로그 문맥에서 유지됨.
  - Live Ask가 `질의 보강 -> 실행 제안 -> 확인` 순서를 지원해 "즉답"보다 근거 기반 진행 흐름을 강화.
  - governor trace(`trace/tool/duration/token/cache`)를 남겨 "무엇을 근거로 어떤 판단을 했는지"를 재검토 가능하게 함.
  - run 아카이브 기반으로 재열람/재작성/추가 실행이 가능한 운영 형태를 유지.
- 보강 필요:
  - 철학 문장을 UI 온보딩(Help/tooltip)에 더 직관적으로 축약 노출할 필요.
  - Report Hub 협업 write-flow(comment/followup/link) 완성 후, 토의/리비전 루프를 UI에서 직접 닫는 작업 필요.

---

## 8) 인계 메모 (한 줄)
현재 코드는 **agentic 전환 + 인증/권한 + UI P0 안정화(1차) + instruction 확인 게이트 + 질의 보강 플로우 + governor tool trace 가시화(2차)**가 반영된 상태이며, 다음 세션의 1순위는 **권한 운영 문서화 + Playwright 회귀 자동화 + Report Hub 협업 write-flow 완성**이다.
