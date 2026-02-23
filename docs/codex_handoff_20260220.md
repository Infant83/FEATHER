# Codex Handoff - 2026-02-22 (Latest)

> Canonical handoff has moved to `docs/codex_handoff_20260222.md` (use this file as the primary status source from 2026-02-22 onward).

Last updated: 2026-02-22 07:17:54 +09:00 (UI refresh v30: non-sticky layout + live composer floating + workflow readability uplift + white workspace contrast fix + playwright re-audit)

## 목적
- 중단된 세션을 다음 Codex 대화에서 **즉시 재개**할 수 있도록,
  - 현재 반영된 변경,
  - 검증 상태,
  - 미완 원인,
  - 다음 실행 순서를 최신 기준으로 고정한다.

---

## 1) 현재 상태 요약

### 1.1 플랫폼 축
- `Feather`: 소스 수집/아카이브
- `Federlicht`: 다단계 보고서 생성/품질 루프
- `Federnett`: 실행/검토/반복 UI
- `FederHav`: 질의 보강 + 실행 제안 + 후속 수정 가이드

### 1.2 이번 세션에서 반영된 핵심
- Live Logs/Workflow Studio UI 안정화(표/mermaid 렌더, 로그 브릿지 compact, stage selector 가시성 개선).
- Feather/Federlicht 옵션 노출 정책 업데이트:
  - `Advanced` 접힘 패널 제거, 실행 옵션 기본 노출
  - backend-model 자동 연동 강화(특히 Codex backend 전환 시 모델 자동 보정)
- Live Logs compact 카드 1-line 요약 강화:
  - summary 한 줄에 agent/tool/command 요약 집약
- run/site 분리 정책 정리 문서 보강(`docs/run_site_publish_strategy.md`).
- 보고서 품질 규칙 강화(프롬프트 정책):
  - 방법론 투명성(선정/제외 기준, 절차, 한계)
  - 결과 추적성(evidence matrix)
  - 불확실성 분리(확정/추정 구분 + 추가 검증 제안)
  - **유연화 1차 완료**: `depth + template_rigidity + free_format` 조합에 따라
    - strict/deep: 강한 구조 요구
    - balanced/deep: 권장 중심
    - brief/free-format/loose: 목적 적합형 최소 구조
- report hub 발행 전용 모듈 추가:
  - `python -m federlicht.hub_publish --report ... --hub site/report_hub`
  - run 산출물을 `site/report_hub/reports/<run>/...`로 복사 + manifest/index 갱신
  - HTML 로컬 링크 자산(img/css/csv/pdf 등) 동반 복사(기본 on, `--no-linked-assets`로 비활성)
- Federnett Run Studio에 `Publish to Report Hub` 버튼 연결:
  - `POST /api/report-hub/publish`
  - publish 결과(`published_asset_rels`, `skipped_asset_refs`)를 로그/응답으로 추적
- Codex backend 모델 전달 안정화:
  - `GPT-5.3-Codex-Spark` 같은 대문자 토큰을 `gpt-5.3-codex-spark`로 정규화
  - UI/route/command 빌더 전 구간에서 codex 모델 토큰 소문자 정렬
  - generate_prompt/scout 단계에서 codex bridge 실패 재현 케이스 완화
- Prompt 파일 경로 정합성 강화(`site/runs` vs `runs`):
  - Federlicht `Generate Prompt` 기본 경로를 선택 run의 실제 root 기준으로 생성
  - 상대경로 확장 시 선택 run root를 우선하여 `run`과 `output` root 불일치 방지
  - `Generate Prompt` 버튼 라벨 명시화
- Workspace root 전역 설정(런타임 반영) 추가:
  - `GET/POST /api/workspace/settings`
  - 저장 파일: `site/federnett/workspace_settings.json`
  - 서버 시작 시 저장 설정(`run_roots/site_root/report_hub_root`) 자동 로드/적용
- Run Folder 전역 UX 전환:
  - 상단 버튼(`Run Folder`)으로 `Load / Open / Create` 통합
  - Federlicht 패널 내부 `Open Run Folder` 버튼 제거
  - run 생성 시 `run_root` 지정 지원(`/api/runs/create`)
