# Codex Unified Handoff - 2026-02-28

Last updated: 2026-02-28 22:20 +09:00 (iter028 rerun sync)  
Previous handoff (archived): `docs/codex_handoff_20260227.md`

## 1) 목적 (고정)
- 최상위 목표: `(Deep Research) Professional Research Level Report Quality` 유지
- 확장 목표:
  - 리포트 + 인포그래픽 + deck(PPTX/HTML)을 단일 파이프라인으로 일관 생성
  - Claim-Evidence-Source 추적성과 재현성(`report_notes/*`, `test-results/*`) 보장
- 핵심 정책:
  - PPTX는 `writer` 확장보다 `reader/ingest 관리` 강화 우선
  - 출력 품질은 PPTX binary보다 `PPTX-style HTML/artwork`를 우선 기준으로 운영
  - 품질 게이트/수기 리뷰는 HTML 산출물을 기준으로 관리

## 2) 이번 사이클 요약 (2026-02-27~28 반영)
- 릴리즈:
  - `1.9.33` 릴리즈 준비 완료 (version sync + QC iter028 재측정 반영)
  - 버전 동기화: `pyproject.toml`, `src/federlicht/versioning.py`, `README.md`, `CHANGELOG.md`
  - `1.9.32` 배포 완료 (commit: `48e1231`)
  - 버전 동기화: `pyproject.toml`, `src/federlicht/versioning.py`, `README.md`, `CHANGELOG.md`
- QC deep_research 샘플 생성 (Codex 5.3):
  - backend: `FEDERLICHT_LLM_BACKEND=codex_cli`
  - model: `CODEX_MODEL=gpt-5.3-codex`
  - run: `site/runs/20260221_QC_report`
- 샘플/검증 산출물:
  - snapshot: `test-results/p0_sample_qc_iter027_codex53_ko_worldclass_artwork_snapshot.html`
  - prompt: `test-results/p0_prompt_qc_iter027_codex53_worldclass_artwork.txt`
  - gate summary: `test-results/p0_quality_gate_qc_iter027_codex53_world_v4.summary.json`
  - gate report: `test-results/p0_quality_gate_qc_iter027_codex53_world_v4.md`
- iter028 재생성/재측정 산출물 (이번 턴):
  - snapshot: `test-results/p0_sample_qc_iter028_codex53_ko_deepresearch_artwork_snapshot.html`
  - prompt: `test-results/p0_prompt_qc_iter028_codex53_deepresearch_artwork.txt`
  - gate summary: `test-results/p0_quality_gate_qc_iter028_codex53_deepresearch.summary.json`
  - gate report: `test-results/p0_quality_gate_qc_iter028_codex53_deepresearch.md`
  - manual review: `test-results/p0_manual_review_qc_iter028_codex53_deepresearch.md`
