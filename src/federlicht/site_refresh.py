from __future__ import annotations

import datetime as dt
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional, Callable


class _HTMLStripper(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []

    def handle_data(self, data: str) -> None:
        if data:
            self._chunks.append(data)

    def get_text(self) -> str:
        return "".join(self._chunks)


def html_to_text(value: str) -> str:
    parser = _HTMLStripper()
    parser.feed(value)
    return parser.get_text()


def truncate_text(text: str, limit: int = 200) -> str:
    if len(text) <= limit:
        return text
    return text[: max(limit - 1, 1)].rstrip() + "…"


def simple_title(title: str, limit: int = 72) -> str:
    cleaned = re.sub(r"\s+", " ", title).strip()
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 1].rstrip() + "…"


def extract_section_summary_html(report: str, targets: set[str]) -> Optional[str]:
    if not report:
        return None
    pattern = re.compile(r"(?is)<h([1-6])[^>]*>(.*?)</h\1>(.*?)(?=<h[1-6]|\Z)")
    for match in pattern.finditer(report):
        title = html_to_text(match.group(2)).strip().lower()
        title = re.sub(r"[^a-z0-9가-힣\s]", "", title)
        if not title:
            continue
        if title in targets:
            body = match.group(3)
            para = re.search(r"(?is)<p[^>]*>(.*?)</p>", body)
            if para:
                text = html_to_text(para.group(1)).strip()
            else:
                text = html_to_text(body).strip()
            text = re.sub(r"\s+", " ", text).strip()
            return text or None
    return None


def derive_report_summary(report: str, limit: int = 220) -> str:
    targets = {"abstract", "executive summary", "요약", "초록", "핵심 요약"}
    summary = extract_section_summary_html(report, targets)
    if summary:
        return truncate_text(summary, limit)
    text = html_to_text(report)
    text = re.sub(r"\s+", " ", text).strip()
    return truncate_text(text, limit) if text else ""


def extract_title_from_report(content: str) -> Optional[str]:
    if not content:
        return None
    match = re.search(r"(?is)<h1[^>]*>(.*?)</h1>", content)
    if match:
        return html_to_text(match.group(1)).strip()
    match = re.search(r"(?is)<title[^>]*>(.*?)</title>", content)
    if match:
        return html_to_text(match.group(1)).strip()
    return None


def extract_author_from_report(content: str) -> Optional[str]:
    if not content:
        return None
    text = html_to_text(content)
    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith("federlicht assisted and prompted by"):
            return line.split("by", 1)[-1].strip().strip("\"")
        if line.lower().startswith("byline"):
            return line.split(":", 1)[-1].strip()
    return None


def extract_misc_metadata_from_report(content: str) -> dict:
    if not content:
        return {}
    text = html_to_text(content)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    meta: dict = {}
    for line in lines:
        if line.startswith("Template: "):
            meta["template"] = line.split("Template: ", 1)[1].strip()
        elif line.startswith("Model: "):
            meta["model"] = line.split("Model: ", 1)[1].strip()
        elif line.startswith("Output format: "):
            meta["format"] = line.split("Output format: ", 1)[1].strip()
        elif line.startswith("Language: "):
            meta["language"] = line.split("Language: ", 1)[1].strip()
        elif line.startswith("Tags: "):
            tags = [tag.strip() for tag in line.split("Tags: ", 1)[1].split(",")]
            meta["tags"] = [tag for tag in tags if tag]
    return meta


def parse_report_overview_metadata(overview_path: Path) -> dict:
    data: dict = {}
    if not overview_path.exists():
        return data
    for line in overview_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("Template: "):
            data["template"] = line.split("Template: ", 1)[1].strip()
        elif line.startswith("Format: "):
            data["format"] = line.split("Format: ", 1)[1].strip()
        elif line.startswith("Language: "):
            data["language"] = line.split("Language: ", 1)[1].strip()
    return data


def iter_report_files(run_dir: Path) -> list[Path]:
    return sorted([path for path in run_dir.glob("report*.html") if path.is_file()])


def build_site_entries_for_run(
    run_dir: Path,
    site_root: Path,
    build_entry: Callable[..., Optional[dict]],
    default_author: str,
) -> list[dict]:
    entries: list[dict] = []
    meta_path = run_dir / "report_notes" / "report_meta.json"
    meta: dict = {}
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            meta = {}
    report_overview_dir = run_dir / "report"
    workflow_path = run_dir / "report_notes" / "report_workflow.md"
    template_name = str(meta.get("template") or "unknown")
    language = str(meta.get("language") or "unknown")
    output_format = str(meta.get("output_format") or "html")
    model_name = str(meta.get("model") or "unknown")
    tags_list = meta.get("tags") or []
    for report_path in iter_report_files(run_dir):
        content = report_path.read_text(encoding="utf-8", errors="replace")
        misc_meta = extract_misc_metadata_from_report(content)
        title = extract_title_from_report(content) or meta.get("title") or report_path.stem
        title = simple_title(str(title))
        author = extract_author_from_report(content) or meta.get("author") or default_author
        summary = derive_report_summary(content)
        stamp = dt.datetime.fromtimestamp(report_path.stat().st_mtime)
        overview_path = report_overview_dir / f"run_overview_{report_path.stem}.md"
        overview_meta = parse_report_overview_metadata(overview_path) if overview_path.exists() else {}
        template_entry = str(
            overview_meta.get("template")
            or misc_meta.get("template")
            or template_name
        )
        language_entry = str(
            overview_meta.get("language")
            or misc_meta.get("language")
            or language
        )
        format_entry = str(
            overview_meta.get("format")
            or misc_meta.get("format")
            or output_format
        )
        model_entry = str(misc_meta.get("model") or model_name)
        tags_entry = misc_meta.get("tags") or tags_list
        entry = build_entry(
            site_root,
            run_dir,
            report_path,
            str(title),
            str(author),
            summary,
            format_entry,
            template_entry,
            language_entry,
            stamp,
            report_overview_path=overview_path if overview_path.exists() else None,
            workflow_path=workflow_path if workflow_path.exists() else None,
            model_name=model_entry,
            tags=tags_entry if isinstance(tags_entry, list) else None,
        )
        if entry:
            entry["id"] = f"{run_dir.name}:{report_path.stem}"
            entries.append(entry)
    return entries


def refresh_site_from_runs(
    site_root: Path,
    runs_root: Optional[Path],
    build_entry: Callable[..., Optional[dict]],
    write_manifest: Callable[[Path, list[dict]], dict],
    write_index: Callable[[Path, dict, int], Path],
    refresh_minutes: int = 10,
    default_author: str = "Federlicht",
) -> tuple[dict, Path]:
    runs_dir = runs_root or (site_root / "runs")
    entries: list[dict] = []
    if runs_dir.exists():
        for run_dir in sorted([path for path in runs_dir.iterdir() if path.is_dir()]):
            entries.extend(build_site_entries_for_run(run_dir, site_root, build_entry, default_author))
    manifest = write_manifest(site_root, entries)
    index_path = write_index(site_root, manifest, refresh_minutes)
    return manifest, index_path
