## 0) 포커스/제약 재확인 (요청 반영)
- **리포트 포커스**: arXiv 논문 *“3D Molecule Generation from Rigid Motifs via SE(3) Flows”* (2601.16955v1, 2026)의 **핵심 아이디어·방법론·데이터/평가·정량 결과**를 **R&D 리더/도메인 전문가 관점**에서 **재현 가능성과 검증 필요사항까지** 포함해 심층 기술 검토.
- **증거/인용 소스 제한**: 제공된 **arXiv PDF/TeX/appendix(소스 포함)** 중심.
- **오프토픽 제외**: LinkedIn URN 관련 Tavily 결과는 **본 주제 근거로 사용 불가**(필요 시 “오프토픽/공개정보 한계”로만 언급).

---

## 1) 아카이브 매핑(coverage) 요약
### 1.1 핵심 1차 소스(arXiv)
- PDF: `archive/arxiv/pdf/2601.16955v1.pdf`
- 추출 텍스트(리포트 인용용 보조): `archive/arxiv/text/2601.16955v1.txt`
- TeX 소스(핵심 근거/구현·실험 세부 확인용):
  - `archive/arxiv/src/2601.16955/main.tex`
  - `archive/arxiv/src/2601.16955/contents/intro.tex`
  - `archive/arxiv/src/2601.16955/contents/background.tex`
  - `archive/arxiv/src/2601.16955/contents/related_work.tex`
  - `archive/arxiv/src/2601.16955/contents/method.tex`
  - `archive/arxiv/src/2601.16955/contents/experiments.tex`
  - `archive/arxiv/src/2601.16955/contents/appendix.tex`
  - `archive/arxiv/src/2601.16955/references.bib`

### 1.2 소스 인덱스(JSONL) 점검(필수 파일)
- 열람 완료:
  - `archive/arxiv/papers.jsonl` (해당 논문 메타 1건)
  - `archive/tavily_search.jsonl` (**LinkedIn URN 관련** 결과들 → 오프토픽)
- 미존재/해당없음:
  - `archive/openalex/works.jsonl` (파일 목록에 없음)
  - `archive/youtube/videos.jsonl` (파일 목록에 없음)
  - `archive/local/manifest.jsonl` (**없음**; 읽기 시도에서 path error 확인)

### 1.3 보조 인덱스/메모(작업용)
- Run 인덱스: `archive/20260126_arxiv-3d_molgen-index.md`
- 소스 인덱스: `report_notes/source_index.jsonl`
- 소스 트리아지: `report_notes/source_triage.md`
- Instruction: `instruction/20260126_arxiv-3d_molgen.txt` (arXiv PDF + LinkedIn 링크 포함)

---

## 2) 구조화 인벤토리(오프토픽 분리)
### A. **리포트 근거로 사용할 1차 소스(우선)**
1. `archive/arxiv/pdf/2601.16955v1.pdf`  
2. `archive/arxiv/src/2601.16955/contents/method.tex`
3. `archive/arxiv/src/2601.16955/contents/experiments.tex`
4. `archive/arxiv/src/2601.16955/contents/appendix.tex`
5. `archive/arxiv/src/2601.16955/contents/background.tex`
6. `archive/arxiv/src/2601.16955/contents/related_work.tex`
7. `archive/arxiv/src/2601.16955/contents/intro.tex`
8. `archive/arxiv/src/2601.16955/contents/conclusion.tex`
9. `archive/arxiv/src/2601.16955/main.tex` (문서 구조/figure/table include 추적)
10. `archive/arxiv/src/2601.16955/references.bib` (관련 work 정확한 식별용)

### B. **작업/인덱싱 보조(본문 근거로는 비권장)**
- `archive/arxiv/text/2601.16955v1.txt` (PDF text 추출본: 검색/스캐닝용)
- `archive/arxiv/src_text/2601.16955.txt` (TeX 추출 텍스트: grep/탐색용)
- `archive/arxiv/src_manifest.jsonl`, `archive/arxiv/src/2601.16955/00README.json` (소스 구성 확인용)

### C. **오프토픽(본문 근거 사용 금지)**
- `archive/tavily_search.jsonl` 내 Stack Overflow/Microsoft Learn/LinkedIn URN 관련 문서들  
  - 본 논문 기술 검토와 직접 근거 관계 없음 → 필요 시 “공개정보 한계/오프토픽”으로만 언급

---

## 3) 핵심 소스 파일 식별(왜 이 파일들이 ‘핵심’인지)
- **방법론의 재현 핵심**은 대부분 `contents/method.tex` + `contents/appendix.tex`에 있을 가능성이 큼  
  (모티프 분해 규칙, SE(3) flow parameterization, 상태공간 정의, 학습 objective/알고리즘, 샘플링 절차, 하이퍼파라미터/아키텍처/추가 ablation 등)
