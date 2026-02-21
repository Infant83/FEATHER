# Codex Handoff - 2026-02-21 (Latest)

Last updated: 2026-02-21 (prompt flexibility patch + local hub publish verified)

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
- GitLab Pages CI 추가(`.gitlab-ci.yml`): smoke test + pages 배포 파이프라인.

---

## 2) 완료/부분완료/미완 상태표 (2026-02-21)

1. run root / site 정책 분리
- 상태: **완료**
- 기본 run root: `runs,site/runs`
- 신규 run은 `runs/*` 우선, `site/runs/*`는 레거시 호환

2. 산출물(run) vs report hub 분리
- 상태: **완료(2차)**
- 정책 문서 고정: `docs/run_site_publish_strategy.md`
- 발행 전용 모듈 추가: `src/federlicht/hub_publish.py`

3. Sidebar 탭 UX 통일(Feather/Federlicht/Run Studio)
- 상태: **완료**
- 강제 포커스 이동 제거, 탭별 단일 실행 버튼 유지

4. Live Logs 렌더 가독성
- 상태: **완료(2차)**
- markdown 표/코드블록/이미지 렌더 강화
- 로그 브릿지 카드 compact 요약(한 줄)

5. Workflow Studio 가시성/직관성
- 상태: **완료(2차)**
- 작은 상단 frame 제거
- Stage 선택 드롭다운 + 현재 선택 stage 힌트 + prompt override 미리보기
- "사용 가능 도구: 로딩중" 고정 노출 문제 완화

6. READY 노드 의미 정합성
- 상태: **완료**
- READY = 실행 가능(선행 조건 충족) 대기 상태

7. Federlicht 보고서 품질(내용 중심)
- 상태: **부분완료(유연화 1차 반영)**
- 프롬프트 정책 강화 + 유연화 분기(강제/권장/요약형) 반영 완료
- 템플릿/평가 루프의 도메인별 고도화(산업/의학/정책 등)는 추가 스프린트 필요

8. Report Hub 협업 write-flow UI(comment/followup/link)
- 상태: **부분완료**
- API는 구현됨(`src/federnett/report_hub.py`)
- UI 플로우 완성/운영 규칙 노출은 잔여

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

---

## 3) 검증 스냅샷 (최신)

### 3.1 테스트
- `pytest -q tests/test_report_prompt_quality_policy.py tests/test_report_reasoning_policy.py tests/test_federnett_commands.py tests/test_federnett_routes.py`
  - 결과: `58 passed`
- `pytest -q tests/test_hub_publish.py tests/test_site_hub_separation.py tests/test_report_prompt_quality_policy.py tests/test_federnett_commands.py tests/test_federnett_routes.py`
  - 결과: `57 passed`
- `pytest -q tests/test_report_prompt_quality_policy.py`
  - 결과: `7 passed` (유연화 분기 회귀 테스트)
- `pytest -q tests/test_report_reasoning_policy.py tests/test_hub_publish.py tests/test_site_hub_separation.py tests/test_federnett_commands.py tests/test_federnett_routes.py`
  - 결과: `59 passed`

### 3.2 Playwright 스모크
- 대상: `http://127.0.0.1:8767/`
- 확인:
  - Live Logs thread 표시
  - Workflow Studio 패널 열림
  - stage selector / focus hint 노출
  - 도구 영역 "로딩중" 고정 비노출
  - `site/report_hub/index.html` 로컬 렌더 + 게시된 run(`openclaw`) 확인

### 3.3 로컬 예제 실행/발행
- 예제 검토 실행:
  - `python -m feather --review ./site/runs/openclaw --format text`
- report hub 발행:
  - `python -m federlicht.hub_publish --report ./site/runs/openclaw/report_full.html --run ./site/runs/openclaw --hub ./site/report_hub`
- 결과:
  - `site/report_hub/reports/openclaw/report_full.html` 생성/갱신
  - `site/report_hub/manifest.json`, `site/report_hub/index.html` 갱신

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
  - 원인: API 선구현 후 UI 연결이 후행
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
