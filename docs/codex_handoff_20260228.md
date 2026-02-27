# Codex Unified Handoff - 2026-02-28

Last updated: 2026-02-28 10:40 +09:00 (for 2026-02-28 turnover)  
Previous handoff (archived): `docs/codex_handoff_20260227.md`

## 1) 목적 (고정)
- 최상위 목표: `(World-Class) Professional Research Level Report Quality` 유지
- 확장 목표:
  - 리포트 + 인포그래픽 + deck(PPTX/HTML)을 단일 파이프라인으로 일관 생성
  - Claim-Evidence-Source 추적성과 재현성(`report_notes/*`, `test-results/*`) 보장
- 핵심 정책:
  - PPTX는 `writer` 확장보다 `reader/ingest 관리` 강화 우선
  - 출력 품질은 PPTX binary보다 `PPTX-style HTML/artwork`를 우선 기준으로 운영
  - 품질 게이트/수기 리뷰는 HTML 산출물을 기준으로 관리

## 2) 이번 사이클 요약 (2026-02-27 반영)
- 릴리즈:
  - `1.9.32` 배포 완료 (commit: `48e1231`)
  - 버전 동기화: `pyproject.toml`, `src/federlicht/versioning.py`, `README.md`, `CHANGELOG.md`
- QC 월드클래스 샘플 생성 (Codex 5.3):
  - backend: `FEDERLICHT_LLM_BACKEND=codex_cli`
  - model: `CODEX_MODEL=gpt-5.3-codex`
  - run: `site/runs/20260221_QC_report`
- 샘플/검증 산출물:
  - snapshot: `test-results/p0_sample_qc_iter027_codex53_ko_worldclass_artwork_snapshot.html`
  - prompt: `test-results/p0_prompt_qc_iter027_codex53_worldclass_artwork.txt`
  - gate summary: `test-results/p0_quality_gate_qc_iter027_codex53_world_v4.summary.json`
  - gate report: `test-results/p0_quality_gate_qc_iter027_codex53_world_v4.md`
- 이번 턴 추가 반영(2026-02-28):
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

## 3) 품질 결과 스냅샷
- world_class gate (final v4): `PASS`
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
  - `pytest -q tests/test_report_prompt_quality_policy.py tests/test_report_quality_heuristics.py tests/test_render_html_mermaid.py` -> `31 passed`
  - `python tools/run_report_quality_gate.py --input test-results/p0_sample_qc_iter027_codex53_ko_worldclass_artwork_snapshot.html ... --quality-profile world_class`
    - 결과: `PASS` (`overall=92.35`, `claim_support=97.67`, `unsupported=1`, `section_coherence=100`)
    - 산출: `test-results/p0_quality_gate_qc_iter027_codex53_world_postfix.summary.json`, `test-results/p0_quality_gate_qc_iter027_codex53_world_postfix.md`

## 4) 진행률 재정렬 (2026-02-28 계획 기준)
- P0 (world-class sustain): `100%` (완료/유지)
- P1 (DeepAgent + section rewrite UX): `54%` (서술 연결/인용 무결성/flow heuristic 강화 반영)
- P2 (Productization + infographic pipeline): `94%` (mermaid/html 렌더 안정화 반영)
- P3 (PPT reader-first + deck/html pipeline): `58%` (HTML artwork 품질 루프 강화 반영)

### P3 세부 상태
| Phase | 상태 | 진행률 | 완료 기준 |
| --- | --- | --- | --- |
| Phase 1: schema + planner/composer contract | 완료 | 100% | outline/ast 계약 + validator + tests |
| Phase 2: PPTX read/ingest 관리 강화 | 진행중 | 80% | 텍스트/이미지/slide anchor/provenance 계약 고정 |
| Phase 3: PPTX-style HTML/artwork quality loop | 진행중 | 80% | diagram/chart/infographic html 렌더 품질 + gate 연동 |
| Phase 4: Federnett publish/hub 확장 | 진행중 | 25% | deck artifact hub/index E2E + UI 노출 |
| Phase 5: FederHav partial patch API | 미시작 | 0% | slide/component patch + 승인 후 재렌더 |

## 5) 리스크 / 갭
- 국가별 투자·오류율 지표는 일부가 `Simulated/Illustrative` 의존:
  - 1차 데이터 소스(공공예산/공시/동질 벤치마크) 보강 필요
- `site/runs/`는 git ignore 정책:
  - 운영 산출물은 `test-results` 스냅샷 중심 버전관리 유지 필요
- deck 품질 기준과 report world_class 기준의 정책 맵핑 미완:
  - slide gate profile(`baseline/professional/world_class`) 정의 필요

## 6) 향후 진행 과제 (우선순위 + 완료기준)
1. PPTX Reader 계약 고도화 (최우선)
- 작업:
  - `readers/pptx.py` 추출 스키마 정리(`slide_id`, `shape_type`, `text/image`, `source_path`, `anchor`)
  - provenance 메타를 report/deck 공통 계약으로 통일
- 완료기준:
  - 계약 문서 + 단위테스트 + 샘플 PPTX ingest 리포트 1건

2. HTML 아트워크 렌더 품질 고도화
- 작업:
  - mermaid/d2/chart 렌더 블록 정규화(코드블록 잔존 방지) `진행`
  - figure caption에 `지표/단위/기간/정규화/출처` 템플릿 필수화
- 완료기준:
  - 회귀 테스트 + 샘플 리포트 수기점검 PASS

3. QC 실측 데이터팩 구축 (시뮬레이션 비중 축소)
- 작업:
  - 국가별 투자/오류율/큐비트 비교를 위한 1차 데이터셋 수집
  - `Simulated` 항목과 `Measured` 항목 분리 태깅
- 완료기준:
  - 데이터 소스 인덱스 + 인포그래픽 spec 업데이트 + gate 재측정

4. Federnett Hub/Index E2E 완결
- 작업:
  - deck 엔트리(`run_name-deck`)와 companion path(`deck_html`, `deck_pptx`) UI 노출
  - runtime summary에 deck quality 메타 표시
- 완료기준:
  - 라우트 테스트 + 실제 run 스냅샷 1건 + 문서화

5. FederHav Partial Patch API 착수
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
  - report world_class gate + deck gate 동시 측정
  - 수기 리뷰 md 기록
- 릴리즈 전:
  - `python tools/check_version_consistency.py` PASS
  - 최종 산출물은 `test-results` 스냅샷으로 커밋
