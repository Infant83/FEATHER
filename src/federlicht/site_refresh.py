from __future__ import annotations

import datetime as dt
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional, Callable


_STRIP_BLOCK_RE = re.compile(r"(?is)<(script|style|noscript)[^>]*>.*?</\\1>")
_TOKEN_RE_EN = re.compile(r"[a-z]{3,}")
_TOKEN_RE_KO = re.compile(r"[가-힣]{2,}")

_STOPWORDS_EN = {
    "the","and","for","with","from","this","that","are","is","was","were","be","been","being","to","of","in","on","at",
    "by","as","or","not","it","its","we","our","you","your","they","their","he","she","his","her","them","a","an","but",
    "into","over","under","about","after","before","than","then","so","if","also","can","could","should","would","may",
    "might","will","shall","such","these","those","via","etc","et","al","e.g","i.e","per","vs","based",
    "report","reports","paper","papers","study","studies","summary","abstract","executive","overview","introduction",
    "methods","method","results","discussion","conclusion","appendix","section","figure",
    "federlicht",
}

_STOPWORDS_KO = {
    "그리고","그러나","하지만","또한","또는","및","등","또","더","것","수","때","위해","대한","관련",
    "있다","없다","한다","된다","하는","하면","하며","했다","했다는","였습니다","입니다","합니다",
    "보고서","요약","초록","서론","방법","결과","결론","부록","섹션","그림",
    "이번","최근","여기","이를","이를","그것","이것","저것","우리","사용자",
}


def strip_html_noise(value: str) -> str:
    if not value:
        return ""
    return _STRIP_BLOCK_RE.sub(" ", value)


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
    parser.feed(strip_html_noise(value))
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


def extract_section_texts_html(report: str, targets: set[str]) -> str:
    if not report:
        return ""
    pattern = re.compile(r"(?is)<h([1-6])[^>]*>(.*?)</h\1>(.*?)(?=<h[1-6]|\Z)")
    sections: list[str] = []
    for match in pattern.finditer(report):
        title = html_to_text(match.group(2)).strip().lower()
        title = re.sub(r"[^a-z0-9가-힣\\s]", "", title)
        if not title or title not in targets:
            continue
        body = match.group(3)
        para = re.search(r"(?is)<p[^>]*>(.*?)</p>", body)
        if para:
            text = html_to_text(para.group(1)).strip()
        else:
            text = html_to_text(body).strip()
        text = re.sub(r"\\s+", " ", text).strip()
        if text:
            sections.append(text)
    return " ".join(sections).strip()


def tokenize_text(text: str) -> list[str]:
    if not text:
        return []
    cleaned = re.sub(r"https?://\\S+", " ", text.lower())
    tokens = _TOKEN_RE_EN.findall(cleaned) + _TOKEN_RE_KO.findall(cleaned)
    return tokens


def build_keyword_counts(text: str, limit: int = 24) -> list[list[object]]:
    tokens = []
    for token in tokenize_text(text):
        if token in _STOPWORDS_EN or token in _STOPWORDS_KO:
            continue
        if len(token) > 30:
            continue
        tokens.append(token)
    if not tokens:
        return []
    counts = Counter(tokens)
    return [[term, int(count)] for term, count in counts.most_common(limit)]


