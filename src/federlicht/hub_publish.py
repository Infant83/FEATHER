from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from . import report as report_mod
from . import site_refresh as refresh_mod


@dataclass
class HubPublishResult:
    run_dir: Path
    report_path: Path
    hub_root: Path
    published_report_path: Path
    published_overview_path: Optional[Path]
    published_workflow_path: Optional[Path]
    manifest_path: Path
    index_path: Path
    entry_id: str


def _resolve_run_dir(report_path: Path, run_dir: Optional[Path]) -> Path:
    if run_dir:
        return run_dir.resolve()
    if report_path.parent.name.lower() == "report" and report_path.parent.parent.exists():
        return report_path.parent.parent.resolve()
    return report_path.parent.resolve()


def _read_report_meta(run_dir: Path) -> dict:
    meta_path = run_dir / "report_notes" / "report_meta.json"
    if not meta_path.exists():
        return {}
    try:
        payload = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _copy_if_exists(source: Optional[Path], destination: Path, *, overwrite: bool) -> Optional[Path]:
    if not source or not source.exists():
        return None
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not overwrite:
        return destination
    shutil.copy2(source, destination)
    return destination


def publish_report_to_hub(
    *,
    report_path: Path,
    hub_root: Path,
    run_dir: Optional[Path] = None,
    title: Optional[str] = None,
    author: Optional[str] = None,
    summary: Optional[str] = None,
    copy_overview: bool = True,
    copy_workflow: bool = True,
    refresh_minutes: int = 10,
    overwrite: bool = True,
) -> HubPublishResult:
    report_abs = report_path.resolve()
    if not report_abs.exists() or not report_abs.is_file():
        raise FileNotFoundError(f"report not found: {report_abs}")
    run_abs = _resolve_run_dir(report_abs, run_dir)
    hub_abs = hub_root.resolve()
    hub_abs.mkdir(parents=True, exist_ok=True)

    published_run_dir = hub_abs / "reports" / run_abs.name
    published_run_dir.mkdir(parents=True, exist_ok=True)
    published_report_path = published_run_dir / report_abs.name
    if published_report_path.exists() and not overwrite:
        raise FileExistsError(f"published report already exists: {published_report_path}")
    shutil.copy2(report_abs, published_report_path)

    overview_src = run_abs / "report" / f"run_overview_{report_abs.stem}.md"
    if not overview_src.exists():
        legacy_overview = run_abs / "report" / "run_overview.md"
        overview_src = legacy_overview if legacy_overview.exists() else overview_src
    workflow_src = run_abs / "report_notes" / "report_workflow.md"
    published_overview_path = (
        _copy_if_exists(overview_src, published_run_dir / overview_src.name, overwrite=overwrite)
        if copy_overview
        else None
    )
    published_workflow_path = (
        _copy_if_exists(workflow_src, published_run_dir / workflow_src.name, overwrite=overwrite)
        if copy_workflow
        else None
    )

    output_format = report_mod.choose_format(str(report_abs))
    meta = _read_report_meta(run_abs)
    body = report_abs.read_text(encoding="utf-8", errors="replace")
    resolved_title = (
        str(title or "").strip()
        or str(meta.get("title") or "").strip()
        or refresh_mod.extract_title_from_report(body)
        or report_abs.stem
    )
    resolved_title = refresh_mod.simple_title(resolved_title)
    resolved_author = (
        str(author or "").strip()
        or str(meta.get("author") or "").strip()
        or refresh_mod.extract_author_from_report(body)
        or report_mod.DEFAULT_AUTHOR
    )
    resolved_summary = (
        str(summary or "").strip()
        or str(meta.get("summary") or "").strip()
        or refresh_mod.derive_report_summary(body)
    )
    template_name = str(meta.get("template") or "unknown")
    language = str(meta.get("language") or "unknown")
    model_name = str(meta.get("model") or "")
    tags = meta.get("tags")
    if not isinstance(tags, list):
        tags = []
    generated_at = dt.datetime.fromtimestamp(report_abs.stat().st_mtime)

    entry = report_mod.build_site_manifest_entry(
        site_root=hub_abs,
        run_dir=published_run_dir,
        output_path=published_report_path,
        title=resolved_title,
        author=resolved_author,
        summary=resolved_summary,
        output_format=output_format,
        template_name=template_name,
        language=language,
        generated_at=generated_at,
        report_overview_path=published_overview_path,
        workflow_path=published_workflow_path,
        model_name=model_name,
        tags=tags,
    )
    if not entry:
        raise RuntimeError("failed to build report_hub manifest entry")
    manifest = report_mod.update_site_manifest(hub_abs, entry)
    index_path = report_mod.write_site_index(hub_abs, manifest, refresh_minutes=refresh_minutes)
    return HubPublishResult(
        run_dir=run_abs,
        report_path=report_abs,
        hub_root=hub_abs,
        published_report_path=published_report_path,
        published_overview_path=published_overview_path,
        published_workflow_path=published_workflow_path,
        manifest_path=hub_abs / "manifest.json",
        index_path=index_path,
        entry_id=str(entry.get("id") or run_abs.name),
    )


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Publish a run report into report_hub and update manifest/index.",
    )
    parser.add_argument("--report", required=True, help="Path to report file (html/md/tex).")
    parser.add_argument("--hub", default="site/report_hub", help="Hub root path (default: site/report_hub).")
    parser.add_argument("--run", default="", help="Optional run directory path.")
    parser.add_argument("--title", default="", help="Optional title override.")
    parser.add_argument("--author", default="", help="Optional author override.")
    parser.add_argument("--summary", default="", help="Optional summary override.")
    parser.add_argument(
        "--refresh-minutes",
        type=int,
        default=10,
        help="Meta-refresh minutes for generated index.html (default: 10).",
    )
    parser.add_argument(
        "--no-overview",
        action="store_true",
        default=False,
        help="Skip copying run_overview markdown into hub.",
    )
    parser.add_argument(
        "--no-workflow",
        action="store_true",
        default=False,
        help="Skip copying report_workflow markdown into hub.",
    )
    parser.add_argument(
        "--no-overwrite",
        action="store_true",
        default=False,
        help="Do not overwrite existing published files.",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    run_dir = Path(args.run).resolve() if str(args.run or "").strip() else None
    result = publish_report_to_hub(
        report_path=Path(args.report),
        hub_root=Path(args.hub),
        run_dir=run_dir,
        title=args.title or None,
        author=args.author or None,
        summary=args.summary or None,
        copy_overview=not bool(args.no_overview),
        copy_workflow=not bool(args.no_workflow),
        refresh_minutes=max(1, int(args.refresh_minutes)),
        overwrite=not bool(args.no_overwrite),
    )
    print(f"Published report: {result.published_report_path}")
    if result.published_overview_path:
        print(f"Published overview: {result.published_overview_path}")
    if result.published_workflow_path:
        print(f"Published workflow: {result.published_workflow_path}")
    print(f"Updated manifest: {result.manifest_path}")
    print(f"Updated index: {result.index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

