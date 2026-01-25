## 아카이브 맵(coverage 파악)

### 1) 실행/지시(스코프 정의)
- **/instruction/20260113_linkedin-review.txt**  
  - 수집 대상 URL 3개:
    1) LinkedIn 포스트: `https://www.linkedin.com/feed/update/urn:li:activity:7399939023072358401/`  
    2) arXiv: `https://arxiv.org/abs/2511.16652` (논문 *Evolution Strategies at the Hyperscale*)  
    3) 블로그(tistory): `https://muni-dev.tistory.com/entry/Evolution-Strategies-at-the-Hyperscale`

- **/archive/20260113_linkedin-review-index.md**  
  - Tavily extract로 3개 URL 텍스트 스냅샷이 생성되어 있음을 명시.

### 2) 산출물/요약 문서(이미 작성된 리포트류)
- **/archive/20260113_linkedin-review.md** (약 3.5KB)  
  - “EGGROLL” 중심으로 요약/리스크/시사점 형태의 보고서 초안.
- **/archive/20260113_linkedin-review-final.md** 및 **final-v2~v5.md** (각 4.7KB)  
  - 동일 용량으로 보아 거의 동일 내용의 버전 관리본(차이 확인 필요).

### 3) 원문 추출(핵심 근거 소스)
- **/archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt** (16.7KB)  
  - LinkedIn 글 raw_content(한국어). EGGROLL/ES, low-rank perturbation, counter-based RNG, population scaling(예: 262,144) 등의 주장 포함.
- **/archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt** (11.4KB)  
  - arXiv 초록/메타 중심. “Evolution Guided General Optimization via Low-rank Learning (EGGROLL)” 정의와 병목(perturbation matrix, batched matmul) 및 low-rank(A,B) 아이디어가 직접 근거로 존재.
- **/archive/tavily_extract/0003_https_muni-dev.tistory.com_entry_Evolution-Strategies-at-the-Hyperscale.txt** (17.9KB)  
  - 블로그 논문리뷰(한국어). 논문 링크/코드 링크(eshyperscale.github.io) 포함. LoRA 유추, 수식/섹션별 해설.

### 4) 잡/로그
- **/archive/_job.json**, **/archive/_log.txt**  
  - 수집 설정/에러/다운로드 여부 점검용(리포트 품질관리에는 유용하지만 내용 근거는 아님).

### 5) 메타데이터 JSONL 인덱스
- 이번 아카이브에는 **JSONL 메타데이터 파일이 존재하지 않음**(요구사항 체크 완료).  
  - 즉, openalex/arxiv/youtube/tavily_search 인덱스 기반 확장 커버리지는 없고, 현재는 “Tavily extract 3개 + 요약 md들”이 전부.

---

## 핵심 소스 파일 인벤토리(구조화)

### A. 1차 근거(원문/발췌)
1. `/archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt` — 논문 메타/초록(정의·문제·해결책의 원전)
2. `/archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt` — 대중/업계 관점의 주장(강한 표현·해석 포함)
3. `/archive/tavily_extract/0003_https_muni-dev.tistory.com_entry_Evolution-Strategies-at-the-Hyperscale.txt` — 해설/2차 정리(논문 이해 보조)

### B. 2차 산출물(리포트/버전)
4. `/archive/20260113_linkedin-review-final.md`
5. `/archive/20260113_linkedin-review.md`
6. `/archive/20260113_linkedin-review-final-v2.md` ~ `final-v5.md` (버전 차이 점검용)

### C. 재현성/수집 맥락
7. `/instruction/20260113_linkedin-review.txt`
8. `/archive/20260113_linkedin-review-index.md`
9. `/archive/_job.json`
10. `/archive/_log.txt`

---

## 우선순위 읽기 리스트 (최대 12개, 추천 순서 + rationale)

1) **archive/tavily_extract/0002_https_arxiv.org_abs_2511.16652.txt**  
- *rationale:* “EGGROLL”의 공식 정의/초록이 있는 1차 소스. LinkedIn/블로그 주장 검증의 기준점.

2) **archive/tavily_extract/0001_https_www.linkedin.com_feed_update_urn_li_activity_7399939023072358401.txt**  
- *rationale:* 이번 Query의 트리거로 보이는 콘텐츠. 과장/해석/수치 주장(population 262,144, 통신비용 0 등)을 체크해야 함.

3) **archive/tavily_extract/0003_https_muni-dev.tistory.com_entry_Evolution-Strategies-at-the-Hyperscale.txt**  
- *rationale:* 논문 내용을 한국어로 구조적으로 재진술. 오독 가능 지점(LoRA 비교, O(1/r) 의미 등) 확인에 유용.

4) **archive/20260113_linkedin-review-final.md**  
- *rationale:* 최종 산출물. 어떤 주장/리스크/액션이 요약됐는지 확인하고 근거 연결 상태 점검.

5) **archive/20260113_linkedin-review.md**  
- *rationale:* final과 비교해 누락/추가된 논점이 있는지 확인(초안 vs 최종).

6) **archive/20260113_linkedin-review-final-v5.md**  
- *rationale:* 최종 직전 버전일 가능성. final과 동일 용량이라도 문구 차이/근거 링크 차이 확인용.

7) **archive/20260113_linkedin-review-final-v4.md**  
- *rationale:* 버전 비교(주장 강도/리스크 항목 변화 추적).

8) **archive/20260113_linkedin-review-final-v3.md**  
- *rationale:* 동일.

9) **archive/20260113_linkedin-review-final-v2.md**  
- *rationale:* 동일.

10) **instruction/20260113_linkedin-review.txt**  
- *rationale:* 의도한 스코프(무엇을 리뷰해야 했는지) 재확인.

11) **archive/20260113_linkedin-review-index.md**  
- *rationale:* 커버리지 누락 여부(원래는 PDF 다운로드 옵션이 있었는데 실제 PDF가 없다는 점 등) 확인.

12) **archive/_job.json** (필요 시)  
- *rationale:* 수집 파라미터(예: download-pdf) 대비 실제 산출물 불일치 원인 점검.

(참고) `/archive/_log.txt`는 위 12개에 포함하진 않아도 되지만, 수집 실패/차단(LinkedIn 접근 제한 등) 흔적이 있으면 확인 가치가 있습니다.