# Codex Unified Handoff - 2026-02-24

Last updated: 2026-02-24 14:33:10 +09:00  
Previous handoff: `docs/dev_history/handoffs/codex_handoff_20260223.md` (full iter log archive, 1~100)

## 1) 목적 (고정)
- 최상위 목표: `(World-Class) Professional Research Level Report Quality`
- 원칙:
- 정형 템플릿 강제보다 **에이전트 협업 구조(Scout/Plan/Evidence/Writer/Quality)** 최적화 중심
- 근거 추적성(Claim-Evidence-Source) + 반복 개선 가능성 + 운영 안정성 동시 달성

## 2) 마일스톤 상태 (M1~M5)

| Milestone | 상태 | 현재 코드 반영 | 잔여 갭 |
| --- | --- | --- | --- |
| M1 Layer Contract | 부분완료 | evidence packet 스키마/검증, quality contract 기록 | 섹션 앵커 표준/validator 고도화 |
| M2 Structured Synthesis(AST) | 부분완료 | `section_ast.py` 존재, orchestration 연동 일부 | section-level rewrite를 기본 경로로 승격 필요 |
| M3 Validation Interface | 부분완료 | heuristic signals + gate + contract consistency | benchmark/contract 정합 자동 수렴 루프 미완 |
| M4 FederHav Governor 고도화 | 부분완료 | Phase B 계열(runtime tools/action plan) 진행 | Phase C(수렴/예산/다중 서브에이전트) 본격화 필요 |
| M5 Benchmark Harness | 부분완료 | benchmark/gate/compare 도구 + 회귀 테스트 | CI quality gate와 장문 샘플셋 확장 필요 |

## 3) 진행률 (현재 기준)
- P0(core): `100%`
- P0+(quality uplift): `100%`
- P1(DeepAgent Phase C): `0%`
- P2(productization): `0%`

## 4) DONE 요약 (20260223 -> 20260224 승계)
- 품질 프로파일 체계 확립:
- `smoke / baseline / professional / world_class` 공통 정책화
- quality contract 정합 개선:
- contract metric source를 `final_signals` 기준으로 정렬
- quality loop 개선:
- profile 기반 iteration plan + plateau 조기수렴 + quality focus directives
- 후보 선택 개선:
- gate pass/failure distance 기반 ranking 도입
- 진단 도구 확장:
- `report_quality_profile_compare.py` (프로파일 매트릭스)
- 버전 일관성 체계 도입:
- `tools/check_version_consistency.py` + 테스트
- 문서 반영:
- `docs/report_quality_threshold_policy.md` 작성
- `docs/development_workflow_guide.md`에 버전 정합 체크 절차 반영
- Iter 101~120 반영:
- 품질 휴리스틱의 비정상 감점 구간 보정(섹션 alias 인식 + non-content 섹션 제외)
- QC 샘플 재측정: `overall 91.05 / claim_support 72.73 / unsupported 6 / coherence 92`
- world_class gate PASS 확인:
- `test-results/p0_quality_gate_report_qc_iter120_world.md`
- 회귀 테스트 통과:
- quality 관련 테스트 묶음 `31 passed`
- Iter 121 반영:
- Data Scientist 분석 단계(근거/출처/해석 가드레일) 추가:
  - `prompts.build_data_scientist_prompt(...)`
  - evidence 이후 `analysis_notes.md` 생성 및 writer/quality 컨텍스트 주입
  - 관련 엔트리: `src/federlicht/orchestrator.py`, `src/federlicht/agent_info_impl.py`
- 보고서 "목록으로" 링크 경로 안정화:
  - 생성기 기준 `../../report_hub/index.html` 우선 + 다중 후보 probe
  - 반영 파일: `src/federlicht/render/html.py`, `src/federlicht/templates/preview_default.html`
- 기존 QC 보고서 실파일 즉시 보정:
  - `site/runs/20260221_QC_report/report_full_iter51.html`
- 테스트:
  - `tests/test_report_prompt_quality_policy.py` 확장
  - `tests/test_render_back_link.py` 추가
  - 회귀 통과: 49 passed(관련 묶음)
- Iter 122 반영:
- 품질 휴리스틱 인용 인식 범용화:
  - `https://...`/`[n]` 외에 도메인 라벨(`openclaw.ai`), archive/run 경로(`.../archive/...txt`, `runs/...`), DOI, escaped numeric citation(`\\[1\\]`) 인식 추가.
  - 반영: `src/federlicht/report.py::_count_citations`
