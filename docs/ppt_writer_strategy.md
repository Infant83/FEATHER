# PPT Writer Strategy (Draft)

Last updated: 2026-02-21

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

## 구현 단계(권장)
1. Phase 1: schema + planner/composer JSON contract 고정
2. Phase 2: minimal pptx renderer(텍스트/표/이미지) + smoke tests
3. Phase 3: mermaid/d2 snapshot 삽입 + quality loop 통합
4. Phase 4: Federnett UI publish flow 및 hub index 확장

## 리스크
- 과도한 템플릿 강제는 유연성 저하를 유발하므로, `template_rigidity`와 동일한 강도 제어를 slide pipeline에도 적용해야 한다.
- 모델/토큰 비용이 커질 수 있어, slide planner와 composer 사이에 compact claim packet을 재사용해야 한다.
