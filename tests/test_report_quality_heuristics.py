from __future__ import annotations

from federlicht import report


def test_heuristic_quality_signals_reward_traceable_reports() -> None:
    required = ["Executive Summary", "Scope & Methodology", "Key Findings"]
    good_report = """
## Executive Summary
Industrial QC adoption remains early but measurable in optimization pilots [https://example.com/pilot].

## Scope & Methodology
We used explicit selection criteria and exclusion criteria across vendor case studies [https://example.com/method].

## Key Findings
Claim | Evidence summary | Source URL/path | Confidence | Limits
--- | --- | --- | --- | ---
Speedup in routing | Pilot benchmark vs baseline | https://example.com/benchmark | medium | small sample
"""
    weak_report = """
Quick summary without clear structure.
There might be improvements but no grounded references.
"""
    good = report.compute_heuristic_quality_signals(
        good_report,
        required,
        "md",
        depth="deep",
        report_intent="research",
    )
    weak = report.compute_heuristic_quality_signals(
        weak_report,
        required,
        "md",
        depth="deep",
        report_intent="research",
    )
    assert good["overall"] > weak["overall"]
    assert good["traceability"] >= weak["traceability"]
    assert good["claim_support_ratio"] >= weak["claim_support_ratio"]
    assert good["unsupported_claim_count"] <= weak["unsupported_claim_count"]


def test_heuristic_brief_mode_keeps_method_weight_lighter() -> None:
    required = ["Executive Summary", "Key Findings"]
    concise = """
## Executive Summary
Top recommendation: run a 12-week pilot with explicit stop/go criteria [https://example.com/policy].

## Key Findings
- Option A: lower risk, slower ROI [https://example.com/a]
- Option B: higher upside, integration risk [https://example.com/b]
"""
    signals = report.compute_heuristic_quality_signals(
        concise,
        required,
        "md",
        depth="brief",
        report_intent="briefing",
    )
    assert signals["overall"] >= 55.0
    assert "section_coherence_score" in signals
    assert "evidence_density_score" in signals
    assert "narrative_density_score" in signals
    assert "narrative_flow_score" in signals


def test_heuristic_handles_html_headings_and_links() -> None:
    html_report = """
<html><body>
<h2>Executive Summary</h2>
<p>OpenClaw pilot outcome shows moderate automation gain <a href="https://example.com/pilot">[1]</a>.</p>
<h2>Key Findings</h2>
<p>Risk remains around IAM and audit trail <a href="https://example.com/risk">[2]</a>.</p>
</body></html>
"""
    signals = report.compute_heuristic_quality_signals(
        html_report,
        ["Executive Summary", "Key Findings"],
        "html",
        depth="brief",
        report_intent="briefing",
    )
    assert signals["section_coverage"] >= 99.0
    assert signals["citation_density"] > 0.0
    assert signals["citation_integrity_score"] > 0.0
    assert signals["claim_support_ratio"] > 0.0


def test_heuristic_counts_domain_and_archive_style_source_mentions() -> None:
    html_report = """
<html><body>
<h2>Executive Summary</h2>
<p>
OpenClaw deployment risks are analyzed from public evidence
(official: openclaw.ai, /archive/tavily_extract/0001_https_openclaw.ai.txt).
</p>
<h2>Key Findings</h2>
<p>
Gateway exposure can be reduced with ACL hardening and sandbox isolation
(source: darkreading.com, /archive/tavily_extract/0002_https_darkreading.com.txt).
</p>
</body></html>
"""
    signals = report.compute_heuristic_quality_signals(
        html_report,
        ["Executive Summary", "Key Findings"],
        "html",
        depth="deep",
        report_intent="research",
    )
    assert signals["claim_support_ratio"] >= 90.0
    assert signals["unsupported_claim_count"] == 0.0