- LLM 설정 단일 진입점 추가:
  - 상단 `LLM Settings` 버튼 + Global Sync Lock
  - Feather/Federlicht/FederHav backend/model 정책 동기화
  - backend별 모델 목록 분리(openai/codex datalist)
  - 모델 입력값 blank 편집 유지(즉시 강제복원 제거)
- LLM 설정 일원화 2차 정리:
  - Feather/Federlicht/Live Ask/Workflow Studio의 개별 backend/model 입력 제거
  - runtime payload는 `LLM Settings` 전역 정책만 사용하도록 동기화
  - 전역 정책 변경 시 `federnett:model-policy-updated` 이벤트로 패널 상태 즉시 동기화
- Workflow pipeline 상태칩 가독성 개선:
  - `READY` 등 저신호 배지 억제, 문제/진행 신호 중심으로 표시
- White 테마 대비/가독성 보정:
  - topbar, panel, form input/select, dropdown option, live log card 대비 강화
  - 화이트 테마에서 dark 고정 배경으로 발생하던 가독성 저하 완화
  - Live Ask/Workflow Studio/Run Studio/Run Folder modal/LLM Settings/File Preview까지
    dark 잔여 배경을 light palette로 재정렬(Playwright 스캔 기준 dark-like 0)
- 테마 일관성 3차(전체 테마):
  - `default/white/black/sky/crimson/sage/amber` 공통 링크/하이라이트 색을
    테마별 팔레트 변수(`--link*`)로 전환
  - cyan 고정 링크색 제거로 theme mismatch 완화 및 가독성/시각 일관성 강화
- Federnett 상단 바/Live Logs 레이아웃 조정:
  - top `Federnett` 바 sticky 제거(스크롤 시 자연스럽게 화면 밖으로 이동)
  - Live Logs 답변 영역을 고정 크기에서 동적 확장형으로 조정
    (초기 최소 높이 -> 뷰포트 상한까지 확장 -> 이후 내부 스크롤)
- Workspace Sidebar/Live Logs 레이아웃 정리:
  - 좌우 드래그 splitter(`layout-splitter`) 제거
  - 브라우저 폭 기준 2열 자동 확장 레이아웃으로 전환
- UI/UX 리프레시 5차(v30):
  - `control/telemetry` sticky 제거(스크롤 시 자연 이동)
  - Live Logs 패널 높이 확장(뷰포트 활용) + thread 높이 확대
  - FederHav 입력창을 sticky composer 형태로 단순화(질문 중심)
  - Workflow strip/node 칩 가독성 상향(크기/명도/대비 보정)
  - Workspace Settings(white theme) dark 잔여 배경 제거 및 pink 저대비 텍스트 교정
- FederHav 액션 의도 판별 강화:
  - 일반 콘텐츠 질의(예: “PPT 한 장 가능?”)는 run 액션으로 자동 비약하지 않도록 제한
  - run/workflow/stage/instruction/prompt 등 workspace 조작 의도일 때만 run_* 액션 허용
  - action planner prompt의 `short generic -> run_feather 우선` 편향 지시 제거
- GitLab Pages CI 추가(`.gitlab-ci.yml`): smoke test + pages 배포 파이프라인.
- Run Folder 단일 진입 정책(2차):
  - Feather/Federlicht 패널에서 Run Name/Run Folder 직접 수정 제거(readonly)
  - Run Folder 변경은 상단 `Run Folder` 모달에서만 수행
  - Run Picker에서 임의 `run root` 추가 입력 + 저장 + 즉시 재로딩 플로우 제공
- 경로 정합성 보강(Feather/Federlicht):
  - Feather submit 시 run-folder를 부모 root로 재해석하던 휴리스틱 제거
  - Federlicht output은 선택 run 하위 파일명으로 강제 정규화(런 폴더 이탈 방지)
- Live Logs compact v2:
  - Live Ask `질문 실행/중단` 단일 토글 버튼화
  - Workflow strip를 thread 하단으로 재배치(order) + 상태 배지 최소화
  - 보조로그 기본 요약량 2.2k, placeholder를 적응형 요약 정책으로 명시
