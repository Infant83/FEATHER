- [x] 연구 질문·의사결정 프레이밍 확정 — 범위: “OpenClaw(에이전트형 자동화/프로액티브 어시스턴트)를 우리 환경에 도입할 때(when) 어떤 배치 옵션(if: 로컬/원격/샌드박스)이 허용 가능한가?”로 고정. 평가 기준: IAM·Secrets·네트워크(egress)·로깅/감사·샌드박스 격리·변경관리·규정준수. | Evidence: /archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt, https://www.darkreading.com/application-security/openclaw-ai-runs-wild-business-environments
- [x] 소스 인벤토리/인용번호 고정 및 근거-주장 매핑 — 아카이브 기준 [1]~[5] 존재 확인 완료. 라벨 규칙 추가: **관찰(원문 명시)** / **추정(분석·권고)** 를 문장 단위로 태깅. | Evidence: /archive/tavily_extract/0002_https_openclaw.ai.txt, https://openclaw.ai/
- [x] 방법론/소스 선정·제외 기준 수립 — 선정/제외 규칙 명문화(공식/1차 우선, 2차는 1차 역추적 가능 시만 강하게 인용, 스냅샷에서 원문 확인 불가시 인용 제외). | Evidence: /archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt, https://www.darkreading.com/application-security/openclaw-ai-runs-wild-business-environments

- [ ] 딥리드(최소 범위) 실행 계획 — 0002/0005 “헤드라인·리드·핵심 불릿·보안/권한 섹션” 인용 후보 문장 수집(현재 **도구 출력 예산 초과로 추가 발췌 실패**). | Evidence: /archive/tavily_extract/0002_https_openclaw.ai.txt, https://openclaw.ai/
  - 누락 단계(추가): **발췌 대상 문장/섹션을 더 작은 청크로 재-읽기**(max_chars 축소, start 위치 재조정) 후, 인용 후보를 확정.
- [ ] 비교 분석 전개(옵션 비교표 포함) — 옵션×통제 매트릭스 표 작성(각 셀 “근거([n])/추정” 강제) 필요. | Evidence: /archive/tavily_extract/0002_https_openclaw.ai.txt, https://openclaw.ai/
- [ ] 아키텍처/신뢰경계 다이어그램 작성 — mermaid 다이어그램 필요.
- [ ] 리스크·불확실성 평가 및 추가 검증(when/if 조건) — 문서/레포/보안가이드 부재로 인한 불확실성 목록화 + POC 체크리스트 필요. | Evidence: /archive/tavily_extract/0002_https_openclaw.ai.txt, https://openclaw.ai/
- [ ] 권고안 및 의사결정 게이트 정의 — ‘즉시/제한적 POC/보류’ 3안 + 게이트/롤백 조건 필요.
- [ ] 최종 보고서 본문 작성 및 형식 점검 — Executive Summary→Methods→Findings/Comparison→Risks→Recommendation 구성으로 작성, **모든 주장 문장 끝 inline 인용([n])**, 비교표 1개+다이어그램 1개 렌더 가능 여부 점검 필요. | Evidence: /archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt, https://www.darkreading.com/application-security/openclaw-ai-runs-wild-business-environments

추가로 발견된 중요한 누락/리스크
- (누락) source_index.jsonl을 “생성/저장”하는 단계가 계획에는 있으나, 실제 파일 생성 단계가 없음 → 보고서 재현성/추적성 위해 **파일로 남기는 작업** 추가 필요.
- (블로커) 현재 아카이브 문서 추가 읽기에서 “Tool output budget exhausted”가 발생 → **인용문 확정이 지연**.