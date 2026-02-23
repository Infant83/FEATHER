**스카우트 결과 (openclaw)**  
실제 파일셋은 워크스페이스 기준 `site/runs/openclaw`에서 확인했습니다. 스카우트 목적에 맞춰 인덱스/메타 중심으로만 확인했고, 긴 본문 정독은 하지 않았습니다.

**구조화 인벤토리**
| 경로 | 유형 | 볼륨(문자) | 메모 |
|---|---|---:|---|
| `site/runs/openclaw/archive/openclaw-index.md` | 아카이브 인덱스 | 908 | Query ID, 수집 범위, 소스 목록 요약 |
| `site/runs/openclaw/archive/_job.json` | 수집 설정 메타 | 1446 | 수집일(2026-02-03), URL 5개, queries 0 |
| `site/runs/openclaw/archive/_log.txt` | 실행 로그 | 708 | 운영 로그(비핵심 소스) |
| `site/runs/openclaw/archive/_feather_log.txt` | 실행 로그 | 708 | 운영 로그(비핵심 소스) |
| `site/runs/openclaw/archive/tavily_extract/0001_https_twofootdog.tistory.com_555.txt` | 웹 추출(JSON 래핑) | 7070 | 설치/연동 실전 가이드 |
| `site/runs/openclaw/archive/tavily_extract/0002_https_openclaw.ai.txt` | 웹 추출(JSON 래핑) | 49280 | 공식 사이트(`OpenClaw — Personal AI Assistant`) |
| `site/runs/openclaw/archive/tavily_extract/0003_https_dev.to_czmilo_moltbot-the-ultimate-personal-ai-assistant-guide-for-2026-d4e.txt` | 웹 추출(JSON 래핑) | 76607 | 커뮤니티 2차 종합 글 |
| `site/runs/openclaw/archive/tavily_extract/0004_https_skywork.ai_skypage_en_moltbot-proactive-ai-assistants_2016342203473260544.txt` | 웹 추출(JSON 래핑) | 28836 | 2차 “Technical Report” 성격 |
| `site/runs/openclaw/archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt` | 웹 추출(JSON 래핑) | 17275 | 보안 리스크 기사 |
| `site/runs/openclaw/instruction/generated_prompt_openclaw.txt` | 포커스 프롬프트 | 1477 | ACS-style, 화학·재료 관점, 리스크/거버넌스 강조 |
| `site/runs/openclaw/instruction/openclaw.txt` | 입력 URL 목록 | 310 | 5개 URL 원본 입력 |
| `site/runs/openclaw/report_notes/source_triage.md` | 소스 트리아지 | 19 | `(no sources ranked)` |
| `site/runs/openclaw/report_notes/source_index.jsonl` | 소스 인덱스(JSONL) | 0 | 비어 있음 |

**필수 JSONL 메타데이터 커버리지**
- `archive/tavily_search.jsonl`: 없음  
- `archive/openalex/works.jsonl`: 없음  
- `archive/arxiv/papers.jsonl`: 없음  
- `archive/youtube/videos.jsonl`: 없음  
- `archive/local/manifest.jsonl`: 없음  

**우선 읽기 목록 (최대 12) + 선정 이유**
1. `site/runs/openclaw/archive/tavily_extract/0002_https_openclaw.ai.txt`  
선정 이유: 1차 공식 소스. 기능/아키텍처 주장 검증의 기준점.
2. `site/runs/openclaw/archive/tavily_extract/0005_https_www.darkreading.com_application-security_openclaw-ai-runs-wild-business-environments.txt`  
선정 이유: 보안·거버넌스 섹션 핵심 근거(기업/IAM/Shadow AI 리스크).
3. `site/runs/openclaw/archive/tavily_extract/0001_https_twofootdog.tistory.com_555.txt`  
선정 이유: 설치·운영 경로(Windows/WSL/Node/API key) 구체 정보.
4. `site/runs/openclaw/archive/tavily_extract/0004_https_skywork.ai_skypage_en_moltbot-proactive-ai-assistants_2016342203473260544.txt`  
선정 이유: 분류표/비교 프레임 보조. 단, 2차 출처라 교차검증 전제.
5. `site/runs/openclaw/archive/tavily_extract/0003_https_dev.to_czmilo_moltbot-the-ultimate-personal-ai-assistant-guide-for-2026-d4e.txt`  
선정 이유: 활용 시나리오 폭이 넓음. 잡음 많아 필요한 절만 선별 읽기.
6. `site/runs/openclaw/instruction/generated_prompt_openclaw.txt`  
선정 이유: 보고서 섹션 요구사항과 주장-출처 매핑 규칙의 기준.
7. `site/runs/openclaw/archive/openclaw-index.md`  
선정 이유: 스코프 경계(소스 5개 제한) 명시, 커버리지 확인용.
8. `site/runs/openclaw/archive/_job.json`  
선정 이유: 수집 조건(기간 365일, URL 직접 입력, OpenAlex/YouTube on but 결과 없음) 확인.
9. `site/runs/openclaw/report_notes/source_triage.md`  
선정 이유: 현재 트리아지 공백 상태 확인, 재우선순위 필요성 근거.
10. `site/runs/openclaw/report_notes/source_index.jsonl`  
선정 이유: 인덱스 비어 있어 근거-클레임 매핑을 새로 구축해야 함.
11. `site/runs/openclaw/instruction/openclaw.txt`  
선정 이유: 원 입력 URL 레퍼런스(추적성 유지).
12. `site/runs/openclaw/archive/_log.txt`  
선정 이유: 충돌/누락 의심 시에만 확인하는 보조 운영 로그.

**스카우트 판단**
- 포커스 적합 소스는 5개 전부이며, 이 중 핵심은 `openclaw.ai`(공식) + `Dark Reading`(리스크) + `twofootdog`(운영 실무)입니다.  
- `dev.to`, `skywork.ai`는 2차 종합/요약 성격이 강해 “미검증” 태그 전제로 제한적으로 사용하는 것이 안전합니다.  
- 현재 `source_index.jsonl`이 비어 있어, 다음 단계에서 클레임 단위 인덱싱을 먼저 만드는 것이 효율적입니다.