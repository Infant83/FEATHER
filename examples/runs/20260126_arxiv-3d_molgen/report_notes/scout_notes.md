요청(쿼리 ID: 20260126_arxiv-3d_molgen)에 따라 아카이브를 스캔하고, 논문 "3D Molecule Generation from Rigid Motifs via SE(3) Flows" (arXiv:2601.16955v1, 2026)의 핵심 소스 파일을 식별했습니다. 아래는 발견된 소스의 구조화된 인벤토리와 우선 읽기(최대 12) 목록 및 각 항목 선정 이유와 읽기 계획입니다. 노트: 메타데이터 JSONL 파일들은 커버리지 판단을 위해 열람했으며(아래에 명시), LinkedIn/Tavily 관련 항목들은 리포트 근거로 사용하지 않고 오프토픽으로 간주합니다(요청 지침 준수).

요약 — 지금까지 연 산출물
- 필수 메타데이터 파일 열람: archive/tavily_search.jsonl, archive/arxiv/papers.jsonl (커버리지 확인 목적)
- 핵심 소스(TeX 소스, 부록, PDF, 시각화 등) 모두 아카이브에 존재함 — 재현성/정밀 검토에 필요한 원천 자료 확보됨.

1) 구조화된 인벤토리 (핵심 파일만 선별)
- archive/arxiv/papers.jsonl
  - 역할: 논문 메타데이터(식별자, 요약). 커버리지/버전 확인용.
- archive/arxiv/pdf/2601.16955v1.pdf
  - 역할: 최종 렌더링된 논문(PDF) — 도표/그림/캡션/표 번호의 최종 참조점.
- archive/arxiv/src/2601.16955/main.tex
  - 역할: 논문 구조(섹션 배치) 확인용.
- archive/arxiv/src/2601.16955/contents/method.tex
  - 역할: 핵심 방법론(프래그먼트 표현, SE(3) flow 수식·정의·알고리즘) — 최우선 자료.
- archive/arxiv/src/2601.16955/contents/appendix.tex
  - 역할: Implementation Details, Evaluation Metrics, Extended Results(표·실험 조건·하이퍼파라미터) — 재현성 검토 핵심.
- archive/arxiv/src/2601.16955/contents/experiments.tex
  - 역할: 실험 설정(데이터셋, 전처리, 평가 프로토콜, 비교 대상) — 결과 해석에 반드시 필요.
- archive/arxiv/src/2601.16955/contents/background.tex
  - 역할: Technical Background(정의·관련작업 비교) — SE(3)/flow 배경 및 관련작업과의 차별점 근거.
- archive/arxiv/src/2601.16955/contents/intro.tex
  - 역할: 연구 목적/주장·성과 요약(비교 주장, 샘플링·압축 주장 등 근거 추적용).
- archive/arxiv/src/2601.16955/contents/00README.json (또는 src/2601.16955/00README.json)
  - 역할: 소스 패키지(visuals 포함) 설명, 빌드/figure 파일 위치 확인.
- archive/arxiv/src_manifest.jsonl
  - 역할: 소스내 파일 목록/관계 파악(시각화 파일 및 보조 자료 위치 확인).