def test_citation_integrity_score_penalizes_broken_link_syntax_html() -> None:
    clean_html = """
<html><body>
<h2>Executive Summary</h2>
<p>Validated result with citation <a href="https://example.com/a">[1]</a>.</p>
<h2>Key Findings</h2>
<p>Second grounded claim <a href="https://example.com/b">[2]</a>.</p>
</body></html>
"""
    broken_html = """
<html><body>
<h2>Executive Summary</h2>
<p>Broken citation chain [\\[1\\]](<a href="https://example.com/a)[\\[2\\]](https://example.com/b">https://example.com/a)[\\[2\\]](https://example.com/b</a>).</p>
<h2>Key Findings</h2>
<p>Another sentence with malformed chain [\\[3\\]](<a href="https://example.com/c)[\\[4\\]](https://example.com/d">https://example.com/c)[\\[4\\]](https://example.com/d</a>).</p>
</body></html>
"""
    clean = report.compute_heuristic_quality_signals(
        clean_html,
        ["Executive Summary", "Key Findings"],
        "html",
        depth="deep",
        report_intent="research",
    )
    broken = report.compute_heuristic_quality_signals(
        broken_html,
        ["Executive Summary", "Key Findings"],
        "html",
        depth="deep",
        report_intent="research",
    )
    assert broken["citation_integrity_score"] < clean["citation_integrity_score"]
    assert broken["overall"] < clean["overall"]


def test_heuristic_section_coverage_supports_semantic_heading_aliases_html() -> None:
    html_report = """
<html><body>
<h2>Lede</h2>
<p>Industrial QC adoption remains early but measurable [https://example.com/lede].</p>
<h2>How It Works</h2>
<p>Methodology and scope use explicit inclusion/exclusion criteria [https://example.com/method].</p>
<h2>The Story So Far</h2>
<p>Current findings are mixed across production pilots [https://example.com/findings].</p>
<h2>Open Questions</h2>
<p>Residual risk remains around benchmark comparability [https://example.com/risk].</p>
</body></html>
"""
    signals = report.compute_heuristic_quality_signals(
        html_report,
        ["Executive Summary", "Scope & Methodology", "Key Findings", "Risks & Gaps"],
        "html",
        depth="deep",
        report_intent="research",
    )
    assert signals["section_coverage"] >= 99.0


def test_unsupported_claim_examples_ignore_non_content_sections_html() -> None:
    html_report = """
<html><body>
<h2>Executive Summary</h2>
<p>Grounded claim with citation [https://example.com/a].</p>
<h2>References</h2>
<p>This long reference note has no inline citation and should not be treated as a core claim candidate in quality heuristics.</p>
<h2>Miscellaneous</h2>
<p>This long transparency notice paragraph has no citation but should stay outside unsupported claim detection scope.</p>
</body></html>
"""
    examples = report._unsupported_claim_examples(html_report, "html", max_items=8)
    assert examples == []


def test_unsupported_claim_examples_detects_missing_citations() -> None:
    report_text = """
## Executive Summary
This line is grounded with citation [https://example.com/a].
This line states a strong claim without any source and should be flagged by detector.
"""
    examples = report._unsupported_claim_examples(report_text, "md", max_items=4)
    assert examples
    assert any("strong claim without any source" in item for item in examples)


def test_unsupported_claim_examples_skip_proposal_interpretation_markers() -> None:
    report_text = """
## Key Findings
성공 지표(KPI): (제안) 임무당 에너지와 지연 기반 운영 지표를 도입한다.
운영 관점 해석: (해석) 저비트 최적화는 하드웨어 성숙도에 따라 변동될 수 있다.
"""
    examples = report._unsupported_claim_examples(report_text, "md", max_items=4)
    assert examples == []


def test_quality_gate_failures_supports_threshold_checks() -> None:
    signals = {
        "overall": 68.0,
        "claim_support_ratio": 38.0,
        "unsupported_claim_count": 29.0,
        "section_coherence_score": 52.0,
    }
    failures = report.quality_gate_failures(
        signals,
        min_overall=70.0,
        min_claim_support=45.0,
        max_unsupported=25.0,
        min_section_coherence=60.0,
    )
    assert len(failures) == 4


