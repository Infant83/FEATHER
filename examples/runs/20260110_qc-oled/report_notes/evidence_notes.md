## 1) 메타/수집 설정(범위·한계 근거)

- **수집 기간/옵션**
  - 본 run은 **2026-01-10 기준 최근 365일** 범위로 수집되었음(명시: “Date: 2026-01-10 (range: last 365 days)”). 또한 `--max-results 5`, `--download-pdf`, `--openalex --oa-max-results 5` 옵션 사용. [archive/20260110_qc-oled-index.md]
  - 지시문(Instruction)은 “quantum computing materials discovery OLED emitters industrial applications” 및 삼성/ LG/ UDC 관련 쿼리, site 제한 쿼리 등을 포함. [instruction/20260110_qc-oled.txt], [archive/_job.json]

- **수집 편향/누락(다운로드 실패)**
  - OpenAlex PDF 다운로드 과정에서 **Wiley(여러 DOI), ASME, MDPI PDF가 403 Forbidden으로 실패**. 따라서 OA 메타에 잡힌 일부 논문이 실제 본문/텍스트로 확보되지 않았음. [archive/_log.txt]
    - 예: `https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/adhm.202500195` 403 [archive/_log.txt]
    - 예: `https://asmedigitalcollection.asme.org/.../ep-25-1066.pdf` 403 [archive/_log.txt]
    - 예: `https://www.mdpi.com/.../6325/pdf` 403 [archive/_log.txt]

---

## 2) 학술(주출처 후보: OpenAlex로 확보된 PDF/텍스트)

### 2.1 (간접/워크플로) Nature Communications 논문(생성·탐색 파이프라인)
- **Using GNN property predictors as molecule generators** (Nature Communications, 2025)
  - GNN을 **물성 예측기(property predictor)**로 학습한 뒤, 그 모델의 **미분가능성(differentiability)**을 이용해 입력(분자 그래프)을 **gradient ascent로 직접 최적화**하여 목표 물성(예: HOMO–LUMO gap)을 만족하는 분자를 생성하는 접근을 제시. [archive/openalex/text/W4410193211.txt]
  - “추가적인 분자 생성 모델 재학습 없이(no additional training)”, “DFT로 검증된 특정 에너지 갭” 분자 생성 등을 주장. [archive/openalex/text/W4410193211.txt]
  - OLED 직접 적용 언급은 텍스트 초반에서 “**efficient blue organic light emitting**” 관련 응용 관심을 언급하는 수준으로 보이며(문장 도중 잘림), **QC(양자컴퓨팅) 직접 근거는 아님**. [archive/openalex/text/W4410193211.txt]
  - 원문 PDF: https://www.nature.com/articles/s41467-025-59439-1.pdf [archive/openalex/pdf/W4410193211.pdf]

### 2.2 (용어 혼동 방지용) “quantum materials” 리뷰(주제 비정합 가능)
- **Exploring quantum materials and applications: a review** (Journal of Materials Science: Materials in Engineering, 2025)
  - “quantum confinement, strong electronic correlations, topology, symmetry” 등 **양자물질(quantum materials)**을 정의/분류하고 응용을 논의. [archive/openalex/text/W4406477905.txt]
  - OLED 발광재료나 “양자컴퓨팅 기반 재료탐색”과는 결이 달라, 본 보고서에서는 **개념 대비(quantum materials vs quantum computing for chemistry/materials)** 용도로만 제한적으로 유용. [archive/openalex/text/W4406477905.txt]
  - 원문 PDF: https://jmsg.springeropen.com/counter/pdf/10.1186/s40712-024-00202-7 [archive/openalex/pdf/W4406477905.pdf]

### 2.3 (OLED 인접 배경) organoluminophores 리뷰
- **Electrospinning vs Fluorescent Organic Nano-Dots: A Comparative Review of Nanotechnologies in Organoluminophores Utilization** (Journal of Inorganic and Organometallic Polymers and Materials, 2025)
  - 약어 정의에 **OLED, TADF** 등이 포함되나, 본문은 주로 electrospinning/fluorescent organic nano-dots 기반의 organoluminophores 응용을 다룸. [archive/openalex/text/W4406330631.txt]
  - QC 기반 탐색/설계 근거는 확인되지 않아, OLED 발광재료 “배경” 이상으로 사용하기는 제한적. [archive/openalex/text/W4406330631.txt]
  - 원문 PDF: https://link.springer.com/content/pdf/10.1007/s10904-024-03567-6.pdf [archive/openalex/pdf/W4406330631.pdf]

