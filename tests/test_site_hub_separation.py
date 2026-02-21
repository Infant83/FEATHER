from __future__ import annotations

from datetime import datetime
from pathlib import Path

from federlicht import report as report_mod
from federlicht import site_refresh


def test_build_site_manifest_entry_supports_report_hub_relative_paths(tmp_path: Path) -> None:
    site_root = tmp_path / "site" / "report_hub"
    site_root.mkdir(parents=True, exist_ok=True)
    run_dir = tmp_path / "site" / "runs" / "demo"
    run_dir.mkdir(parents=True, exist_ok=True)
    report_path = run_dir / "report_full.html"
    report_path.write_text("<h1>demo</h1>", encoding="utf-8")

    entry = report_mod.build_site_manifest_entry(
        site_root=site_root,
        run_dir=run_dir,
        output_path=report_path,
        title="demo",
        author="tester",
        summary="summary",
        output_format="html",
        template_name="default",
        language="ko",
        generated_at=datetime.now(),
    )

    assert entry is not None
    assert entry["paths"]["report"] == "../runs/demo/report_full.html"
    assert entry["paths"]["run"] == "../runs/demo"


def test_site_refresh_falls_back_to_sibling_runs_when_hub_has_no_runs(tmp_path: Path) -> None:
    site_root = tmp_path / "site" / "report_hub"
    site_root.mkdir(parents=True, exist_ok=True)
    run_dir = tmp_path / "site" / "runs" / "demo"
    run_dir.mkdir(parents=True, exist_ok=True)
    report_path = run_dir / "report_full.html"
    report_path.write_text("<h1>demo</h1><p>summary</p>", encoding="utf-8")

    manifest, index_path = site_refresh.refresh_site_from_runs(
        site_root,
        None,
        report_mod.build_site_manifest_entry,
        report_mod.write_site_manifest,
        report_mod.write_site_index,
        refresh_minutes=10,
        default_author="Federlicht",
    )

    assert index_path.exists()
    items = manifest.get("items")
    assert isinstance(items, list)
    assert len(items) == 1
    assert items[0]["paths"]["report"] == "../runs/demo/report_full.html"