- Federlicht 품질 루프 2차 강화:
  - `report_intent`(research/review/decision/briefing/explainer/slide/narrative/generic) 도입
  - planner/evidence/writer/writer-finalizer/evaluator 프롬프트를 동일 intent 축으로 정렬
  - quality evaluator에 LLM 점수 + 구조 휴리스틱(섹션 커버리지/인용 밀도/방법론/추적성/불확실성) 결합
  - quality critique/revise 단계에 “수정 시 근거 밀도/방법론 설명 약화 금지” 가드 추가
- HTML 기준 휴리스틱 보정:
  - `<h2>` 헤딩/`href` 링크/숫자 인용(`[1]`) 인식으로 quality 신호 왜곡 완화
  - Markdown 링크(`[]()`) 인용 밀도 계산 반영
- 예제 생성(로컬):
  - `site/runs/openclaw/report_full_iter_brief_example.html`
  - `site/runs/openclaw/report_full_iter_brief_quality.html`
  - `site/runs/openclaw/report_full_iter_brief_base.md`
  - deep + full quality 장시간 실행은 Codex backend 응답 지연으로 타임아웃 케이스 존재(아래 미완 원인 참고)

---

## 2) 완료/부분완료/미완 상태표 (2026-02-21)

1. run root / site 정책 분리
- 상태: **완료(전역 설정 2차)**
- 기본 run root: `runs,site/runs`
- 신규 run은 `runs/*` 우선, `site/runs/*`는 레거시 호환
- root 설정 API를 통해 런타임 변경/저장 가능(서버 재기동 시 자동 재적용)

2. 산출물(run) vs report hub 분리
- 상태: **완료(3차)**
- 정책 문서 고정: `docs/run_site_publish_strategy.md`
- 발행 전용 모듈 추가: `src/federlicht/hub_publish.py`
- linked-assets publish 정책 반영(HTML 로컬 참조 파일 동반 복사)

3. Sidebar 탭 UX 통일(Feather/Federlicht/Run Studio)
- 상태: **완료**
- 강제 포커스 이동 제거, 탭별 단일 실행 버튼 유지

4. Live Logs 렌더 가독성
- 상태: **부분완료(5차 진행 중)**
- markdown 표/코드블록/이미지 렌더 강화
- 로그 브릿지 카드 compact 요약(한 줄) 고도화
- 질문 실행/중단 단일 토글 + thread 우선 레이아웃 적용
- composer/toolbar 압축 및 workflow strip 하단 재배치
- 답변창 동적 높이 확장(뷰포트 상한) + 내부 스크롤 전환 반영
- sticky composer(플로팅 입력창) + thread 고도 확장(실측 약 1000px @ 1720x1160)

5. Workflow Studio 가시성/직관성
- 상태: **부분완료(3차 진행 중)**
- 작은 상단 frame 제거
- Stage 선택 드롭다운 + selected/focus 배지 + prompt override 미리보기
- "사용 가능 도구: 로딩중" 고정 노출 문제 완화

6. READY 노드 의미 정합성
- 상태: **완료(가시성 간소화 반영)**
- READY = 실행 가능(선행 조건 충족) 대기 상태
- 표시 정책: running/error/off/resume 등 고신호 상태 중심

7. Federlicht 보고서 품질(내용 중심)
- 상태: **부분완료(유연화 2차 + intent-aware 반영)**
- 완료:
  - intent-aware 프롬프트(Plan/Evidence/Writer/Evaluate) 일관 적용
  - 품질평가 LLM+휴리스틱 결합(모델 변동 완충)
  - critique/revise 회귀 방지 가드(근거 밀도/방법론 약화 금지)
- 잔여:
  - deep 모드 장시간 실행 안정화(backend latency budget/timeout 전략)
  - 도메인별(산업/의학/정책) 평가 축 가중치 세분화

8. Report Hub 협업 write-flow UI(comment/followup/link)
- 상태: **부분완료(3차)**
- API는 구현됨(`src/federnett/report_hub.py`)
- Run Studio publish 버튼 및 API 연결 완료
- post/comment/followup/link 협업 패널 본 UI 완성은 잔여

9. Playwright 회귀 자동화
- 상태: **부분완료**
- 수동/스크립트 스모크는 동작
- CI에서 브라우저 기반 e2e 고정 스위트는 미완