- unsupported 감지 과대계수 보정:
  - HTML claim 후보에서 `tr` 기반 표 구조 텍스트 제외(내러티브 블록 `p/li` 중심).
  - `(제안)/(해석)/(전망)` 등 인식론적 표식 문장을 unsupported claim 집계에서 제외.
  - 반영: `src/federlicht/report.py::_iter_quality_claim_candidates`, `_is_substantive_claim_candidate`
- 테스트 확장:
  - `tests/test_report_quality_heuristics.py`
  - 회귀 통과: `20 passed`
- 다중 run world_class gate 재검증 PASS:
  - `test-results/p0_quality_gate_multi_iter122_world.md`
  - avg: `overall 93.42 / claim_support 81.48 / unsupported 6.00 / section_coherence 90.67`
- Iter 123~132 반영 (10-iter batch):
- P0Q-3 contract-benchmark 수렴 자동화 완료:
  - quality contract metric version 체계 도입:
    - `src/federlicht/quality_contract.py`
    - `QUALITY_CONTRACT_METRIC_VERSION = qc-metrics.v2`
  - orchestrator가 최신 contract에 `metric_version` 기록:
    - `src/federlicht/orchestrator.py` (`quality_contract.latest.json`)
  - quality gate 도구의 stale contract 자동 판정/스킵 정책 도입:
    - `tools/run_report_quality_gate.py`
    - legacy source(`selected_eval`) 또는 `metric_version` 누락/불일치 시 consistency FAIL이 아닌 `stale skip` 처리
    - gate report에 `skipped/stale/stale_reason/metric_version` 명시
- 런타임 안정성 버그 수정:
  - Data Scientist 단계에서 stage budget 인자 불일치(`min_budget/max_budget`)로 중단되던 오류 수정
  - deep 모드에서 `condensed` 참조 가능성(미정의) 제거
  - 반영: `src/federlicht/orchestrator.py`
- 테스트:
  - 추가: `tests/test_quality_contract.py`
  - 확장: `tests/test_report_quality_contract_consistency_tool.py`
  - 회귀: `26 passed` (`quality_contract`, gate/iteration, pipeline e2e 핵심 묶음)
- Codex 모델 실샘플 생성/평가:
  - 생성: `site/runs/openclaw/report_full_iter123_codex_brief.html`
  - 스냅샷: `test-results/p0_sample_openclaw_iter123_codex_snapshot.html`
  - world_class gate: PASS
    - `test-results/p0_quality_gate_openclaw_iter123_codex_world.md`
    - signals: `overall 96.53 / claim_support 97.22 / unsupported 1 / coherence 100`

## 5) 충돌/리스크/미진점

### A. 충돌
- `품질 점수 대폭 상승` vs `실제 본문 품질 향상분 검증 필요`:
- 해결 정책: 점수 보정 자체를 목표로 두지 않고, 다음 iter에서 실제 생성 결과(신규 run) 교차검증 병행

### B. 리스크
- stale contract(구버전 run)는 consistency 비교에서 `stale skip`으로 처리되므로,
  운영 리포트에서 stale 비율이 높으면 재생성 배치를 계획해야 함

### C. 미진점
- section-level synthesis/repair를 기본 작성 경로로 승격하지 못함
- FederHav Phase C(예산·수렴 기반 governor) 본격 구현 미착수
- Federnett 대규모 모듈 분리(`app.js`)는 아직 백로그
- 도메인/경로 인식 확대로 citation 계수가 과대평가될 가능성 -> 샘플셋 확대 검증 필요

## 6) TODO 재설정 (동일 원칙 유지)

### P0+ (최우선)
- P0Q-1. baseline 안정 통과 회복
- 상태: `완료`
- 결과: QC 샘플 기준 baseline/professional/world_class 모두 PASS
- P0Q-2. writer/evidence 루프 품질 튜닝
- 목표: revise pass마다 `quality_pass_trace` 개선폭이 실제 양(+)이 되도록 보정
- 수단: critic/reviser 지시문과 evidence packet 압축 정책 재설계
- 상태: `완료`
- 결과: metric version tagging + stale contract skip 정책 적용
- P0Q-4. 문서 수준 uplift (신규/상향)
- 목표: 섹션당 심층 서술(3~5+ 문단), 표/다이어그램/정량 해석의 자연스러운 통합, 톤 일관성 확보
- 구현축:
  - Data Scientist 분석 노트(`analysis_notes.md`)를 writer 기본 입력으로 사용
  - visuals(표/다이어그램) 생성을 "선택적 장식"이 아니라 근거-해석 연결 자산으로 승격
  - figure/table caption에서 데이터 출처·해석 근거를 자연문으로 설명(라벨형 문구 금지)
- 검증축:
  - QC / openclaw / physical_ai 3개 축으로 world_class gate + 본문 수기 리뷰 병행
