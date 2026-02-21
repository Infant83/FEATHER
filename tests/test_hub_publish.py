from __future__ import annotations

import json
from pathlib import Path

from federlicht.hub_publish import publish_report_to_hub


def test_publish_report_to_hub_copies_assets_and_updates_manifest(tmp_path: Path) -> None:
    run_dir = tmp_path / "runs" / "demo"
    report_path = run_dir / "report_full.html"
    overview_path = run_dir / "report" / "run_overview_report_full.md"
    workflow_path = run_dir / "report_notes" / "report_workflow.md"
    meta_path = run_dir / "report_notes" / "report_meta.json"
    overview_path.parent.mkdir(parents=True, exist_ok=True)
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report_path.write_text(
        "<html><body><h1>Demo Report</h1><p>A concise summary sentence.</p></body></html>",
        encoding="utf-8",
    )
    overview_path.write_text("# Run Overview\n", encoding="utf-8")
    workflow_path.write_text("# Workflow\n", encoding="utf-8")
    meta_path.write_text(
        json.dumps(
            {
                "title": "Demo Report",
                "author": "Test Author",
                "summary": "summary from meta",
                "template": "default",
                "language": "ko",
                "model": "gpt-5.2",
                "tags": ["qc", "demo"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    hub_root = tmp_path / "site" / "report_hub"
    result = publish_report_to_hub(report_path=report_path, hub_root=hub_root, run_dir=run_dir)

    assert result.published_report_path.exists()
    assert result.published_overview_path and result.published_overview_path.exists()
    assert result.published_workflow_path and result.published_workflow_path.exists()
    assert result.index_path.exists()
    assert result.manifest_path.exists()

    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    item = manifest["items"][0]
    assert item["title"] == "Demo Report"
    assert item["author"] == "Test Author"
    assert item["paths"]["report"] == "reports/demo/report_full.html"
    assert item["paths"]["run"] == "reports/demo"
    assert item["paths"]["overview"] == "reports/demo/run_overview_report_full.md"
    assert item["paths"]["workflow"] == "reports/demo/report_workflow.md"


def test_publish_report_to_hub_inferrs_run_dir_from_report_subfolder(tmp_path: Path) -> None:
    run_dir = tmp_path / "runs" / "demo2"
    report_dir = run_dir / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "report_full.html"
    report_path.write_text("<html><body><h1>Auto Run Dir</h1></body></html>", encoding="utf-8")

    hub_root = tmp_path / "site" / "report_hub"
    result = publish_report_to_hub(report_path=report_path, hub_root=hub_root)

    assert result.run_dir == run_dir.resolve()
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    item = manifest["items"][0]
    assert item["id"] == "demo2"
    assert item["paths"]["report"] == "reports/demo2/report_full.html"