10. GitLab Pages 배포 실체화
- 상태: **완료(1차)**
- `.gitlab-ci.yml` 추가
- smoke test + `site/report_hub` 배포 경로 고정

11. PPT Writer 확장 전략
- 상태: **부분완료(설계 명확화 단계)**
- 현재 상태: PPT/PPTX 입력 파싱 및 figure 추출은 구현됨
- 미완: 슬라이드 지향 출력 파이프라인(`slide plan -> component layout -> pptx render`)과 품질 루프

12. Codex 모델명 정규화 이슈
- 상태: **완료**
- 원인: Codex CLI는 계정/브리지 조건에서 대문자 codex 모델 토큰을 비지원으로 처리할 수 있음
- 조치: backend=`codex_cli`일 때 모델 토큰을 소문자 canonical form으로 정규화

13. Federlicht prompt 경로 root 불일치(`site/runs` vs `runs`)
- 상태: **완료**
- 원인: 기본 경로 생성이 run 이름 기반 + 전역 run root 우선 적용으로 선택 run root와 분리될 수 있었음
- 조치: 선택 run 경로 기반 기본값/상대경로 확장 정책으로 통일

14. Run Folder/Workspace Settings 전역 제어
- 상태: **완료(2차)**
- 상단 `Run Folder`에서 run load/open/create 동작 통합
- workspace root 설정(run_roots/site_root/report_hub_root) API/저장/적용 반영
- root auth enabled 환경에서는 저장 시 root unlock 필요
- Feather/Federlicht 패널의 run 직접 편집 제거(단일 진입 정책 고정)
- Run Picker에서 custom run root 추가 후 즉시 저장/리로드 가능

15. LLM 설정 일원화
- 상태: **완료(2차)**
- 상단 `LLM Settings` 모달 + Global Sync Lock 반영
- backend별 모델 목록 분리(openai/codex)
- panel 입력 blank 유지 + 실행 시점 기본값 해석
- Feather/Federlicht/FederHav/Workflow Studio 내 개별 LLM 입력 제거(전역 정책 단일화)

16. FederHav 액션 과잉유도 완화
- 상태: **완료(1차)**
- workspace 조작 의도(run/workflow/Feather/Federlicht)가 없는 일반 콘텐츠 질의는 action planning 제외
- safe fallback에서 `analysis-like` 문장만으로 run 자동 제안하지 않도록 가드 추가

17. Elicit 수준 목표 대응(반복 개선 루프)
- 상태: **부분완료(실행 루프 시작)**
- 완료:
  - intent 기반 작성정책 + 품질 신호 계량화 도입
  - 예제 run 생성/검증 루프 재가동
- 잔여:
  - deep quality 실행 타임아웃 감소
  - 장문 보고서 품질 벤치마크(샘플 세트) 자동화

18. White 테마 전면 점검(전체 UI/UX)
- 상태: **완료(4차)**
- Live Logs, Workflow Studio, Run Studio, Run Folder/LLM Settings modal, File Preview 포함
  주요 패널 전수 점검 완료
- Playwright 스캔 리포트:
  - `test-results/white-theme-audit-after2.json`
  - `test-results/white-theme-global-scan-after2.json`
  - `test-results/white-theme-multiview-scan-after4.json`
  - `test-results/white-theme-workspace-contrast-20260222.json`

19. 전 테마(colorway) 일관성/가독성 점검
- 상태: **완료(2차)**
- 대상: `default/white/black/sky/crimson/sage/amber`
- 조치:
  - 링크/하이라이트 스타일을 테마별 팔레트 변수(`--link`, `--link-hover`, `--link-bg`, `--link-border`) 기반으로 통일
  - 고정 청록 링크 톤 제거, 각 테마의 accent 계열과 조화되도록 보정
  - `Theme` 드롭다운 option 컬러를 고정 다크값에서 테마 변수 기반(`--bg-2`, `--ink`)으로 동기화
- 검증 리포트:
  - `test-results/theme-contrast-audit-round1.json`
  - `test-results/theme-contrast-audit-round2.json`
  - `test-results/theme-smoke-round3.json`
- 기준: 주요 패널/입력/모달/링크 contrast ratio 4.5 미만 `0건`

