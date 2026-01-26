제목
ICCV 2025 — 오픈액세스·코드 공개 현황과 GitHub 생태계에 대한 심층 리뷰

한 줄 요약
ICCV 2025(Oct 19–23, Honolulu)는 CVF(Open Access)에서 논문별 OA 버전을 제공하며, GitHub에는 (1) 커뮤니티 집계 레포지토리(논문↔코드 매핑), (2) 개별 논문의 공식/비공식 코드, (3) 주제별/워크숍별 코드·데이터 모음이 활발히 존재 — 다만 일부 수치는 커뮤니티 소스에서 확인되어 추가 검증이 필요함.

사전 메타데이터(검토 완료)
- 열람한 인덱스/메타파일: archive/tavily_search.jsonl, archive/openalex/works.jsonl, archive/20251015_iccv25-index.md, ./instruction/20251015_iccv25.txt
- 위 파일들은 소스 인덱스로 분석에 사용(본문 인용문으로 사용하지 않음). 이 인덱스들을 통해 ICCV 공식 페이지, CVF Open Access, OpenReview, 여러 GitHub 레포 등이 후보 소스로 식별됨.

1) 구조화된 소스 인벤토리 (요약)
- 공식(컨퍼런스/프로그램/날짜)
  - ICCV 공식 홈페이지 — https://iccv.thecvf.com/ (권위 있는 일정·CFP·프로그램 정보 원천)
  - ICCV Dates 페이지 — https://iccv.thecvf.com/Conferences/2025/Dates (제출·리뷰·결정·등록 등 공식 마감일)
  - OpenReview ICCV 2025 그룹 (PCS/제출 관련 메타정보)
- 오픈액세스 저장소
  - CVF Open Access ICCV2025 — https://openaccess.thecvf.com/ICCV2025 (논문별 OA pdf/보조자료 링크)
  - ICCV 2025 “All Papers” 뷰 — https://openaccess.thecvf.com/ICCV2025?day=all
- 학술/색인 자료
  - OpenAlex 수집(archive/openalex/works.jsonl) — 워크숍/챌린지/데이터셋·관련 arXiv 보고서 목록(예: VQualA, DRL4Real, R-LiViT 등)
- 대학·랩의 수집·목록
  - MMLab@NTU ICCV2025 accepted list (커뮤니티 페이지; 논문→프로젝트 페이지 링크 포함)
- GitHub (주요 발견)
  - amusi/ICCV2025-Papers-with-Code — 커뮤니티 수집(논문↔코드) (large)
  - DmitryRyumin/ICCV-2023-25-Papers — 유사 수집
  - 다양한 개별 레포(공식/비공식): hwjiang1510/RayZer, NYCU-MAPL/HyTIP, vvangfaye/HoliTracer, RAIVNLab/trajvit 등
- 기타 (워크숍·챌린지 보고서, 데이터)
  - OpenAlex에 수록된 워크숍·챌린지 arXiv 보고서들 (VQualA 등) — 대부분 OA(arXiv)로 공개

