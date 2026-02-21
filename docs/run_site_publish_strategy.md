# Run / Site 분리 및 Report Hub 발행 전략

Last updated: 2026-02-21

## 1) 디렉터리 역할 분리
- 작업(run 아카이브): `runs/<run_name>/...`
- 레거시 run 호환: `site/runs/<run_name>/...` (읽기/이관 용도)
- Federnett UI: `site/federnett/...`
- 발행 허브(report hub): `site/report_hub/...`

핵심 원칙:
- `runs/`는 실험/중간산출/로그가 포함된 **작업 공간**이다.
- `site/report_hub/`는 승인 완료 보고서만 모으는 **배포 공간**이다.

## 2) 현재 기본 동작
- run root 기본값: `runs,site/runs`
- 신규 run은 `runs/*` 우선
- `site/runs/*`는 하위 호환으로 스캔 가능
- hub root는 `site/report_hub`로 분리

## 3) 권장 발행 방식 (on-prem 포함)

### 3.1 생성
1. on-prem Federlicht 실행
2. 보고서 생성: `runs/<run>/report_full.html`

### 3.2 승인/발행
- 승인 후 아래 명령으로 허브에 게시:

```bash
python -m federlicht.hub_publish \
  --report ./runs/<run>/report_full.html \
  --run ./runs/<run> \
  --hub ./site/report_hub
```

동작:
- `site/report_hub/reports/<run>/report_full.html`로 복사
- (선택) `run_overview_*.md`, `report_workflow.md` 동반 복사
- `site/report_hub/manifest.json`, `site/report_hub/index.html` 갱신

### 3.3 배포
- `site/report_hub/*`만 GitLab Pages로 배포
- run 원본(`runs/*`)은 내부 작업 저장소에 유지

## 4) Git 전략 권장안

### 옵션 A: 단일 저장소 + 분리 커밋
- 코드/문서 커밋: `src/`, `site/federnett/`, `docs/`, `tests/`
- 발행 커밋: `site/report_hub/*` 중심
- 장점: 운영 단순
- 단점: 코드 변경과 발행 산출물 동시 관리 필요

### 옵션 B: 이원 저장소(권장)
- Repo 1 (product): 코드/문서/테스트
- Repo 2 (hub-publish): `site/report_hub` 전용
- 장점: 권한/리뷰/배포 분리, 감사 추적 용이
- 단점: CI 동기화 작업 필요

## 5) GitLab Pages 운영
- `.gitlab-ci.yml`에서 Pages job은 `site/report_hub`를 `public/report_hub`로 복사해 배포
- `public/index.html`은 `report_hub/index.html`로 리다이렉트

주의:
- Pages는 정적 호스팅이므로 Federnett 인증/세션 로직을 직접 처리하지 않는다.
- 인증 기반 작성/승인은 내부 Federnett API에서 수행하고, Pages는 읽기 허브로 사용한다.

## 6) Federnett와 run 혼동 방지 규칙
- UI/문서에서 run root와 report hub root를 분리 표기
- publish 액션은 run 내부 파일을 직접 공유하지 않고 hub 복사본을 기준으로 수행
- 향후 권장: Federnett Publish 버튼이 내부적으로 `federlicht.hub_publish`를 호출하도록 연결

## 7) 단계적 마이그레이션
- 즉시 전량 이관 대신 점진 전환
  - 신규는 `runs/`
  - 기존 `site/runs/`는 읽기 호환 유지
  - 빈번 사용 run만 선택 이관
