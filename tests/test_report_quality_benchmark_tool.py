from __future__ import annotations

import json
import importlib.util
from pathlib import Path


def _load_benchmark_module():
    path = Path("tools/report_quality_benchmark.py")
    spec = importlib.util.spec_from_file_location("report_quality_benchmark", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bench = _load_benchmark_module()


def test_collect_files_supports_glob_and_file(tmp_path: Path) -> None:
    report_a = tmp_path / "a.md"
    report_b = tmp_path / "b.html"
    report_a.write_text("## Executive Summary\nhello [https://example.com]", encoding="utf-8")
    report_b.write_text("<h2>Executive Summary</h2><p>hello <a href='https://example.com'>x</a></p>", encoding="utf-8")
    files = bench._collect_files([str(report_a), str(tmp_path / "*.html")])
    paths = sorted(path.name for path in files)
    assert paths == ["a.md", "b.html"]


def test_run_benchmark_returns_quality_rows(tmp_path: Path) -> None:
    report_path = tmp_path / "report.md"
    report_path.write_text(
        "\n".join(
            [
                "## Executive Summary",
                "Pilot showed measurable gain [https://example.com/pilot].",
                "## Scope & Methodology",
                "Selection criteria and exclusions were documented [https://example.com/method].",
                "## Key Findings",
                "Claim | Evidence summary | Source URL/path | Confidence | Limits",
                "--- | --- | --- | --- | ---",
                "A | benchmark | https://example.com/bench | medium | small sample",
            ]
        ),
        encoding="utf-8",
    )
    rows = bench._run_benchmark(
        [report_path],
        required_sections=["Executive Summary", "Scope & Methodology", "Key Findings"],
        depth="deep",
        report_intent="research",
    )
    assert len(rows) == 1
    assert rows[0]["overall"] > 0.0
    assert rows[0]["claim_support_ratio"] >= 0.0


def test_json_output_serializable(tmp_path: Path) -> None:
    rows = [
        {
            "path": "x.md",
            "format": "md",
            "overall": 70.0,
            "claim_support_ratio": 80.0,
            "unsupported_claim_count": 2.0,
            "evidence_density_score": 68.0,
            "section_coherence_score": 74.0,
            "signals": {"overall": 70.0},
        }
    ]
    out = tmp_path / "bench.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    loaded = json.loads(out.read_text(encoding="utf-8"))
    assert loaded[0]["path"] == "x.md"


def test_compute_summary_and_load_rows_bundle(tmp_path: Path) -> None:
    rows = [
        {"overall": 70.0, "claim_support_ratio": 52.0, "unsupported_claim_count": 20.0, "evidence_density_score": 60.0, "section_coherence_score": 66.0},
        {"overall": 74.0, "claim_support_ratio": 64.0, "unsupported_claim_count": 14.0, "evidence_density_score": 68.0, "section_coherence_score": 72.0},
    ]
    summary = bench._compute_summary(rows)
    assert summary["overall"] == 72.0
    assert summary["claim_support_ratio"] == 58.0
    bundle_path = tmp_path / "bundle.json"
    bundle_path.write_text(json.dumps({"rows": rows}, ensure_ascii=False), encoding="utf-8")
    loaded_rows = bench._load_rows(bundle_path)
    assert len(loaded_rows) == 2


def test_load_suite_counts(tmp_path: Path) -> None:
    suite = {
        "suite_id": "demo",
        "prompts": [
            {"id": "a", "intent": "research", "depth": "deep", "prompt": "x"},
            {"id": "b", "intent": "briefing", "depth": "brief", "prompt": "y"},
            {"id": "c", "intent": "research", "depth": "normal", "prompt": "z"},
        ],
    }
    path = tmp_path / "suite.json"
    path.write_text(json.dumps(suite, ensure_ascii=False), encoding="utf-8")
    meta = bench._load_suite(path)
    assert meta["suite_id"] == "demo"
    assert meta["suite_size"] == 3
    assert meta["intent_counts"]["research"] == 2
    assert meta["depth_counts"]["brief"] == 1


def test_render_compare_markdown_table() -> None:
    current = {
        "overall": 72.0,
        "claim_support_ratio": 58.0,
        "unsupported_claim_count": 16.0,
        "evidence_density_score": 64.0,
        "section_coherence_score": 69.0,
    }
    baseline = {
        "overall": 70.0,
        "claim_support_ratio": 55.0,
        "unsupported_claim_count": 18.0,
        "evidence_density_score": 60.0,
        "section_coherence_score": 66.0,
    }
    delta = {
        "overall": 2.0,
        "claim_support_ratio": 3.0,
        "unsupported_claim_count": -2.0,
        "evidence_density_score": 4.0,
        "section_coherence_score": 3.0,
    }
    table = bench._render_compare_markdown(current, baseline, delta)
    assert "| metric | current | baseline | delta |" in table
    assert "| overall | 72.00 | 70.00 | +2.00 |" in table
