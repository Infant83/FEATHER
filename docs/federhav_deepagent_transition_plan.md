# FederHav DeepAgent 전환 설계 (Draft)

## 목표
- FederHav를 단일 Q/A 헬퍼가 아니라 `governing agent`로 전환한다.
- 대화 맥락은 단순 최근 로그 tail이 아니라 `state_memory(run/workflow/artifact/source/dialogue)`로 유지한다.
- User <-> FederHav <-> Orchestrator(Feather/Federlicht) 제어를 일관된 액션 정책으로 통합한다.

## 현재 상태 (2026-02-20)
- Federlicht 리포트 파이프라인은 `create_deep_agent` 기반 경로를 이미 사용한다.
- FederHav(help_agent)는 OpenAI API/Codex CLI 직접 호출 기반이며, history 압축 + log tail 보조 방식이다.
- 이번 반영으로 UI/API에 `state_memory` 전달 경로를 추가했다.

## 타겟 아키텍처
1. Governing Agent (`federhav.governor`)
- 입력: user query, state_memory, policy(plan/act), capability registry.
- 역할: 의도 분류, 실행 계획 생성, subagent orchestration.

2. Subagents (동적 생성/해체)
- `help`: 설명/요약/대화
- `executor`: run/switch/focus/preset 같은 안전 액션 실행
- `planner`: multi-step plan 작성
- `evidence`: 근거/파일/링크 검증
- `writer`: instruction/prompt 초안 생성
- `quality`: 결과 검수/회귀 점검

3. Middleware
- `context_compaction`: 토큰 예산 기반 히스토리/상태 압축
- `state_sync`: run/workflow/result/artifact 상태 동기화
- `policy_guard`: plan/act + allow_artifacts 강제
- `model_guard`: backend/model/reasoning 호환성 필터
- `tool_budget`: 고비용 도구 호출 횟수 제한

## 상태 메모리 스키마 (v1)
- `scope`: run_rel, profile_id, agent, execution_mode, allow_artifacts
- `workflow`: kind/status/active_stage/selected_stages/running/has_error
- `run`: latest_report, counts, recent_reports/index/instructions
- `recent_sources`: 최근 근거 경로/라인
- `dialogue_state`: 압축된 최근 대화

## 단계별 전환
1. Phase A (완료/진행중)
- UI에서 state_memory 생성 및 `/api/help/ask` 전달.
- help prompt에 state_memory 블록 포함.

2. Phase B
- `federhav.agent_runtime` 모듈 추가.
- governor + help/executor subagent를 deepagent로 1차 연결.

3. Phase C
- planner/evidence/writer/quality subagent 확장.
- Federlicht Orchestrator와 공통 capability/tool registry 공유.

4. Phase D
- 자동 회귀 점검(실행/로그/보고서 산출물)을 federhav quality loop에 편입.

## 핵심 리스크
- tool 권한 경계가 흐려지면 의도치 않은 파일 변경 가능성 증가.
- model/backend 조합 불일치 시 연쇄 실패 가능.
- long-running 대화에서 압축 손실로 인한 실행 정확도 저하.

## 완화 전략
- 실행 전 dry-run preview + run-target 확인 강제.
- model/reasoning compatibility 사전 검증 + fallback 정책 로그화.
- state_memory 스키마 버저닝 + 길이 제한 + 요약 품질 테스트.