2) 우선 읽기(최대 12, 우선순위·이유) — 우선순위대로 정렬
1. ICCV 공식 홈페이지 (https://iccv.thecvf.com/)
   - 이유: 공식 일정, 장소(Oct 19–23, Honolulu), 프로그램 링크와 공지(현장·온라인 비디오·현지 안내) — CFP·Deadlines·오픈액세스 정책의 1차 출처.
   - 읽기 목표: Official policy(오픈액세스 안내), 제출·결정·등록 마감일, 프로그램(주요 세션 구조).

2. ICCV Dates 페이지 (https://iccv.thecvf.com/Conferences/2025/Dates)
   - 이유: 제출/리뷰/리젝·수락·저자반론·포스터 업로드 등 세부 데드라인(확인 필수).
   - 읽기 목표: CFP 관련 마감·타임라인을 리뷰 리포트에 정확 반영.

3. CVF Open Access — ICCV2025 (https://openaccess.thecvf.com/ICCV2025?day=all)
   - 이유: 논문별 OA PDF·supp·bibtex 링크의 집합(오픈액세스 현황 직접 확인).
   - 읽기 목표: OA 논문 목록, PDF/보조자료 유무, 논문별 OA 유형(저자 보관/저널 제공 등).

4. OpenReview ICCV2025 그룹 (https://openreview.net/group?id=thecvf.com/ICCV/2025/Conference)
   - 이유: 제출 기간·PCS 연락처·CFP 메타정보(공식 확인 보강).
   - 읽기 목표: 제출창·리뷰 일정·PCS 연락처 등 CFP 운영 정보 확인.

5. CVF Virtual Papers 페이지 (https://iccv.thecvf.com/virtual/2025/papers.html)
   - 이유: 세션별 프로그램(Orals, Posters) 정렬. 발표 순서·시간 확인에 유용.
   - 읽기 목표: 주요 발표(Oral/Spotlight) 식별 및 코드 공개 가능성 높은 그룹 추적.

6. CV/랩별 “Accepted Papers” 요약(예: MMLab@NTU ICCV2025 page)
   - 이유: 특정 연구실의 Accepted list → 프로젝트 페이지·코드 링크가 포함되는 경우가 많음.
   - 읽기 목표: 프로젝트 페이지/코드 링크 수집(예: Project page, arXiv↔code).

7. GitHub: amusi/ICCV2025-Papers-with-Code (https://github.com/amusi/ICCV2025-Papers-with-Code)
   - 이유: 대규모 커뮤니티 집계(논문 ↔ code) — 빠른 코드 탐색/수집에 유용.
   - 읽기 목표: 레포 구조(논문-코드 매핑) 검증, 수집 자동화 가능성 평가.

8. GitHub topics: iccv2025 (https://github.com/topics/iccv2025)
   - 이유: 태그로 묶인 IC C V2025 관련 저장소 탐색(공식/비공식 모두).
   - 읽기 목표: 주제별·워크숍별 코드 저장소 발굴.

9. Example official code repo — hwjiang1510/RayZer (https://github.com/hwjiang1510/RayZer)
   - 이유: “Code for ICCV'2025” 표기·구현·체크포인트 등 — 공식 코드 사례로 분석 가치 높음.
   - 읽기 목표: 리포지토리 구조(데이터/학습/추론 스크립트), 라이선스·사용법, 체크포인트 공개 여부 확인.

10. Example official code repo — vvangfaye/HoliTracer (https://github.com/vvangfaye/HoliTracer)
    - 이유: ICCV 2025 논문 공식 구현(공식 표기) — remote sensing vectorization 사례.
    - 읽기 목표: 데이터 준비·튜토리얼·데모 여부 확인.

11. Example official code repo — NYCU-MAPL/HyTIP (https://github.com/NYCU-MAPL/HyTIP)
    - 이유: Accepted to ICCV 2025 표기, 코드·재현성 관련 업데이트(랩 레벨).
    - 읽기 목표: 성능·재현성·참고문헌(실험표) 확인.

12. OpenAlex works (archive/openalex/works.jsonl 및 해당 arXiv PDF들)
    - 이유: 워크숍·챌린지 보고서(오픈 액세스), 데이터셋·체크리스트(예: VQualA, R-LiViT) — ICCV 부대행사·데이터·경쟁 현황 파악에 유용.
    - 읽기 목표: 워크숍 보고서/챌린지 결과와 공개 리포지토리(예: GitHub 링크) 추적.

참고: 위 목록은 '공식 정책·프로그램 확인'을 최우선으로 하며, 그다음으로 '오픈액세스 저장소(논문 PDF·보조자료)' 및 '코드 공개 상태(공식 레포·커뮤니티 집계)'를 추적하도록 구성됨.

3) 리뷰 리포트 — 섹션별 본문 (키워드별/주제별)
(아래 각 소제목에 핵심 사실 · 관련 링크 · 확인된 출처 요약을 함께 제시합니다.)

A. 키워드: "ICCV 2025" / "International Conference on Computer Vision 2025"
- 핵심 사실
  - 일정/장소: ICCV 2025는 2025년 10월 19일–23일, Honolulu, Hawaii (Hawaii Convention Center) — 공식 홈페이지 표기.
  - 구성: Workshops (Oct 19–20) + Main Conference (Oct 21–23).
  - 프로그램 구성: Keynotes, Orals, Posters, Tutorials, Workshops, Demos, Challenges 등.
- 관련 링크 (우선 확인 권고)
  - ICCV 공식: https://iccv.thecvf.com/
  - ICCV Dates: https://iccv.thecvf.com/Conferences/2025/Dates
  - Virtual Papers 페이지(프로그램): https://iccv.thecvf.com/virtual/2025/papers.html
- 확인된 출처 요약
  - ICCV 공식 사이트가 일정·마감·프로그램의 1차 근거이며, OpenReview(그룹 페이지)는 제출·PCS 연락처·제출 기간 등 CFP 관련 메타데이터 보강에 유용.
- 불확실성 / 주의
  - 일부 서드파티(기업 블로그·랩 페이지)는 현장 세부 일정(부스·세션 시간)을 제공하지만, 공식 시각은 항상 ICCV 사이트를 우선 확인해야 함.

B. 키워드: "ICCV 2025 Open Access"
- 핵심 사실
  - CVF(Open Access)는 ICCV 2025의 Open Access 버전을 제공 — 논문 PDF/보조자료(supplementary)를 논문별로 수록. (CVF 문구: OA 버전은 accepted 버전과 동일하나 워터마크 존재; 최종 출판본은 IEEE Xplore에 게재)
  - OA 제공 목적: 빠른 지식 확산. 저작권은 저자 또는 원권리자에게 유지됨.
- 관련 링크
  - CVF Open Access ICCV2025: https://openaccess.thecvf.com/ICCV2025
  - ICCV OpenAccess 개요: https://openaccess.thecvf.com/
- 확인된 출처 요약
  - CVF Open Access 페이지에서 개별 논문의 [pdf] [supp] [arXiv] 링크를 직접 확인 가능. 많은 논문이 arXiv 및 CVF OA로 배포되어 있어 접근성 높음.
- 정책적 함의
  - 연구자·실무자는 CVF OA를 통해 접근 가능하나, “최종 IEEE Xplore 버전”과의 차이는 저작권·형식(페이지 번호·최종 편집) 수준일 수 있음.
- 불확실성 / 주의
  - 일부 논문은 OA/저자 보관(version)·arXiv만 공개되어 있을 수 있고, 추가 자료(코드·데이터)는 별도 링크를 통해 공개됨. 코드 공개 여부는 논문마다 다름.

C. 키워드: "GitHub"
- 핵심 사실
  - GitHub 생태계 유형(주요 분류):
    1. Papers-with-Code 집계형 레포 (예: amusi/ICCV2025-Papers-with-Code, DmitryRyumin 등) — 커뮤니티 기반 매핑
    2. 개별 논문의 공식 레포(저자/소속기관) — 실험/코드/체크포인트 포함(예: hwjiang1510/RayZer, NYCU-MAPL/HyTIP, vvangfaye/HoliTracer, RAIVNLab/trajvit)
    3. 워크숍/챌린지·데이터셋 레포(예: VQualA 관련 GitHub)
    4. 재현·비공식 reimplementation 레포
    5. 토픽 태그 페이지(Topic: iccv2025) — 태그 기반 탐색
  - 커뮤니티 집계 레포가 매우 활성화되어 있어 초기 코드/프로젝트 탐색에 효율적.
- 관련 링크 (예시)
  - amusi/ICCV2025-Papers-with-Code: https://github.com/amusi/ICCV2025-Papers-with-Code
  - GitHub topic iccv2025: https://github.com/topics/iccv2025
  - 예: hwjiang1510/RayZer, vvangfaye/HoliTracer, NYCU-MAPL/HyTIP, RAIVNLab/trajvit
- 확인된 출처 요약
  - amusi 레포: 커뮤니티가 논문↔코드 링크를 수집·업데이트(문서의 신뢰성은 기여자·이슈·PR에 의존). README 내에 “Acceptance rate = 24% = 2699 / 11239” 등의 수치가 있으나 이는 커뮤니티 제공 정보로 추가 검증 필요.
  - 개별 공식 레포: ‘ICCV2025’ 표기를 포함하며, 종종 체크포인트·데모·설치법을 제공. 일부 레포는 “re-implementation”임을 명시.
- 불확실성 / 주의
  - GitHub의 커뮤니티 레포는 업데이트 시점·완성도·라이선스가 제각각. “ICCV2025” 표기가 있어도 반드시 논문 본문/저자 페이지로 확인 필요.

D. 키워드: "ICCV 2025 paper code" — 오픈 코드 현황
- 핵심 사실
  - 다수의 ICCV 2025 논문이 GitHub에 코드(공식/비공식)를 공개했음(예: RayZer, HoliTracer, HyTIP, trajvit 등). 다만 공개 비율은 논문 전체 대비 일부이며 분야·저널·연구실에 따라 편차 큼.
  - 코드 유형: 완전한 학습/평가 스크립트 + 데이터 전처리 + 체크포인트 제공(완전 구현), 데모/추론 코드만 제공, 혹은 핵심 알고리즘 파트만 제공(부분적).
- 관련 링크(예시)
  - hwjiang1510/RayZer — “Code for ICCV'2025 ‘RayZer’” (공식 구현/체크포인트 포함 가능)
  - vvangfaye/HoliTracer — Official implementation (remote sensing)
  - NYCU-MAPL/HyTIP — Accepted to ICCV 2025, 레포에 업데이트·성능 개선 사항 포함
  - RAIVNLab/trajvit — codebase for iccv 2025 paper
  - amusi/ICCV2025-Papers-with-Code — 논문→코드 매핑(커뮤니티)
- 확인된 출처 요약
  - 개별 공식 레포는 논문을 읽을 때 우선 방문 대상이며, CVF OA 페이지나 arXiv의 paper 페이지(또는 논문 footer)에서 GitHub 링크가 자주 제공됨.
- 불확실성 / 주의
  - 일부 레포의 “official” 표기는 저자/기관 표기가 없거나 re-implementation임. 라이선스·데이터 재배포 가능성(예: 데이터셋 라이선스)을 반드시 확인해야 함.

4) 오픈액세스 논문/코드 공개 현황 요약 (요지·예시 포함)
- 정책 요약
  - CVF(Open Access)는 ICCV 2025 논문의 OA(accepted-version)를 제공. 최종 IEEE Xplore 출판본과는 별개(저작권은 저자/권리자).
  - arXiv와 CVF OA가 병행되는 사례가 일반적: 많은 저자들이 arXiv에 preprint를 올리고 CVF OA에 accepted PDF를 업로드.
- 현황(요약)
  - OA 접근성: CVF OA에서 대다수 논문의 pdf + supp 확인 가능(다만 일부 보조자료는 제공되지 않을 수 있음).
  - 코드 공개: 분야·연구그룹별 차이. 대형랩/산업(구글·페이스북·애플 등)·데이터 공개 성향이 높은 연구자는 코드·데이터를 공개하는 비율이 높음. 커뮤니티 집계 레포는 이를 빠르게 연결해 줌.
- 예시 표(참고문헌 표 형식 — 핵심 자료들, OA/코드 여부)
  - (아래 표는 예시이며, 구체적 PDF·레포 확인은 우선 읽기 항목에서 권장)

  참고문헌 표 (예시)
  - 열: Paper Title | OA(가능 여부) | OA 출처 | 코드 공개 여부 | 코드 링크(있다면)
  - 행 예시:
    - RayZer: A Self-supervised Large View Synthesis Model | OA(arXiv / CVF OA 가능) | arXiv/CVF OA | 코드 공개(레포 있음) | https://github.com/hwjiang1510/RayZer
    - HoliTracer: Holistic Vectorization... | OA(arXiv/CVF OA 가능) | arXiv/CVF OA | 코드 공개(레포 있음) | https://github.com/vvangfaye/HoliTracer
    - HyTIP: Hybrid Temporal Information Propagation... | OA(arXiv/CVF OA) | arXiv/CVF OA | 코드 공개(레포 있음) | https://github.com/NYCU-MAPL/HyTIP
    - VQualA challenge reports (ISRGen-QA, Engagement prediction) | OA(arXiv) | arXiv | 데이터/리더보드·레포 링크(예: GitHub) | 링크는 각 arXiv/README에 표기

  - (주의) 위 표의 각 항목은 개별 pdf·레포 확인이 필요(권장 우선 읽기 항목 참조).

5) GitHub에서 공개된 ICCV 2025 관련 저장소 유형(분류)
- 저장소 유형(세부)
  1. Papers-with-Code / Aggregator (커뮤니티 수집) — 예: amusi/ICCV2025-Papers-with-Code, DmitryRyumin
     - 역할: 논문 → 코드·데이터 · project page 매핑, 빠른 색인
     - 주의: 수작업 기반, 업데이트·정확성 차이 있음.
  2. Official implementation (저자/소속 제공) — 예: hwjiang1510/RayZer, vvangfaye/HoliTracer, NYCU-MAPL/HyTIP
     - 역할: 학습·평가 코드, 체크포인트, 재현 스크립트
     - 신뢰성: 보통 높음(저자 표기 확인 요망)
  3. Re-implementations / Reproductions — 제3자에 의한 재현
     - 역할: 원본 코드가 없을 때 기능 제공, 성능 차이 존재 가능
  4. Topic / Tag pages (iccv2025) — 검색용 그룹화
  5. Workshop/Challenge repos — 데이터·리더보드·baseline 제공(예: VQualA)
  6. Tooling/utility repos (e.g., poster/video upload scripts, dataset converters)
- 권장 검색 전략
  - 논문 PDF(아카이브 또는 CVF OA)의 Acknowledgement / footnote / supplementary에서 GitHub 링크 확인 → 해당 레포가 공식인지 판단(저자/기관 표기 여부).

6) 불확실하거나 추가 확인이 필요한 정보 (명확 표시)
- Acceptance rate 24% = 2699 / 11239: amusi 레포 README에 기재된 수치이나, 공식 ICCV 발표(프로그램 위원회·공식 공지)로 확인되지 않음 → “커뮤니티 수치(추정)”로 표기하고 공식 출처에서 확인 권장.
- 일부 GitHub 레포의 “ICCV2025” 표기는 커뮤니티 태그·re-implementation·모의 레포일 수 있음. “공식” 표기는 저자/소속 계정·논문 본문/프로젝트 페이지에서 교차검증 필요.
- CVF OA 목록이 “빠르게 갱신”되지만, 특정 논문 보조자료(supp)를 일부 누락하거나 제출 후 보완자료가 늦게 업로드되는 경우가 있어 논문별 페이지를 직접 확인 권장.
- IEEE Xplore의 “최종 출판본”은 유료 접근 가능성이 있으므로 최종 포맷·페이지·출판 저작권 확인 시 IEEE 표기를 참조.

7) 권장 후속 작업(실행 계획)
- 단기(즉시 권장)
  1. 공식 소스(ICC V Dates, CVF OpenAccess All Papers, OpenReview)를 먼저 읽고 CFP·데드라인·오픈액세스 정책을 공식 문구로 리포트에 확정 반영.
  2. amusi/ICCV2025-Papers-with-Code와 GitHub topic(iccv2025)을 기반으로 ‘논문→코드’ 매핑 초기 리스트 자동 수집(스크립트 또는 수동 크롤링).
  3. 예시 공식 레포(hwjiang1510, vvangfaye, NYCU-MAPL, RAIVNLab)에서 README·LICENSE·체크포인트·데모 확인.
- 중기(심층)
  1. CVF OA에서 관심 분야(예: Generation, 3D, Video) 논문 PDF 다운로드·보조자료 확보.
  2. 각 논문에 대해 code 공개 여부(README·paper footnote·project page) 추적 후 표로 정리(출판·데이터셋·라이선스 포함).
  3. 의심스러운 수치(acceptance rate 등)는 ICCV 조직위원회 또는 공식 공지에서 재확인.
- 도구 제안
  - 자동화: 논문 리스트 → arXiv/CVF 페이지 → GitHub 링크 자동크롤(도움 필요 시 서포트 제공).
  - 검증: 코드가 ‘공식인지’ 확인하기 위한 체크(저자 계정/논문 본문 링크 일치 등).

8) 최종 권고 요약(핵심)
- 공식 정보(일정·CFP·OA 정책)는 ICCV 공식 사이트와 CVF Open Access를 우선적으로 인용·확인하십시오.
- GitHub에는 다양한 형태의 코드가 존재하므로, “저자 소속/논문 본문에 링크가 있는지”를 기준으로 ‘공식 코드’ 여부를 교차확인하세요.
- 현재(인덱스 기반)로는 CVF OA와 arXiv를 통한 OA 접근성이 매우 양호하며, 커뮤니티(예: amusi 레포)가 코드 수집을 활발히 수행하고 있으나 일부 통계(예: 수락률)는 별도 검증이 필요합니다.

참고 링크 목록(우선권 있는 원문)
- ICCV 공식: https://iccv.thecvf.com/
- ICCV Dates: https://iccv.thecvf.com/Conferences/2025/Dates
- CVF Open Access — ICCV 2025: https://openaccess.thecvf.com/ICCV2025
- ICCV Virtual Papers: https://iccv.thecvf.com/virtual/2025/papers.html
- OpenReview ICCV2025 group: https://openreview.net/group?id=thecvf.com/ICCV/2025/Conference
- amusi/ICCV2025-Papers-with-Code: https://github.com/amusi/ICCV2025-Papers-with-Code
- GitHub topic iccv2025: https://github.com/topics/iccv2025
- 예시 공식 코드 레포:
  - hwjiang1510/RayZer — https://github.com/hwjiang1510/RayZer
  - vvangfaye/HoliTracer — https://github.com/vvangfaye/HoliTracer
  - NYCU-MAPL/HyTIP — https://github.com/NYCU-MAPL/HyTIP
  - RAIVNLab/trajvit — https://github.com/RAIVNLab/trajvit
- OpenAlex 워크숍/챌린지(예시 arXiv 보고서)
  - VQualA challenges (arXiv entries) — OpenAlex 색인(archive/openalex/works.jsonl) 참조
  - R-LiViT dataset (arXiv) — OpenAlex 색인 참조

마무리(요청 시 다음 단계)
- 원하시면 제가 우선 읽기 목록(위 12개)을 순서대로 열람해(각 페이지의 PDF·README·보조자료를 직접 읽고) “논문별 OA·코드 공개 상태 표”를 채워 드리겠습니다. 자동화(스크립트)로 GitHub-mapping을 수집·정리해 CSV/표로 드릴 수도 있습니다. 어느 쪽을 우선할지 알려 주세요.

(참고) 위 리포트는 제공된 로컬 인덱스(archive/*)와 해당 인덱스가 참조하는 공개 웹 자원(공식 ICCV·CVF·GitHub 등)을 기반으로 작성되었습니다. 추가로 특정 논문·레포를 열람하여 상세 표(참고문헌 표)를 완성하길 원하시면 지시해 주세요.