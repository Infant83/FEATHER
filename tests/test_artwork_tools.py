from __future__ import annotations

import json

from federlicht import artwork


def test_build_mermaid_flowchart_basic() -> None:
    snippet = artwork.build_mermaid_flowchart(
        "start|Start;writer|Writer;result|Result",
        "start->writer|draft;writer->result|publish",
        direction="LR",
        title="Workflow",
    )
    assert "```mermaid" in snippet
    assert "flowchart LR" in snippet
    assert 'start["Start"]' in snippet
    assert "start -->|draft| writer" in snippet
    assert "Figure: Workflow" in snippet


def test_build_mermaid_timeline_basic() -> None:
    snippet = artwork.build_mermaid_timeline("2026-Q1|kickoff;2026-Q2|draft")
    assert "```mermaid" in snippet
    assert "timeline" in snippet
    assert "2026-Q1 : kickoff" in snippet
    assert "2026-Q2 : draft" in snippet


def test_render_d2_svg_missing_cli(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(artwork, "_resolve_d2_command", lambda: [])
    result = artwork.render_d2_svg(tmp_path, "a -> b")
    assert result["ok"] == "false"
    assert result["error"] == "d2_cli_missing"


def test_render_diagrams_missing_package(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(artwork, "_has_diagrams_package", lambda: False)
    result = artwork.render_diagrams_architecture(tmp_path, "a|A;b|B", "a->b")
    assert result["ok"] == "false"
    assert result["error"] == "diagrams_missing"


def test_render_diagrams_missing_dot(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(artwork, "_has_diagrams_package", lambda: True)
    monkeypatch.setattr(artwork, "_resolve_dot_command", lambda: None)
    result = artwork.render_diagrams_architecture(tmp_path, "a|A;b|B", "a->b")
    assert result["ok"] == "false"
    assert result["error"] == "graphviz_dot_missing"


def test_list_artwork_capabilities_includes_infographic() -> None:
    text = artwork.list_artwork_capabilities()
    assert "infographic_spec_builder" in text
    assert "infographic_claim_packet_builder" in text
    assert "infographic_html" in text


def test_build_infographic_spec_from_table_csv() -> None:
    table = "Month,SK hynix,Samsung\nJan,100,100\nFeb,108,102\nMar,115,101\n"
    spec_text = artwork.build_infographic_spec_from_table(
        table,
        title="Auto Spec Demo",
        chart_title="Relative Trend",
        source="https://example.com/series",
        simulated=False,
    )
    payload = json.loads(spec_text)
    charts = payload.get("charts")
    assert isinstance(charts, list)
    assert charts
    first = charts[0]
    assert first.get("title") == "Relative Trend"
    assert first.get("source") == "https://example.com/series"
    assert first.get("simulated") is False
    labels = first.get("labels")
    assert labels == ["Jan", "Feb", "Mar"]
    datasets = first.get("datasets")
    assert isinstance(datasets, list)
    assert len(datasets) == 2
    assert datasets[0].get("label") == "SK hynix"
    assert datasets[0].get("data") == [100, 108, 115]


def test_render_infographic_html_writes_html_and_spec(tmp_path) -> None:
    spec = {
        "title": "Demo Infographic",
        "subtitle": "Performance snapshot",
        "charts": [
            {
                "id": "trend",
                "library": "chartjs",
                "type": "line",
                "title": "Quarterly Trend",
                "labels": ["Q1", "Q2", "Q3"],
                "datasets": [{"label": "alpha", "data": [10, 14, 19], "color": "#00BCD4"}],
                "source": "https://example.com/data",
                "simulated": True,
            }
        ],
    }
    result = artwork.render_infographic_html(tmp_path, json.dumps(spec))
    assert result["ok"] == "true"
    path = tmp_path / str(result["path"]).lstrip("./")
    data_path = tmp_path / str(result["data_path"]).lstrip("./")
    assert path.exists()
    assert data_path.exists()
    html = path.read_text(encoding="utf-8")
    stored_spec = data_path.read_text(encoding="utf-8")
    assert "Demo Infographic" in html
    assert "Simulated/Illustrative" in html
    assert "Quarterly Trend" in html
    assert "Demo Infographic" in stored_spec


def test_build_infographic_spec_from_claim_packet() -> None:
    packet = {
        "stats": {"selected_claims": 3, "selected_evidence": 7, "index_only_ratio": 0.1},
        "claims": [
            {
                "claim_id": "C001",
                "claim_text": "HBM yield improved",
                "evidence_ids": ["E001", "E002", "E003"],
                "strength": "high",
                "score": 0.92,
            },
            {
                "claim_id": "C002",
                "claim_text": "DRAM ASP recovered",
                "evidence_ids": ["E004", "E005"],
                "strength": "medium",
                "score": 0.77,
            },
        ],
    }
    spec_text = artwork.build_infographic_spec_from_claim_packet(
        json.dumps(packet),
        source="./report_notes/claim_evidence_map.json",
        simulated=False,
    )
    payload = json.loads(spec_text)
    charts = payload.get("charts")
    assert isinstance(charts, list)
    assert charts
    first = charts[0]
    assert first.get("source") == "./report_notes/claim_evidence_map.json"
    assert first.get("simulated") is False
    datasets = first.get("datasets")
    assert isinstance(datasets, list)
    assert len(datasets) == 2


def test_build_infographic_spec_from_claim_packet_split_by_section() -> None:
    packet = {
        "stats": {"selected_claims": 4, "selected_evidence": 8, "index_only_ratio": 0.0},
        "claims": [
            {
                "claim_id": "C001",
                "claim_text": "A",
                "section_hint": "key_findings",
                "evidence_ids": ["E001", "E002"],
                "strength": "high",
                "score": 0.92,
            },
            {
                "claim_id": "C002",
                "claim_text": "B",
                "section_hint": "risks_gaps",
                "evidence_ids": ["E003", "E004"],
                "strength": "medium",
                "score": 0.81,
            },
            {
                "claim_id": "C003",
                "claim_text": "C",
                "section_hint": "scope_methodology",
                "evidence_ids": ["E005"],
                "strength": "low",
                "score": 0.5,
            },
        ],
    }
    spec_text = artwork.build_infographic_spec_from_claim_packet(
        json.dumps(packet),
        source="./report_notes/claim_evidence_map.json",
        split_by_section=True,
        max_charts=4,
    )
    payload = json.loads(spec_text)
    charts = payload.get("charts")
    assert isinstance(charts, list)
    assert len(charts) >= 2
    titles = [str(item.get("title") or "") for item in charts if isinstance(item, dict)]
    assert any("Evidence Profile" in title for title in titles)


def test_build_infographic_spec_from_claim_packet_auto_chart_type_by_section() -> None:
    packet = {
        "stats": {"selected_claims": 4, "selected_evidence": 8, "index_only_ratio": 0.0},
        "claims": [
            {
                "claim_id": "C001",
                "claim_text": "A",
                "section_hint": "key_findings",
                "evidence_ids": ["E001", "E002"],
                "strength": "high",
                "score": 0.92,
            },
            {
                "claim_id": "C002",
                "claim_text": "B",
                "section_hint": "scope_methodology",
                "evidence_ids": ["E003", "E004"],
                "strength": "medium",
                "score": 0.81,
            },
            {
                "claim_id": "C003",
                "claim_text": "C",
                "section_hint": "risks_gaps",
                "evidence_ids": ["E005"],
                "strength": "low",
                "score": 0.5,
            },
        ],
    }
    spec_text = artwork.build_infographic_spec_from_claim_packet(
        json.dumps(packet),
        source="./report_notes/claim_evidence_map.json",
        split_by_section=True,
        chart_type="auto",
        max_charts=4,
    )
    payload = json.loads(spec_text)
    charts = [item for item in (payload.get("charts") or []) if isinstance(item, dict)]
    assert charts
    assert str(charts[0].get("type") or "").lower() == "bar"
    chart_types = {str(item.get("id") or ""): str(item.get("type") or "").lower() for item in charts}
    assert chart_types.get("claim_evidence_scope_methodology") == "line"
    assert chart_types.get("claim_evidence_risks_gaps") == "line"


def test_lint_infographic_spec_flags_missing_source() -> None:
    spec = {
        "title": "Lint demo",
        "charts": [
            {
                "id": "demo",
                "type": "bar",
                "labels": ["A", "B"],
                "datasets": [{"label": "x", "data": [1, 2]}],
            }
        ],
    }
    issues = artwork.lint_infographic_spec(spec)
    assert any("source is missing" in item for item in issues)
    assert any("simulated flag is missing" in item for item in issues)
