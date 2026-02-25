# Codex Unified Handoff - 2026-02-25

Last updated: 2026-02-25 10:31:48 +09:00  
Previous handoff (archived): `docs/dev_history/handoffs/codex_handoff_20260224.md`

## 1) 목적 (고정)
- 최상위 목표: `(World-Class) Professional Research Level Report Quality`
- 원칙:
- 정형 템플릿 강제보다 **에이전트 협업 구조(Scout/Plan/Evidence/Writer/Quality)** 최적화 중심
- 근거 추적성(Claim-Evidence-Source) + 반복 개선 가능성 + 운영 안정성 동시 달성

## 2) Iter 운영 기준 (20260225 리셋)
- Iter count는 오늘부터 `0`에서 재시작한다.
- 기록 단위:
  - 5 iter마다 handoff 진행률/변경점/리스크 업데이트
  - 20 iter마다 샘플 보고서 생성 + world-class gate 측정 + 수기 리뷰 메모
- 배치 종료 시점에만 commit/push (사용자 요청 예외)

## 3) 운영 정책 (신규 고정)
- **게이트 측정 입력은 반드시 같은 배치에서 “새로 생성한 보고서”여야 한다.**
  - 금지: 과거 보고서만 재평가해서 품질 상승을 주장하는 방식
  - 허용: 회귀 점검 목적의 과거 보고서 재측정(별도 표기 필수)
- 보고서 생성 시 프롬프트 다양성 정책:
  - 동일 주제라도 독자/톤/설명수준을 바꾼 3개 변형 샘플을 순환 적용
  - 예: 기술리더 대상 / 일반 독자 친화 / 대학교 수업 수준
- 보고서 생성 산출물과 gate 결과(`test-results`)를 함께 버전 관리한다.

## 4) 마일스톤 상태 (M1~M5)

| Milestone | 상태 | 현재 코드 반영 | 잔여 갭 |
| --- | --- | --- | --- |
| M1 Layer Contract | 부분완료 | evidence packet 스키마/검증, quality contract 기록 | 섹션 앵커 표준/validator 고도화 |
| M2 Structured Synthesis(AST) | 부분완료 | `section_ast.py` 존재, orchestration 연동 일부 | section-level rewrite 기본 경로 승격 |
| M3 Validation Interface | 부분완료 | heuristic signals + gate + contract consistency | benchmark/contract 수렴 자동화 고도화 |
| M4 FederHav Governor | 부분완료 | Phase-B + Phase-C(초기) 수렴 루프/로그 브릿지 연동 | 정책 기반 governor 설정 UI 연동 |
| M5 Benchmark Harness | 부분완료 | benchmark/gate/compare 도구 + 회귀 테스트 | CI 품질게이트 + 장문 샘플셋 확장 |

## 5) 진행률 (리셋 기준)
- P0(world-class sustain v2): `100% (완료)`
- P1(DeepAgent Phase C): `36%`
- P2(productization): `0%`

## 6) DONE (전일 승계 핵심)
- FederHav governor loop 도입 + `execution_handoff.governor_loop` 메타 확장
- governor 메타를 Federnett Live Logs(로그 브릿지/trace chip)에 노출
- stream fallback에서도 trace step을 Live Logs에 재주입
- QC/openclaw/physical_ai world-class gate PASS(단, 기존 보고서 기준 재측정)
- 운영정책 문서에 "동일 배치 신규 생성물 gate 측정" 규칙 고정
- 신규 codex 생성 + gate 검증 완료(동일 배치):
  - 기술리더 톤: `site/runs/openclaw/report_full_iter001_codex_leader.html`
  - 일반독자 톤: `site/runs/20260221_QC_report/report_full_iter002_codex_general.html`
  - 수업형 톤: `site/runs/physical_ai_insight/report_full_iter003_codex_classroom.html`
- 신규 world-class gate PASS 결과:
  - `test-results/p0_quality_gate_openclaw_iter001_world.md`
  - `test-results/p0_quality_gate_qc_iter002_world.md`
  - `test-results/p0_quality_gate_physical_iter003_world.md`