20. Sidebar-Logs splitter 제거
- 상태: **완료**
- `index.html`의 `layout-splitter` 제거
- CSS grid를 3열(사이드바/분할바/로그)에서 2열(사이드바/로그)로 변경
- 검증:
  - `test-results/layout-no-splitter-8881.json` (`splitterExists=false`)

---

## 3) 검증 스냅샷 (최신)

### 3.1 테스트
- `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py tests/test_help_agent.py`
  - 결과: `101 passed`
- `pytest -q tests/test_help_agent.py`
  - 결과: `44 passed` (FederHav action-intent guard 회귀 포함)
- `pytest -q tests/test_help_agent.py` (white-theme patch 이후 재검증)
  - 결과: `44 passed`
- `pytest -q tests/test_federnett_routes.py` (layout/theme patch 이후 재검증)
  - 결과: `39 passed`
- `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py`
  - 결과: `57 passed`
- `pytest -q tests/test_report_prompt_quality_policy.py tests/test_report_reasoning_policy.py tests/test_federnett_commands.py tests/test_federnett_routes.py`
  - 결과: `58 passed`
- `pytest -q tests/test_hub_publish.py tests/test_site_hub_separation.py tests/test_report_prompt_quality_policy.py tests/test_federnett_commands.py tests/test_federnett_routes.py`
  - 결과: `57 passed`
- `pytest -q tests/test_report_prompt_quality_policy.py`
  - 결과: `7 passed` (유연화 분기 회귀 테스트)
- `pytest -q tests/test_report_reasoning_policy.py tests/test_hub_publish.py tests/test_site_hub_separation.py tests/test_federnett_commands.py tests/test_federnett_routes.py`
  - 결과: `59 passed`
- `pytest -q tests/test_hub_publish.py tests/test_federnett_routes.py`
  - 결과: `37 passed`
- `pytest -q tests/test_federnett_routes.py tests/test_federnett_commands.py`
  - 결과: `56 passed`
- `pytest -q tests/test_report_prompt_quality_policy.py tests/test_report_quality_heuristics.py tests/test_report_reasoning_policy.py tests/test_federnett_commands.py tests/test_federnett_routes.py tests/test_help_agent.py`
  - 결과: `116 passed`
- `pytest -q tests/test_report_prompt_quality_policy.py tests/test_report_quality_heuristics.py tests/test_report_reasoning_policy.py tests/test_report_citation_rewrite.py tests/test_report_codex_bridge_tools.py tests/test_report_create_agent_fallback.py tests/test_report_style_pack.py`
  - 결과: `34 passed`
- `pytest -q tests/test_federnett_commands.py tests/test_federnett_routes.py tests/test_help_agent.py tests/test_hub_publish.py`
  - 결과: `104 passed`
- `pytest -q tests/test_federnett_routes.py`
  - 결과: `39 passed` (UI refresh v30 이후 재검증)
- `pytest -q tests/test_help_agent.py`
  - 결과: `44 passed` (UI refresh v30 이후 재검증)
- `pytest -q tests/test_federnett_commands.py tests/test_federnett_auth.py`
  - 결과: `22 passed`

