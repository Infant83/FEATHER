# Codex Unified Handoff - 2026-02-27

Last updated: 2026-02-27 00:20 +09:00  
Previous handoff (archived): `docs/codex_handoff_20260226.md`

## 1) 목적 (고정)
- 최상위 목표: `(World-Class) Professional Research Level Report Quality` 유지
- 확장 목표:
  - 리포트 + 인포그래픽 + deck(PPTX/HTML)를 단일 파이프라인으로 일관 생성
  - Claim-Evidence-Source 추적성과 재현성(`report_notes/*`)을 artifact까지 보존
- 원칙:
  - 품질 게이트 수치 기반(pass/fail) 운영
  - 자동 보정 루프는 1회 기본, trace 파일 필수 기록
  - 배포(hub/site index) 경로는 report/deck 충돌 없이 분리 ID 사용

## 1-1) 정책 강화 (2026-02-27)
- 우선순위 전환:
  - `PPTX 작성기(writer)` 확장보다 `PPTX 읽기(reader)/관리` 강화에 우선 투자
  - deck는 PPTX binary 자체보다 `PPTX 스타일 HTML 렌더` 품질을 우선 목표로 운영
- 실행 원칙:
  - PPTX는 ingestion/근거 추출/슬라이드 구조 해석의 입력 자산으로 표준화
  - 시각 요소는 HTML 아트워크(mermaid/d2/chart/infographic)로 품질 반복 개선
  - 최종 보고서 품질 개선은 HTML 스타일(가독성, 흐름, 시각 근거 배치)을 1순위로 수행
- 운영 정책:
  - PPTX export는 유지하되, 실패 시 HTML deck fallback을 표준 경로로 간주
  - 품질 게이트/수기 리뷰의 기본 산출물도 HTML 기준으로 기록

## 2) 현재 스냅샷
- 기준 브랜치: `main`
- 최신 반영 커밋:
  - `a470fa2` - slide deck pipeline Phase 1~4 bootstrap + quality loop
  - `fd40f81` - artwork 상대 run_dir 경로 버그 수정 + 회귀 테스트 추가
- 주요 상태:
  - 보고서 품질 게이트(world_class) 운영 안정
  - deck 품질 루프(초기 FAIL -> auto-revision PASS) 동작 확인
  - deck manifest entry(`run_name-deck`) 및 companion path(`deck_html`, `deck_pptx`) 반영 완료

## 3) 진행률 재정렬 (2026-02-27 기준)

### 트랙별 진행률
- P0 (world-class sustain): `100%` (완료, 유지 모드)
- P1 (DeepAgent + section rewrite UX): `47%` (변동 없음)
- P2 (Productization + infographic pipeline): `91%` (안정화 단계)
- P3 (PPT writer / deck pipeline): `53%` (Phase 3 안정화 + Phase 4 착수)

### P3 상세(Deck)
| Phase | 상태 | 진행률 | 완료 기준 |
| --- | --- | --- | --- |
| Phase 1: schema + planner/composer contract | 완료 | 100% | outline/ast 스키마 + validator + tests |
| Phase 2: minimal renderer | 진행중 | 75% | html/pptx 렌더 + fallback + tests |
| Phase 3: diagram snapshot + quality loop | 진행중 | 70% | snapshot + auto-revision + quality trace |
| Phase 4: Federnett publish/hub 확장 | 진행중 | 20% | deck artifact hub/index 반영 E2E |
| Phase 5: FederHav partial patch API | 미시작 | 0% | slide/component patch + 승인 후 재렌더 |

## 4) 이번 주기 핵심 반영 (26 -> 27)
- `src/federlicht/artwork.py`
  - `render_d2_svg`, `render_diagrams_architecture`, `render_mermaid_diagram`에서
    상대 `run_dir` 입력 시 path 계산 실패하던 케이스 수정
  - `_rel_under_run(...)` helper 추가로 절대경로 기준 상대 path 일관화
- `tests/test_artwork_tools.py`
  - `test_render_d2_svg_accepts_relative_run_dir`
  - `test_render_mermaid_accepts_relative_run_dir`
- 문서 갱신
  - `docs/ppt_writer_strategy.md`
  - `CHANGELOG.md`