- P0-2 보강(코드):
  - `compute_heuristic_quality_signals`에 `narrative_density_score` 신호 추가
  - deep/research 계열 가중치에 서술 밀도 반영
  - 회귀 테스트 추가: `tests/test_report_quality_heuristics.py::test_narrative_density_rewards_deeper_reports_in_deep_mode`
- 온프렘/클라우드 자동 LLM 기본정책 반영:
  - `src/federnett/routes.py`에서 `OPENAI_BASE_URL` 기반 deployment mode 감지
  - on-prem 기본 모델 맵(`Qwen3/Llama-4`) + cloud 기본(`gpt-5-nano`, federhav `gpt-4o-mini`)
  - `/api/info`에 `llm_defaults.deployment_mode`, `recommended_model_options`, `onprem_policy` 노출
- FederHav 런타임 기본모델 정책 반영:
  - `src/federhav/agentic_runtime.py`에서 on-prem 감지 시 `Qwen3-235B-A22B-Thinking-2507` 기본 사용
  - 회귀 테스트 추가: `tests/test_federhav_agentic_runtime.py` (on-prem/public API 분기)
- CDN 장애/지연 대응 로컬-first 로더 반영:
  - `src/federlicht/render/html.py` MathJax/Mermaid 스크립트 로더를 local->cdn 순으로 변경
  - `site/federnett/app.js` Mermaid 로더를 후보 체인 기반 폴백으로 변경
  - vendor 자산 포함: `site/federnett/vendor/mathjax/tex-svg.js`, `site/federnett/vendor/mermaid/mermaid.min.js`
- `gpt-5-nano` 샘플 보고서 생성+게이트 PASS:
  - `site/runs/openclaw/report_full_iter004_gpt5nano_leader.html`
  - `test-results/p0_quality_gate_openclaw_iter004_gpt5nano_world.md`
  - `site/runs/20260221_QC_report/report_full_iter005_gpt5nano_general.html`
  - `test-results/p0_quality_gate_qc_iter005_gpt5nano_world.md`
- 구조 정규화 패치:
  - `src/federlicht/orchestrator.py`에서 `coerce_required_headings`/`coerce_repair_headings`를 확장
  - `###` 승격뿐 아니라 단독 섹션 라벨(`Executive Summary` 등)도 `##`로 자동 정규화
  - 효과: brief 보고서의 section coverage/coherence 하락 이슈 완화
- KO 우선 신규 생성물 world-class PASS(동일 배치):
  - 리더 톤(gpt-5-nano): `site/runs/openclaw/report_full_iter008_gpt5nano_ko_world.html`
  - 일반독자 톤(gpt-5.2): `site/runs/20260221_QC_report/report_full_iter013_gpt52_ko_general_world.html`
  - 수업형 톤(gpt-5.2): `site/runs/physical_ai_insight/report_full_iter015_gpt52_ko_classroom_world.html`
  - deep/decision 보강(gpt-5.2): `site/runs/openclaw/report_full_iter016_gpt52_ko_deep_world.html`
  - gate 결과:
    - `test-results/p0_quality_gate_openclaw_iter008_gpt5nano_ko_world.md`
    - `test-results/p0_quality_gate_qc_iter013_gpt52_ko_world.md`
    - `test-results/p0_quality_gate_physical_iter015_gpt52_ko_world.md`
    - `test-results/p0_quality_gate_openclaw_iter016_gpt52_ko_world.md`
- P0-1~P0-4 완료 판정:
  - P0-1: 신규 생성물 기준 gate 운영 고정 유지
  - P0-2: deep 샘플(`iter016`)에서 world-class PASS
  - P0-3: deep 경로에서 시각화 통합(비교표/mermaid) 확인
  - P0-4: 3톤(리더/일반/수업형) KO 샘플 world-class PASS 확보

## 7) TODO (P0/P1/P2)

### P0 (world-class sustain v2)
- 상태: `완료(2026-02-25 10:31 +09:00)`
- 후속 유지보수 항목(회귀 감시):
  - 모델별 quality loop 퇴행(critique 텍스트가 본문을 덮어쓰는 현상) 감시/회귀 테스트 강화
  - KO 톤 샘플 20 iter 주기 재생성 + gate 재검증

