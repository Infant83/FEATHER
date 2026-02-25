from __future__ import annotations

import json
from pathlib import Path

from federlicht import report


def _write_claim_packet(notes_dir: Path) -> None:
    payload = {
        "stats": {
            "selected_claims": 4,
            "selected_evidence": 9,
            "index_only_ratio": 0.0,
        },
        "claims": [
            {
                "claim_id": "C001",
                "claim_text": "HBM demand accelerated.",
                "section_hint": "key_findings",
                "evidence_ids": ["E001", "E002", "E003"],
                "strength": "high",
                "score": 0.94,
            },
            {
                "claim_id": "C002",
                "claim_text": "Power cost volatility remains.",
                "section_hint": "risks_gaps",
                "evidence_ids": ["E004", "E005"],
                "strength": "medium",
                "score": 0.71,
            },
        ],
    }
    (notes_dir / "claim_evidence_map.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def test_auto_insert_claim_packet_infographic_inserts_block(tmp_path: Path) -> None:
    run_dir = tmp_path
    notes_dir = run_dir / "report_notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    _write_claim_packet(notes_dir)
    report_text = "\n".join(
        [
            "## Executive Summary",
            "",
            "Summary line.",
            "",
            "## Key Findings",
            "",
            "Finding paragraph with source [https://example.com/source].",
            "",
            "## Risks & Gaps",
            "",
            "Risk paragraph with source [https://example.com/risk].",
            "",
        ]
    )

    updated, meta = report.auto_insert_claim_packet_infographic(
        report_text,
        output_format="md",
        run_dir=run_dir,
        report_dir=run_dir,
        notes_dir=notes_dir,
        report_title="Demo",
        language="ko",
        max_claims=6,
    )

    assert meta.get("inserted") is True
    sections = {str(item) for item in (meta.get("sections") or [])}
    assert "Key Findings" in sections
    assert "Risks & Gaps" in sections
    assert updated.count("report-infographic") >= 2
    assert int(meta.get("chart_count", 0) or 0) >= 2
    paths = [str(item) for item in (meta.get("paths") or []) if str(item).strip()]
    data_paths = [str(item) for item in (meta.get("data_paths") or []) if str(item).strip()]
    assert len(paths) >= 2
    assert len(data_paths) >= 2
    for rel in paths:
        assert (run_dir / rel.lstrip("./")).exists()
    for rel in data_paths:
        assert (run_dir / rel.lstrip("./")).exists()
    loaded_specs = [
        json.loads((run_dir / rel.lstrip("./")).read_text(encoding="utf-8"))
        for rel in data_paths
    ]
    chart_types: set[str] = set()
    for spec in loaded_specs:
        charts = spec.get("charts")
        if not isinstance(charts, list):
            continue
        for chart in charts:
            if not isinstance(chart, dict):
                continue
            chart_types.add(str(chart.get("type") or "").strip().lower())
    assert "line" in chart_types
    assert (notes_dir / "infographic_lint_auto_claim_snapshot.txt").exists()
    assert (notes_dir / "infographic_auto_insert.json").exists()


def test_auto_insert_claim_packet_infographic_skips_without_packet(tmp_path: Path) -> None:
    run_dir = tmp_path
    notes_dir = run_dir / "report_notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    report_text = "## Executive Summary\n\nNo packet here.\n"

    updated, meta = report.auto_insert_claim_packet_infographic(
        report_text,
        output_format="md",
        run_dir=run_dir,
        report_dir=run_dir,
        notes_dir=notes_dir,
        report_title="Demo",
        language="en",
    )

    assert updated == report_text
    assert meta.get("inserted") is False
    assert meta.get("reason") == "claim_packet_missing"
