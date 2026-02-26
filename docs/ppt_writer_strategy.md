# PPT Writer Strategy (Draft)

Last updated: 2026-02-26

## 진행률 체크 (2026-02-26)
- Overall: **51% (Phase 1 완료 + Phase 2 진행 + Phase 3 중반 + Phase 4 착수)**
- 기준: 각 Phase를 동일 가중치로 집계

| Phase | 상태 | 진행률 | 체크 기준(완료 정의) |
| --- | --- | --- | --- |
| Phase 1: schema + planner/composer JSON contract | 완료 | 100% | slide outline/ast 계약 모듈 + 스키마 + 단위테스트 통과 |
| Phase 2: minimal pptx renderer | 진행중 | 75% | 텍스트/표/이미지 렌더 + smoke tests |
| Phase 3: mermaid/d2 + quality loop | 진행중 | 65% | 다이어그램 snapshot + slide quality evaluator |
| Phase 4: Federnett publish/hub 확장 | 진행중 | 15% | deck artifact 게시 플로우/인덱스 반영 |
| Phase 5: FederHav partial patch API | 미시작 | 0% | 슬라이드 단위 patch 액션 + 승인 후 재렌더 자동화 |

### 최근 반영(Phase 1)
- `src/federlicht/slide_pipeline.py`
  - `build_slide_outline`, `build_slide_ast` 계약 구현
  - `validate_slide_outline`, `validate_slide_ast` 검증기 구현
  - outline/ast 요약 formatter 구현
- `src/federlicht/schemas/slide_outline_v1.schema.json`
- `src/federlicht/schemas/slide_ast_v1.schema.json`
- `tests/test_slide_pipeline.py`
  - 계약 생성/검증/포맷터 단위테스트 추가

### 최근 반영(Phase 2 진행)
- `src/federlicht/pptx_renderer.py`
  - `render_slide_ast_html`: slide AST -> deck HTML 렌더
  - `render_slide_ast_pptx`: slide AST -> PPTX 렌더(의존성 미설치 시 안전 fallback)
  - `render_slide_ast_bundle`: html/pptx 동시 산출 메타 반환
- `src/federlicht/pipeline_runner_impl.py`
  - `--output *.pptx` 경로에서 deck 렌더러 호출
  - `report_notes/slide_outline.v1.json`, `slide_ast.v1.json` 자동 기록
  - PPTX 미지원 환경에서 HTML deck fallback + 상태 메타 기록
- `tests/test_pptx_renderer.py`
  - HTML 렌더 smoke
  - PPTX 의존성 미설치 fallback 동작 검증
  - bundle 메타/산출물 검증
- `tests/test_pipeline_runner_impl.py`
  - deck output helper/slide count 규칙/HTML fallback 검증 추가

### 최근 반영(Phase 3 착수)
- `src/federlicht/slide_quality.py`
  - slide AST 품질 요약기(`traceability`, `density`, `narrative_flow`, `visual_integrity`, `overall`) 추가
  - quality gate pass/fail 및 리포트 텍스트 생성기 추가
- `src/federlicht/pipeline_runner_impl.py`
  - deck export 시 `slide_quality.summary.json`, `slide_quality.md` 자동 기록
  - deck 메타에 quality score/gate 상태 포함
- `tests/test_slide_quality.py`
  - 균형 deck PASS / 비정상 deck FAIL 케이스 검증

### 최근 반영(Phase 3 확장)
- `src/federlicht/pptx_renderer.py`
  - diagram block(mermaid/d2) snapshot SVG 물질화 경로 추가
  - bundle 메타에 `diagram_snapshot_count/paths/errors` 기록
  - HTML deck에서 snapshot 이미지를 우선 렌더하고, 실패 시 spec fallback 유지
- `src/federlicht/pipeline_runner_impl.py`
  - deck 메타에 diagram snapshot 수/경로/오류 집계 추가
- `tests/test_pptx_renderer.py`
  - mermaid snapshot 렌더 삽입 검증(모킹 기반) 추가

### 최근 반영(Phase 3 quality loop)
- `src/federlicht/slide_quality.py`
  - `revise_slide_ast_for_quality(...)` 추가
  - 품질 게이트 실패 시 intro/summary anchor, ref 보강, 빈 block 보정, 과도 텍스트 trim
- `src/federlicht/pipeline_runner_impl.py`
  - deck export 시 quality fail이면 1회 자동 보정 + 재평가
  - `report_notes/slide_quality.trace.json` 기록
  - run meta에 `deck_quality_iterations`, `deck_quality_actions`, `deck_quality_trace_path` 포함
- `tests/test_slide_quality.py`
  - auto-revision으로 quality score 개선되는 케이스 검증 추가