## 5) 품질/검증 결과 (최신)
- 리포트 게이트:
  - 입력: `site/runs/physical_ai_insight/report_full_iter015_gpt52_ko_classroom_world.html`
  - 실행: `tools/run_report_quality_gate.py --quality-profile world_class`
  - 결과: `PASS`
  - 수치: `overall=89.41`, `claim_support=69.57`, `unsupported=7`, `section_coherence=94.00`
- deck 예제 작업:
  - 산출 경로: `test-results/p0_deck_example_physical_ai_iter015/`
  - 초기 품질: `overall=67.33` (`FAIL`)
  - auto-revision 1회 후: `overall=100.00` (`PASS`)
  - 렌더 상태: `pptx_ok=True`, `html_ok=True`, `diagram_snapshot_count=1`
- 테스트:
  - `pytest -q tests/test_artwork_tools.py` -> `15 passed`
  - `pytest -q tests/test_slide_pipeline.py tests/test_pptx_renderer.py tests/test_slide_quality.py tests/test_pipeline_runner_impl.py` -> `19 passed`

## 6) 리스크 / 잔여 갭
- deck 품질 평가지표가 report world_class와 아직 독립 체계여서, 운영 임계/프로파일 정렬이 필요
- deck publish 경로는 코드 반영 완료 수준이며, 실제 Federnett UI-런타임 E2E 점검이 잔여
- PPTX 의존성(`python-pptx`) 부재 환경에서 fallback은 확보됐지만, 운영 환경별 산출물 편차 점검 필요

## 7) 다음 목표 재설정 (우선순위)
1. PPTX Reader/관리 강화 (신규 최우선)
- 목표:
  - `readers/pptx.py` 중심으로 slide text/image/structure 추출 계약 강화
  - report/deck 파이프라인에서 PPTX provenance 메타(`pptx_path`, slide anchor) 일관화
- 완료 기준:
  - reader 회귀 테스트 + 샘플 PPTX 1건 ingest 검증 + metadata 스냅샷 문서화

2. PPTX 스타일 HTML 렌더/아트워크 고도화
- 목표:
  - slide HTML에서 visual block 품질(typography/layout/figure integrity) 상향
  - diagram/chart/infographic 렌더를 HTML 우선 경로로 표준화
- 완료 기준:
  - 샘플 deck HTML 1건 world-class 수준 수기점검 PASS + 렌더 회귀 테스트 통과

3. HTML 보고서 스타일 고도화
- 목표:
  - 본문 섹션 가독성/전개/시각 근거 블록 배치를 HTML 중심으로 개선
  - report 품질 게이트 결과와 HTML 스타일 개선 항목을 연결 운영
- 완료 기준:
  - quality gate PASS + manual review(md)에서 스타일/근거 배치 기준 충족

4. Phase 4 완결: deck hub/index E2E 검증
- 목표:
  - deck run 결과가 site index에 별도 엔트리(`run_name-deck`)로 기록
  - `deck_html`/`deck_pptx` companion path 노출 확인
- 완료 기준:
  - e2e 테스트 + 샘플 run 1건 PASS + 산출물 링크 검증 문서화

5. Phase 5 착수 준비 (Partial Patch API)
- 목표:
  - `update_slide_text`, `replace_table_data`, `swap_diagram_type` 액션 계약 정의
- 완료 기준:
  - API spec 초안 + 저장 구조(`artifacts/deck/<deck_id>/...`) 샘플 1건

## 8) 운영 규칙 (20260227 배치)
- 5 iter마다: 진행률/리스크/완료 기준 재기록
- 20 iter마다: 샘플 1건 필수
  - report world_class gate
  - deck quality gate(초기 + auto-revision 결과)
  - 필요 시 수기 리뷰 md 추가
- commit/push:
  - 배치 종료 시 1회 원칙(요청 시 예외)

## 9) 즉시 실행 체크리스트
- `pytest -q tests/test_slide_pipeline.py tests/test_pptx_renderer.py tests/test_slide_quality.py tests/test_pipeline_runner_impl.py`
- `pytest -q tests/test_artwork_tools.py tests/test_federlicht_cli_args.py tests/test_version_consistency_tool.py`
- deck e2e sample run 1회 후 아래 기록:
  - `report_notes/slide_quality.summary.json`
  - `report_notes/slide_quality.trace.json`
  - site index 반영 스냅샷 경로