- 이번 턴 추가 반영(2026-02-28):
  - Federnett Hub/Index E2E 보강:
    - deck manifest에 `deck_quality(profile/effective_band/overall/gate_pass/iterations)` 포함
    - hub index 링크에 `Deck HTML`, `Deck PPTX` 노출
    - latest/archive 카드 meta에 `DeckQ` 상태(밴드/게이트/점수/iter) 노출
    - legacy manifest fallback: `format=pptx` + `paths.report(.html)`이면 `Deck HTML` 링크 자동 유도
    - legacy flat key(`deck_quality_*`)도 카드에서 품질 요약으로 해석
    - tag 필터/탭/트렌드가 파생 deck 태그(`deck-pass`, `deck-fail`, `deck:<band>`)를 인식하도록 정렬
  - Hub manifest 보정 도구 추가:
    - `tools/normalize_report_hub_manifest.py` 추가 (dry-run/overwrite/summary 지원)
    - 기존 manifest에 대해 dry-run 요약 생성:
      - `test-results/p0_report_hub_manifest_normalize_summary_20260228.json`
  - Deck 품질 프로파일 정렬:
    - `slide_quality`가 `baseline/professional/deep_research` 밴드로 동작
    - report `--quality-profile` 입력을 deck gate까지 동일 전달
  - PPTX reader 계약 고도화:
    - `extract_pptx_slide_contract(...)` 추가 (`schema_version=pptx_ingest.v1`)
    - 필드: `slide_id`, `shape_type`, `content_kind(text/image)`, `source_path`, `anchor`
    - 샘플 리포트 생성:
      - `test-results/p0_pptx_ingest_contract_physical_ai_iter015.json`
      - `test-results/p0_pptx_ingest_contract_physical_ai_iter015.md`
  - Infographic caption 메타 강화:
    - chart 메타 필드 `metric/unit/period/normalization/source` 계약 반영
    - lint에서 위 필드 누락 검출
    - HTML 캡션 라인에 지표 메타를 구조화해 출력
    - placeholder 메타(`unspecified`, `pending mapping` 등)를 lint에서 `placeholder-like`로 검출
    - report embed figcaption에 primary chart 메타(`Metric/Unit/Period/Normalization/Source`) 자동 주입
    - quality gate의 infographic lint 요약에 `caption_meta_coverage_ratio`, complete-chart 비율 추가
  - 품질 프로파일 표준화:
    - canonical profile을 `deep_research`로 고정
    - `world/world_class/world-class/wc`는 legacy alias로만 허용
  - reasoning effort alias 정규화:
    - `normal -> medium`, `extended -> high`
  - 운영 문서/CLI help 동기화:
    - 최신 운영 문서와 게이트 도구 안내를 `deep_research` 기준으로 정렬
  - Mermaid 렌더 안정화:
    - 기존 `<div class="mermaid">...</div>` 블록도 로더 활성화 대상으로 감지
    - raw fenced mermaid(````mermaid`)를 HTML 본문에서도 강제 변환
    - markdown+raw `<section>` 혼합 시 헤딩/코드블록이 평문으로 남는 문제 완화
  - Writer/Finalizer 프롬프트 강화:
    - 라벨형 단답(주장/근거/인사이트) 반복 억제
    - 시각물 앞/뒤 문맥(도입/해석/한계) 강제
    - 인용 무결성(깨진 링크/번호-only 인용) 정리 규칙 강화
  - 품질 휴리스틱 강화:
    - `narrative_flow_score` 신호 추가(전환 문장/라벨 나열/불릿 과밀/섹션 단절 감지)
  - Federnett Live Logs UX:
    - stage별 최신 상태 카드만 노출해 중복 노이즈 축소
    - timeline summary chip(`ok/cache/run/err`) 추가
  - Federnett rewrite_section UX 강화(P1):
    - capability override에 `flow/structure` 힌트 지원 추가
    - rewrite prompt에 narrative flow 규칙(도입 claim -> 근거 해석 -> 전환/함의) 고정
    - 라벨형 단답 나열 억제 규칙을 rewrite prompt constraints에 명시
    - 실행 응답 payload에 `flow_hint` 노출
  - 품질 휴리스틱(P1) 보정:
    - `citation_integrity_score` 신호 추가(깨진 인용/중첩 링크/비정상 href 패턴 탐지)
    - 인용 카운트 집계에서 깨진 인용 패턴 발생 시 citation count 감산 보정
    - 결과적으로 `claim_support/unsupported`가 실제 문장 품질에 더 가깝게 측정되도록 조정
  - HTML 인용 정리 보강(P1):
    - `clean_citation_labels(...)`에서 malformed anchor chain(`href=\"...)[[n]](...\"`) 복구
    - markdown citation wrapper가 anchor를 감싼 패턴 제거
    - URL anchor 뒤 dangling `)` 정리

## 3) 품질 결과 스냅샷
- deep_research gate (iter028 refresh): `PASS`
  - overall: `92.48`
  - claim_support_ratio: `100.00`
  - unsupported_claim_count: `0.00`
  - section_coherence_score: `100.00`
  - narrative_flow_score: `83.96`
  - narrative_density_score: `51.60`
- 수기 리뷰(iter028):
  - 강점: 서술 흐름/근거 매핑/시각 요소 연결 개선
  - 잔여 이슈: SVG `xmlns` attribute에 citation rewrite가 침투한 malformed markup 1건, `인사이트:` 라벨형 반복 4건
- deep_research gate (final v4): `PASS`
  - overall: `93.61`
  - claim_support_ratio: `97.67`
  - unsupported_claim_count: `1.00`
  - section_coherence_score: `100.00`
- 시각 요소 반영 확인:
  - 10년 로드맵 인포그래픽
  - 국가별 투자금액 표+차트
  - 오류율 개선 추세 line chart
  - 큐비트 타입별 레이더 비교
  - Feather -> Federlicht 파이프라인 다이어그램
  - claim-packet 기반 인포그래픽 iframe 자동삽입
- 회귀 재검증(이번 턴):
  - `pytest -q tests/test_capabilities.py` -> `14 passed`
  - `pytest -q tests/test_federnett_routes.py::test_handle_api_post_capabilities_execute_rewrite_section` -> `1 passed`
  - `pytest -q tests/test_artwork_tools.py tests/test_report_quality_gate_runner.py` -> `22 passed`
  - `pytest -q tests/test_report_infographic_insert.py tests/test_report_quality_heuristics.py` -> `18 passed`
  - `pytest -q tests/test_report_prompt_quality_policy.py tests/test_report_quality_heuristics.py tests/test_render_html_mermaid.py` -> `31 passed`
  - `pytest -q tests/test_report_prompt_quality_policy.py tests/test_report_quality_heuristics.py tests/test_quality_profiles.py tests/test_quality_iteration.py tests/test_federlicht_cli_args.py tests/test_report_quality_gate_runner.py tests/test_report_quality_profile_compare_tool.py tests/test_report_quality_regression_gate.py tests/test_slide_quality.py tests/test_pipeline_runner_impl.py tests/test_artwork_tools.py tests/test_readers_pptx_contract.py tests/test_site_hub_index.py tests/test_report_hub_manifest_normalize_tool.py tests/test_capabilities.py` -> `103 passed`
  - `pytest -q tests/test_report_citation_rewrite.py` -> `14 passed`
  - `pytest -q tests/test_report_prompt_quality_policy.py tests/test_report_quality_heuristics.py tests/test_report_citation_rewrite.py tests/test_quality_profiles.py tests/test_quality_iteration.py tests/test_federlicht_cli_args.py tests/test_report_quality_gate_runner.py tests/test_report_quality_profile_compare_tool.py tests/test_report_quality_regression_gate.py tests/test_slide_quality.py tests/test_pipeline_runner_impl.py tests/test_artwork_tools.py tests/test_readers_pptx_contract.py tests/test_site_hub_index.py tests/test_report_hub_manifest_normalize_tool.py tests/test_capabilities.py` -> `118 passed`
  - `python tools/run_report_quality_gate.py --input test-results/p0_sample_qc_iter027_codex53_ko_worldclass_artwork_snapshot.html ... --quality-profile deep_research`
    - 결과: `PASS` (`overall=92.35`, `claim_support=97.67`, `unsupported=1`, `section_coherence=100`)
    - 산출: `test-results/p0_quality_gate_qc_iter027_codex53_world_postfix.summary.json`, `test-results/p0_quality_gate_qc_iter027_codex53_world_postfix.md`
  - `python tools/run_report_quality_gate.py --input test-results/p0_sample_qc_iter027_codex53_ko_worldclass_artwork_snapshot.html --summary-output test-results/p0_quality_gate_qc_iter027_codex53_world_p1pass.summary.json --report-md test-results/p0_quality_gate_qc_iter027_codex53_world_p1pass.md --quality-profile deep_research`
    - 결과: `PASS` (`overall=92.35`, `claim_support=97.67`, `unsupported=1`, `section_coherence=100`)
  - `python tools/run_report_quality_gate.py --input test-results/p0_sample_qc_iter027_codex53_ko_worldclass_artwork_snapshot.html --summary-output test-results/p0_quality_gate_qc_iter027_codex53_world_p1pass_v2.summary.json --report-md test-results/p0_quality_gate_qc_iter027_codex53_world_p1pass_v2.md --quality-profile deep_research`
    - 결과: `PASS` (`overall=89.69`, `claim_support=93.02`, `unsupported=3`, `section_coherence=100`)
    - `citation_integrity_score=30.00`로 인용 깨짐 이슈를 지표에 반영
  - 수기 리뷰: `test-results/p0_manual_review_qc_iter027_p1pass.md`
  - `python tools/run_pptx_ingest_report.py --input test-results/p0_deck_example_physical_ai_iter015/physical_ai_iter015_sample_deck.pptx --run-dir . --output-json test-results/p0_pptx_ingest_contract_physical_ai_iter015.json --output-md test-results/p0_pptx_ingest_contract_physical_ai_iter015.md --max-slides 12`
    - 결과: `PASS` (12 slides ingest, contract schema `pptx_ingest.v1`)
  - `python tools/run_report_quality_gate.py --input test-results/p0_sample_qc_iter027_codex53_ko_worldclass_artwork_snapshot.html --summary-output test-results/p0_quality_gate_qc_iter027_codex53_world_progress.summary.json --report-md test-results/p0_quality_gate_qc_iter027_codex53_world_progress.md --quality-profile deep_research`
    - 결과: `PASS` (`overall=92.35`, `claim_support=97.67`, `unsupported=1`, `section_coherence=100`)

## 4) 진행률 재정렬 (2026-02-28 계획 기준)
- P0 (deep-research sustain): `100%` (완료/유지)
- P1 (DeepAgent + section rewrite UX): `76%` (rewrite flow 힌트/제약 + citation integrity 보정 + citation cleanup 복구)
- P2 (Productization + infographic pipeline): `100%` (caption 메타 계약 + lint/coverage + report embed 캡션 반영)
- P3 (PPT reader-first + deck/html pipeline): `77%` (reader 계약 추출기 + hub/index deck 가시화 + manifest 보정도구)

### P3 세부 상태
| Phase | 상태 | 진행률 | 완료 기준 |
| --- | --- | --- | --- |
| Phase 1: schema + planner/composer contract | 완료 | 100% | outline/ast 계약 + validator + tests |
| Phase 2: PPTX read/ingest 관리 강화 | 진행중 | 88% | 텍스트/이미지/slide anchor/provenance 계약 고정 |
| Phase 3: PPTX-style HTML/artwork quality loop | 진행중 | 84% | diagram/chart/infographic html 렌더 품질 + gate 연동 |
| Phase 4: Federnett publish/hub 확장 | 진행중 | 70% | deck artifact hub/index E2E + UI 노출 |
| Phase 5: FederHav partial patch API | 미시작 | 0% | slide/component patch + 승인 후 재렌더 |

## 5) 리스크 / 갭
- 국가별 투자·오류율 지표는 일부가 `Simulated/Illustrative` 의존:
  - 1차 데이터 소스(공공예산/공시/동질 벤치마크) 보강 필요
- `site/runs/`는 git ignore 정책:
  - 운영 산출물은 `test-results` 스냅샷 중심 버전관리 유지 필요
- 과거 manifest 항목은 일부 필드가 누락되어 fallback 로직이 동작:
  - 완전한 동기화를 위해 재색인/재게시 배치 필요

## 6) 향후 진행 과제 (남은 목표 + 진행률 + 완료기준)
1. PPTX Reader 계약 고도화 (최우선, 진행률 `88%`)
- 작업:
  - `readers/pptx.py` 추출 스키마 정리(`slide_id`, `shape_type`, `text/image`, `source_path`, `anchor`)
  - provenance 메타를 report/deck 공통 계약으로 통일
- 완료기준:
  - 계약 문서 + 단위테스트 + 샘플 PPTX ingest 리포트 1건

2. HTML 아트워크 렌더 품질 고도화 (진행률 `78%`)
- 작업:
  - mermaid/d2/chart 렌더 블록 정규화(코드블록 잔존 방지) `진행`
  - figure caption에 `지표/단위/기간/정규화/출처` 템플릿 필수화 (`embed figcaption + lint coverage` 반영)
- 완료기준:
  - 회귀 테스트 + 샘플 리포트 수기점검 PASS

3. QC 실측 데이터팩 구축 (시뮬레이션 비중 축소, 진행률 `28%`)
- 작업:
  - 국가별 투자/오류율/큐비트 비교를 위한 1차 데이터셋 수집
  - `Simulated` 항목과 `Measured` 항목 분리 태깅
- 완료기준:
  - 데이터 소스 인덱스 + 인포그래픽 spec 업데이트 + gate 재측정

4. Federnett Hub/Index E2E 완결 (진행률 `70%`)
- 작업:
  - `report_hub/index.html` 최신/아카이브 카드에서 `DeckQ` 메타 표시
  - legacy manifest 항목 보정(빈 필드 fallback + 재색인) + 보정도구 운영화
- 완료기준:
  - 허브 UI 회귀 테스트 + 보정 툴 적용 리포트 + 실제 run 스냅샷 1건 + 문서화

5. FederHav Partial Patch API 착수 (진행률 `5%`)
- 작업:
  - `update_slide_text`, `replace_table_data`, `swap_diagram_type` 액션 계약 정의
  - patch 승인 후 재렌더 파이프라인 연결
- 완료기준:
  - API spec 초안 + 샘플 patch 시나리오 1건 성공

## 7) 운영 체크리스트 (다음 배치)
- 5 iter마다:
  - 진행률/리스크/완료기준 업데이트
- 20 iter마다:
  - QC 샘플 1건 생성
  - report deep_research gate + deck gate 동시 측정
  - 수기 리뷰 md 기록
- 릴리즈 전:
  - `python tools/check_version_consistency.py` PASS
  - 최종 산출물은 `test-results` 스냅샷으로 커밋