- archive/arxiv/src/2601.16955/visuals/*
  - 구체 파일(예): visuals/ablations/frag_comparison.png, visuals/cond_generation/main.png, visuals/entity_distributions/distribution_qmugs_middle_threshold.pdf, visuals/title_figure.png, visuals/uncond_samples/qmugs.png 등
  - 역할: 주장(압축비, ablation, 샘플, 분포)의 시각적 증거 — 표/그림 번호와 연결해 검증 필요.
- archive/arxiv/src_text/2601.16955.txt
  - 역할: 텍스트 단일파일(전체 TeX가 아닌 렌더링 텍스트) — 빠른 전체 훑기 및 표·그림 참조용.

2) 우선 읽기 목록(최대 12) — 권장 순서 및 선정 이유
아래 항목들은 논문 핵심 주장( rigid motif 표현 + SE(3) equivariant flow 설계), 방법론(수식·알고리즘), 데이터/평가(메트릭·테이블), 정량 결과(표·그림) 및 재현성 점검에 따라 우선순위를 매겼습니다.

1. archive/arxiv/src/2601.16955/contents/method.tex
   - 이유: 프래그먼트(정의·수식), rigid frame 표기(SE(3) 표기), Multimodal Flow(연속/이산 분해), loss/목표 함수, symmetry 처리(orbit 정렬) 등 논문 핵심 기술 내용이 집중됨. 재현성 위해 가장 먼저 상세 수식·알고리즘을 검토해야 함.
   - 읽기 초점: Sections "Rigid-Motif Decomposition", "Canonicalisation and Vocabulary", "Multimodal Flow", "SE(3) Flow" (수식(13-), 식·알고리즘·정의).

2. archive/arxiv/src/2601.16955/contents/appendix.tex
   - 이유: Implementation Details(모델 아키텍처, 하이퍼파라미터, 학습 스케줄), Evaluation Metrics(정의·계산법), Extended Results(표들: QM9/GEOM-Drugs 등), ablation 세부 결과가 모두 포함. 재현과 검증에 필수.
   - 읽기 초점: "Implementation Details", "Experimental Details", "Evaluation Metrics", Extended Results tables (Table references: qm9_uncond_extended, geom_uncond_extended 등).

3. archive/arxiv/src/2601.16955/contents/experiments.tex
   - 이유: 데이터셋(예: QM9, GEOM-Drugs, QMugs 등), 전처리, 훈련/평가 프로토콜, baseline 세팅 비교(steps, 모델 크기 등) — 결과 해석에서 조건 분리 필요.
   - 읽기 초점: 데이터셋 분할·전처리 규칙, epoch/learning rate, sampling steps, baseline 구현/참고(EquiFM/EDM/END 등).

4. archive/arxiv/pdf/2601.16955v1.pdf
   - 이유: 표·그림의 최종 배치와 캡션(표 번호·그림 번호)이 PDF에서 확정됨. "주장→근거(표/그림/절 번호)" 연결 시 반드시 PDF의 표/그림 번호를 참조.
   - 읽기 초점: 핵심 그림(타이틀 피겨), 표(주요 성능 비교), ablation 그림 캡션.

5. archive/arxiv/src/2601.16955/contents/background.tex
   - 이유: Technical Background(정의: SE(3) equivariance, frame/rigid-body, flow/diffusion 맥락, motif 개념 정의) 및 관련작업 비교(EDM/GeoDiff/EquiFM 등) — 비교 축(표현–학습 목표–샘플링 비용) 정리 출발점.
   - 읽기 초점: 정의·관련작업 요약 문단, 직접 비교 문장.

6. archive/arxiv/src_text/2601.16955.txt
   - 이유: 논문 전체 텍스트(검색·빠른 크로스체크용). 표·문장·주장 위치 확인에 유용.
   - 읽기 초점: 본문 전반(특히 주장 요약부와 결과 해석), 특정 문장 인용 검증.

7. archive/arxiv/src/2601.16955/contents/intro.tex
   - 이유: 연구 동기·주장(샘플링 속도, 압축비, atom stability 우위 등)의 근거 출처 추적에 필요.
   - 읽기 초점: 핵심 주장(성능·효율)과 비교 요약.

8. archive/arxiv/src/2601.16955/contents/method.tex — (특정 부분: symmetry·alignment 방식 확인)
   - 이유: symmetry orbit alignment (GeoDiff-style alignment)와 loss 계산 관련 구현 세부(식(102-105) 등) — 섬세한 수학적 해석 필요.
   - 읽기 초점: rotation alignment, loss 항분해(translation vs rotation), discrete flow CTMC 정의(식(80-89)).

9. archive/arxiv/src/2601.16955/visuals/entity_distributions/distribution_qmugs_middle_threshold.pdf
   - 이유: 논문이 주장하는 "3.5x compression" 등의 근거가 되는 분포 시각화 — fragmentation 통계 및 압축비 검증용.
   - 읽기 초점: 캡션, 축·범례, fragmentation 파라미터(α=0.1) 조건 확인.

10. archive/arxiv/src/2601.16955/visuals/ablations/frag_comparison.png
    - 이유: fragmentation hyperparameter α에 대한 ablation 결과 — 모티프 분해 규칙 민감도 검증에 필수.
    - 읽기 초점: ablation 설정(다른 α 값들), 측정 지표(Validity, Atom Stability 등)와 표/문단의 연결.

11. archive/arxiv/src/2601.16955/visuals/cond_generation/main.png (또는 visuals/cond_generation/*.png)
    - 이유: 조건부(conditional) 생성 사례와 성능 시각화 — composition/substructure conditioning 방법 검증.
    - 읽기 초점: conditional 설정(어떤 conditioning signal 사용; appendix 섹션과 대조).

12. archive/arxiv/src/2601.16955/references.bib
    - 이유: 비교 대상(EDM, EquiFM, GeoLDM, END 등) 원문 참조 확인 및 방법별 차이점(표현/학습 목표/샘플링 비용) 크로스체크에 필요.
    - 읽기 초점: 각 참조의 핵심 특성(모델 패밀리·샘플링 비용·표현 방법).

참고: 추가적으로 src/2601.16955.tar.gz(소스 전체 압축본)는 필요 시 로컬에서 전체 파일 구조를 빠르게 확인/추출하는 용도로 보관.

3) 읽기 계획(권장 작업 순서 — 재현성과 검증 관점)
- 1단계(핵심 이론·표현): method.tex (Rigid-Motif Decomposition, Multimodal Flow, 수식/표기 검토) — 목표: 표현 공간(SE(3)^K × V_m^K)·loss 정리·알고리즘 단계화.
- 2단계(구현·하이퍼파라미터): appendix.tex (Implementation Details, Training schedules, Evaluation Metrics, Extended Results 표) — 목표: 재현 체크리스트 초안(필수 파일·하이퍼파라미터·데이터 전처리 단계).
- 3단계(데이터·프로토콜): experiments.tex + visuals(entity_distributions 등) — 목표: fragmentation 규칙(α), 데이터셋별 전처리·training epochs·sampling steps 분리.
- 4단계(결과 검증): pdf(표·그림 전체 확인) + visuals(ablations, cond_generation) — 주장→근거(표/그림/절 번호) 매핑 및 실험 조건(steps, model size) 분리.
- 5단계(관련작업 대비): background.tex + references.bib — EDM/GeoDiff/EquiFM 등과의 차이 비교(표현–학습 목표–샘플링 비용 축으로 정리).
- 6단계(재현성·검증 항목 작성): appendix 기반으로 재현 체크리스트(필수 파일, seed, 전처리 스크립트, 평가 스크립트 가정) 작성.

4) 우선 검토 포인트(검증/재현 관점에서 반드시 확인할 항목)
- Motif fragmentation 규칙의 정확한 알고리즘(어떤 결합을 자르는지, 수소 결합 취급, dummy atoms 추가 규칙) — method.tex (섹션 "Rigid-Motif Decomposition", 식/문장 참조).
- 모티프 보캐뷸러리 구성·pruning 기준(α 값의 기본값 0.1 및 ablation) — method.tex and appendix/ablations figure.
- SE(3) flow 수식(translation: Euclidean interpolant, rotation: geodesic interpolant), vector field 목표(translation vs rotation 분리) 및 training objective(Flow Matching / CFM) — appendix (Flow Matching in Euclidean Spaces) & method.tex.
- Discrete motif flow(CTMC masking prior, rate matrix Q_t) 수식 및 discrete denoiser(p_theta) 학습 방식 — method.tex (식(75-91) 등).
- Symmetry 처리(모티프의 discrete symmetry S_i와 alignment) — method.tex (식(101-105) 및 alignment 정책).
- 아키텍처 상세: IPA 기반 backbone 변경점(헤드 수·hidden dim·triangle updates·split-head rotation update) 및 파라미터 수(12.4M / 13.7M) — appendix Implementation Details.
- 학습/샘플링 하이퍼파라미터: epochs(QM9 1000, GEOM-Drugs 135 등), learning rate 1e-4, rotational exponential schedulerFactor=10, discrete flow temperature/remasking η — appendix/Experimental Details.
- 평가 정의·계산법(Validity, Connectivity, Atom Stability, Total Variation, Strain Energy, SA, QED) — appendix "Evaluation Metrics" (구체 계산법·툴: rdkit/openbabel).
- 결과 표의 실험 조건(steps, sampling temperature, solver 등) — appendix Extended Results (예: Table qm9_uncond_extended에서 각 method의 steps 표기 및 주석).
- 샘플링 비용 주장(“2x–10x reduction in generation steps”, "3.5x compression")의 근거(어떤 baseline과 비교했는지, 동일한 평가 파이프라인인지) — intro/experiments/appendix 표·주석과 cross-check.

5) 오프토픽 / 공개정보 한계
- tavily/LinkedIn 관련 문서(archive/tavily_search.jsonl에 색인됨)은 본 주제(논문 기술적 검토)의 근거로 사용하지 않음. 해당 자료는 "오프토픽/공개정보 한계"로만 언급 예정.

6) 다음 액션(권장)
- 제가 바로 "우선 읽기 목록 1–4" (method.tex, appendix.tex, experiments.tex, pdf) 을 순차적으로 정밀히 읽어 핵심 주장들을 (섹션/표/그림 번호)와 연결한 상세 검토 보고서를 작성할 수 있습니다. 이 작업은 심층(재현성·검증 포함) 분석으로 다음 산출물을 포함합니다:
  - 방법론 요약(수식·알고리즘 단계화) + 구현 의사 코드(알고리즘 블록)
  - 데이터·전처리·평가 스크립트 재현 체크리스트
  - 결과 근거 매핑(주장 → (섹션/표/그림/식) 근거)
  - 추가 실험 제안(검증이 필요한 가정·리스크) 및 Speculation/Recommendation 섹션
- 진행을 원하시면 바로 1순위 파일(method.tex)부터 읽기 시작하겠습니다. 작업 후 각 단계별로 완료 표시 및 요약을 제공하겠습니다.

원하시는 대로 지금 바로 읽기(즉시 분석)를 시작할까요? 또는 우선 특정 섹션(예: 재현 체크리스트 우선, 또는 실험표 집중)부터 진행하길 원하십니까?