### 3.2 Playwright 스모크
- 대상: `http://127.0.0.1:8767/`
- 확인:
  - Live Logs thread 표시
  - Workflow Studio 패널 열림
  - stage selector / focus hint 노출
  - 도구 영역 "로딩중" 고정 비노출
  - `site/report_hub/index.html` 로컬 렌더 + 게시된 run(`openclaw`) 확인
  - Run Studio `Publish to Report Hub` 버튼 노출 확인
  - report가 있는 run 선택 시 publish 버튼 활성화 확인
  - Federlicht `Generate Prompt` 실행 후 `Inline Prompt` 자동 반영 확인
    (`site/runs/20260221_QC_report` 기준, 완료 `rc=0`, inline 길이 832)
  - 상단 전역 버튼 노출 확인:
    - `Reload Runs / Run Folder / LLM Settings / Agent Workspace Settings`
  - Run Folder 모달에서 workspace settings 필드 노출 확인
  - LLM Settings backend 전환 시 모델 datalist가 `openai -> codex`로 전환되는지 확인
  - Federlicht 모델 입력 수동 clear 후 blank 유지 확인
  - White theme에서 topbar/panel/input/live-thread 배경이 light palette로 반영되는지 확인
  - White theme 전역 스캔:
    - `test-results/white-theme-audit-after2.json` -> dark-like `0`
    - `test-results/white-theme-global-scan-after2.json` -> dark-like block `0`
    - `test-results/white-theme-multiview-scan-after4.json` -> main/tab/workflow/modal dark-like `0`
  - 전 테마 contrast 스캔:
    - `test-results/theme-contrast-audit-round1.json` -> bad(<3.2) `0`
    - `test-results/theme-contrast-audit-round2.json` -> bad(<4.5) `0`
  - 전 테마 pageerror 스캔:
    - `test-results/theme-pageerror-scan-round1.json` -> `default/white/black/sky/crimson/sage/amber` 모두 pageerror `0`
    - `test-results/theme-smoke-round3.json` -> `default/white/black/sky/crimson/sage/amber` 모두 pageerror `0`
  - UI refresh v30 재검증:
    - `test-results/theme-ui-refresh-audit-20260222.json`
      - min_contrast: `6.07`
      - pageerror: `0`
      - topbar_scroll_follow_delta: `818.0` (스크롤 따라붙음 제거 확인)
      - live thread height: `1000.34px` (@1720x1160)
    - `test-results/white-theme-workspace-contrast-20260222.json`
      - workspace panel title contrast: `15.27`
      - readonly hint contrast: `4.56`
  - splitter 제거 확인:
    - `test-results/layout-no-splitter-8881.json` -> `splitterExists=false`
  - JS runtime pageerror(`renderAskPanelState is not defined`) 재발 없음 확인
  - 최신 패치 검증(임시 최신 서버 `http://127.0.0.1:8877/`):
    - `#feather-output` readonly=true
    - `#run-select` hidden=true
    - `#federlicht-run-display` 노출 확인
    - `#live-ask-stop` 제거 + `#live-ask-run` 단일 토글 버튼 확인
    - `#workspace-run-root-add`, `#workspace-run-root-add-btn` 노출 확인
    - workflow strip/order 확인(`workflow-strip=2`, `live-ask-main=1`)
    - pageerror 0건

주의:
- 기존에 실행 중인 Federnett(예: `127.0.0.1:8767`)가 이전 코드 프로세스면 신규 API(`/api/report-hub/publish`)가 404일 수 있음.
- 이 경우 Federnett 서버 재시작 후 검증 필요.

### 3.3 로컬 예제 실행/발행
- 예제 검토 실행:
  - `python -m feather --review ./site/runs/openclaw --format text`
- report hub 발행:
  - `python -m federlicht.hub_publish --report ./site/runs/openclaw/report_full.html --run ./site/runs/openclaw --hub ./site/report_hub`
- 결과:
  - `site/report_hub/reports/openclaw/report_full.html` 생성/갱신
  - `site/report_hub/manifest.json`, `site/report_hub/index.html` 갱신
- 추가 예제 생성(품질 루프 검증):
  - `python -m federlicht.report --run site/runs/openclaw --output site/runs/openclaw/report_full_iter_brief_example.html --template quanta_magazine --depth brief --quality-iterations 0 ...`
  - `python -m federlicht.report --run site/runs/openclaw --output site/runs/openclaw/report_full_iter_brief_quality.html --template quanta_magazine --depth brief --quality-iterations 1 ...`
  - 산출물: `report_full_iter_brief_example.html`, `report_full_iter_brief_quality.html`, `report_full_iter_brief_base.md`
  - 품질 휴리스틱 스냅샷(briefing intent):
    - base_md: overall `92.67`
    - quality_md: overall `89.08`
  - 해석: quality 루프가 간결성 개선을 시도하는 동안 불확실성 서술 밀도가 일부 감소하는 회귀가 관측됨(다음 스프린트에서 quality-revision 보정 필요)
  - 주의: deep + full quality 실행은 Codex backend 응답 지연으로 CLI timeout에 걸릴 수 있어, 단기적으로 `quality_max_chars`/stage budget 튜닝이 필요

---

## 4) Playwright 실행 이슈 정리

