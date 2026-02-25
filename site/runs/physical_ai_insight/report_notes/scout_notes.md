아카이브 `physical_ai_insight`는 **“Physical AI(물리 세계에서 작동하는 AI)와 이를 구현하는 로보틱스 파운데이션/VLA(vision-language-action) 계열 모델”**을 설명 리포트(배경→개념→근거→한계)로 쓰기 위한 **arXiv 10편 + NVIDIA Glossary 1건**으로 구성되어 있습니다. (OpenAlex/YouTube/Tavily JSONL 인덱스 파일은 이번 run 폴더에 존재하지 않음)

아래는 **스카우트(인벤토리/우선순위 산정)** 결과와 **읽기 계획**입니다. (원문 정독/대량 read는 하지 않음)

---

## 1) 커버리지/구성 인벤토리(아카이브 맵)

### A. 개념 정의·대중 설명(배경 섹션에 유용)
1) **NVIDIA Glossary – “What is Physical AI?”**  
- 경로: `archive/tavily_extract/0001_https_www.nvidia.com_en-us_glossary_generative-physical-ai.txt`  
- 용도: “Physical AI” 용어 정의/직관적 설명(서론·배경)용.  
- 주의: glossary라 기술적 근거(실험/벤치마크)는 제한적.

### B. “Generalist robot policy / VLA” 코어 논문(개념+근거의 중심축)
(아카이브 인덱스 기준 arXiv 10편 모두 로봇 파운데이션/VLA/정책학습 계열)

- **Octo** (2024) – generalist robot policy, Open X-Embodiment 기반 대규모 사전학습/파인튜닝
- **OpenVLA** (2024) – 오픈소스 VLA, RT-2-X 등과 비교 주장, 효율적 파인튜닝/서빙(양자화 등) 포인트
- **π₀ (pi-zero)** (2024/업데이트 2026) – flow matching 기반 VLA/정책(개념적으로 “행동 생성” 프레임 설명에 도움)
- **CogACT** (2024) – cognition+action 시너지(아키텍처/학습 구성 관점 비교에 도움)
- **Towards Generalist Robot Policies: What Matters…** (2024) – “무엇이 중요한가” 계열: 비교표/설계요인 정리에 특히 유리

### C. 2025년 동향(근거+한계/실시간성/효율 섹션 강화)
- **Gemini Robotics** (2025) – “AI를 물리 세계로”라는 큰 그림(Physical AI narrative) 연결점
- **GR00T N1** (2025) – 휴머노이드 generalist/foundation 모델 흐름(플랫폼 관점 비교에 좋음)
- **BitVLA** (2025) – 1-bit(초저정밀)로 효율/경량화(한계·현실 적용 제약과도 연결)
- **PD-VLA(Parallel Decoding + Action Chunking)** (2025) – 지연/추론속도 개선(실시간 이슈의 근거)
- **Real-Time Execution of Action Chunking Flow Policies** (2025) – action chunking을 “실시간 실행”으로 잇는 시스템 관점(한계/실용성 섹션 근거)

---

## 2) 핵심 소스 파일 식별(리포트에 직접 쓰일 “앵커”)

리포트 포커스(대학 수업용 설명, 비교표 1개, 근거/한계 포함)를 기준으로 “정의 1 + 코어 4~6 + 실시간/효율 2~3” 조합이 가장 안정적입니다.

- **정의/배경 앵커**: NVIDIA Glossary(Physical AI 용어)  
- **개념/근거 앵커**: OpenVLA, Octo, π₀, “What matters…”  
- **확장(최근/휴머노이드/산업계)**: GR00T N1, Gemini Robotics  
- **한계/시스템 이슈(실시간·효율)**: PD-VLA, Real-Time Execution…, BitVLA

---

## 3) 우선 읽기 목록(최대 12개) + 선정 이유
(※ 지금은 “읽기 우선순위”만 제안. 실제 정독은 다음 단계에서, 필요 구간만 발췌 권장)

1) **NVIDIA Glossary: “What is Physical AI?”**  
   - 배경/정의 섹션에서 Physical AI를 간단히 규정하는 데 필요.

