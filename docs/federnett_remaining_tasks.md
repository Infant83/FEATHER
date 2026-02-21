# Federnett Remaining Tasks

Last updated: 2026-02-21

Reference roadmap: `docs/federnett_roadmap.md`

## P0 - Stability and UX

- [x] Live Logs markdown readability baseline
  - Status: done (2026-02-21)
  - Scope: markdown table fallback(탭/공백 정렬), fenced markdown table 렌더, 이미지/mermaid 후처리.

- [x] Workflow Studio visibility pass
  - Status: done (2026-02-21)
  - Scope: 상단 작은 detail frame 제거, stage selector/focus hint/context preview 추가.

- [x] run root / report hub 정책 분리 반영
  - Status: done (2026-02-21)
  - Scope: `runs,site/runs` + `site/report_hub` 분리 표기/운영.

- [ ] Live Logs tool trace card 최종 compact
  - Scope: log-only 카드의 1-line summary를 기본으로 유지하고, 확장 상세의 밀도/간격 추가 개선.

- [ ] Report Hub write-flow UI 완성
  - Scope: comment/followup/link API를 실제 submit UI로 연결.

## P1 - Identity and Permission

- [ ] 계정/권한 운영 문서화
  - root/admin/user 정책표, bootstrap 절차, 세션 만료/회수 정책.

- [ ] Agent profile ownership 고도화
  - built-in / private / org-shared 권한 모델을 UI에 명확히 표시.

## P2 - Report Hub and Publish

- [x] run/site 분리 기반 발행 모듈
  - Status: done (2026-02-21)
  - `python -m federlicht.hub_publish` 추가.

- [x] GitLab Pages 기본 CI
  - Status: done (2026-02-21)
  - `.gitlab-ci.yml` pages job 추가(허브 정적 배포).

- [ ] 승인 워크플로우(초안->검토->발행) UI
  - Scope: Federnett에서 승인된 결과만 hub publish 되도록 버튼/상태 모델 연결.

## P3 - Regression and Observability

- [ ] Playwright e2e CI 고정
  - Scope: Live Logs 질문->제안->실행->결과 확인 시나리오를 자동화.

- [ ] Stage 비용/시간 대시보드
  - Scope: run 단위 stage elapsed/token/cache 집계 카드.

## Open decisions

- [ ] Pages 배포 브랜치 전략 확정
  - 단일 repo(main + pages job) vs 이원 repo(product + hub-publish)

- [ ] run 산출물 git 추적 정책 확정
  - 기본 ignore 유지 vs 샘플 run 일부만 추적