def _cache_key(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", value)


def load_keyword_cache(cache_path: Path, source_mtime: int, source_size: int) -> Optional[list[list[object]]]:
    if not cache_path.exists():
        return None
    try:
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if payload.get("source_mtime") != source_mtime or payload.get("source_size") != source_size:
        return None
    return payload.get("keywords")


def save_keyword_cache(cache_path: Path, source_mtime: int, source_size: int, keywords: list[list[object]]) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source_mtime": source_mtime,
        "source_size": source_size,
        "keywords": keywords,
    }
    cache_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def derive_report_summary(report: str, limit: int = 220) -> str:
    targets = {
        "abstract",
        "executive summary",
        "lede",
        "hook",
        "synopsis",
        "overview",
        "summary",
        "요약",
        "초록",
        "핵심 요약",
        "개요",
        "개관",
    }
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
    existing_items: Optional[dict[str, dict]] = None,
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
    meta_stem = str(meta.get("report_stem") or "")
    cache_dir = site_root / "analytics" / "cache"
    def needs_refresh(existing: dict, report_path: Path) -> bool:
        title = str(existing.get("title") or "")
        summary = str(existing.get("summary") or "")
        stem = report_path.stem
        if not summary:
            return True
        if title.strip() == stem:
            return True
        noisy_tokens = ("window.MathJax", "@import", "MathJax")
        if any(token in summary for token in noisy_tokens):
            return True
        if existing.get("template") in {"unknown", None}:
            return True
        if existing.get("lang") in {"unknown", None}:
            return True
        return False
    for report_path in iter_report_files(run_dir):
        report_id = f"{run_dir.name}:{report_path.stem}"
        stat = report_path.stat()
        existing = existing_items.get(report_id) if existing_items else None
        if (
            existing
            and existing.get("source_mtime") == int(stat.st_mtime)
            and existing.get("source_size") == int(stat.st_size)
            and not needs_refresh(existing, report_path)
        ):
            entries.append(existing)
            continue
        overview_path = report_overview_dir / f"run_overview_{report_path.stem}.md"
        overview_meta = parse_report_overview_metadata(overview_path) if overview_path.exists() else {}
        use_meta = meta_stem and meta_stem == report_path.stem
        title = (meta.get("title") if use_meta else None)
        author = (meta.get("author") if use_meta else None) or default_author
        summary = (meta.get("summary") if use_meta else None) or ""
        keywords: list[list[object]] = []
        template_entry = str(overview_meta.get("template") or template_name)
        language_entry = str(overview_meta.get("language") or language)
        format_entry = str(overview_meta.get("format") or output_format)
        model_entry = str(model_name)
        tags_entry = tags_list
        content = ""
        misc_meta = {}
        cache_path = cache_dir / f"{_cache_key(report_id)}.json"
        keywords = load_keyword_cache(cache_path, int(stat.st_mtime), int(stat.st_size)) or []
        needs_content = (
            not summary
            or not title
            or not author
            or template_entry == "unknown"
            or language_entry == "unknown"
            or not keywords
        )
        if needs_content:
            content = report_path.read_text(encoding="utf-8", errors="replace")
            misc_meta = extract_misc_metadata_from_report(content)
        if not title:
            title = extract_title_from_report(content) or report_path.stem
        title = simple_title(str(title))
        if not author:
            author = extract_author_from_report(content) or default_author
        if not summary:
            summary = derive_report_summary(content)
        if not keywords:
            targets = {
                "abstract",
                "executive summary",
                "lede",
                "hook",
                "synopsis",
                "overview",
                "summary",
                "요약",
                "초록",
                "핵심 요약",
                "개요",
                "개관",
            }
            focus_text = extract_section_texts_html(content, targets)
            if not focus_text:
                focus_text = summary or derive_report_summary(content)
            keywords = build_keyword_counts(focus_text, limit=24)
            save_keyword_cache(cache_path, int(stat.st_mtime), int(stat.st_size), keywords)
        if misc_meta:
            template_entry = str(misc_meta.get("template") or template_entry)
            language_entry = str(misc_meta.get("language") or language_entry)
            format_entry = str(misc_meta.get("format") or format_entry)
            model_entry = str(misc_meta.get("model") or model_entry)
            tags_entry = misc_meta.get("tags") or tags_entry
        stamp = dt.datetime.fromtimestamp(stat.st_mtime)
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
            entry["id"] = report_id
            entry["source_mtime"] = int(stat.st_mtime)
            entry["source_size"] = int(stat.st_size)
            entry["run"] = run_dir.name
            entry["report_stem"] = report_path.stem
            entry["keywords"] = keywords
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
    existing_items: dict[str, dict] = {}
    manifest_path = site_root / "manifest.json"
    if manifest_path.exists():
        try:
            existing_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing_manifest = {}
        for item in existing_manifest.get("items", []) if isinstance(existing_manifest, dict) else []:
            if isinstance(item, dict) and item.get("id"):
                existing_items[str(item["id"])] = item
    if runs_dir.exists():
        for run_dir in sorted([path for path in runs_dir.iterdir() if path.is_dir()]):
            entries.extend(
                build_site_entries_for_run(
                    run_dir,
                    site_root,
                    build_entry,
                    default_author,
                    existing_items=existing_items,
                )
            )
    manifest = write_manifest(site_root, entries)
    index_path = write_index(site_root, manifest, refresh_minutes)
    write_site_analytics(site_root, entries, window_days=30)
    return manifest, index_path


def write_site_analytics(site_root: Path, entries: list[dict], window_days: int = 30) -> None:
    analytics_dir = site_root / "analytics"
    analytics_dir.mkdir(parents=True, exist_ok=True)
    cutoff = dt.datetime.now() - dt.timedelta(days=window_days)
    def is_recent(item: dict) -> bool:
        stamp = item.get("timestamp") or item.get("date")
        if not stamp:
            return False
        try:
            when = dt.datetime.fromisoformat(stamp)
        except ValueError:
            try:
                when = dt.datetime.strptime(stamp, "%Y-%m-%d")
            except ValueError:
                return False
        return when >= cutoff
    recent_items = [item for item in entries if is_recent(item)]
    counts: Counter[str] = Counter()
    for item in recent_items:
        for pair in item.get("keywords") or []:
            if isinstance(pair, (list, tuple)) and len(pair) == 2:
                term = str(pair[0])
                count = int(pair[1])
                counts[term] += count
            elif isinstance(pair, str):
                counts[pair] += 1
    keywords = [[term, int(count)] for term, count in counts.most_common(60)]
    payload = {
        "generated_at": dt.datetime.now().isoformat(),
        "window_days": window_days,
        "total_reports": len(entries),
        "total_recent": len(recent_items),
        "keywords": keywords,
    }
    (analytics_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