def test_narrative_density_rewards_deeper_reports_in_deep_mode() -> None:
    required = ["Executive Summary", "Scope & Methodology", "Key Findings", "Implications"]
    short_deep = """
## Executive Summary
One short paragraph with a citation [https://example.com/1].

## Scope & Methodology
Short method note [https://example.com/2].

## Key Findings
Short finding note [https://example.com/3].
"""
    long_deep = """
## Executive Summary
Industrial adoption accelerated in selected pilot pathways with measurable constraints [https://example.com/a].

This section explains why pilots scaled in narrow workflows while broader rollout lagged [https://example.com/b].

## Scope & Methodology
We used explicit source selection criteria, exclusion criteria, and staged evidence synthesis [https://example.com/c].

The workflow mapped claims to evidence paths before interpretation to reduce unsupported conclusions [https://example.com/d].

## Key Findings
First, operational gains appear in constrained optimization windows and are not universal [https://example.com/e].

Second, integration overhead and governance requirements remain dominant blockers in enterprise deployments [https://example.com/f].

Third, benchmark comparability limits direct cross-vendor ranking and requires context-aware interpretation [https://example.com/g].

## Implications
Decision makers should sequence pilots by integration readiness and define stop/go criteria early [https://example.com/h].

Risk controls and evidence refresh cadence must be set before scale-out decisions [https://example.com/i].
"""
    short_signals = report.compute_heuristic_quality_signals(
        short_deep,
        required,
        "md",
        depth="deep",
        report_intent="research",
    )
    long_signals = report.compute_heuristic_quality_signals(
        long_deep,
        required,
        "md",
        depth="deep",
        report_intent="research",
    )
    assert long_signals["narrative_density_score"] > short_signals["narrative_density_score"]
    assert long_signals["overall"] > short_signals["overall"]


def test_visual_evidence_score_rewards_mermaid_in_deep_mode() -> None:
    required = ["Executive Summary", "Key Findings"]
    no_visual = """
## Executive Summary
핵심 요약과 근거 연결을 문장으로만 설명합니다 [https://example.com/a].

## Key Findings
운영 리스크와 기대효과를 텍스트로만 정리했습니다 [https://example.com/b].
"""
    with_visual = """
## Executive Summary
핵심 요약과 근거 연결을 문장으로 설명합니다 [https://example.com/a].

## Key Findings
```mermaid
flowchart LR
  A[질문] --> B[근거]
  B --> C[해석]
```

시각화는 주장-근거 경로를 요약합니다 [https://example.com/b].
"""
    signals_plain = report.compute_heuristic_quality_signals(
        no_visual,
        required,
        "md",
        depth="deep",
        report_intent="research",
    )
    signals_visual = report.compute_heuristic_quality_signals(
        with_visual,
        required,
        "md",
        depth="deep",
        report_intent="research",
    )
    assert signals_visual["visual_evidence_score"] > signals_plain["visual_evidence_score"]
    assert signals_visual["overall"] > signals_plain["overall"]


def test_narrative_flow_score_penalizes_label_list_style_blocks() -> None:
    required = ["Executive Summary", "Key Findings"]
    list_style = """
## Executive Summary
주장: 도입 우선순위를 조정해야 한다 [https://example.com/a].
근거: 파일럿 편차가 크다 [https://example.com/b].
인사이트: 운영 KPI 중심으로 재설계해야 한다 [https://example.com/c].

## Key Findings
주장: 통합 복잡도가 핵심 병목이다 [https://example.com/d].
근거: 조직별 표준 편차가 크다 [https://example.com/e].
인사이트: 단계별 게이트가 필요하다 [https://example.com/f].
"""
    prose_style = """
## Executive Summary
양자컴퓨팅 도입의 성패는 단일 성능 수치보다 운영 환경에서의 재현성에 달려 있다 [https://example.com/a].
따라서 의사결정자는 파일럿의 평균 성과보다 편차 원인을 먼저 추적해야 하며, 이를 기반으로 단계별 게이트를 설계해야 한다 [https://example.com/b].
이러한 기준은 다음 섹션의 실행 조건 정의로 이어진다 [https://example.com/c].

## Key Findings
통합 복잡도는 기술 자체보다 조직 표준 부재에서 더 크게 발생하는 경향이 확인된다 [https://example.com/d].
한편 운영 단위 KPI를 사전에 맞추면 실패비용을 줄이면서도 실험 속도를 유지할 수 있다 [https://example.com/e].
결론적으로 단계별 도입 로드맵은 기술 지표와 운영 지표를 함께 묶어 설계되어야 한다 [https://example.com/f].
"""
    list_signals = report.compute_heuristic_quality_signals(
        list_style,
        required,
        "md",
        depth="deep",
        report_intent="research",
    )
    prose_signals = report.compute_heuristic_quality_signals(
        prose_style,
        required,
        "md",
        depth="deep",
        report_intent="research",
    )
    assert prose_signals["narrative_flow_score"] > list_signals["narrative_flow_score"]