### 최근 반영(Phase 4 착수)
- `src/federlicht/pipeline_runner_impl.py`
  - PPTX deck 경로에서 hub manifest entry 작성 로직 추가
  - HTML deck을 기본 artifact로, PPTX를 companion artifact로 paths에 동시 기록
  - deck manifest entry id를 `run_name-deck`으로 분리해 기존 report entry와 충돌 방지
- `tests/test_pipeline_runner_impl.py`
  - deck manifest entry의 companion path(`deck_html`, `deck_pptx`) 검증 추가

### 지속 체크 방법
- 단계 완료 시마다 아래를 고정 수행:
  1. `pytest -q tests/test_slide_pipeline.py tests/test_pptx_renderer.py`
  2. 관련 회귀 묶음 실행
  3. 본 문서의 `진행률 체크` 표 갱신

### 최신 체크 결과
- `2026-02-26`: `pytest -q tests/test_slide_pipeline.py tests/test_pptx_renderer.py tests/test_slide_quality.py tests/test_pipeline_runner_impl.py` -> `19 passed`
- `2026-02-26`: `pytest -q tests/test_federlicht_cli_args.py tests/test_version_consistency_tool.py` -> `4 passed`

## 목표
- Federlicht가 보고서뿐 아니라 **슬라이드형 결과물(PPTX/slide HTML/PDF)** 을 같은 파이프라인에서 생성하도록 확장한다.
- 핵심은 "템플릿 강제"가 아니라, 요청 목적과 depth에 맞는 슬라이드 구조를 에이전트가 계획/조정하는 것이다.

## 현재 구현 상태
- 입력 측면:
  - `.pptx` 텍스트 읽기: `src/federlicht/readers/pptx.py`
  - `.pptx` 이미지 추출 및 figure 연계: `src/federlicht/report.py`
- 미구현:
  - 슬라이드 전용 계획(agent node)
  - 슬라이드 레이아웃/컴포넌트 모델
  - pptx 최종 렌더러(작성기)
  - 슬라이드 품질 critic/evaluator

## 제안 아키텍처
1. `slide_planner` (new stage/subagent)
- 입력: report prompt, depth, audience, time budget
- 출력: slide outline JSON
  - `slide_id`, `intent`, `key_claim`, `evidence_refs`, `visual_type(table/diagram/image/bullets)`

2. `slide_composer` (new stage/subagent)
- 입력: outline + evidence packet
- 출력: slide AST(JSON)
  - title block, body blocks, table spec, diagram spec(mermaid/d2), citation footer

3. `pptx_renderer` (tool/module)
- 입력: slide AST + style pack
- 출력: `.pptx` + optional `.html` slide deck + export metadata

4. `slide_quality` (quality loop extension)
- 평가 축:
  - claim-evidence traceability
  - slide density/readability
  - narrative flow(도입-근거-결론)
  - visual correctness(table/diagram integrity)

## Federnett/FederHav 연계
- Federnett:
  - output format 선택(`html`, `pdf`, `pptx`, `all`)
  - run 승인 후 `report_hub` publish와 동일하게 `deck_hub` 또는 hub 내 deck artifact 게시
- FederHav:
  - "이 보고서를 12장 의사결정용 브리핑으로 변환" 같은 후속 요청을 대화형으로 처리
  - slide별 톤/난이도(임원용/기술위원회용) 재작성 지원
  - 특정 슬라이드/요소만 부분 수정(예: 4번 슬라이드 표만 업데이트, 결론 슬라이드 톤 완화) 가능한 액션 제공

## 부분 산출물/인스턴스 조정 전략
- 단일 output 전체 재생성 대신, slide/component 단위 patch를 허용한다.
- 권장 구조:
  - `artifacts/deck/<deck_id>/slides/<slide_id>.json`
  - `artifacts/deck/<deck_id>/components/<component_id>.json`
  - `artifacts/deck/<deck_id>/rendered/*.pptx|*.html|*.pdf`
- FederHav는 변경 요청을 다음 액션으로 분해:
  - `update_slide_text`
  - `replace_table_data`
  - `swap_diagram_type` (mermaid <-> d2)
  - `retheme_slide_pack`
- 변경 이력은 run 로그 + `deck_change_log.jsonl`로 남겨 추적성을 유지한다.

## 구현 단계(권장)
1. Phase 1: schema + planner/composer JSON contract 고정
2. Phase 2: minimal pptx renderer(텍스트/표/이미지) + smoke tests
3. Phase 3: mermaid/d2 snapshot 삽입 + quality loop 통합
4. Phase 4: Federnett UI publish flow 및 hub index 확장
5. Phase 5: FederHav 대화형 partial patch API + 승인 후 재렌더링 자동화

## 리스크
- 과도한 템플릿 강제는 유연성 저하를 유발하므로, `template_rigidity`와 동일한 강도 제어를 slide pipeline에도 적용해야 한다.
- 모델/토큰 비용이 커질 수 있어, slide planner와 composer 사이에 compact claim packet을 재사용해야 한다.