### 2.4 (신뢰도 재검토 필요) 일반론 성격의 “Quantum-AI Synergy…” 리뷰
- **Quantum-AI Synergy and the Framework for Assessing Quantum Advantage** (Journal of Pioneering Artificial Intelligence Research, 2025)
  - 양자-AI 시너지(오류정정, 회로 최적화, 하드웨어 캘리브레이션, QML 등) 개관 및 “평가 프레임워크”를 주장. [archive/openalex/text/W4417018335.txt]
  - 예시로 “IonQ의 양자화학 시뮬레이션이 carbon capture material design에서 40% 효율 개선” 등 수치를 제시하나, **해당 수치의 1차 근거 출처는 본문 발췌 구간에서 확인 불가**(인용 시 교차검증 필요). [archive/openalex/text/W4417018335.txt]
  - 원문 PDF(doi 랜딩): https://doi.org/10.63721/25jpair0118 [archive/openalex/pdf/W4417018335.pdf]

---

## 3) 웹/업계/공식 발표(“supporting” 성격이지만 OLED×QC 직접 연결이 강한 항목 포함)

### 3.1 IBM Research 블로그(산업 협업 + OLED TADF 여기상태 QC 계산 언급)
- **IBM Research – “Unlocking today's quantum computers for OLED applications”**
  - Mitsubishi Chemical(IBM Quantum Innovation Center/Keio)과 협업, **오류 완화(error mitigation)·새 알고리즘**을 통해 OLED 후보 물질의 **excited states(여기상태) 전이 계산**을 다룬다고 설명. [archive/tavily_search.jsonl]
  - 대상 분자로 “phenylsulfonyl-carbazole (PSPCz) molecules”를 언급하며 **TADF emitter** 후보임을 명시. [archive/tavily_search.jsonl]
  - URL: https://research.ibm.com/blog/quantum-for-oled [archive/tavily_search.jsonl]

### 3.2 Mitsubishi Chemical 공개 PDF(공식 자료 성격, qEOM-VQE/VQD·여기상태·TADF)
- **[PDF] A Joint Paper on Prediction of Optical Properties of OLED Materials …** (mcgc.com)
  - IBM/미쓰비시케미칼/JSR/Keio 협업으로 **TADF emitters의 excited states 계산**, **오류 완화로 정확도 개선**을 주장하며 “commercial materials”에 excited-state 계산을 적용한 “world-first”라는 표현 포함. [archive/tavily_search.jsonl]
  - 목표를 “two quantum algorithms (qEOM-VQE and VQD) … predict excited states energies of TADF materials”로 명시. [archive/tavily_search.jsonl]
  - URL: https://www.mcgc.com/english/news_mcc/2021/__icsFiles/afieldfile/2021/05/26/qhubeng.pdf [archive/tavily_search.jsonl]

### 3.3 npj Computational Materials(1차 학술 링크: TADF·ΔEST·qEOM-VQE/VQD)
- **Nature (npj Computational Materials) – “Applications of quantum computing for investigations of electronic …”**
  - “phenylsulfonyl-carbazole TADF emitters used in OLED display”의 excited states를 **qEOM-VQE 및 VQD**로 조사했다고 결론부에서 요약. [archive/tavily_search.jsonl]
  - **ΔE_ST** 예측이 실험과 “good agreement”이며, 구조 변화와 excited-state 에너지 관계 이해에 유용하다고 서술. [archive/tavily_search.jsonl]
  - URL: https://www.nature.com/articles/s41524-021-00540-6 [archive/tavily_search.jsonl]

### 3.4 OLED-Info(업계 매체: QAOA·회로 압축 등 언급, 유료/2차 가능성 유의)
- **OLED-Info – “Mitsubishi Chemical, Deloitte Tohmatsu and Classiq manage to dramatically improve…”**
  - Mitsubishi Chemical이 **QAOA**를 OLED emitter material 개발에 활용해 왔고, 노이즈 누적이 정확도를 저해했다는 문제의식을 언급. [archive/tavily_search.jsonl]
  - “Compression of quantum circuits for OLED material discovery” 등 회로 최적화/압축을 시사. [archive/tavily_search.jsonl]
  - URL: https://www.oled-info.com/mitsubishi-chemcial-deloitte-tohmatsu-and-classiq-manage-dramatically-improve [archive/tavily_search.jsonl]
- **OLED-Info – “Transforming Materials Science Through Quantum Collaboration”**
  - 양자화학/양자알고리즘 일반론 성격이며, 본문 전체는 **OLED-Info Pro 구독 필요** 문구가 있어 원문 검증이 제한될 수 있음. [archive/tavily_search.jsonl]
  - URL: https://www.oled-info.com/transforming-materials-science-through-quantum-collaboration [archive/tavily_search.jsonl]