def test_section_coherence_score_relaxes_optional_short_sections() -> None:
    report_text = """
## Executive Summary
One concise summary sentence with context.

## Scope & Methodology
Method scope remains compact in this sample run.

## Key Findings
Key findings are listed briefly for smoke validation.

## Risks & Gaps
Risk and gap notes are present but concise.

## Critics
Short critics note.

## Appendix
    Artifact links.
"""
    score = report._section_coherence_score(report_text, "md")
    assert score >= 40.0
    assert score < 85.0


def test_section_coherence_score_optional_section_has_limited_impact() -> None:
    base_text = """
## Executive Summary
Sentence one with moderate context and rationale.

## Scope & Methodology
Method notes include selection criteria and constraints briefly.

## Key Findings
Findings are compact but include evidence-oriented wording.

## Risks & Gaps
Risks and limits are summarized in concise form.
"""
    with_optional = base_text + "\n## Critics\nVery short note.\n"
    score_base = report._section_coherence_score(base_text, "md")
    score_optional = report._section_coherence_score(with_optional, "md")
    assert score_optional >= (score_base - 10.0)


def test_visual_fallback_inserts_mermaid_when_deep_and_missing_visuals() -> None:
    report_text = """
## Executive Summary
핵심 서술 [https://example.com/a].

## Key Findings
핵심 결과를 설명합니다 [https://example.com/b].
"""
    updated, inserted = report.ensure_visual_evidence_fallback(
        report_text,
        output_format="md",
        language="ko",
        depth="deep",
        report_intent="research",
        citation_refs=[{"target": "https://example.com/a"}],
    )
    assert inserted is True
    assert "```mermaid" in updated
    assert "핵심 주장과 해석 경로" in updated


def test_text_lint_findings_detects_sparse_sections_and_missing_claim_citations() -> None:
    report_text = """
## Executive Summary
이 문단은 의사결정에 영향을 주는 비교 결론을 단정적으로 제시하지만 검증 가능한 인용이 전혀 없어 신뢰를 확보하기 어렵다.

## Key Findings
이 문단은 운영 성과가 크게 개선된다고 주장하지만 근거 링크와 출처가 없어 재현성과 추적성 기준을 충족하지 못한다.

## Why It Matters
이 문단은 비용과 리스크에 중대한 함의를 말하지만 실제 근거를 제시하지 않아 실행 판단에 바로 쓰기 어렵다.
"""
    lint = report.text_lint_findings(
        report_text,
        "md",
        report_intent="research",
        depth="deep",
    )
    rules = {str(item.get("rule") or "") for item in lint.get("issues") or []}
    assert "core_claim_missing_citation" in rules
    assert "heading_list_low_body_density" in rules


def test_text_lint_findings_flags_simulated_numeric_without_explicit_label() -> None:
    report_text = """
## Key Findings
2030년 시나리오에서는 오류율이 0.02%까지 낮아지고 운영 비용이 18% 줄어드는 것으로 전망되며 이는 산업 확장에 직접 연결된다.
"""
    lint = report.text_lint_findings(
        report_text,
        "md",
        report_intent="research",
        depth="deep",
    )
    rules = {str(item.get("rule") or "") for item in lint.get("issues") or []}
    assert "simulated_without_explicit_label" in rules


def test_format_text_lint_summary_handles_empty_payload() -> None:
    summary = report.format_text_lint_summary({"issue_count": 0, "issues": []})
    assert "No critical text-lint issues detected." in summary