2) **OpenVLA: An Open-Source Vision-Language-Action Model (2024)**  
   - VLA를 대표하는 오픈소스 기준점. 비교표의 중심축(모델 규모, 데이터, 성능 주장, 파인튜닝/서빙) 잡기 좋음.

3) **Octo: An Open-Source Generalist Robot Policy (2024)**  
   - “generalist policy” 관점의 대표 앵커. 데이터(trajectories)·멀티플랫폼·파인튜닝 서사를 제공.

4) **Towards Generalist Robot Policies: What Matters in Building VLA Models (2024)**  
   - 수업용 설명에 중요한 “설계 요인/체크리스트”를 구조화해 줄 가능성이 큼(근거+한계 연결).

5) **π₀: A Vision-Language-Action Flow Model for General Robot Control (2024)**  
   - 행동 생성(continuous control)에서 flow 기반 접근을 설명하며, Diffusion/Flow 계열 개념 정리에 도움.

6) **Gemini Robotics: Bringing AI into the Physical World (2025)**  
   - Physical AI “큰 그림”을 최신 사례로 연결(동기/배경 강화, 산업계 트렌드 근거).

7) **GR00T N1: An Open Foundation Model for Generalist Humanoid Robots (2025)**  
   - 휴머노이드라는 응용축을 추가해 비교표(적용 로봇 범주)와 한계(범용성 vs embodiment)의 논점 제공.

8) **Accelerating VLA + Action Chunking via Parallel Decoding (2025)**  
   - 실시간성/지연시간 감소를 “기법 이름”으로 명확히 제시(근거 섹션의 시스템 관점 강화).

9) **Real-Time Execution of Action Chunking Flow Policies (2025)**  
   - “연구 아이디어→실시간 실행” 간극을 다루는 것으로 보이며, 한계(실시간 제약) 섹션에 특히 유용.

10) **BitVLA: 1-bit VLA Models for Robotics Manipulation (2025)**  
   - 효율(메모리/연산) 관점 핵심. 배포/온디바이스/지연과 연결해 한계·전망 논의 가능.

11) **CogACT (2024)**  
   - cognition-action 결합이라는 다른 설계 철학을 비교표의 “아키텍처/목표” 행에 추가할 때 유용.

12) (선택/여유) **아카이브 인덱스 자체** `archive/physical_ai_insight-index.md`  
   - 최종 리포트 작성 전 “소스 누락/중복” 점검용(인용 번호 체계 잡기에도 도움).

---

## 4) 추천 읽기 계획(스카우트→작성 준비 단계로 넘어갈 때)
- **1차(아주 짧게, 초록/서론 위주):** 2,3,4,6을 먼저 훑어 “배경-개념-근거-한계” 골격을 잡기  
- **2차(비교표 재료 수집):** 2(OpenVLA),3(Octo),5(π₀),7(GR00T)에서 각 4~6개 항목만 추출  
  - 예: 목표(조작/휴머노이드), 입력(vision+language), 출력(action representation), 데이터(규모/종류), 학습/추론 특징(파인튜닝, 실시간), 공개 여부  
- **3차(한계 강화):** 8,9,10에서 “실시간/효율/서빙 제약”에 대한 근거 문장 후보만 체크  
- **4차(정의/도입 마감):** 1(NVIDIA Glossary)로 용어 정의를 깔끔히 정리하고 서론을 닫기

---

## 5) 오프토픽/누락 체크
- 이번 아카이브에는 **OpenAlex(후속 인용망), YouTube(강의/데모), Tavily JSONL 검색 인덱스**가 없어, “대중적 영상/기사” 근거를 넓히기는 어려움.  
- 대신 **arXiv 논문 중심**으로 “근거(실험/데이터/구성)”를 탄탄히 하고, 정의는 NVIDIA Glossary로 보완하는 구성이 적합.

원하면 다음 단계에서, 위 우선순위 1~4번부터 **각 문서의 초록/서론 일부만 최소 범위로 확인**해 “비교표 후보 컬럼”과 “핵심 주장 문장(인용번호 [n] 매핑)”까지 스카우트-플러스 형태로 정리해 드릴 수 있습니다.