### 3.5 기업 IR/보도자료(산업 동향은 있으나 “QC 적용” 직접 근거는 제한적)
- **Universal Display Corporation(UDC) – Press Release(특허자산 인수)**
  - Merck KGaA로부터 emissive OLED 관련 특허 자산(“more than 300 issued and pending patents…”) 인수 계약을 발표. [archive/tavily_search.jsonl]
  - 다만 이는 **IP/사업 동향**이며 “양자컴퓨팅 기반 재료탐색”과 직접 연결되는 근거는 아님. [archive/tavily_search.jsonl]
  - URL: https://ir.oled.com/newsroom/press-releases/press-release-details/2025/Universal-Display-Corporation-to-Acquire-Emissive-OLED-Patent-Assets-from-Merck-KGaA-Darmstadt-Germany/default.aspx [archive/tavily_search.jsonl]
- **UDC – Press Release(공급/라이선스 계약)**
  - Tianma와 장기 OLED 재료 공급·라이선스 계약 체결 발표. [archive/tavily_search.jsonl]
  - QC 연계 근거는 없음. [archive/tavily_search.jsonl]
  - URL: https://ir.oled.com/newsroom/press-releases/press-release-details/2026/Tianma-and-Universal-Display-Corporation-Enter-into-Long-Term-OLED-Agreements/default.aspx [archive/tavily_search.jsonl]
- **LG Corp / LG Display–LG Chem 보도자료(p-Dopant)**
  - LG Display와 LG Chem이 OLED 핵심 소재 **p-Dopant**를 공동 개발했다고 발표(“approximately 10 years” 협업 등). [archive/tavily_search.jsonl]
  - QC/양자컴퓨팅 활용 근거는 없음(소재 개발/공급망 측면). [archive/tavily_search.jsonl]
  - URL: https://www.lgcorp.com/media/release/26853 [archive/tavily_search.jsonl]
- **Samsung Display 기술 페이지(QD-OLED)**
  - QD-OLED 구조/반사 저감 등 기술 설명. QC 연계 근거는 없음. [archive/tavily_search.jsonl]
  - URL: https://www.samsungdisplay.com/eng/tech/quantum-dot.jsp [archive/tavily_search.jsonl]

---

## 4) (보강) arXiv/LinkedIn 등(근거는 있으나 “supporting” 처리 권장)
- **arXiv HTML – “Towards Quantum Advantage in Chemistry”**
  - iQCC를 VQE 계열 알고리즘으로 소개하며, **OLED phosphorescent emitters(Ir(III), Pt(II) complexes)**의 excited-state 에너지 벤치마크를 수행했다고 서술. [archive/tavily_search.jsonl]
  - URL: https://arxiv.org/html/2512.13657v1 [archive/tavily_search.jsonl]
- **LinkedIn post(OTI Lumionics 관련)**
  - iQCC를 OLED 재료(“Ir(III) and Pt(II) phosphorescent emitters”)에 적용, MAE/상관계수 등 수치를 주장하나, 소셜 포스트이므로 **1차 논문과 교차검증 전에는 supporting으로 제한** 권장. [archive/tavily_search.jsonl]
  - URL: https://www.linkedin.com/posts/scott-genin-943a9118_towards-quantum-advantage-in-chemistry-activity-7413657675890122752-JrEs [archive/tavily_search.jsonl]

---

## 5) 오프토픽/배제 권고(본 보고서 초점 대비)
- OpenAlex로 다운로드된 다음 텍스트/논문은 **OLED 발광재료 × 양자컴퓨팅/양자화학**과 직접 관련성이 낮음:
  - “Advancing adaptive facades…”(건축 파사드) [archive/openalex/text/W4406399672.txt]
  - “Convergence of nanotechnology and AI in liver cancer…”(의생명) [archive/openalex/text/W4406707630.txt]
  - 위 항목은 인용/분석에서 배제하는 편이 타당(주제 일탈 방지).

원하시면, 위 “supporting” 웹 출처 중에서 **(i) IBM Research 블로그 ↔ (ii) npj Computational Materials 논문 ↔ (iii) Mitsubishi Chemical PDF**로 이어지는 **1차 근거 체인(Claim–Evidence map)**만 따로 뽑아, “주장→근거→한계→의미/근거강도” 템플릿에 맞춘 카드 형태로 재정리해드릴 수 있습니다.