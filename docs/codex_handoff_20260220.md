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

## 3.1 사용자 요구 대비 상태 (2026-02-21 최신)

1. run root / site 정책 분리
- 상태: **완료(2차)**
- `DEFAULT_RUN_ROOTS=("runs","site/runs")`로 전환되어 신규 run은 `runs/*`를 우선 사용.
- 기존 `site/runs/*`는 하위 호환으로 계속 스캔/열람 가능.

2. 산출물(run)과 report hub 분리
- 상태: **완료(1차)**
- `run roots`와 `report_hub_root(site/report_hub)`를 분리 노출하고 메타 스트립에 병렬 표기.
- report hub는 게시/공유 목적, run은 작업 아카이브 목적이라는 역할 분리 유지.

3. Sidebar 탭 UX 통일(Feather/Federlicht/Run Studio)
- 상태: **완료**
- Run Studio 탭 클릭 시 강제 포커스 이동(`focusPanel`) 제거.
- Quick 버튼은 탭별 단일 버튼만 표시(`Run Feather` 또는 `Run Federlicht`), `Open Run Studio` 제거.

4. Feather Run Folder 입력 가시성
- 상태: **완료**
- `Run Folder (Output)` 라벨로 명확화하고 run root 기준 resolved 경로 힌트를 실시간 표시.

5. Workflow Result 상태 오표시(`RUNNING`) 수정
- 상태: **완료**
- `activeStep=result`만 남은 완료 상태에서 `running`으로 보이지 않도록 노드 상태 판정 분리.

6. Live Ask 작업로그 표시 개선
- 상태: **완료(2차)**
- 작업로그를 접힘형으로 바꾸고 summary에 `Ran <command>` 형태를 표시.
- turn 로그가 없을 때 글로벌 로그 카드가 대화 하단에 붙도록 정리.

7. Workflow Studio 중복 설정 정리
- 상태: **완료(1차)**
- `Feather 설정`, `Federlicht 설정`, `Quality 루프 설정` 중복 섹션 제거.
- Studio는 pipeline 선택/Stage override/FederHav bridge 중심으로 축소.

8. Workflow Studio 패널 렌더링 가시성
- 상태: **완료(1차)**
- stagebar/detail frame의 배경/경계/z-index/overflow를 조정해 잘림/겹침 현상 완화.

9. `READY` 노드 의미 정합성
- 상태: **완료(정의 확인)**
- 현재 구현에서 `READY`는 해당 노드가 실행 가능하며 선행 조건이 충족된 대기 상태를 의미.
- 사용자 설명(“작업 수행 준비 상태”)과 구현 의미가 일치함.

10. Federlicht 철학 반영(Feather -> Archive -> Federlicht)
- 상태: **부분완료**
- 질문 보강/근거 추적/run archive 재활용 흐름은 반영됨.
- report hub의 토론/코멘트/follow-up write-flow UI 완성은 잔여.

11. 계정/권한 운영 문서화
- 상태: **부분완료**
- auth API와 signed metadata는 반영.
- 운영 정책(초기 root bootstrap, 권한 분기 가이드) 문서 정리는 추가 필요.

12. Playwright 회귀 자동화
- 상태: **부분완료**
- 수동 회귀 시나리오는 안정화.
- CI 고정 smoke 시나리오는 미완.

---

## 4) 남은 핵심 TODO (새 대화 첫 스프린트 권장)

## P0 (즉시 유지)

- [ ] 계정/권한 운영 문서화 마무리
  - root/admin/user 권한표, root unlock/session auth 정책, built-in profile 편집 기준을 한 문서로 고정.

- [ ] Report Hub write-flow UI 완성
  - comment/followup/link API를 UI submit 플로우와 연결.
  - 게시 승인(사용자 허락) 이후 hub 게시 흐름 명시.

- [ ] Playwright 회귀셋 상시화
  - 핵심 플로우(질문 -> 제안 -> run 전환 -> Feather/Federlicht 실행 -> 결과 확인)를 CI smoke로 고정.

## P1 (개선)

- [ ] 대형 run 성능 최적화
  - Run Studio 트리(수백 파일)에서 렌더/필터 체감지연 계측 후 가상화/지연 렌더링 검토.

- [ ] Workflow 관측 대시보드
  - stage-level 비용/시간 집계를 run 단위 카드로 분리 노출.

## 4.1 미완 원인 분석

- 원인 A: 기능 구현이 문서화 속도를 앞질러 운영 가이드가 뒤처짐.
  - 조치: 권한/게시 정책을 README+docs로 동기화.

- 원인 B: Report Hub는 API 선구현, UI 연결은 후행이라 사용자 관점 completion이 낮음.
  - 조치: write-flow 최소 UI를 먼저 붙여 운영 루프를 닫기.

- 원인 C: Playwright는 수동 점검 중심이라 회귀 누락 위험이 남아 있음.
  - 조치: smoke 시나리오를 스크립트화해 고정.

## 4.2 목표 조정 (지금 굳이 완성하지 않아도 되는 항목)

- `site/runs`의 즉시 물리적 대규모 마이그레이션은 보류 가능.
  - 이유: 현재 `runs/*` 우선 + `site/runs/*` 호환으로 운영 리스크 없이 점진 이전 가능.

- Federnett/Federlicht 코드베이스의 별도 리포 분리(완전 분기)는 당장 필수 아님.
  - 이유: 경로/정책 분리와 산출물 분리만으로도 pages publish/git 관리 효율을 즉시 확보 가능.

- Workflow Studio의 세부 시각효과(애니메이션/미세 타이포 튜닝)는 후순위.
  - 이유: 현재 우선순위는 기능 일관성/오표시 제거/회귀 안정화.

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