- **정량 결과·평가 프로토콜**은 `contents/experiments.tex` + appendix의 추가 표/그림에 집중될 가능성이 큼  
  (Validity/Atom stability/Mol stability, steps/속도, 데이터셋 전처리, baseline 비교 조건)
- **비교축(표현–목표–샘플링 비용)** 정리는 `background.tex` + `related_work.tex`가 근거가 됨
- **그림/표 참조 연결**은 `main.tex`에서 include/label 구조를 먼저 파악하면 PDF에서 빠르게 역추적 가능

---

## 4) 우선 읽기 목록 (최대 12개) + 선정 이유
1) **`archive/arxiv/pdf/2601.16955v1.pdf`**  
- 최종 근거 원천. 표/그림/식 번호 기반 인용이 필요(요청사항 충족).

2) **`archive/arxiv/src/2601.16955/contents/method.tex`**  
- rigid motif 표현, SE(3) equivariant flow 설계, 상태공간/목적함수/학습·샘플링 알고리즘의 1차 근거.

3) **`archive/arxiv/src/2601.16955/contents/experiments.tex`**  
- 데이터셋(QM9/GEOM-Drugs/QMugs 등), 전처리, 메트릭 정의/계산, 비교 설정(steps, model size), 정량 결과의 핵심 근거.

4) **`archive/arxiv/src/2601.16955/contents/appendix.tex`**  
- 재현성 디테일(하이퍼파라미터, fragmentation 세부 규칙, 추가 실험/ablation, 평가 스크립트 가정) 가능성이 가장 큼.

5) **`archive/arxiv/src/2601.16955/contents/background.tex`**  
- SE(3) equivariance, flow/diffusion 계열, frame/rigid-body 표현 등 “Technical Background” 섹션을 논문 근거로 채우기 위해 필요.

6) **`archive/arxiv/src/2601.16955/contents/related_work.tex`**  
- EDM/GeoDiff/EquiFM 등과의 관계를 논문이 어떻게 positioning 하는지 확인(요청된 비교축 정리에 필요).

7) **`archive/arxiv/src/2601.16955/main.tex`**  
- 문서 구성(섹션 include), figure/table 파일 경로 및 label을 빠르게 찾기 위한 허브.

8) **`archive/arxiv/src/2601.16955/contents/intro.tex`**  
- 문제정의/핵심 주장(steps 2–10x, 3.5x compression 등)을 “주장→근거” 형태로 연결하기 위한 출발점.

9) **`archive/arxiv/src/2601.16955/contents/conclusion.tex`**  
- 저자들이 명시하는 한계/후속과제 문구를 정확히 인용해 Limitations/Open Questions에 반영.

10) **`archive/arxiv/src/2601.16955/references.bib`**  
- baseline 및 비교대상(EDM/GeoDiff/EquiFM 등) 정확한 서지 식별(동명이인/버전 혼동 방지).

11) **`archive/arxiv/text/2601.16955v1.txt`**  
- PDF 전체에서 키워드(“atom stability”, “SE(3) flow”, “motif”, “steps”) 빠른 탐색용. 최종 인용은 PDF/TeX로 되돌아가 확인.

12) **`archive/arxiv/src/2601.16955/visuals/*` (필요한 그림 파일만 선별 열람)**  
- PDF에서 해상도/라벨이 부족할 때, 원본 figure로 수치/구성 요소를 판독(단, 본문 근거는 여전히 “Figure X”로 PDF/TeX 기준으로 연결).

---

## 5) 권장 읽기/분석 플로우(보고서 섹션에 맞춘 실행 계획)
1. **main.tex → PDF 목차/구조 매칭**: 섹션/figure/table label 체계를 먼저 파악  
2. **intro.tex + PDF 서론**: 핵심 주장 리스트업(압축률, step 감소, 성능 우위)  
3. **method.tex 집중 정독**:  
   - motif 분해/표현(기호/정의)  
   - SE(3) flow의 파라미터화/등변성 보장 방식  
   - 학습 objective, sampling 알고리즘을 “알고리즘 단계”로 재구성  
4. **experiments.tex 정독**: 데이터셋/전처리/메트릭 계산법/평가 프로토콜 분해(조건 차이 분리)  
5. **appendix.tex로 재현성 보강**: 누락된 하이퍼파라미터/규칙/추가 ablation/에러바 등 체크  
6. **background/related_work로 비교축(표현–목표–샘플링 비용) 정리**  
7. **결론/한계 문구를 근거로 Limitations/Risks/Critics 초안 작성**  
8. 마지막으로 **재현 체크리스트**(필수 파일/파라미터/평가 스크립트 가정) 구성

원하면 다음 단계로, 제가 위 우선순위대로 `method.tex/experiments.tex/appendix.tex`부터 실제로 열어 핵심 수식·알고리즘·표/그림 근거 위치(섹션/식/표 번호)를 뽑아 “주장→근거” 매트릭스를 만들어 드릴 수 있습니다.