### 4.1 관측된 에러
- Codex extension startup 중 MCP server `playwright`에서
  - `resources/templates/list failed: Method not found(-32601)`
  - 이후 Codex process unavailable

### 4.2 원인(현재 판단)
- 확장(클라이언트)과 Playwright MCP 서버 간 프로토콜 호환성 불일치.
- 즉, extension이 호출하는 MCP 메서드와 서버 구현 버전이 안 맞는 상태.

### 4.3 현재 안전 운영안
- `C:\Users\angpa\.codex\config.toml`에서 playwright MCP를 비활성화한 상태 유지.
- UI 검증은 Python Playwright 스모크로 수행.

### 4.4 재활성화 시 체크
1. `npx @playwright/mcp@latest --version`으로 실제 버전 확인
2. `tools/playwright_mcp_recover.ps1` 실행(락/프로세스 정리)
3. Codex extension reload 후 handshake 재확인
4. 재발 시 MCP 비활성 + Python Playwright 경로 유지

---

## 5) on-prem + GitLab Pages 운영 전략

### 5.1 권장 분기
- 작업(run) 영역: `runs/*` (에이전트 작업, 임시 산출, 로그)
- 발행(hub) 영역: `site/report_hub/*` (승인된 결과만)

### 5.2 on-prem 발행 플로우
1. on-prem Federlicht 실행으로 보고서 생성 (`runs/<run>/report_full.html`)
2. 사용자 승인
3. 발행 명령:
   - `python -m federlicht.hub_publish --report ./runs/<run>/report_full.html --hub ./site/report_hub --run ./runs/<run>`
4. `site/report_hub`만 GitLab remote로 push
5. GitLab Pages에서 `public <- site/report_hub` 배포

### 5.3 login/agent profile 연계 포인트
- Federnett 세션 인증/프로필은 **운영 API 계층**에서 처리.
- GitLab Pages는 정적 사이트이므로 인증 로직 직접 수행 불가.
- 권장 이원화:
  - 내부 Federnett(API): 인증/작성/승인
  - Pages(정적): 승인된 결과 조회 전용

---

## 6) 미완 원인 및 우선 TODO

### P0
- [ ] Report Hub 협업 UI(write-flow) 완성
  - 원인: publish 버튼은 연결 완료됐지만 comment/followup/link 전용 협업 패널이 아직 미완
- [ ] Playwright e2e CI 고정
  - 원인: 로컬 수동 검증 비중이 높음
- [ ] 권한 운영 문서(root/admin/user + bootstrap) 확정

### P1
- [ ] 대형 run 렌더 성능 최적화(가상화/지연 렌더)
- [ ] stage별 시간/비용 대시보드 강화
- [ ] 보고서 품질 evaluator 지표 확장(방법론 투명성/결과 추적성 score 분리)
- [ ] PPT Writer 파이프라인 설계 확정
  - slide planner -> layout composer -> artifact pack(pptx/html/pdf) -> quality critic 루프

### 보류 가능 항목
- `site/runs` 대규모 즉시 마이그레이션
  - 현재는 `runs` 우선 + 레거시 호환으로 리스크 낮음
- UI 미세 애니메이션/시각효과 튜닝
  - 기능 안정/운영성 대비 우선순위 낮음

---

## 7) 다음 세션 권장 실행 순서

1. 워크트리/브랜치 확인
2. 핵심 테스트 스모크
3. Federnett 실행 + Playwright 스모크
4. P0 항목 1개 선택
5. 구현 -> 테스트 -> Playwright -> 문서 업데이트 반복

---

## 8) 참고 파일
- `docs/run_site_publish_strategy.md`
- `docs/ppt_writer_strategy.md` (신규 설계 문서)
- `docs/federnett_remaining_tasks.md`
- `docs/federhav_deepagent_transition_plan.md`
- `README.md`
- `CHANGELOG.md`

---

## 9) 인계 한 줄
현재 기준으로 **run/hub 분리 정책 + 허브 발행 모듈 + GitLab Pages CI + Live Logs/Workflow Studio 가시성 개선 + 보고서 품질 프롬프트 강화**가 반영되었고, 다음 1순위는 **Report Hub 협업 UI 완성과 Playwright e2e CI 고정**이다.