### P1 (FederHav DeepAgent Phase C)
- governor 정책의 workspace LLM settings 연동(환경변수 의존 축소)
- planning-execution loop 고도화(수렴/예산/trace 계약 일관화)
- 턴 단위 로그 브릿지 요약 카드 개선
- quality loop 안정화:
  - `gpt-5-nano`에서 critique/revision 초안이 최종 본문을 오염시키는 퇴행 경로 차단
  - final selection 시 섹션 완결성/required section 우선 가중

### P2 (Productization)
- CI 품질 게이트 통합
- 장문 벤치마크 세트 확대 + stale run 재생성 정책
- Federnett UI 모듈 분리 및 가독성 회귀 자동검증

## 8) 충돌/리스크
- 품질 점수와 실제 서술 품질 간 괴리 위험:
  - 대응: 20 iter마다 샘플 생성물 수기 리뷰를 게이트 결과와 함께 기록
- stale contract 비율 증가 위험:
  - 대응: stale run 재생성 배치 정책 수립
- codex_cli 생성 시간 리스크(brief 기준 10~14분/보고서):
  - 대응: 20 iter 배치에서 3개 샘플은 유지하되, 각 샘플은 `depth=brief` + quality stage 생략 후 외부 gate로 검증
- 시각화 삽입률 리스크(현재 baseline 3/3 보고서에서 실제 `<figure>` 0건):
  - 대응: P0-3에서 figure/diagram 생성 트리거를 명시하고 미삽입 사유를 로그에 기록
- 모델별 quality loop 변동성 리스크:
  - 대응: nano 계열은 quality loop 보수 운영(또는 상위 모델 fallback), 선택기 회귀 테스트 추가

## 9) 필수 참조 문서
- `docs/development_workflow_guide.md`
- `docs/codex_resume_guide.md`
- `docs/report_quality_threshold_policy.md`
- `docs/dev_history/README.md`

## 10) Iter 로그 (당일)
- Iter 1~5 완료 (2026-02-25 01:13 +09:00)
  - 운영정책 반영 + 문서 기준점(20260225) 확정
  - 동일 배치 신규 생성물 3종 + world-class gate PASS 확인
  - P0 진행률 `33% -> 49%`
- Iter 6~10 완료 (2026-02-25 01:25 +09:00)
  - 서술 밀도 품질신호(`narrative_density_score`)를 품질계약에 통합
  - 품질 휴리스틱/게이트 회귀 테스트 통과(17 passed)
  - 동일 신규 생성물 3종 gate 재측정 PASS 유지
  - P0 진행률 `49% -> 58%`
- Iter 11 완료 (2026-02-25 06:29 +09:00)
  - on-prem/cloud LLM 기본정책 자동감지 + `/api/info` 기본정책 메타 확장
  - MathJax/Mermaid 로컬-first CDN 폴백 체인 반영(offline/on-prem 지연 완화)
  - `gpt-5-nano` 샘플 생성/게이트 PASS 확인
  - 회귀 테스트 통과(34 passed), P0 진행률 변화 없음(`58%`)
- Iter 12 완료 (2026-02-25 06:40 +09:00)
  - `gpt-5-nano` QC 샘플 추가 생성 + world-class gate PASS
  - 샘플 다각화(리더/일반독자 톤) 2건 확보
  - P0 진행률 변화 없음(`58%`)
- Iter 13~16 완료 (2026-02-25 10:31 +09:00)
  - `orchestrator` 섹션 헤딩 정규화 패치 적용(plain section label -> H2)
  - KO 우선 신규 샘플 생성/게이트:
    - `openclaw iter008 (gpt-5-nano, leader)` PASS
    - `QC iter013 (gpt-5.2, general)` PASS
    - `physical iter015 (gpt-5.2, classroom)` PASS
    - `openclaw iter016 (gpt-5.2, deep/decision)` PASS
  - P0 진행률 `58% -> 100%` 및 완료 처리

## 11) 다음 Iter 계획 (즉시)
- P1 Phase-C 집중:
  - governor 정책/수렴 규칙을 LLM Settings와 일관 연결
  - 턴별 로그 브릿지 품질 개선(요약 카드 + 원로그 가독성)
  - quality loop 안정성 회귀 테스트(특히 nano 계열)
- 운영:
  - 5 iter마다 handoff 업데이트
  - 20 iter마다 KO 샘플 3종 재생성 + world-class gate 재검증
