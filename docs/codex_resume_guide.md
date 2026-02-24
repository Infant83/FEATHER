# Codex Resume Guide

Last updated: 2026-02-25

## 1) 목적
- 다른 로컬 clone에서도 Codex 작업을 **맥락 손실 없이** 재개하기 위한 문서 구조를 고정한다.

## 2) 최소 필수 파일
- `docs/codex_handoff_YYYYMMDD.md`
- 현재 목표, 진행률, 충돌사항, 즉시 TODO, 다음 iter 계획
- `docs/development_workflow_guide.md`
- iter 운영 규칙, commit/push 규칙, 버전 정합 체크 규칙
- `docs/dev_history/README.md`
- 과거 handoff/이미지 아카이브 인덱스
- `docs/dev_history/version_summary.md`
- 버전별 간략 개발 이력
- `docs/report_quality_threshold_policy.md`
- score 해석, profile 기준, world-class 판정 정책
- `README.md`
- 실행/환경/컴포넌트 개요
- `CHANGELOG.md`
- 최근 반영 내역 및 버전 히스토리

## 3) 권장 보강 파일
- `docs/federhav_deepagent_transition_plan.md`
- `docs/federnett_roadmap.md`
- `docs/run_site_publish_strategy.md`
- `docs/ppt_writer_strategy.md`

## 4) 새 clone에서 재개 체크리스트
1. `python tools/check_version_consistency.py` 실행
2. `docs/codex_handoff_YYYYMMDD.md`의 진행률/차단 이슈 확인
3. 최근 5~10 iter의 실패 축(quality gate fail 원인) 확인
4. `docs/development_workflow_guide.md` 규칙대로 iter 배치 범위 확정
5. 배치 종료 시 handoff 업데이트 + commit/push
6. quality gate 실행 시 입력 보고서가 같은 배치의 신규 생성물인지 확인

## 5) handoff 파일 필수 섹션 템플릿
- 목적(고정 문장)
- 마일스톤 상태(M1~M5)
- DONE 요약
- TODO(P0/P1/P2)
- 진행률(%)
- 충돌/리스크/미진점
- 코드/문서 일관성 체크 결과
- 다음 iter 계획(5-step)

## 6) 운영 권고
- handoff는 매일 날짜 파일로 갱신하고, 전일 파일은 archive로 유지
- 상세 iter 로그가 길어지면 “요약 handoff(당일)” + “상세 로그(전일 파일)”로 분리
- 버전 변경은 README/CHANGELOG/pyproject/versioning 동시 반영
- 20 iter 배치 단위로 3개 독자 톤(기술리더/일반독자/수업형) 샘플 보고서를 생성해 품질 편차를 검증