- 상태: `1차 완료`
- 결과: Codex 샘플(openclaw brief)에서 world_class PASS + high claim-support 확인
- 잔여: deep 장문(3~5+ 문단/섹션)에서 동일 수준 재현 검증 필요

### P1
- FederHav DeepAgent Phase C 착수
- governor convergence 조건(`delta_threshold`, `budget`, `max_iter`) 도입

### P2
- CI 품질 게이트 통합
- 장문 벤치마크 세트 확대
- Federnett UI 모듈 분리/가독성 회귀 자동검증

## 7) Iter 맥락 요약 (상세 로그는 20260223 참조)
- Iter 1~25: 스키마/게이트/벤치마크 기초 구축
- Iter 26~50: 품질 게이트 루프 연결 및 계약 산출물 정착
- Iter 51~75: world-class 미달 원인 탐지 + consistency/fallback 안정화
- Iter 76~90: quality profile/loop convergence/profile compare 체계 확립
- Iter 91~100: gate-distance ranking + 버전 일관성 정책 자동검증 도입
- Iter 101~120: quality heuristic calibration (section semantic alias + non-content exclusion), QC world_class gate pass 회복

## 8) 코드/문서 일관성 체크 (2026-02-24 기준)
- 버전 일관성:
- `README.md`, `pyproject.toml`, `CHANGELOG.md`, `src/federlicht/versioning.py` -> `1.9.29` 일치
- 검증 명령:
- `python tools/check_version_consistency.py` -> PASS
- 최근 테스트 스냅샷:
- 품질 회귀 스위트(핵심 묶음) `31 passed`
- QC world_class gate: `PASS` (`test-results/p0_quality_gate_report_qc_iter120_world.md`)

## 9) Codex Iter 운영 규칙 (재확정)
- 5 iter마다: 진행률/검증/리스크/다음 액션을 handoff에 기록
- iter 배치 종료 시점에만 commit/push (사용자 별도 지시 예외)
- 버전 변경이 있으면:
- README + CHANGELOG + pyproject + versioning 동시 반영
- `tools/check_version_consistency.py` 통과 필수

## 10) 클론 환경에서 작업 재개 시 필수 문서 세트

### 필수(최소)
- `docs/codex_handoff_20260224.md`: 현재 목표/진행률/즉시 TODO
- `docs/development_workflow_guide.md`: iter/commit/정리 규칙
- `docs/codex_resume_guide.md`: 새 clone 재개 체크리스트/문서 구성 원칙
- `docs/dev_history/README.md`: 과거 개발 이력 인덱스/버전별 요약
- `docs/report_quality_threshold_policy.md`: 품질 점수 해석/게이트 기준
- `CHANGELOG.md`: 최근 반영 이력
- `README.md`: 실행/구성 개요

### 권장(상세 전략)
- `docs/federhav_deepagent_transition_plan.md`
- `docs/federnett_roadmap.md`
- `docs/run_site_publish_strategy.md`
- `docs/ppt_writer_strategy.md`

### 재개 시 확인해야 할 핵심 정보
- 현재 목표 레벨(P0+/P1/P2), 진행률, 차단 이슈
- 최근 5~10 iter에서 실패한 품질 축(예: unsupported/coherence)
- 실행/테스트 표준 명령과 통과 기준
- 버전 일관성 상태와 릴리스 스냅샷

## 11) 다음 Iter 제안 (P1 착수)
- Iter-133: FederHav Phase C governor convergence 최소 루프(δ-threshold + max_iter) 구현
- Iter-134: stage budget 정책을 phase governor와 연결(예산 초과 시 자동 축약)
- Iter-135: section-level rewrite 기본 경로 승격 실험(기본 ON, 실패시 fallback)
- Iter-136: deep 장문 Codex 샘플(QC) 재생성 + world_class + 수기 리뷰 병행
- Iter-137: openclaw/physical_ai deep 장문 재생성 + 비교 리포트
- Iter-138: P1 중간점검 + handoff 갱신 + commit/push

## 12) Docs 구조 운영 (2026-02-24 정리본)
- Active docs(현재 운영):
- `docs/codex_handoff_20260224.md`
- `docs/development_workflow_guide.md`
- `docs/codex_resume_guide.md`
- `docs/report_quality_threshold_policy.md`
- Historical docs(과거 이력):
- `docs/dev_history/handoffs/` (과거 handoff 원문)
- `docs/dev_history/images/` (과거 스크린샷)
- `docs/dev_history/version_summary.md` (버전 중심 요약)
- 규칙:
- 과거 handoff는 `docs/` 루트에 두지 않고 `docs/dev_history/handoffs/`로 이동 유지
- 새 날짜 handoff만 `docs/` 루트의 단일 canonical 파일로 운영
