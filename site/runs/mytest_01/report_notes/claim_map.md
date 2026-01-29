Claim | Evidence | Strength | Flags
--- | --- | --- | ---
**Query ID:** `mytest_01` | (none) | none | no_evidence
**포커스:** “다음 논문을 요약해줘.” → 단일 논문 요약 | (none) | none | no_evidence
**핵심 소스(트리아지):** | (none) | none | no_evidence
** _Learning Radical Excited States from Sparse Data_** (arXiv:2412.10149v2, 2024/2025 업데이트) | arXiv | low | -
텍스트: `./archive/arxiv/text/2412.10149v2.txt` | ./archive/arxiv/text/2412.10149v2.txt`; /archive/arxiv/text/2412.10149v2.txt` | high | -
PDF: `./archive/arxiv/pdf/2412.10149v2.pdf` | ./archive/arxiv/pdf/2412.10149v2.pdf`; /archive/arxiv/pdf/2412.10149v2.pdf` | low | -
인덱스/노트 파일 확인: | (none) | none | no_evidence
`instruction/mytest.txt` (요약 요청) | (none) | none | no_evidence
`archive/mytest_01-index.md` (아카이브 구성) | (none) | none | no_evidence
`report_notes/source_index.jsonl`, `report_notes/source_triage.md` | (none) | none | no_evidence
`archive/arxiv/papers.jsonl` (메타) | (none) | none | no_evidence
`archive/arxiv/papers.jsonl` | (none) | none | no_evidence
`report_notes/source_index.jsonl` | (none) | none | no_evidence
`report_notes/source_triage.md` | (none) | none | no_evidence
`archive/mytest_01-index.md` | (none) | none | no_evidence
요약에 필요한 서론/방법/결과/결론 텍스트가 모두 포함(가장 빠른 1차 독해). | (none) | none | no_evidence
Fig. 1–6, Table 1, 스펙트럼/회귀 플롯 등 **정량 결과/그림 해석**을 정확히 하기 위해 필요. | (none) | none | no_evidence
**유기 라디칼(organic radicals)**은 고효율 OLED(특히 deep red/NIR/IR) 및 **molecular qubits** 후보로 주목받지만, | (none) | none | no_evidence
라디칼의 들뜬상태(excited states)는 **spin-contamination**과 **multireference 성격** 때문에 TD-DFT 등 저비용 방법으로는 신뢰도가 떨어지고, CASPT2/MCSCF/CC 등 고정확도 방법은 **고비용**이라 고속 스크리닝에 부적합함. | (none) | none | no_evidence
저비용이면서 spin-pure한 준경험적 방법인 **ExROPPP (Extended Restricted Open-shell Pariser–Parr–Pople + XCIS)**가 있으나, 특히 **N, Cl 등 헤테로원자**까지 일반적으로 다룰 **일관된 파라미터 세트가 부족**함. | (none) | none | no_evidence
“블랙박스 ML”로 들뜬상태를 직접 예측하기엔 라디칼 데이터가 부족하고(대규모 데이터셋 부재), 들뜬상태는 비국소적 특성이라 학습이 까다로움. | (none) | none | no_evidence
대신 **물리 기반 서로게이트 모델(ExROPPP)**을 두고, **실험 UV-vis 데이터로 ExROPPP의 파라미터를 ‘학습/최적화’**하는 데이터-드리븐 파라미터 피팅을 제안. | (none) | none | no_evidence
저자들은 C/H/N/Cl로 구성된 **라디칼 81종의 UV-vis + 구조(DFT 최적화 기하)** 데이터베이스를 구축했다고 주장. | (none) | none | no_evidence
학습 타깃(스펙트럼의 핵심 요약량): | (none) | none | no_evidence
**첫 번째 들뜬 doublet 상태 에너지** \(E_{D1}\) | (none) | none | no_evidence
**가장 강한(밝은) 흡수 피크 에너지** \(E_{brt}\) | (none) | none | no_evidence
상대 세기 비 \(I^{rel}_{D1} = \varepsilon_{D1}/\varepsilon_{brt}\) | (none) | none | no_evidence
목적함수(가중 제곱오차 형태): | (none) | none | no_evidence
\(f = w_{D1}(E_{D1}^{calc}-E_{D1}^{exp})^2 + w_{brt}(E_{brt}^{calc}-E_{brt}^{exp})^2 + w_I(I_{D1}^{rel,calc}-I_{D1}^{rel,exp})^2\) | (none) | none | no_evidence
최적화: | (none) | none | no_evidence
파라미터 탐색은 **Nelder–Mead (derivative-free)** 사용. | (none) | none | no_evidence
분자군을 나눠 먼저 예비학습한 뒤 전체를 학습하는 **“stratified training”**이 더 좋다고 보고. | (none) | none | no_evidence
PPP 파라미터화: | (none) | none | no_evidence
on-site 에너지/홉핑/허바드 U/거리 스케일 등 원자종-특이 파라미터. | (none) | none | no_evidence
홉핑은 거리 지수감쇠 + dihedral 각의 cos 스케일을 사용. | (none) | none | no_evidence
N을 **pyridine type** vs **pyrrole/aniline type**으로 구분(π-전자 기여 차이). | (none) | none | no_evidence
**문헌 파라미터 대비 학습 파라미터가 들뜬상태 에너지 예측을 크게 개선.** | (none) | none | no_evidence
(훈련셋 81종 기준, “all states”) | (none) | none | no_evidence
**RMSE:** 0.86 eV → **0.24 eV** | (none) | none | no_evidence
**MAD:** 0.80 eV → **0.16 eV** | (none) | none | no_evidence
**R²:** -0.71 → **0.87** | (none) | none | no_evidence
**Spearman rank:** 0.79 → **0.88** | (none) | none | no_evidence
대표 분자(예: **TTM-1Cz**, **TTM-1Cz-An**) 스펙트럼 재현이 개선되며, | (none) | none | no_evidence
TTM-1Cz-An의 경우 특이한 전자구조(낮은 quartet 상태 등) 특성도 정성적으로는 맞춘다고 서술. | (none) | none | no_evidence
다만 실험에 없는 추가 흡수(예: ~500 nm 부근)를 예측하는 경우가 있어, **목적함수(스펙트럼 전체가 아닌 일부 요약량만 피팅)**의 한계 가능성을 언급. | (none) | none | no_evidence
**4개 신규 라디칼**(M2TTM-4Me, M2TTM-3PCz, M2TTM-3TPA, M2TTM-4TPA)을 합성하고 UV-vis 측정 후 테스트셋으로 사용(이 대목은 본문 뒷부분에 더 상세가 있을 가능성이 큼). | (none) | none | no_evidence
요지는 “학습된 ExROPPP 파라미터가 미지 분자에도 잘 전이된다(transferable)”는 주장. | (none) | none | no_evidence
**의의:** 라디칼 들뜬상태를 “큰 데이터로 end-to-end 예측”하기보다, **물리모델(ExROPPP)을 실험 데이터로 보정**해 고속·spin-pure 예측을 가능하게 하는 실용적 경로를 제시. 라디칼 기반 OLED 소재 탐색에 유용. | (none) | none | no_evidence
**한계/주의:** 피팅 타깃이 스펙트럼의 일부 특징량이라, 스펙트럼의 다른 피크/상태 재현은 덜 제약될 수 있음(저자도 artifact 가능성 언급). 또한 적용 범위는 주로 C/H/N/Cl 및 특정 라디칼 계열에 집중. | (none) | none | no_evidence