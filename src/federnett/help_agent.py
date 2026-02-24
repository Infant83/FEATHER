from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator
from urllib.parse import urlparse

from .capabilities import infer_capability_action, runtime_capabilities
from .constants import DEFAULT_RUN_ROOTS
from .utils import safe_rel

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover - optional runtime dependency
    requests = None  # type: ignore

try:
    import tomllib
except Exception:  # pragma: no cover - Python <3.11 fallback
    tomllib = None  # type: ignore


_INCLUDE_PATHS = (
    "pyproject.toml",
    "CHANGELOG.md",
    "README.md",
    "docs",
    "src",
    "scripts",
    "site/federnett",
)
_EXCLUDE_PREFIXES = (
    "runs",
    "site/runs",
    "site/analytics",
)
_EXCLUDE_PARTS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}
_TEXT_EXTS = {
    ".md",
    ".txt",
    ".py",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".json",
    ".jsonl",
    ".ndjson",
    ".csv",
    ".tsv",
    ".toml",
    ".yml",
    ".yaml",
}
_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "are",
    "was",
    "how",
    "what",
    "when",
    "where",
    "which",
    "agent",
    "help",
    "code",
    "using",
    "use",
    "show",
    "설명",
    "기능",
    "옵션",
    "사용법",
    "방법",
    "관련",
    "그리고",
    "에서",
    "있는",
    "합니다",
    "해주세요",
}
_MAX_FILE_BYTES = 400_000
_CHUNK_LINES = 80
_CHUNK_OVERLAP = 24
_MAX_SOURCE_TEXT = 360
_MAX_CONTEXT_CHARS = 12000
_MAX_LIVE_LOG_CONTEXT_CHARS = 5200
_MAX_STATE_MEMORY_CONTEXT_CHARS = 4200
_CACHE_LOCK = threading.Lock()
_INDEX_CACHE: dict[str, "_IndexCache"] = {}
_CODEX_MODEL_HINT_LOCK = threading.Lock()
_CODEX_MODEL_HINT_CACHE: dict[str, str] = {}
_HISTORY_TURNS = 10
_HISTORY_CHARS = 1400
_HISTORY_SUMMARY_PREFIX = "[context-compress]"
_META_PATH_HINTS = (
    "pyproject.toml",
    "CHANGELOG.md",
    "README.md",
    "docs/federlicht_report.md",
    "docs/federnett_roadmap.md",
    "src/federnett/app.py",
    "src/federnett/help_agent.py",
)


def _build_known_run_root_prefixes() -> tuple[str, ...]:
    prefixes: list[str] = []
    for raw in [*DEFAULT_RUN_ROOTS, "runs", "site/runs"]:
        token = str(raw or "").strip().replace("\\", "/").strip("/").lower()
        if not token:
            continue
        if token not in prefixes:
            prefixes.append(token)
    prefixes.sort(key=len, reverse=True)
    return tuple(prefixes)


_KNOWN_RUN_ROOT_PREFIXES = _build_known_run_root_prefixes()


def _strip_known_run_root_prefix(token: str) -> str:
    value = str(token or "").strip().replace("\\", "/").strip("/")
    if not value:
        return ""
    lowered = value.lower()
    for prefix in _KNOWN_RUN_ROOT_PREFIXES:
        if lowered == prefix:
            return ""
        marker = f"{prefix}/"
        if lowered.startswith(marker):
            return value[len(marker) :]
    return value


def _mentions_run_root_token(text: str) -> bool:
    lowered = str(text or "").strip().lower()
    if not lowered:
        return False
    return any(f"{prefix}/" in lowered for prefix in _KNOWN_RUN_ROOT_PREFIXES)


def _extract_path_hints(question: str) -> list[str]:
    text = str(question or "").strip().replace("\\", "/")
    if not text:
        return []
    lowered = text.lower()
    candidates: list[str] = []
    candidates.extend(re.findall(r"(?:[a-z0-9_가-힣.\-]+/){1,}[a-z0-9_가-힣.\-]+", lowered))
    candidates.extend(re.findall(r"[a-z0-9_가-힣.\-]+\.(?:jsonl|ndjson|json|md|txt|csv|tsv|log)", lowered))
    deduped: list[str] = []
    seen: set[str] = set()
    for raw in candidates:
        token = str(raw or "").strip().strip("`'\".,;:!?()[]{}")
        token = token.strip("/")
        if not token:
            continue
        if token in seen:
            continue
        seen.add(token)
        deduped.append(token)
    return deduped


def _has_run_content_path_reference(question: str) -> bool:
    text = str(question or "").strip().replace("\\", "/")
    if not text:
        return False
    lowered = text.lower()
    if _extract_path_hints(lowered):
        return True
    marker_tokens = (
        "archive/",
        "instruction/",
        "report_notes/",
        "report/",
        "supporting/",
        "archive 폴더",
        "instruction 폴더",
        "report 폴더",
        "report_notes 폴더",
        "archive 파일",
        "instruction 파일",
        "report 파일",
        "report_notes 파일",
    )
    if any(token in lowered for token in marker_tokens):
        return True
    return bool(
        re.search(
            r"(archive|instruction|report[_\s]?notes?|supporting)\s*(폴더|파일|folder|file|dir|directory)",
            lowered,
            flags=re.IGNORECASE,
        )
    )


def _matches_path_hints(rel_path: str, run_scoped_rel_path: str, path_hints: list[str]) -> bool:
    if not path_hints:
        return True
    rel_l = str(rel_path or "").strip().lower()
    scoped_l = str(run_scoped_rel_path or "").strip().lower()
    rel_leaf = rel_l.rsplit("/", 1)[-1]
    scoped_leaf = scoped_l.rsplit("/", 1)[-1]
    for hint in path_hints:
        token = str(hint or "").strip().lower().strip("/")
        if not token:
            continue
        if "/" in token:
            if token in rel_l or token in scoped_l:
                return True
            if scoped_l.startswith(token):
                return True
        else:
            if token in rel_l or token in scoped_l:
                return True
            if token == rel_leaf or token == scoped_leaf:
                return True
    return False
_RUN_CONTEXT_PATTERNS = (
    "instruction/*.txt",
    "instruction/*.md",
    "report/*.md",
    "report/*.txt",
    "report_notes/*.md",
    "supporting/help_agent/web_search.jsonl",
    "supporting/help_agent/web_extract/*.txt",
    "supporting/help_agent/web_text/*.txt",
    "README.md",
)
_RUN_CONTEXT_ARCHIVE_PATTERNS = (
    "archive/**/*.md",
    "archive/**/*.txt",
    "archive/**/*.json",
    "archive/**/*.jsonl",
    "archive/**/*.ndjson",
    "archive/**/*.csv",
    "archive/**/*.tsv",
)
_MAX_RUN_CONTEXT_FILES = 80
_HELP_LLM_BACKENDS = {"openai_api", "codex_cli"}
_HELP_REASONING_EFFORT_CHOICES = ("off", "none", "low", "medium", "high", "extra_high")
_HELP_REASONING_EFFORT_TO_OPENAI = {
    "off": "",
    "none": "",
    "low": "low",
    "medium": "medium",
    "high": "high",
    "extra_high": "high",
}
_HELP_DEFAULT_REASONING_EFFORT = "off"
_HELP_REASONING_MODEL_RE = re.compile(r"^(gpt-5|o1|o3|o4)", re.IGNORECASE)
_HELP_AGENTIC_ACTION_TYPES = {
    "none",
    "run_feather",
    "run_federlicht",
    "run_feather_then_federlicht",
    "create_run_folder",
    "switch_run",
    "preset_resume_stage",
    "focus_editor",
    "set_action_mode",
    "run_capability",
}
_GENERIC_EXECUTION_TOKENS = (
    "실행",
    "실행해",
    "run",
    "start",
    "돌려",
    "해줘",
    "해 줘",
    "시작",
)
_EXECUTION_INTENT_EXPLICIT_TOKENS = (
    "작업하자",
    "작업해",
    "진행하자",
    "진행해",
    "진행해줘",
    "실행하자",
    "실행해줘",
    "바로실행",
    "지금실행",
    "돌려줘",
    "run it",
    "run now",
    "execute",
    "go ahead",
)
_TOPIC_SIGNAL_TOKENS = (
    "분석",
    "동향",
    "리포트",
    "보고서",
    "요약",
    "근거",
    "evidence",
    "topic",
    "주제",
    "question",
    "문헌",
    "기술",
    "전망",
    "한계",
    "리스크",
)
_WORKSPACE_ACTION_TOKENS = (
    "feather",
    "federlicht",
    "federhav",
    "workflow",
    "pipeline",
    "run folder",
    "run ",
    "run=",
    "런 ",
    "런폴더",
    "스테이지",
    "stage",
    "resume",
    "재시작",
    "instruction",
    "prompt",
    "inline prompt",
    "switch run",
    "mode",
    "모드",
)


@dataclass
class _Doc:
    rel_path: str
    mtime_ns: int
    size: int
    lines: list[str]


@dataclass
class _IndexCache:
    docs: dict[str, _Doc]
    built_at: float


def _is_path_allowed(rel_path: str, *, allow_run_prefixes: bool = False) -> bool:
    rel = rel_path.replace("\\", "/")
    if not rel:
        return False
    if not allow_run_prefixes:
        for prefix in _EXCLUDE_PREFIXES:
            if rel == prefix or rel.startswith(f"{prefix}/"):
                return False
    parts = [p for p in rel.split("/") if p]
    if any(part in _EXCLUDE_PARTS for part in parts):
        return False
    if any(part.endswith(".egg-info") or part.endswith(".dist-info") for part in parts):
        return False
    if any(part.startswith(".") and part not in {".well-known"} for part in parts):
        return False
    suffix = Path(rel).suffix.lower()
    if suffix and suffix not in _TEXT_EXTS:
        return False
    return True


def _iter_candidate_files(root: Path) -> list[Path]:
    files: list[Path] = []
    seen: set[str] = set()
    for raw in _INCLUDE_PATHS:
        target = (root / raw).resolve()
        if not target.exists():
            continue
        if target.is_file():
            rel = safe_rel(target, root)
            if _is_path_allowed(rel) and rel not in seen:
                seen.add(rel)
                files.append(target)
            continue
        for child in target.rglob("*"):
            if not child.is_file():
                continue
            rel = safe_rel(child, root)
            if rel in seen or not _is_path_allowed(rel):
                continue
            try:
                if child.stat().st_size > _MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            seen.add(rel)
            files.append(child)
    return files


def _read_doc(path: Path, root: Path) -> _Doc | None:
    try:
        stat = path.stat()
    except OSError:
        return None
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    rel = safe_rel(path, root)
    return _Doc(
        rel_path=rel,
        mtime_ns=stat.st_mtime_ns,
        size=stat.st_size,
        lines=text.splitlines(),
    )


def _load_index(root: Path) -> _IndexCache:
    key = str(root.resolve())
    with _CACHE_LOCK:
        cached = _INDEX_CACHE.get(key)
        docs = dict(cached.docs) if cached else {}
        current: dict[str, Path] = {}
        for path in _iter_candidate_files(root):
            rel = safe_rel(path, root)
            current[rel] = path
        for rel in list(docs.keys()):
            if rel not in current:
                docs.pop(rel, None)
        for rel, path in current.items():
            try:
                stat = path.stat()
            except OSError:
                continue
            prev = docs.get(rel)
            if prev and prev.mtime_ns == stat.st_mtime_ns and prev.size == stat.st_size:
                continue
            doc = _read_doc(path, root)
            if doc is None:
                continue
            docs[rel] = doc
        out = _IndexCache(docs=docs, built_at=time.time())
        _INDEX_CACHE[key] = out
        return out


def _query_tokens(question: str) -> list[str]:
    lowered = question.strip().lower()
    raw_tokens = re.findall(r"[a-z0-9_가-힣-]{2,}", lowered)
    deduped: list[str] = []
    seen: set[str] = set()
    for tok in raw_tokens:
        parts = [tok]
        # Split mixed-script tokens (e.g., "federnett에서" -> "federnett", "에서")
        parts.extend(re.findall(r"[a-z0-9_]{2,}", tok))
        parts.extend(re.findall(r"[가-힣]{2,}", tok))
        for part in parts:
            if part in _STOPWORDS:
                continue
            if part in seen:
                continue
            seen.add(part)
            deduped.append(part)
    return deduped


def _iter_chunks(lines: list[str]) -> list[tuple[int, int, str]]:
    if not lines:
        return []
    if len(lines) <= _CHUNK_LINES:
        return [(1, len(lines), "\n".join(lines))]
    chunks: list[tuple[int, int, str]] = []
    step = max(1, _CHUNK_LINES - _CHUNK_OVERLAP)
    start = 0
    while start < len(lines):
        end = min(start + _CHUNK_LINES, len(lines))
        text = "\n".join(lines[start:end])
        chunks.append((start + 1, end, text))
        if end >= len(lines):
            break
        start += step
    return chunks


def _chunk_score(
    path: str,
    text: str,
    tokens: list[str],
    question_l: str,
    run_rel_l: str = "",
) -> float:
    if not text:
        return 0.0
    text_l = text.lower()
    path_l = path.lower()
    text_tokens = re.findall(r"[a-z0-9_가-힣-]{2,}", text_l)
    token_counts: dict[str, int] = {}
    for token in text_tokens:
        token_counts[token] = token_counts.get(token, 0) + 1
    path_tokens = set(re.findall(r"[a-z0-9_가-힣-]{2,}", path_l))
    score = 0.0
    if question_l and len(question_l) >= 6 and question_l in text_l:
        score += 10.0
    if run_rel_l and path_l.startswith(run_rel_l):
        score += 4.0
    for tok in tokens:
        count = token_counts.get(tok, 0)
        if count:
            score += float(min(count, 8) * 2)
        if tok in path_tokens:
            score += 2.0
        if tok.startswith("--") and tok in text_l:
            score += 3.0
    option_intent = any(
        tok.startswith("--") or tok in {"option", "options", "arg", "args", "옵션"}
        for tok in tokens
    )
    if option_intent and "--" in text and ("option" in text_l or "arg" in text_l):
        score += 1.0
    meta_intent = any(
        token in question_l
        for token in ("version", "버전", "changelog", "변경", "release", "readme", "업데이트")
    )
    if meta_intent and any(
        marker in path_l for marker in ("pyproject.toml", "readme.md", "changelog.md", "__init__.py")
    ):
        score += 7.0
    auth_intent = any(
        token in question_l
        for token in ("login", "signin", "auth", "계정", "로그인", "권한", "인증", "프로필")
    )
    if auth_intent and any(marker in path_l for marker in ("auth", "profile", "agent_profiles", "federnett")):
        score += 5.0
    return score


def _fallback_sources(index: _IndexCache, max_sources: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for hint in _META_PATH_HINTS:
        doc = index.docs.get(hint)
        if not doc or not doc.lines:
            continue
        excerpt = "\n".join(doc.lines[: min(20, len(doc.lines))]).strip()
        if len(excerpt) > _MAX_SOURCE_TEXT:
            excerpt = excerpt[: _MAX_SOURCE_TEXT - 1] + "..."
        out.append(
            {
                "path": doc.rel_path,
                "start_line": 1,
                "end_line": min(len(doc.lines), 20),
                "score": 0.1,
                "excerpt": excerpt,
            },
        )
        if len(out) >= max(1, max_sources):
            break
    for idx, item in enumerate(out, start=1):
        item["id"] = f"S{idx}"
    return out


def _resolve_run_dir(root: Path, run_rel: str | None) -> Path | None:
    normalized = (run_rel or "").strip().replace("\\", "/").strip("/")
    if not normalized:
        return None
    try:
        run_dir = (root / normalized).resolve()
        run_dir.relative_to(root.resolve())
    except Exception:
        return None
    if not run_dir.exists() or not run_dir.is_dir():
        return None
    return run_dir


def _iter_run_context_files(root: Path, run_rel: str | None, *, question: str = "") -> list[Path]:
    run_dir = _resolve_run_dir(root, run_rel)
    if run_dir is None:
        return []
    normalized_question = str(question or "").strip().lower().replace("\\", "/")
    path_hints = _extract_path_hints(normalized_question)
    include_archive = any("archive" in hint for hint in path_hints) or any(
        token in normalized_question for token in ("archive", "아카이브", ".jsonl", ".ndjson")
    )
    patterns: list[str] = list(_RUN_CONTEXT_PATTERNS)
    if include_archive:
        patterns.extend(_RUN_CONTEXT_ARCHIVE_PATTERNS)
    run_rel_norm = (run_rel or "").strip().replace("\\", "/").strip("/").lower()
    run_prefix = f"{run_rel_norm}/" if run_rel_norm else ""
    files: list[Path] = []
    seen: set[str] = set()
    for pattern in patterns:
        for path in run_dir.glob(pattern):
            if not path.is_file():
                continue
            rel = safe_rel(path, root)
            if rel in seen or not _is_path_allowed(rel, allow_run_prefixes=True):
                continue
            rel_l = rel.replace("\\", "/").lower()
            run_scoped_rel = rel_l
            if run_prefix and rel_l.startswith(run_prefix):
                run_scoped_rel = rel_l[len(run_prefix) :]
            if path_hints and not _matches_path_hints(rel_l, run_scoped_rel, path_hints):
                continue
            try:
                if path.stat().st_size > _MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            seen.add(rel)
            files.append(path)
            if len(files) >= _MAX_RUN_CONTEXT_FILES:
                return files
    return files


def _score_run_context_sources(
    root: Path,
    run_rel: str | None,
    *,
    question: str,
    tokens: list[str],
    question_l: str,
    max_sources: int,
) -> list[dict[str, Any]]:
    scored: list[dict[str, Any]] = []
    run_rel_l = (run_rel or "").strip().replace("\\", "/").strip("/").lower()
    path_hint_bonus = 8.0 if _extract_path_hints(question) else 0.0
    for path in _iter_run_context_files(root, run_rel, question=question):
        doc = _read_doc(path, root)
        if doc is None or not doc.lines:
            continue
        for start, end, text in _iter_chunks(doc.lines):
            score = _chunk_score(doc.rel_path, text, tokens, question_l, run_rel_l=run_rel_l)
            if score <= 0:
                continue
            excerpt = text.strip()
            if len(excerpt) > _MAX_SOURCE_TEXT:
                excerpt = excerpt[: _MAX_SOURCE_TEXT - 1] + "..."
            scored.append(
                {
                    "path": doc.rel_path,
                    "start_line": start,
                    "end_line": end,
                    "score": round(score + 3.0 + path_hint_bonus, 3),
                    "excerpt": excerpt,
                }
            )
    scored.sort(
        key=lambda item: (-float(item["score"]), len(str(item["path"])), int(item["start_line"])),
    )
    return scored[: max(1, max_sources)]


def _select_sources(
    root: Path,
    question: str,
    max_sources: int,
    run_rel: str | None = None,
) -> tuple[list[dict[str, Any]], int]:
    index = _load_index(root)
    tokens = _query_tokens(question)
    question_l = question.strip().lower()
    run_rel_l = (run_rel or "").strip().replace("\\", "/").strip("/").lower()
    scored: list[dict[str, Any]] = []
    for doc in index.docs.values():
        if not doc.lines:
            continue
        for start, end, text in _iter_chunks(doc.lines):
            score = _chunk_score(doc.rel_path, text, tokens, question_l, run_rel_l=run_rel_l)
            if score <= 0:
                continue
            excerpt = text.strip()
            if len(excerpt) > _MAX_SOURCE_TEXT:
                excerpt = excerpt[: _MAX_SOURCE_TEXT - 1] + "..."
            scored.append(
                {
                    "path": doc.rel_path,
                    "start_line": start,
                    "end_line": end,
                    "score": round(score, 3),
                    "excerpt": excerpt,
                }
            )
    scored.sort(
        key=lambda item: (-float(item["score"]), len(str(item["path"])), int(item["start_line"])),
    )
    run_context_scored = _score_run_context_sources(
        root,
        run_rel,
        question=question,
        tokens=tokens,
        question_l=question_l,
        max_sources=max(2, min(6, max_sources)),
    )
    if run_context_scored:
        scored.extend(run_context_scored)
        scored.sort(
            key=lambda item: (-float(item["score"]), len(str(item["path"])), int(item["start_line"])),
        )
    selected: list[dict[str, Any]] = []
    seen_chunks: set[tuple[str, int, int]] = set()
    for item in scored:
        key = (
            str(item.get("path") or ""),
            int(item.get("start_line") or 0),
            int(item.get("end_line") or 0),
        )
        if key in seen_chunks:
            continue
        seen_chunks.add(key)
        selected.append(item)
        if len(selected) >= max(1, max_sources):
            break
    if not selected:
        selected = _fallback_sources(index, max_sources)
    for idx, item in enumerate(selected, start=1):
        item["id"] = f"S{idx}"
    return selected, len(index.docs)


def _build_context(sources: list[dict[str, Any]]) -> str:
    chunks: list[str] = []
    used = 0
    for src in sources:
        piece = (
            f"[{src['id']}] {src['path']}:{src['start_line']}-{src['end_line']}\n"
            f"{src['excerpt']}\n"
        )
        next_used = used + len(piece)
        if next_used > _MAX_CONTEXT_CHARS and chunks:
            break
        chunks.append(piece)
        used = next_used
    return "\n".join(chunks).strip()


def _normalize_history(history: Any) -> list[dict[str, str]]:
    if not isinstance(history, list):
        return []
    cleaned: list[dict[str, str]] = []
    for item in history[-40:]:
        if not isinstance(item, dict):
            continue
        role = str(item.get("role") or "").strip().lower()
        if role not in {"user", "assistant"}:
            continue
        content = str(item.get("content") or "").strip()
        if not content:
            continue
        cleaned.append(
            {
                "role": role,
                "content": content[:_HISTORY_CHARS],
            },
        )
    if not cleaned:
        return []
    recent = cleaned[-_HISTORY_TURNS:]
    summary_entry: dict[str, str] | None = None
    for item in cleaned:
        if item.get("role") != "assistant":
            continue
        content = str(item.get("content") or "").strip()
        if not content:
            continue
        if content.lower().startswith(_HISTORY_SUMMARY_PREFIX):
            summary_entry = item
    if summary_entry:
        summary_content = str(summary_entry.get("content") or "").strip()
        if summary_content and all(str(item.get("content") or "").strip() != summary_content for item in recent):
            return [summary_entry, *recent]
    return recent


def _normalize_live_log_tail(live_log_tail: Any) -> str:
    if not isinstance(live_log_tail, str):
        return ""
    text = live_log_tail.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\x00", "").strip()
    if not text:
        return ""
    return text[-_MAX_LIVE_LOG_CONTEXT_CHARS:]


def _normalize_state_memory(state_memory: Any) -> str:
    if not isinstance(state_memory, dict):
        return ""
    try:
        text = json.dumps(state_memory, ensure_ascii=False, default=str)
    except Exception:
        return ""
    text = str(text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return ""
    if len(text) > _MAX_STATE_MEMORY_CONTEXT_CHARS:
        text = f"{text[: max(1, _MAX_STATE_MEMORY_CONTEXT_CHARS - 1)].rstrip()}…"
    return text


def _normalize_execution_mode(value: Any) -> str:
    token = str(value or "").strip().lower()
    if token in {"act", "execute", "run"}:
        return "act"
    return "plan"


def _normalize_runtime_mode(value: Any) -> str:
    token = str(value or "").strip().lower()
    if token in {"off", "0", "false", "none", "disable", "disabled"}:
        return "off"
    if token in {"deepagent", "agentic", "on", "1", "true"}:
        return "deepagent"
    return "auto"


def _resolve_help_runtime_mode(preferred: str | None = None) -> str:
    env_mode = (
        str(os.getenv("FEDERHAV_AGENTIC_RUNTIME") or "").strip()
        or str(os.getenv("FEDERHAV_RUNTIME_MODE") or "").strip()
    )
    return _normalize_runtime_mode(preferred or env_mode or "auto")


def _normalize_agent_label(value: Any) -> str:
    token = str(value or "").strip()
    if not token:
        return "federhav"
    safe = "".join(ch for ch in token if ch.isalnum() or ch in {"_", "-", "."})
    return safe[:80] or "federhav"


def _augment_help_question(
    question: str,
    *,
    execution_mode: str,
    agent: str,
    allow_artifacts: bool,
) -> str:
    q = str(question or "").strip()
    mode = _normalize_execution_mode(execution_mode)
    agent_id = _normalize_agent_label(agent)
    policy = (
        "plan-confirm (suggested actions require confirmation; direct sidebar runs are unaffected)"
        if mode == "plan"
        else "act (safe suggested actions may auto-run; direct sidebar runs are unaffected)"
    )
    artifact_note = "allow_artifacts=true" if allow_artifacts else "allow_artifacts=false"
    hints = (
        "[operator-control]",
        f"agent={agent_id}",
        f"execution_mode={mode}",
        f"policy={policy}",
        "scope=execution_mode controls FederHav suggested actions only",
        artifact_note,
    )
    return f"{q}\n\n" + "\n".join(hints)


def _build_help_web_queries(question: str, history: list[dict[str, str]] | None) -> list[str]:
    queries: list[str] = []
    primary = str(question or "").strip()
    if primary:
        queries.append(primary)
    normalized = _normalize_history(history)
    for item in reversed(normalized):
        if item.get("role") != "user":
            continue
        text = str(item.get("content") or "").strip()
        if not text:
            continue
        if text == primary:
            continue
        queries.append(text)
        if len(queries) >= 3:
            break
    deduped: list[str] = []
    seen: set[str] = set()
    for query in queries:
        key = query.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(query)
    return deduped[:3]


def _should_run_help_web_search(question: str, history: list[dict[str, str]] | None) -> bool:
    text = str(question or "").strip().lower()
    if not text:
        return False
    triggers = (
        "웹검색",
        "web search",
        "검색",
        "찾아",
        "최신",
        "뉴스",
        "논문",
        "paper",
        "arxiv",
        "openalex",
        "link",
        "source",
        "근거",
        "시장",
        "동향",
    )
    if any(token in text for token in triggers):
        return True
    normalized = _normalize_history(history)
    for item in reversed(normalized):
        if item.get("role") != "user":
            continue
        prev = str(item.get("content") or "").strip().lower()
        if any(token in prev for token in triggers):
            return True
    return False


def _run_help_web_research(
    root: Path,
    *,
    question: str,
    run_rel: str | None,
    history: list[dict[str, str]] | None,
) -> str:
    run_dir = _resolve_run_dir(root, run_rel)
    if run_dir is None:
        return "web_search skipped: run folder not selected."
    api_key = str(os.getenv("TAVILY_API_KEY") or "").strip()
    if not api_key:
        return "web_search skipped: TAVILY_API_KEY is not set."
    queries = _build_help_web_queries(question, history)
    if not queries:
        return "web_search skipped: no query generated."
    try:
        from feather.web_research import run_supporting_web_research

        supporting_dir = run_dir / "supporting" / "help_agent"
        summary, _ = run_supporting_web_research(
            supporting_dir=supporting_dir,
            queries=queries,
            max_results=4,
            max_fetch=4,
            max_chars=3200,
            max_pdf_pages=8,
            api_key=api_key,
        )
        rel_dir = safe_rel(supporting_dir, root)
        return f"{summary} (dir={rel_dir})"
    except Exception as exc:
        return f"web_search failed: {exc}"


def _normalize_api_base_url(base_url: str) -> str:
    base = (base_url or "https://api.openai.com").strip().rstrip("/")
    lowered = base.lower()
    for suffix in (
        "/v1/chat/completions",
        "/chat/completions",
        "/v1/responses",
        "/responses",
    ):
        if lowered.endswith(suffix):
            base = base[: -len(suffix)]
            lowered = base.lower()
            break
    return base.rstrip("/")


def _chat_completion_urls(base_url: str) -> list[str]:
    base = _normalize_api_base_url(base_url)
    candidates: list[str]
    if base.endswith("/v1"):
        root = base[:-3].rstrip("/")
        candidates = [
            f"{base}/chat/completions",
            f"{root}/v1/chat/completions",
            f"{root}/chat/completions",
        ]
    else:
        candidates = [f"{base}/v1/chat/completions", f"{base}/chat/completions"]
    out: list[str] = []
    seen: set[str] = set()
    for url in candidates:
        normalized = url.rstrip("/")
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        out.append(normalized)
    return out


def _responses_urls(base_url: str) -> list[str]:
    base = _normalize_api_base_url(base_url)
    candidates: list[str]
    if base.endswith("/v1"):
        root = base[:-3].rstrip("/")
        candidates = [
            f"{base}/responses",
            f"{root}/v1/responses",
            f"{root}/responses",
        ]
    else:
        candidates = [f"{base}/v1/responses", f"{base}/responses"]
    out: list[str] = []
    seen: set[str] = set()
    for url in candidates:
        normalized = url.rstrip("/")
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        out.append(normalized)
    return out


def _payload_variants(base_payload: dict[str, Any]) -> list[dict[str, Any]]:
    first = dict(base_payload)
    first["max_completion_tokens"] = 900
    second = dict(base_payload)
    second["max_tokens"] = 900
    third = dict(second)
    third.pop("reasoning_effort", None)
    fourth = dict(base_payload)
    fourth.pop("temperature", None)
    fourth.pop("reasoning_effort", None)
    return [first, second, third, fourth]


def _responses_payload_variants(base_payload: dict[str, Any]) -> list[dict[str, Any]]:
    first = dict(base_payload)
    first["max_output_tokens"] = 900
    second = dict(base_payload)
    third = dict(base_payload)
    third.pop("reasoning_effort", None)
    fourth = dict(base_payload)
    fourth.pop("temperature", None)
    fourth.pop("reasoning_effort", None)
    return [first, second, third, fourth]


def _is_unsupported_token_error(text: str, key_name: str) -> bool:
    lowered = (text or "").lower()
    if key_name.lower() not in lowered:
        return False
    return any(
        token in lowered
        for token in (
            "unsupported parameter",
            "unrecognized request argument",
            "unknown parameter",
            "unknown argument",
        )
    )


def _expand_env_reference(raw_value: str) -> str:
    text = str(raw_value or "").strip()
    if not text:
        return ""
    if text.startswith("${") and text.endswith("}") and len(text) > 3:
        key = text[2:-1].strip()
        return str(os.getenv(key) or "").strip()
    if text.startswith("$") and len(text) > 1 and " " not in text:
        key = text[1:].strip()
        return str(os.getenv(key) or "").strip()
    return text


def _resolve_help_llm_backend(preferred: str | None = None) -> str:
    raw_preferred = str(preferred or "").strip().lower()
    if raw_preferred in {"codex", "codex_cli", "codex-cli", "cli"}:
        backend = "codex_cli"
        return backend if backend in _HELP_LLM_BACKENDS else "openai_api"
    if raw_preferred in {"openai", "openai_api", "api", "default"}:
        backend = "openai_api"
        return backend if backend in _HELP_LLM_BACKENDS else "openai_api"
    raw = str(os.getenv("FEDERNETT_HELP_LLM_BACKEND") or "").strip().lower()
    if raw in {"codex", "codex_cli", "codex-cli", "cli"}:
        backend = "codex_cli"
        return backend if backend in _HELP_LLM_BACKENDS else "openai_api"
    if raw in {"openai", "openai_api", "api", "default"}:
        backend = "openai_api"
        return backend if backend in _HELP_LLM_BACKENDS else "openai_api"
    return "openai_api"


def _normalize_reasoning_effort(value: Any, default: str = _HELP_DEFAULT_REASONING_EFFORT) -> str:
    token = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    if token in {"false", "0", "disabled", "disable"}:
        return "off"
    if token in _HELP_REASONING_EFFORT_CHOICES:
        return token
    fallback = str(default or "").strip().lower().replace("-", "_").replace(" ", "_")
    if fallback in {"false", "0", "disabled", "disable"}:
        return "off"
    if fallback in _HELP_REASONING_EFFORT_CHOICES:
        return fallback
    return _HELP_DEFAULT_REASONING_EFFORT


def _resolve_help_reasoning_effort(preferred: str | None = None) -> str:
    env_effort = _expand_env_reference(str(os.getenv("FEDERNETT_HELP_REASONING_EFFORT") or ""))
    return _normalize_reasoning_effort(preferred or env_effort or _HELP_DEFAULT_REASONING_EFFORT)


def _openai_reasoning_api_supported(base_url: str) -> bool:
    token = _normalize_api_base_url(base_url)
    host = urlparse(token).netloc.lower()
    if not host:
        return False
    if host.endswith("openai.com") or host.endswith("openai.azure.com"):
        return True
    return False


def _supports_openai_reasoning_model(model_name: str, base_url: str) -> bool:
    if not _openai_reasoning_api_supported(base_url):
        return False
    token = str(model_name or "").strip().lower()
    if not token:
        return False
    if token.startswith("$"):
        token = _expand_env_reference(token).strip().lower()
    if not token:
        return False
    if "codex" in token:
        return False
    if _HELP_REASONING_MODEL_RE.match(token):
        return True
    return "reason" in token


def _resolve_openai_reasoning_token(
    requested_effort: str,
    *,
    model_name: str,
    base_url: str,
) -> str:
    normalized = _normalize_reasoning_effort(requested_effort, _HELP_DEFAULT_REASONING_EFFORT)
    if normalized in {"", "off", "none"}:
        return ""
    if not _supports_openai_reasoning_model(model_name, base_url):
        return ""
    return _HELP_REASONING_EFFORT_TO_OPENAI.get(normalized, "")


def _reported_reasoning_effort(
    requested_effort: str | None,
    *,
    backend: str,
    model_name: str | None,
) -> str:
    normalized = _resolve_help_reasoning_effort(requested_effort)
    if normalized in {"", "off", "none"}:
        return "off"
    if backend == "codex_cli":
        return normalized
    base_url = _normalize_api_base_url(
        (os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE") or "https://api.openai.com").strip()
    )
    token = _resolve_openai_reasoning_token(
        normalized,
        model_name=str(model_name or "").strip(),
        base_url=base_url,
    )
    return normalized if token else "off"


def _extract_codex_model_from_event(event: dict[str, Any]) -> str:
    if not isinstance(event, dict):
        return ""
    candidates: list[str] = []

    def _visit(value: Any) -> None:
        if isinstance(value, dict):
            for key in (
                "model",
                "model_name",
                "model_slug",
                "resolved_model",
                "assistant_model",
                "name",
            ):
                token = value.get(key)
                if isinstance(token, str) and token.strip():
                    candidates.append(token.strip())
            for child in value.values():
                _visit(child)
        elif isinstance(value, list):
            for child in value:
                _visit(child)

    _visit(event)
    for token in candidates:
        lowered = token.lower()
        if lowered in {"agent_message", "item.completed", "event", "message"}:
            continue
        if len(token) < 3:
            continue
        return token
    return ""


def _extract_codex_model_from_stdout(stdout_text: str) -> str:
    for raw in str(stdout_text or "").splitlines():
        line = raw.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except Exception:
            continue
        model = _extract_codex_model_from_event(event)
        if model:
            return model
    return ""


def _probe_codex_cli_default_model_hint(bin_path: str) -> str:
    with _CODEX_MODEL_HINT_LOCK:
        cached = _CODEX_MODEL_HINT_CACHE.get(bin_path)
    if cached:
        return cached
    env_model = _expand_env_reference(str(os.getenv("CODEX_MODEL") or ""))
    if env_model:
        with _CODEX_MODEL_HINT_LOCK:
            _CODEX_MODEL_HINT_CACHE[bin_path] = env_model
        return env_model
    config_path = Path.home() / ".codex" / "config.toml"
    if config_path.exists():
        try:
            model_from_config = ""
            if tomllib is not None:
                parsed = tomllib.loads(config_path.read_text(encoding="utf-8", errors="replace"))
                model_token = parsed.get("model") if isinstance(parsed, dict) else ""
                if isinstance(model_token, str):
                    model_from_config = model_token.strip()
            else:
                for raw in config_path.read_text(encoding="utf-8", errors="replace").splitlines():
                    line = raw.strip()
                    if not line.startswith("model"):
                        continue
                    match = re.match(r'^model\s*=\s*["\']([^"\']+)["\']', line)
                    if match:
                        model_from_config = match.group(1).strip()
                        break
            if model_from_config:
                with _CODEX_MODEL_HINT_LOCK:
                    _CODEX_MODEL_HINT_CACHE[bin_path] = model_from_config
                return model_from_config
        except Exception:
            pass
    commands = (
        [bin_path, "config", "get", "model"],
        [bin_path, "settings", "get", "model"],
    )
    for cmd in commands:
        try:
            proc = subprocess.run(
                cmd,
                text=True,
                capture_output=True,
                timeout=4,
                check=False,
            )
        except Exception:
            continue
        if proc.returncode != 0:
            continue
        text = (proc.stdout or "").strip()
        if not text:
            continue
        line = next((ln.strip() for ln in text.splitlines() if ln.strip()), "")
        if not line:
            continue
        lowered = line.lower()
        if any(token in lowered for token in ("unknown", "error", "usage", "not found")):
            continue
        with _CODEX_MODEL_HINT_LOCK:
            _CODEX_MODEL_HINT_CACHE[bin_path] = line
        return line
    return ""


def _help_system_prompt() -> str:
    return (
        "You are FederHav, the main operator agent in Federnett. "
        "Default output language is Korean. "
        "Prioritize Federnett UI workflow first, then explain CLI only if explicitly requested. "
        "When user intent implies execution, focus on the executable action/result first instead of long manuals. "
        "Do not answer as a passive helper when the user asks to run/create/update something. "
        "The UI may execute safe actions in Act mode, so describe executable intent clearly. "
        "execution_mode(plan/act) controls FederHav suggested-action execution only, never sidebar Run Feather/Run Federlicht. "
        "For model/API schema errors (reasoning_effort, deployment, unauthorized, bad request), prioritize backend/model/reasoning fixes "
        "and do not suggest changing execution_mode unless the user explicitly asks about action policy. "
        "If CLI is not explicitly requested, do not output shell command lines. "
        "For version/release questions, prioritize pyproject.toml and CHANGELOG evidence first. "
        "Do not invent features/settings not grounded in the provided context. "
        "If a feature is unavailable, explicitly say it is unavailable now. "
        "Do not suggest unsafe/destructive commands. "
        "Do not claim execution you did not perform or files you did not modify. "
        "Keep replies concise and actionable. "
        "Use provided context when relevant; if uncertain, explicitly say so. "
        "For pure greeting/small-talk, respond in 1-2 short sentences and ask what they want to do next. "
        "For technical usage questions, include evidence with [S#] markers when sources exist."
    )


def _help_user_prompt(
    question: str,
    context: str,
    live_log_tail: str = "",
    state_memory: str = "",
) -> str:
    log_tail = _normalize_live_log_tail(live_log_tail)
    live_log_block = ""
    if log_tail:
        live_log_block = (
            "라이브 로그 컨텍스트(최근 실행 흐름):\n"
            "```log\n"
            f"{log_tail}\n"
            "```\n\n"
        )
    state_memory_block = ""
    if state_memory:
        state_memory_block = (
            "상태 메모리(state_memory, 압축 컨텍스트/아티팩트/워크플로우):\n"
            "```json\n"
            f"{state_memory}\n"
            "```\n\n"
        )
    return (
        f"질문:\n{question}\n\n"
        f"컨텍스트(코드/문서 발췌):\n{context}\n\n"
        f"{live_log_block}"
        f"{state_memory_block}"
        "출력 지침:\n"
        "- 인사/잡담이면 1~2문장으로 짧게 답하고 형식 목록은 생략.\n"
        "- 실행/생성/수정 요청이라도 파일/폴더/경로 해석 질문이면 예고문 없이 결과를 먼저 제시하고 필요 시 실행 계획을 덧붙이세요.\n"
        "- 질문에 특정 파일/폴더/경로가 포함되면 해당 경로를 우선 분석해 결과를 즉시 제시하고, 참조 경로를 함께 명시하세요.\n"
        "- 설명형 질문이면 핵심 답변 -> 절차 -> 주의사항 -> 근거 순서로 간결하게 답변.\n"
        "- 과도한 장문 템플릿 답변은 피하고, 작업 중심으로 답변.\n"
        "- 코드블록은 반드시 마크다운 fenced code block(```)을 사용.\n"
        "- 질문자가 CLI를 명시하지 않았다면 Federnett UI 단계로 안내.\n"
        "- CLI를 요청받지 않은 상태에서는 명령어를 출력하지 말고, 화면 기준 동작만 안내.\n"
        "- reasoning_effort/model/권한 오류의 해법으로 execution_mode(plan/act) 전환을 기본 제안하지 말 것.\n"
        "- 제공된 소스에 없는 기능(예: 로그인/SSO/권한체계)은 임의로 추가하지 말 것.\n"
        "- `안내 전용이라 실행 불가` 같은 문구는 사용하지 말 것. 실행 가능한 액션이면 그 액션을 중심으로 답변.\n"
        "- state_memory가 주어졌다면 run/워크플로우/아티팩트 상태를 우선 참조하고, 불확실한 항목은 불확실하다고 명시할 것.\n"
    )


def _build_help_messages(
    question: str,
    sources: list[dict[str, Any]],
    history: list[dict[str, str]] | None,
    live_log_tail: str = "",
    state_memory: Any = None,
) -> list[dict[str, str]]:
    context = _build_context(sources)
    normalized_state_memory = _normalize_state_memory(state_memory)
    messages: list[dict[str, str]] = [{"role": "system", "content": _help_system_prompt()}]
    if history:
        messages.extend(_normalize_history(history))
    messages.append(
        {
            "role": "user",
            "content": _help_user_prompt(
                question,
                context,
                live_log_tail,
                state_memory=normalized_state_memory,
            ),
        },
    )
    return messages


def _render_codex_prompt(messages: list[dict[str, str]]) -> str:
    if not messages:
        return ""
    chunks: list[str] = [
        "You are operating in non-interactive mode. Return only the final assistant answer text.",
        "",
    ]
    for item in messages:
        role = str(item.get("role") or "user").strip().lower()
        role_label = "SYSTEM" if role == "system" else ("ASSISTANT" if role == "assistant" else "USER")
        content = str(item.get("content") or "").strip()
        if not content:
            continue
        chunks.append(f"[{role_label}]")
        chunks.append(content)
        chunks.append("")
    return "\n".join(chunks).strip()


def _extract_codex_exec_message(stdout_text: str) -> str:
    lines = [line.strip() for line in str(stdout_text or "").splitlines() if line.strip()]
    last_message = ""
    for line in lines:
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except Exception:
            continue
        if str(event.get("type") or "") != "item.completed":
            continue
        item = event.get("item")
        if not isinstance(item, dict):
            continue
        if str(item.get("type") or "") != "agent_message":
            continue
        text = str(item.get("text") or "").strip()
        if text:
            last_message = text
    return last_message


def _extract_codex_exec_message_from_event(event: dict[str, Any]) -> str:
    if not isinstance(event, dict):
        return ""
    if str(event.get("type") or "") != "item.completed":
        return ""
    item = event.get("item")
    if not isinstance(item, dict):
        return ""
    if str(item.get("type") or "") != "agent_message":
        return ""
    return str(item.get("text") or "")


def _extract_codex_stream_delta_from_event(event: dict[str, Any]) -> str:
    if not isinstance(event, dict):
        return ""
    event_type = str(event.get("type") or "").strip().lower()
    if event_type == "item.completed":
        return ""

    def _text(value: Any) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            for key in ("delta", "text", "output_text", "content"):
                nested = value.get(key)
                if isinstance(nested, str) and nested:
                    return nested
        if isinstance(value, list):
            chunks: list[str] = []
            for entry in value:
                if isinstance(entry, str):
                    chunks.append(entry)
                    continue
                if isinstance(entry, dict):
                    for key in ("delta", "text", "output_text"):
                        token = entry.get(key)
                        if isinstance(token, str) and token:
                            chunks.append(token)
            return "".join(chunks)
        return ""

    for key in ("delta", "text", "output_text"):
        token = _text(event.get(key))
        if token:
            return token

    item = event.get("item")
    if isinstance(item, dict):
        for key in ("delta", "text", "output_text", "content"):
            token = _text(item.get(key))
            if token:
                return token

    data = event.get("data")
    if isinstance(data, dict):
        for key in ("delta", "text", "output_text", "content"):
            token = _text(data.get(key))
            if token:
                return token

    return ""


def _call_llm_codex_cli(
    question: str,
    sources: list[dict[str, Any]],
    model: str | None,
    history: list[dict[str, str]] | None = None,
    live_log_tail: str = "",
    state_memory: Any = None,
    reasoning_effort: str | None = None,
    *,
    root: Path | None = None,
) -> tuple[str, str]:
    codex_bin = _expand_env_reference(str(os.getenv("CODEX_CLI_BIN") or "codex"))
    bin_path = shutil.which(codex_bin) if codex_bin else None
    if not bin_path:
        raise RuntimeError("codex CLI is not available in PATH")
    model_choice = _expand_env_reference(str(model or "")) or _expand_env_reference(str(os.getenv("CODEX_MODEL") or ""))
    messages = _build_help_messages(
        question,
        sources,
        history,
        live_log_tail=live_log_tail,
        state_memory=state_memory,
    )
    prompt = _render_codex_prompt(messages)
    if not prompt:
        raise RuntimeError("codex prompt is empty")
    cmd = [
        bin_path,
        "exec",
        "--json",
        "--ephemeral",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
    ]
    if root is not None:
        cmd.extend(["--cd", str(root)])
    if model_choice:
        cmd.extend(["--model", model_choice])
    effort = _resolve_help_reasoning_effort(reasoning_effort)
    if effort:
        cmd.extend(["-c", f'reasoning_effort="{effort}"'])
    cmd.append("-")
    try:
        proc = subprocess.run(
            cmd,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("codex CLI timed out") from exc
    except Exception as exc:
        raise RuntimeError(f"codex CLI execution failed: {exc}") from exc
    answer = _extract_codex_exec_message(proc.stdout)
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        detail = detail.splitlines()[-1] if detail else ""
        raise RuntimeError(f"codex CLI failed ({proc.returncode}){f': {detail}' if detail else ''}")
    if not answer:
        detail = (proc.stderr or "").strip()
        raise RuntimeError(f"codex CLI returned empty output{f': {detail}' if detail else ''}")
    detected_model = _extract_codex_model_from_stdout(proc.stdout)
    default_hint = _probe_codex_cli_default_model_hint(bin_path)
    used_model = model_choice or detected_model or default_hint or "codex-cli-default"
    return answer, used_model


def _call_llm_stream_codex_cli(
    question: str,
    sources: list[dict[str, Any]],
    model: str | None,
    history: list[dict[str, str]] | None = None,
    live_log_tail: str = "",
    state_memory: Any = None,
    reasoning_effort: str | None = None,
    *,
    root: Path | None = None,
) -> tuple[Iterator[str], str]:
    codex_bin = _expand_env_reference(str(os.getenv("CODEX_CLI_BIN") or "codex"))
    bin_path = shutil.which(codex_bin) if codex_bin else None
    if not bin_path:
        raise RuntimeError("codex CLI is not available in PATH")
    model_choice = _expand_env_reference(str(model or "")) or _expand_env_reference(str(os.getenv("CODEX_MODEL") or ""))
    messages = _build_help_messages(
        question,
        sources,
        history,
        live_log_tail=live_log_tail,
        state_memory=state_memory,
    )
    prompt = _render_codex_prompt(messages)
    if not prompt:
        raise RuntimeError("codex prompt is empty")
    cmd = [
        bin_path,
        "exec",
        "--json",
        "--ephemeral",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
    ]
    if root is not None:
        cmd.extend(["--cd", str(root)])
    if model_choice:
        cmd.extend(["--model", model_choice])
    effort = _resolve_help_reasoning_effort(reasoning_effort)
    if effort:
        cmd.extend(["-c", f'reasoning_effort="{effort}"'])
    cmd.append("-")

    def _iter_chunks(text: str, target_chars: int = 18) -> Iterator[str]:
        raw = str(text or "")
        if not raw:
            return
        bucket: list[str] = []
        size = 0
        for ch in raw:
            bucket.append(ch)
            size += 1
            if ch == "\n" and size >= 8:
                yield "".join(bucket)
                bucket = []
                size = 0
                continue
            if size >= target_chars and ch in {" ", "\t", ",", ".", "!", "?", ";", ":", ")", "]", "}"}:
                yield "".join(bucket)
                bucket = []
                size = 0
        if bucket:
            yield "".join(bucket)

    def _iter() -> Iterator[str]:
        proc: subprocess.Popen[str] | None = None
        timeout_flag = threading.Event()
        timer: threading.Timer | None = None
        captured_lines: list[str] = []
        completed_message = ""
        streamed_any = False
        stderr_text = ""
        try:
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
        except Exception:
            answer, _ = _call_llm_codex_cli(
                question,
                sources,
                model=model,
                history=history,
                state_memory=state_memory,
                reasoning_effort=effort,
                root=root,
            )
            if answer:
                yield from _iter_chunks(answer)
            return
        try:
            def _on_timeout() -> None:
                timeout_flag.set()
                try:
                    proc.kill()  # type: ignore[union-attr]
                except Exception:
                    pass

            timer = threading.Timer(120.0, _on_timeout)
            timer.start()
            if proc.stdin:
                try:
                    proc.stdin.write(prompt)
                    if not prompt.endswith("\n"):
                        proc.stdin.write("\n")
                    proc.stdin.flush()
                finally:
                    proc.stdin.close()
            if proc.stdout:
                for raw_line in proc.stdout:
                    line = str(raw_line or "").strip()
                    if not line:
                        continue
                    captured_lines.append(line)
                    if not line.startswith("{"):
                        continue
                    try:
                        event = json.loads(line)
                    except Exception:
                        continue
                    delta = _extract_codex_stream_delta_from_event(event)
                    if delta:
                        streamed_any = True
                        yield from _iter_chunks(delta, target_chars=16)
                    completed = _extract_codex_exec_message_from_event(event).strip()
                    if completed:
                        completed_message = completed
            if proc.stderr:
                stderr_text = proc.stderr.read()
            returncode = proc.wait()
            if timeout_flag.is_set():
                raise RuntimeError("codex CLI timed out")
            if returncode != 0:
                detail = (stderr_text or "\n".join(captured_lines)).strip()
                detail = detail.splitlines()[-1] if detail else ""
                raise RuntimeError(f"codex CLI failed ({returncode}){f': {detail}' if detail else ''}")
            if streamed_any:
                return
            answer = completed_message or _extract_codex_exec_message("\n".join(captured_lines))
            if not answer:
                detail = (stderr_text or "").strip()
                raise RuntimeError(f"codex CLI returned empty output{f': {detail}' if detail else ''}")
            yield from _iter_chunks(answer)
        finally:
            if timer:
                timer.cancel()
            try:
                if proc and proc.stdout:
                    proc.stdout.close()
            except Exception:
                pass
            try:
                if proc and proc.stderr:
                    proc.stderr.close()
            except Exception:
                pass

    default_hint = _probe_codex_cli_default_model_hint(bin_path)
    used_model = model_choice or default_hint or "codex-cli-default"
    return _iter(), used_model


def _resolve_requested_model(model_input: str | None, *, backend: str | None = None) -> tuple[str, bool]:
    raw = str(model_input or "").strip()
    if raw:
        expanded = _expand_env_reference(raw)
        if expanded:
            # Explicit "$OPENAI_MODEL" is treated as auto-resolution to env model.
            return expanded, not raw.startswith("$")
        if raw.startswith("$"):
            return "", False
        return raw, True
    resolved_backend = _resolve_help_llm_backend(backend)
    if resolved_backend == "codex_cli":
        env_model = _expand_env_reference(str(os.getenv("CODEX_MODEL") or ""))
        return env_model, False
    env_model = _expand_env_reference(str(os.getenv("OPENAI_MODEL") or ""))
    return env_model, False


def _is_model_unavailable_error(status_code: int, text: str) -> bool:
    lowered = (text or "").lower()
    model_hint = any(token in lowered for token in ("model", "deployment"))
    not_found_hint = any(
        token in lowered
        for token in (
            "not found",
            "does not exist",
            "unknown model",
            "unavailable",
            "access",
            "permission",
            "invalid model",
        )
    )
    return (status_code in {400, 404} and model_hint and not_found_hint) or (
        status_code == 404 and "model_not_found" in lowered
    )


def _extract_chat_content(body: dict[str, Any]) -> str:
    choices = body.get("choices") or []
    if not choices:
        return ""
    message = choices[0].get("message") or {}
    return str(message.get("content") or "").strip()


def _extract_responses_content(body: dict[str, Any]) -> str:
    text = body.get("output_text")
    if isinstance(text, str) and text.strip():
        return text.strip()
    output = body.get("output")
    chunks: list[str] = []
    if isinstance(output, list):
        for item in output:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if isinstance(content, list):
                for part in content:
                    if not isinstance(part, dict):
                        continue
                    part_type = str(part.get("type") or "").strip().lower()
                    part_text = part.get("text")
                    if part_type in {"output_text", "text"} and isinstance(part_text, str) and part_text.strip():
                        chunks.append(part_text.strip())
            elif isinstance(content, str) and content.strip():
                chunks.append(content.strip())
    if chunks:
        return "\n".join(chunks).strip()
    return _extract_chat_content(body)


def _iter_sse_json_objects(resp: Any) -> Iterator[dict[str, Any]]:
    for raw_line in resp.iter_lines(decode_unicode=True):
        if raw_line is None:
            continue
        line = str(raw_line).strip()
        if not line or not line.startswith("data:"):
            continue
        payload = line[5:].strip()
        if not payload or payload == "[DONE]":
            break
        try:
            parsed = json.loads(payload)
        except Exception:
            continue
        if isinstance(parsed, dict):
            yield parsed


def _iter_text_fragments(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        if value:
            yield value
        return
    if isinstance(value, list):
        for entry in value:
            if isinstance(entry, str):
                if entry:
                    yield entry
                continue
            if not isinstance(entry, dict):
                continue
            for key in ("text", "content", "value"):
                token = entry.get(key)
                if isinstance(token, str) and token:
                    yield token
                    break


def _iter_chat_stream_content(resp: Any) -> Iterator[str]:
    content_type = str(resp.headers.get("Content-Type") or "").lower()
    if "text/event-stream" not in content_type:
        try:
            body = resp.json()
        except Exception:
            return
        text = _extract_chat_content(body)
        if text:
            yield text
        return
    for event in _iter_sse_json_objects(resp):
        choices = event.get("choices")
        if not isinstance(choices, list) or not choices:
            continue
        first = choices[0] if isinstance(choices[0], dict) else {}
        delta = first.get("delta")
        if isinstance(delta, dict):
            for token in _iter_text_fragments(delta.get("content")):
                yield token
            continue
        message = first.get("message")
        if isinstance(message, dict):
            for token in _iter_text_fragments(message.get("content")):
                yield token


def _iter_responses_stream_content(resp: Any) -> Iterator[str]:
    content_type = str(resp.headers.get("Content-Type") or "").lower()
    if "text/event-stream" not in content_type:
        try:
            body = resp.json()
        except Exception:
            return
        text = _extract_responses_content(body)
        if text:
            yield text
        return
    seen_delta = False
    for event in _iter_sse_json_objects(resp):
        event_type = str(event.get("type") or "").strip().lower()
        if event_type == "response.output_text.delta":
            delta = event.get("delta")
            if isinstance(delta, str) and delta:
                seen_delta = True
                yield delta
            continue
        if event_type == "response.output_text.done":
            text = event.get("text")
            if not seen_delta and isinstance(text, str) and text.strip():
                yield text.strip()
            continue
        if event_type == "response.completed":
            response_payload = event.get("response")
            if isinstance(response_payload, dict):
                text = _extract_responses_content(response_payload)
                if text and not seen_delta:
                    yield text
            continue


def _call_llm_stream_openai(
    question: str,
    sources: list[dict[str, Any]],
    model: str | None,
    history: list[dict[str, str]] | None = None,
    live_log_tail: str = "",
    state_memory: Any = None,
    strict_model: bool = False,
    reasoning_effort: str | None = None,
) -> tuple[Iterator[str], str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    if requests is None:
        raise RuntimeError("requests package is unavailable")
    chosen_model, explicit_model = _resolve_requested_model(model)
    if not chosen_model:
        raise RuntimeError("Model is not configured (set OPENAI_MODEL or pass model)")
    base_url = _normalize_api_base_url(
        (os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE") or "https://api.openai.com").strip()
    )
    chat_urls = _chat_completion_urls(base_url)
    responses_urls = _responses_urls(base_url)
    messages = _build_help_messages(
        question,
        sources,
        history,
        live_log_tail=live_log_tail,
        state_memory=state_memory,
    )
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    requested_effort = _resolve_help_reasoning_effort(reasoning_effort)
    last_error = "LLM request failed: no endpoint attempted"
    for candidate_model in _resolve_model_candidates(
        chosen_model,
        explicit=explicit_model,
        strict_model=bool(strict_model),
    ):
        model_unavailable = False
        effort_token = _resolve_openai_reasoning_token(
            requested_effort,
            model_name=candidate_model,
            base_url=base_url,
        )
        chat_payload_base = {
            "model": candidate_model,
            "messages": messages,
            "temperature": 0.2,
            "stream": True,
        }
        if effort_token:
            chat_payload_base["reasoning_effort"] = effort_token
        for url in chat_urls:
            for payload in _payload_variants(chat_payload_base):
                resp = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=90,
                    stream=True,
                )
                if resp.status_code == 200:
                    def _chat_iter(response_obj: Any = resp) -> Iterator[str]:
                        with response_obj:
                            yield from _iter_chat_stream_content(response_obj)
                    return _chat_iter(), candidate_model
                text = (resp.text or "").strip()
                resp.close()
                last_error = f"LLM request failed: {resp.status_code} {text}"
                if _is_model_unavailable_error(resp.status_code, text):
                    model_unavailable = True
                    break
                if resp.status_code == 404:
                    break
                if _is_unsupported_token_error(text, "max_tokens"):
                    continue
                if _is_unsupported_token_error(text, "max_completion_tokens"):
                    continue
                if _is_unsupported_token_error(text, "temperature"):
                    continue
                if _is_unsupported_token_error(text, "reasoning_effort"):
                    continue
            if model_unavailable:
                break
        if model_unavailable:
            continue
        responses_payload_base = {
            "model": candidate_model,
            "input": messages,
            "temperature": 0.2,
            "stream": True,
        }
        if effort_token:
            responses_payload_base["reasoning_effort"] = effort_token
        for url in responses_urls:
            for payload in _responses_payload_variants(responses_payload_base):
                resp = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=90,
                    stream=True,
                )
                if resp.status_code == 200:
                    def _responses_iter(response_obj: Any = resp) -> Iterator[str]:
                        with response_obj:
                            yield from _iter_responses_stream_content(response_obj)
                    return _responses_iter(), candidate_model
                text = (resp.text or "").strip()
                resp.close()
                last_error = f"LLM request failed: {resp.status_code} {text}"
                if _is_model_unavailable_error(resp.status_code, text):
                    model_unavailable = True
                    break
                if resp.status_code == 404:
                    break
                if _is_unsupported_token_error(text, "max_output_tokens"):
                    continue
                if _is_unsupported_token_error(text, "temperature"):
                    continue
                if _is_unsupported_token_error(text, "reasoning_effort"):
                    continue
            if model_unavailable:
                break
        if model_unavailable:
            continue
    raise RuntimeError(last_error)


def _resolve_model_candidates(chosen_model: str, *, explicit: bool, strict_model: bool = False) -> list[str]:
    allow_fallback = str(os.getenv("FEDERNETT_HELP_ALLOW_MODEL_FALLBACK") or "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    candidates: list[str] = []
    for token in (chosen_model,):
        if token and token not in candidates:
            candidates.append(token)
    if explicit and (strict_model or not allow_fallback):
        return candidates
    for token in (
        _expand_env_reference(str(os.getenv("OPENAI_MODEL") or "")),
        _expand_env_reference(str(os.getenv("FEDERNETT_HELP_FALLBACK_MODEL") or "gpt-4o-mini")),
    ):
        if token and token not in candidates:
            candidates.append(token)
    return candidates


def _call_llm_openai(
    question: str,
    sources: list[dict[str, Any]],
    model: str | None,
    history: list[dict[str, str]] | None = None,
    live_log_tail: str = "",
    state_memory: Any = None,
    strict_model: bool = False,
    reasoning_effort: str | None = None,
) -> tuple[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    if requests is None:
        raise RuntimeError("requests package is unavailable")
    chosen_model, explicit_model = _resolve_requested_model(model)
    if not chosen_model:
        raise RuntimeError("Model is not configured (set OPENAI_MODEL or pass model)")
    base_url = _normalize_api_base_url(
        (os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE") or "https://api.openai.com").strip()
    )
    chat_urls = _chat_completion_urls(base_url)
    responses_urls = _responses_urls(base_url)
    messages = _build_help_messages(
        question,
        sources,
        history,
        live_log_tail=live_log_tail,
        state_memory=state_memory,
    )
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    requested_effort = _resolve_help_reasoning_effort(reasoning_effort)
    last_error = "LLM request failed: no endpoint attempted"
    resp = None
    for candidate_model in _resolve_model_candidates(
        chosen_model,
        explicit=explicit_model,
        strict_model=bool(strict_model),
    ):
        model_unavailable = False
        effort_token = _resolve_openai_reasoning_token(
            requested_effort,
            model_name=candidate_model,
            base_url=base_url,
        )
        chat_payload_base = {
            "model": candidate_model,
            "messages": messages,
            "temperature": 0.2,
        }
        if effort_token:
            chat_payload_base["reasoning_effort"] = effort_token
        for url in chat_urls:
            for payload in _payload_variants(chat_payload_base):
                resp = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=45,
                )
                if resp.status_code == 200:
                    body = resp.json()
                    content = _extract_chat_content(body)
                    if content:
                        return content, candidate_model
                    last_error = "LLM returned empty content"
                    continue
                text = resp.text.strip()
                last_error = f"LLM request failed: {resp.status_code} {text}"
                if _is_model_unavailable_error(resp.status_code, text):
                    model_unavailable = True
                    break
                if resp.status_code == 404:
                    # Endpoint mismatch (common on OpenAI-compatible gateways): try next URL.
                    break
                if _is_unsupported_token_error(text, "max_tokens"):
                    continue
                if _is_unsupported_token_error(text, "max_completion_tokens"):
                    continue
                if _is_unsupported_token_error(text, "temperature"):
                    continue
                if _is_unsupported_token_error(text, "reasoning_effort"):
                    continue
                # For other errors, keep trying alternates but preserve the latest detail.
            if model_unavailable:
                break
            if resp is not None and resp.status_code == 200:
                break
        if model_unavailable:
            continue
        responses_payload_base = {
            "model": candidate_model,
            "input": messages,
            "temperature": 0.2,
        }
        if effort_token:
            responses_payload_base["reasoning_effort"] = effort_token
        for url in responses_urls:
            for payload in _responses_payload_variants(responses_payload_base):
                resp = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=45,
                )
                if resp.status_code == 200:
                    body = resp.json()
                    content = _extract_responses_content(body)
                    if content:
                        return content, candidate_model
                    last_error = "LLM returned empty content"
                    continue
                text = resp.text.strip()
                last_error = f"LLM request failed: {resp.status_code} {text}"
                if _is_model_unavailable_error(resp.status_code, text):
                    model_unavailable = True
                    break
                if resp.status_code == 404:
                    break
                if _is_unsupported_token_error(text, "max_output_tokens"):
                    continue
                if _is_unsupported_token_error(text, "temperature"):
                    continue
                if _is_unsupported_token_error(text, "reasoning_effort"):
                    continue
            if model_unavailable:
                break
            if resp is not None and resp.status_code == 200:
                break
        if model_unavailable:
            continue
    raise RuntimeError(last_error)


def _try_agentic_runtime_answer(
    *,
    question: str,
    sources: list[dict[str, Any]],
    model: str | None,
    history: list[dict[str, str]] | None = None,
    live_log_tail: str = "",
    state_memory: Any = None,
    llm_backend: str | None = None,
    reasoning_effort: str | None = None,
    runtime_mode: str | None = None,
    root: Path | None = None,
) -> tuple[str, str] | None:
    try:
        from federhav.agentic_runtime import runtime_enabled, try_deepagent_answer
    except Exception:
        return None
    if not runtime_enabled(runtime_mode):
        return None
    messages = _build_help_messages(
        question,
        sources,
        history,
        live_log_tail=live_log_tail,
        state_memory=state_memory,
    )
    return try_deepagent_answer(
        question=question,
        messages=messages,
        sources=sources,
        state_memory=state_memory,
        model=model,
        llm_backend=llm_backend,
        reasoning_effort=reasoning_effort,
        runtime_mode=runtime_mode,
        root=root,
    )


def _try_agentic_runtime_stream(
    *,
    question: str,
    sources: list[dict[str, Any]],
    model: str | None,
    history: list[dict[str, str]] | None = None,
    live_log_tail: str = "",
    state_memory: Any = None,
    llm_backend: str | None = None,
    reasoning_effort: str | None = None,
    runtime_mode: str | None = None,
    root: Path | None = None,
) -> tuple[Iterator[str], str] | None:
    try:
        from federhav.agentic_runtime import runtime_enabled, try_deepagent_stream
    except Exception:
        return None
    if not runtime_enabled(runtime_mode):
        return None
    messages = _build_help_messages(
        question,
        sources,
        history,
        live_log_tail=live_log_tail,
        state_memory=state_memory,
    )
    return try_deepagent_stream(
        question=question,
        messages=messages,
        sources=sources,
        state_memory=state_memory,
        model=model,
        llm_backend=llm_backend,
        reasoning_effort=reasoning_effort,
        runtime_mode=runtime_mode,
        root=root,
    )


def _try_agentic_runtime_action_plan(
    *,
    question: str,
    run_rel: str | None,
    history: list[dict[str, str]] | None,
    state_memory: Any,
    capabilities: dict[str, Any] | None,
    execution_mode: str,
    allow_artifacts: bool,
    model: str | None,
    llm_backend: str | None,
    reasoning_effort: str | None,
    runtime_mode: str | None,
    root: Path,
) -> dict[str, Any] | None:
    try:
        from federhav.agentic_runtime import runtime_enabled, try_deepagent_action_plan
    except Exception:
        return None
    if not runtime_enabled(runtime_mode):
        return None
    return try_deepagent_action_plan(
        question=question,
        run_rel=run_rel,
        history=history,
        state_memory=state_memory,
        capabilities=capabilities,
        execution_mode=execution_mode,
        allow_artifacts=allow_artifacts,
        model=model,
        llm_backend=llm_backend,
        reasoning_effort=reasoning_effort,
        runtime_mode=runtime_mode,
        root=root,
    )


def _call_llm(
    question: str,
    sources: list[dict[str, Any]],
    model: str | None,
    history: list[dict[str, str]] | None = None,
    live_log_tail: str = "",
    state_memory: Any = None,
    strict_model: bool = False,
    reasoning_effort: str | None = None,
    runtime_mode: str | None = None,
    *,
    root: Path | None = None,
    llm_backend: str | None = None,
) -> tuple[str, str]:
    backend = _resolve_help_llm_backend(llm_backend)
    deepagent_try = _try_agentic_runtime_answer(
        question=question,
        sources=sources,
        model=model,
        history=history,
        live_log_tail=live_log_tail,
        state_memory=state_memory,
        llm_backend=backend,
        reasoning_effort=reasoning_effort,
        runtime_mode=runtime_mode,
        root=root,
    )
    if deepagent_try:
        return deepagent_try
    if backend == "codex_cli":
        return _call_llm_codex_cli(
            question,
            sources,
            model=model,
            history=history,
            live_log_tail=live_log_tail,
            state_memory=state_memory,
            reasoning_effort=reasoning_effort,
            root=root,
        )
    return _call_llm_openai(
        question,
        sources,
        model=model,
        history=history,
        live_log_tail=live_log_tail,
        state_memory=state_memory,
        strict_model=strict_model,
        reasoning_effort=reasoning_effort,
    )


def _call_llm_stream(
    question: str,
    sources: list[dict[str, Any]],
    model: str | None,
    history: list[dict[str, str]] | None = None,
    live_log_tail: str = "",
    state_memory: Any = None,
    strict_model: bool = False,
    reasoning_effort: str | None = None,
    runtime_mode: str | None = None,
    *,
    root: Path | None = None,
    llm_backend: str | None = None,
) -> tuple[Iterator[str], str]:
    backend = _resolve_help_llm_backend(llm_backend)
    deepagent_try = _try_agentic_runtime_stream(
        question=question,
        sources=sources,
        model=model,
        history=history,
        live_log_tail=live_log_tail,
        state_memory=state_memory,
        llm_backend=backend,
        reasoning_effort=reasoning_effort,
        runtime_mode=runtime_mode,
        root=root,
    )
    if deepagent_try:
        return deepagent_try
    if backend == "codex_cli":
        return _call_llm_stream_codex_cli(
            question,
            sources,
            model=model,
            history=history,
            live_log_tail=live_log_tail,
            state_memory=state_memory,
            reasoning_effort=reasoning_effort,
            root=root,
        )
    return _call_llm_stream_openai(
        question,
        sources,
        model=model,
        history=history,
        live_log_tail=live_log_tail,
        state_memory=state_memory,
        strict_model=strict_model,
        reasoning_effort=reasoning_effort,
    )


def _fallback_answer(question: str, sources: list[dict[str, Any]]) -> str:
    if not sources:
        return (
            "LLM 호출 또는 소스 매칭이 실패했습니다.\n"
            "질문에 기능명/옵션명/파일명을 함께 적어 다시 시도해 주세요.\n"
            "예: `federlicht의 --template-rigidity와 --temperature-level 차이`"
        )
    lines = [
        "LLM 응답을 사용할 수 없어 코드/문서 검색 결과 기반으로 요약합니다.",
        "",
        f"- 질문: {question}",
        "- 권장: 아래 근거 파일을 순서대로 열어 옵션과 실행 절차를 확인하세요.",
        "",
        "핵심 근거:",
    ]
    for src in sources[:6]:
        head = src.get("excerpt", "").splitlines()[0] if src.get("excerpt") else ""
        head = head[:150]
        lines.append(
            f"- [{src['id']}] `{src['path']}:{src['start_line']}` {head}",
        )
    return "\n".join(lines).strip()


def _normalize_run_hint(raw: str) -> str:
    token = str(raw or "").strip()
    if not token:
        return ""
    token = token.replace("\\", "/").strip("`'\" ")
    token = re.sub(r"[.,;:!?]+$", "", token).strip()
    token = re.sub(r"([A-Za-z0-9._/\-])으$", r"\1", token)
    token = re.sub(r"(?:를|을|로|으로)$", "", token).strip()
    token = re.sub(r"^(?:\./)+", "", token)
    token = _strip_known_run_root_prefix(token).strip("/")
    return token[:180]


def _is_invalid_run_hint(candidate: str, *, blocked: set[str] | None = None) -> bool:
    token = _normalize_run_hint(candidate)
    if not token:
        return True
    lowered = token.lower()
    merged = re.sub(r"\s+", "", lowered)
    blocked_tokens = set(blocked or set())
    blocked_tokens.update(
        {
            "run",
            "runs",
            "site",
            "folder",
            "runfolder",
            "run-folder",
            "폴더",
            "런",
            "federnett",
            "federlicht",
            "federhav",
            "feather",
            "plan",
            "act",
            "mode",
            "current",
            "selected",
            "target",
            "default",
            "지금",
            "현재",
            "선택",
            "선택된",
            "대상",
            "대상에서",
            "기준",
            "기반",
            "현재run",
            "선택된run",
            "run대상",
            "run대상에서",
            "에서",
            "사용법",
            "방법",
            "설명",
            "요약",
            "가이드",
            "알려",
            "알려줘",
            "짧게",
            "how",
            "guide",
            "usage",
        },
    )
    if lowered in blocked_tokens or merged in blocked_tokens:
        return True
    if merged.startswith("run") and len(merged) <= 9:
        return True
    if merged.endswith("대상") or merged.endswith("대상에서"):
        return True
    if lowered in {"from", "to", "as", "set", "use", "open", "switch"}:
        return True
    return False


def _extract_run_hint(raw: str, *, strict: bool = False) -> str:
    text = str(raw or "").strip()
    if not text:
        return ""
    blocked = {
        "run",
        "runs",
        "site",
        "folder",
        "folder를",
        "folder을",
        "폴더",
        "폴더를",
        "폴더을",
        "런",
        "run을",
        "run를",
        "runfolder",
        "run-folder",
        "federnett",
        "federlicht",
        "federhav",
        "feather",
        "plan",
        "act",
        "mode",
    }
    run_root_pattern = "|".join(re.escape(prefix) for prefix in _KNOWN_RUN_ROOT_PREFIXES)
    patterns = (
        rf"((?:{run_root_pattern})/[^\s`\"'<>]+)",
        r"`([^`]+)`",
        r"'([^']+)'",
        r"\"([^\"]+)\"",
        r"([A-Za-z0-9가-힣._/\-]{2,})(?=\s*(?:run|런)?\s*(?:로|으로)\s*(?:바꿔|변경|전환|선택|열어|실행|설정|지정|사용|하고))",
        r"(?:run\s*(?:to|as|:|=)\s*)([A-Za-z0-9가-힣._/\-]{2,})",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            continue
        candidate = _normalize_run_hint(match.group(1))
        if "/" in candidate:
            candidate = candidate.split("/", 1)[0].strip()
        if not candidate:
            continue
        if _is_invalid_run_hint(candidate, blocked=blocked):
            continue
        return candidate
    if strict:
        return ""
    lowered_text = text.lower()
    if not any(token in lowered_text for token in ("run", "폴더", "런")) and not _mentions_run_root_token(lowered_text):
        return ""
    for token in re.findall(
        rf"(?:{run_root_pattern}/)?[A-Za-z0-9가-힣][A-Za-z0-9가-힣._/\-]{{2,}}",
        text,
        flags=re.IGNORECASE,
    ):
        candidate = _normalize_run_hint(token)
        if "/" in candidate:
            candidate = candidate.split("/", 1)[0].strip()
        if not candidate:
            continue
        if _is_invalid_run_hint(candidate, blocked=blocked):
            continue
        return candidate
    return ""


def _extract_recent_run_hint(history: list[dict[str, str]] | None) -> str:
    if not history:
        return ""
    for entry in reversed(history[-12:]):
        if str(entry.get("role") or "").strip().lower() != "user":
            continue
        content = str(entry.get("content") or "").strip()
        if not content:
            continue
        lowered = content.lower()
        if not any(
            token in lowered
            for token in (
                "run folder",
                "run 폴더",
                "런 폴더",
                "으로 설정",
                "로 설정",
                "으로 하고",
                "로 하고",
                "run as",
                "use run",
                "run=",
                "run 전환",
                "run 변경",
                "switch run",
                "select run",
            )
        ) and not _mentions_run_root_token(lowered):
            continue
        hint = _extract_run_hint(content, strict=True)
        if hint:
            return hint
    return ""


def _infer_recent_execution_target(history: list[dict[str, str]] | None) -> str:
    if not history:
        return ""
    for entry in reversed(history[-12:]):
        if str(entry.get("role") or "").strip().lower() != "user":
            continue
        content = str(entry.get("content") or "").strip().lower()
        if not content:
            continue
        if any(token in content for token in ("feather부터", "연속 실행", "end-to-end", "파이프라인")):
            return "pipeline"
        if "federlicht" in content or "보고서" in content:
            return "federlicht"
        if "feather" in content or any(token in content for token in ("자료 수집", "검색", "크롤링", "아카이브")):
            return "feather"
    return ""


def _extract_run_rel_from_state_memory(state_memory: Any) -> str:
    memory = state_memory
    if isinstance(memory, str):
        text = memory.strip()
        if text:
            try:
                memory = json.loads(text)
            except Exception:
                memory = {}
        else:
            memory = {}
    if not isinstance(memory, dict):
        return ""
    scope = memory.get("scope")
    if isinstance(scope, dict):
        token = str(scope.get("run_rel") or "").strip().replace("\\", "/").strip("/")
        if token:
            return token
    run = memory.get("run")
    if isinstance(run, dict):
        token = str(run.get("run_rel") or "").strip().replace("\\", "/").strip("/")
        if token:
            return token
    return ""


def _effective_run_rel(run_rel: str | None, state_memory: Any) -> str | None:
    explicit = str(run_rel or "").strip().replace("\\", "/").strip("/")
    if explicit:
        return explicit
    inferred = _extract_run_rel_from_state_memory(state_memory)
    return inferred or None


def _infer_stage_hint(raw: str) -> str:
    text = str(raw or "").strip().lower()
    if not text:
        return ""
    aliases: tuple[tuple[tuple[str, ...], str], ...] = (
        (("scout", "스카우트", "탐색"), "scout"),
        (("plan", "플랜", "기획"), "plan"),
        (("evidence", "근거"), "evidence"),
        (("writer", "작성"), "writer"),
        (("quality", "퀄리티", "critic", "비평"), "quality"),
    )
    for tokens, stage in aliases:
        if any(token in text for token in tokens):
            return stage
    return ""


def _agentic_actions_enabled() -> bool:
    token = str(os.getenv("FEDERNETT_HELP_AGENTIC_ACTIONS") or "1").strip().lower()
    return token not in {"0", "false", "no", "off", "disable", "disabled"}


def _allow_rule_fallback(runtime_mode: str | None) -> bool:
    """
    Keep safe-rule fallback as explicit opt-in.
    Default behavior is agentic-first for all runtime modes.
    Override with FEDERNETT_HELP_RULE_FALLBACK=1 to re-enable rule fallback
    only when runtime_mode is explicitly off. Use FEDERNETT_HELP_RULE_FALLBACK=emergency
    to force-enable regardless of runtime_mode.
    """
    override = str(os.getenv("FEDERNETT_HELP_RULE_FALLBACK") or "").strip().lower()
    if override:
        if override == "emergency":
            return True
        if override not in {"1", "true", "on", "yes"}:
            return False
        mode = _normalize_runtime_mode(runtime_mode)
        return mode == "off"
    return False


def _allow_llm_action_planner_fallback(runtime_mode: str | None) -> bool:
    """
    DeepAgent planner is the default action-planning path.
    LLM action-planner fallback is explicit opt-in only.
    Override with FEDERNETT_HELP_ACTION_LLM_FALLBACK=1 to enable fallback.
    """
    override = str(os.getenv("FEDERNETT_HELP_ACTION_LLM_FALLBACK") or "").strip().lower()
    if override:
        return override in {"1", "true", "on", "yes", "emergency"}
    _ = runtime_mode
    return False


def _extract_first_json_object(raw: str) -> dict[str, Any] | None:
    text = str(raw or "")
    if not text:
        return None
    start = text.find("{")
    while start >= 0:
        depth = 0
        in_string = False
        escaped = False
        for idx in range(start, len(text)):
            ch = text[idx]
            if in_string:
                if escaped:
                    escaped = False
                    continue
                if ch == "\\":
                    escaped = True
                    continue
                if ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
                continue
            if ch == "{":
                depth += 1
                continue
            if ch == "}":
                depth -= 1
                if depth == 0:
                    snippet = text[start : idx + 1]
                    try:
                        payload = json.loads(snippet)
                    except Exception:
                        break
                    if isinstance(payload, dict):
                        return payload
                    break
        start = text.find("{", start + 1)
    return None


def _normalize_action_confidence(value: Any) -> float | None:
    try:
        token = float(value)
    except Exception:
        return None
    if not math.isfinite(token):
        return None
    if token > 1.0 and token <= 100.0:
        token = token / 100.0
    token = max(0.0, min(token, 1.0))
    return round(token, 3)


def _normalize_execution_handoff(raw: Any) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        return None
    out: dict[str, Any] = {}
    planner = str(raw.get("planner") or "").strip().lower()
    if planner:
        out["planner"] = planner[:40]
    intent = str(raw.get("intent") or "").strip().lower()
    if intent:
        out["intent"] = intent[:80]
    rationale = str(raw.get("intent_rationale") or raw.get("rationale") or "").strip()
    if rationale:
        out["intent_rationale"] = rationale[:320]
    confidence = _normalize_action_confidence(raw.get("confidence"))
    if confidence is not None:
        out["confidence"] = confidence
    preflight_raw = raw.get("preflight")
    if isinstance(preflight_raw, dict):
        preflight: dict[str, Any] = {}
        status = str(preflight_raw.get("status") or "").strip().lower()
        if status in {"ok", "missing_run", "missing_instruction", "needs_confirmation"}:
            preflight["status"] = status
        for key in (
            "ready_for_execute",
            "run_exists",
            "create_if_missing",
            "requires_run_confirmation",
            "requires_instruction_confirm",
        ):
            if isinstance(preflight_raw.get(key), bool):
                preflight[key] = bool(preflight_raw.get(key))
        for key in ("run_rel", "run_hint", "resolved_run_rel"):
            token = str(preflight_raw.get(key) or "").strip()
            if token:
                preflight[key] = token[:180]
        instruction_raw = preflight_raw.get("instruction")
        if isinstance(instruction_raw, dict):
            instruction: dict[str, Any] = {}
            for key in ("required", "available"):
                if isinstance(instruction_raw.get(key), bool):
                    instruction[key] = bool(instruction_raw.get(key))
            selected = str(instruction_raw.get("selected") or "").strip()
            if selected:
                instruction["selected"] = selected[:220]
            candidates_raw = instruction_raw.get("candidates")
            if isinstance(candidates_raw, list):
                candidates = [str(item or "").strip() for item in candidates_raw if str(item or "").strip()]
                if candidates:
                    instruction["candidates"] = candidates[:8]
            if instruction:
                preflight["instruction"] = instruction
        notes_raw = preflight_raw.get("notes")
        if isinstance(notes_raw, list):
            notes = [str(item or "").strip() for item in notes_raw if str(item or "").strip()]
            if notes:
                preflight["notes"] = notes[:8]
        if preflight:
            out["preflight"] = preflight
    governor_raw = raw.get("governor_loop")
    if isinstance(governor_raw, dict):
        governor: dict[str, Any] = {}
        for key in ("max_iter", "attempts", "selected_candidate_index", "budget_chars"):
            value = governor_raw.get(key)
            try:
                parsed = int(float(value))
            except Exception:
                parsed = None
            if parsed is not None:
                governor[key] = max(0, parsed)
        converged = governor_raw.get("converged")
        if isinstance(converged, bool):
            governor["converged"] = converged
        delta_threshold = governor_raw.get("delta_threshold")
        try:
            delta_token = float(delta_threshold)
        except Exception:
            delta_token = None
        if delta_token is not None and math.isfinite(delta_token):
            governor["delta_threshold"] = round(max(0.0, min(delta_token, 1.0)), 4)
        candidates_raw = governor_raw.get("candidates")
        if isinstance(candidates_raw, list):
            candidates: list[dict[str, Any]] = []
            for row in candidates_raw:
                if not isinstance(row, dict):
                    continue
                item: dict[str, Any] = {}
                row_type = str(row.get("type") or "").strip().lower()
                if row_type:
                    item["type"] = row_type[:64]
                row_conf = _normalize_action_confidence(row.get("confidence"))
                if row_conf is not None:
                    item["confidence"] = row_conf
                score_raw = row.get("score")
                try:
                    score = float(score_raw)
                except Exception:
                    score = None
                if score is not None and math.isfinite(score):
                    item["score"] = round(score, 3)
                if item:
                    candidates.append(item)
                if len(candidates) >= 6:
                    break
            if candidates:
                governor["candidates"] = candidates
        if governor:
            out["governor_loop"] = governor
    return out or None


def _normalize_agentic_action(raw: Any, *, run_rel: str | None) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        return None
    action_type = str(raw.get("type") or "").strip().lower()
    if action_type not in _HELP_AGENTIC_ACTION_TYPES:
        return None
    if action_type == "none":
        return None
    action: dict[str, Any] = {
        "type": action_type,
        "run_rel": run_rel or "",
    }
    label = str(raw.get("label") or "").strip()
    summary = str(raw.get("summary") or "").strip()
    safety = str(raw.get("safety") or "").strip()
    if label:
        action["label"] = label[:120]
    if summary:
        action["summary"] = summary[:220]
    if safety:
        action["safety"] = safety[:220]
    planner = str(raw.get("planner") or raw.get("planner_source") or "").strip().lower()
    if planner:
        action["planner"] = planner[:40]
    confidence = _normalize_action_confidence(raw.get("confidence"))
    if confidence is not None:
        action["confidence"] = confidence
    rationale = str(raw.get("intent_rationale") or raw.get("rationale") or "").strip()
    if rationale:
        action["intent_rationale"] = rationale[:320]
    execution_handoff = _normalize_execution_handoff(raw.get("execution_handoff"))
    if execution_handoff:
        action["execution_handoff"] = execution_handoff

    if action_type in {
        "run_feather",
        "run_federlicht",
        "run_feather_then_federlicht",
        "switch_run",
    }:
        run_hint = _normalize_run_hint(str(raw.get("run_hint") or ""))
        if run_hint and not _is_invalid_run_hint(run_hint):
            action["run_hint"] = run_hint
        if bool(raw.get("create_if_missing")):
            action["create_if_missing"] = True
        if bool(raw.get("auto_instruction")) and action_type in {"run_feather", "run_feather_then_federlicht"}:
            action["auto_instruction"] = True
        if bool(raw.get("require_instruction_confirm")) and action_type in {"run_feather", "run_feather_then_federlicht"}:
            action["require_instruction_confirm"] = True
        instruction_confirm_reason = str(raw.get("instruction_confirm_reason") or "").strip()
        if instruction_confirm_reason and action_type in {"run_feather", "run_feather_then_federlicht"}:
            action["instruction_confirm_reason"] = instruction_confirm_reason[:120]
        topic_hint = str(raw.get("topic_hint") or "").strip()
        if topic_hint and action_type in {"run_feather", "run_feather_then_federlicht"}:
            action["topic_hint"] = topic_hint[:160]
        effective_hint = str(action.get("run_hint") or "").strip()
        if action_type == "switch_run" and not effective_hint:
            return None
        if action_type == "switch_run" and effective_hint:
            action["label"] = f"Run 전환: {effective_hint}"
        elif action_type == "run_feather":
            action.setdefault("label", "Feather 실행")
        elif action_type == "run_federlicht":
            action.setdefault("label", "Federlicht 실행")
        elif action_type == "run_feather_then_federlicht":
            action.setdefault("label", "Feather -> Federlicht 실행")

    if action_type == "create_run_folder":
        run_name_hint = _normalize_run_hint(str(raw.get("run_name_hint") or ""))
        topic_hint = str(raw.get("topic_hint") or "").strip()
        if run_name_hint:
            action["run_name_hint"] = run_name_hint
        if topic_hint:
            action["topic_hint"] = topic_hint[:160]

    if action_type == "preset_resume_stage":
        stage = _infer_stage_hint(str(raw.get("stage") or ""))
        if not stage:
            return None
        action["stage"] = stage

    if action_type == "focus_editor":
        target = str(raw.get("target") or "").strip().lower()
        if target not in {"feather_instruction", "federlicht_prompt"}:
            return None
        action["target"] = target

    if action_type == "set_action_mode":
        mode = _normalize_execution_mode(raw.get("mode"))
        action["mode"] = mode
        if mode == "act" and bool(raw.get("allow_artifacts")):
            action["allow_artifacts"] = True

    if action_type == "run_capability":
        capability_id = str(raw.get("capability_id") or "").strip().lower()
        if not capability_id:
            return None
        action["capability_id"] = capability_id[:80]

    return action


def _history_has_topic_signal(history: list[dict[str, str]] | None) -> bool:
    normalized = _normalize_history(history)
    if not normalized:
        return False
    for row in reversed(normalized[-8:]):
        if str(row.get("role") or "") != "user":
            continue
        text = str(row.get("content") or "").strip().lower()
        if len(text) >= 20 and any(token in text for token in _TOPIC_SIGNAL_TOKENS):
            return True
    return False


def _is_generic_execution_question(question: str) -> bool:
    q = str(question or "").strip().lower()
    if not q:
        return False
    compact = re.sub(r"\s+", "", q)
    if any(compact == token for token in ("실행해줘", "돌려줘", "해줘", "start", "run", "go")):
        return True
    has_exec = _has_explicit_execution_intent(q) or any(token in q for token in _GENERIC_EXECUTION_TOKENS)
    has_topic = any(token in q for token in _TOPIC_SIGNAL_TOKENS)
    return has_exec and not has_topic and len(compact) <= 18


def _is_file_context_question(question: str) -> bool:
    q = str(question or "").strip().lower().replace("\\", "/")
    if not q:
        return False
    if not _has_run_content_path_reference(q):
        return False
    if _has_explicit_execution_intent(q):
        return False
    return True


def _is_run_content_summary_request(question: str) -> bool:
    q = str(question or "").strip().lower().replace("\\", "/")
    if not q:
        return False
    if _has_explicit_execution_intent(q):
        return False
    if not _has_run_content_path_reference(q):
        return False
    summary_tokens = (
        "정리",
        "요약",
        "무슨 내용",
        "내용 알려",
        "내용 설명",
        "읽어",
        "읽고",
        "분석",
        "요점",
        "summarize",
        "summary",
        "what's in",
        "what is in",
        "show me",
        "explain",
    )
    if any(token in q for token in summary_tokens):
        return True
    return bool(re.search(r"(무슨|어떤).*(내용|파일|폴더)", q))


def _has_explicit_execution_intent(question: str) -> bool:
    q = str(question or "").strip().lower()
    if not q:
        return False
    compact = re.sub(r"\s+", "", q)
    if any(token.replace(" ", "") in compact for token in _EXECUTION_INTENT_EXPLICIT_TOKENS):
        return True
    has_exec = bool(re.search(r"(실행|진행|작업|돌려|시작|\brun\b|\bexecute\b|\bstart\b)", q, flags=re.IGNORECASE))
    has_explain = bool(re.search(r"(설명|차이|이유|왜|방법|가이드|how|what|difference)", q, flags=re.IGNORECASE))
    return has_exec and not has_explain


def _is_workspace_operation_request(question: str) -> bool:
    q = str(question or "").strip().lower()
    if not q:
        return False
    if _mentions_run_root_token(q):
        return True
    return any(token in q for token in _WORKSPACE_ACTION_TOKENS)


def _extract_topic_hint_from_question_or_history(
    question: str,
    history: list[dict[str, str]] | None,
) -> str:
    q = str(question or "").strip()
    if q and not _is_generic_execution_question(q):
        normalized = re.sub(r"\s+", " ", q).strip()
        if normalized:
            return normalized[:160]
    for row in reversed(_normalize_history(history)[-12:]):
        if str(row.get("role") or "") != "user":
            continue
        text = str(row.get("content") or "").strip()
        if not text or _is_generic_execution_question(text):
            continue
        normalized = re.sub(r"\s+", " ", text).strip()
        if normalized:
            return normalized[:160]
    return ""


def _needs_agentic_action_planning(question: str) -> bool:
    q = str(question or "").strip().lower()
    if not q:
        return False
    if _is_run_content_summary_request(q):
        return False
    if _is_file_context_question(q):
        return False
    compact = re.sub(r"\s+", " ", q).strip()
    if not compact or re.fullmatch(r"[\W_]+", compact):
        return False
    if compact.startswith("/"):
        command = compact.split(" ", 1)[0]
        return command in {"/plan", "/act", "/profile", "/agent", "/runtime"}
    explicit_execution = _has_explicit_execution_intent(q)
    if _is_generic_execution_question(q):
        return explicit_execution
    if not _is_workspace_operation_request(q):
        return False
    return explicit_execution


def _capability_prompt_digest(capabilities: dict[str, Any] | None) -> str:
    if not isinstance(capabilities, dict):
        return "-"
    tools = capabilities.get("tools") if isinstance(capabilities.get("tools"), list) else []
    skills = capabilities.get("skills") if isinstance(capabilities.get("skills"), list) else []
    packs = capabilities.get("packs") if isinstance(capabilities.get("packs"), list) else []
    tool_ids = [str(item.get("id") or "").strip() for item in tools if isinstance(item, dict)]
    skill_ids = [str(item.get("id") or "").strip() for item in skills if isinstance(item, dict)]
    pack_ids = [str(item.get("id") or "").strip() for item in packs if isinstance(item, dict)]
    tool_ids = [token for token in tool_ids if token][:12]
    skill_ids = [token for token in skill_ids if token][:10]
    pack_ids = [token for token in pack_ids if token][:8]
    return (
        f"tools={','.join(tool_ids) if tool_ids else '-'}; "
        f"skills={','.join(skill_ids) if skill_ids else '-'}; "
        f"packs={','.join(pack_ids) if pack_ids else '-'}"
    )


def _build_agentic_action_prompt(
    question: str,
    *,
    run_rel: str | None,
    history: list[dict[str, str]] | None,
    state_memory: str,
    capabilities: dict[str, Any] | None,
    execution_mode: str,
    allow_artifacts: bool,
) -> str:
    history_rows = _normalize_history(history)
    history_brief = "\n".join(
        f"- {row['role']}: {str(row['content'])[:180]}"
        for row in history_rows[-8:]
    ) or "- (none)"
    return (
        "FederHav governing-agent action planner.\n"
        "Return exactly one JSON object and nothing else.\n\n"
        "allowed_types=["
        "none,run_feather,run_federlicht,run_feather_then_federlicht,"
        "create_run_folder,switch_run,preset_resume_stage,focus_editor,set_action_mode,run_capability"
        "]\n"
        "schema={type,label,summary,safety,run_hint,create_if_missing,auto_instruction,require_instruction_confirm,instruction_confirm_reason,run_name_hint,topic_hint,stage,target,mode,allow_artifacts,capability_id}\n"
        "rules:\n"
        "- avoid destructive/unbounded actions.\n"
        "- if intent is unclear, type=none.\n"
        "- use run_* actions only when the question clearly requests workspace execution(run/workflow/Feather/Federlicht).\n"
        "- if user asks run switch/create explicitly, fill run_hint or run_name_hint.\n"
        "- use set_action_mode only when user explicitly asks policy mode.\n"
        "- prefer focus_editor when instruction/prompt editing intent is explicit.\n"
        "- execution_mode and allow_artifacts are policy hints, not mandatory action.\n\n"
        f"question={question}\n"
        f"run_rel={run_rel or ''}\n"
        f"execution_mode={execution_mode}\n"
        f"allow_artifacts={str(bool(allow_artifacts)).lower()}\n"
        f"capabilities={_capability_prompt_digest(capabilities)}\n"
        f"recent_history:\n{history_brief}\n"
        f"state_memory_json={state_memory or '{}'}\n"
    )


def _infer_agentic_action(
    root: Path,
    question: str,
    *,
    run_rel: str | None,
    history: list[dict[str, str]] | None,
    state_memory: str,
    capabilities: dict[str, Any] | None,
    execution_mode: str,
    allow_artifacts: bool,
    model: str | None,
    llm_backend: str | None,
    reasoning_effort: str | None,
    runtime_mode: str | None,
    strict_model: bool,
) -> dict[str, Any] | None:
    if _is_run_content_summary_request(question):
        return None
    if not _agentic_actions_enabled():
        return None
    if not _needs_agentic_action_planning(question):
        return None
    payload = _try_agentic_runtime_action_plan(
        question=question,
        run_rel=run_rel,
        history=history,
        state_memory=state_memory,
        capabilities=capabilities,
        execution_mode=execution_mode,
        allow_artifacts=allow_artifacts,
        model=model,
        llm_backend=llm_backend,
        reasoning_effort=reasoning_effort,
        runtime_mode=runtime_mode,
        root=root,
    )
    if isinstance(payload, dict):
        payload = {**payload, "planner": str(payload.get("planner") or "deepagent").strip() or "deepagent"}
    if payload is None and _allow_llm_action_planner_fallback(runtime_mode):
        planner_prompt = _build_agentic_action_prompt(
            question,
            run_rel=run_rel,
            history=history,
            state_memory=state_memory,
            capabilities=capabilities,
            execution_mode=execution_mode,
            allow_artifacts=allow_artifacts,
        )
        try:
            planned, _planned_model = _call_llm(
                planner_prompt,
                [],
                model=model,
                history=None,
                live_log_tail="",
                state_memory=state_memory,
                strict_model=bool(strict_model),
                reasoning_effort=reasoning_effort,
                runtime_mode=runtime_mode,
                root=root,
                llm_backend=llm_backend,
            )
        except Exception:
            return None
        payload = _extract_first_json_object(planned)
        if isinstance(payload, dict):
            payload = {**payload, "planner": str(payload.get("planner") or "llm_fallback").strip() or "llm_fallback"}
    action = _normalize_agentic_action(payload, run_rel=run_rel)
    if not action:
        return None
    action_type = str(action.get("type") or "")
    if action_type in {"run_feather", "run_federlicht", "run_feather_then_federlicht"}:
        q = str(question or "").strip().lower()
        if not _is_workspace_operation_request(q) and not _is_generic_execution_question(q):
            return None
    if action_type in {"run_feather", "run_federlicht", "run_feather_then_federlicht", "switch_run"}:
        run_hint = _normalize_run_hint(str(action.get("run_hint") or ""))
        if run_hint and _is_invalid_run_hint(run_hint):
            action.pop("run_hint", None)
            run_hint = ""
        if not run_hint:
            hint = _extract_recent_run_hint(history)
            if hint:
                action["run_hint"] = hint
                if action_type.startswith("run_"):
                    action.setdefault("create_if_missing", True)
        if action_type == "switch_run" and not str(action.get("run_hint") or "").strip():
            return None
    return action


def _apply_instruction_quality_guard(
    action: dict[str, Any] | None,
    *,
    question: str,
    run_rel: str | None,
    history: list[dict[str, str]] | None,
) -> dict[str, Any] | None:
    if not isinstance(action, dict):
        return action
    action_type = str(action.get("type") or "").strip().lower()
    if action_type not in {"run_feather", "run_feather_then_federlicht"}:
        return action
    if not _is_generic_execution_question(question):
        return action
    next_action = dict(action)
    topic_hint = _extract_topic_hint_from_question_or_history(question, history)
    if not topic_hint:
        return {
            "type": "focus_editor",
            "label": "Feather Instruction 열기",
            "target": "feather_instruction",
            "run_rel": run_rel or "",
            "safety": "실행 전 instruction 품질 확인 필요 (자동 실행 보류)",
            "summary": "요청이 짧아 주제가 불명확합니다. 먼저 질문을 보강한 뒤 instruction을 작성하세요.",
            "clarify_required": True,
            "clarify_question": (
                "어떤 주제로 실행할까요? 예: '양자컴퓨터 최신 기술 동향을 분석해 보고서 작성해줘'"
            ),
        }
    next_action["auto_instruction"] = True
    next_action["require_instruction_confirm"] = True
    next_action["instruction_confirm_reason"] = "short_generic_request"
    next_action["topic_hint"] = topic_hint
    next_action["safety"] = "instruction 품질 점검/자동작성 후 실행 (run 범위 내 파일만 사용)"
    if action_type == "run_feather_then_federlicht":
        next_action["summary"] = "질문이 짧아 instruction을 자동 보정한 뒤 Feather -> Federlicht 연속 실행"
    else:
        next_action["summary"] = "질문이 짧아 instruction을 자동 보정한 뒤 Feather 실행"
    return next_action


def _infer_governed_action(
    root: Path,
    question: str,
    *,
    run_rel: str | None,
    history: list[dict[str, str]] | None,
    state_memory: str,
    capabilities: dict[str, Any] | None,
    execution_mode: str,
    allow_artifacts: bool,
    model: str | None,
    llm_backend: str | None,
    reasoning_effort: str | None,
    runtime_mode: str | None,
    strict_model: bool,
) -> dict[str, Any] | None:
    if _is_run_content_summary_request(question):
        return None
    action = _infer_agentic_action(
        root,
        question,
        run_rel=run_rel,
        history=history,
        state_memory=state_memory,
        capabilities=capabilities,
        execution_mode=execution_mode,
        allow_artifacts=allow_artifacts,
        model=model,
        llm_backend=llm_backend,
        reasoning_effort=reasoning_effort,
        runtime_mode=runtime_mode,
        strict_model=bool(strict_model),
    )
    if action is None and _allow_rule_fallback(runtime_mode):
        action = _infer_safe_action(root, question, run_rel=run_rel, history=history)
        if isinstance(action, dict):
            action = {
                **action,
                "planner": "rule_fallback",
                "confidence": action.get("confidence", 0.41),
                "intent_rationale": str(
                    action.get("intent_rationale")
                    or "Emergency safe-rule fallback used because FEDERNETT_HELP_RULE_FALLBACK=1."
                ).strip(),
            }
    return _apply_instruction_quality_guard(
        action,
        question=question,
        run_rel=run_rel,
        history=history,
    )


def _infer_safe_action(
    root: Path,
    question: str,
    run_rel: str | None = None,
    history: list[dict[str, str]] | None = None,
) -> dict[str, Any] | None:
    q = (question or "").strip().lower()
    if not q:
        return None
    if _is_run_content_summary_request(q):
        return None
    if _is_file_context_question(q):
        return None
    workspace_request = _is_workspace_operation_request(q)
    generic_followup = _is_generic_execution_question(q)
    followup_execution_like = _has_explicit_execution_intent(q)
    custom = infer_capability_action(root, q, run_rel=run_rel)
    if custom:
        action_type = str(custom.get("type") or "").strip().lower()
        if (
            followup_execution_like
            and action_type in {"run_feather", "run_federlicht", "run_feather_then_federlicht", "switch_run"}
            and not str(custom.get("run_hint") or "").strip()
        ):
            hint = _extract_recent_run_hint(history)
            if hint:
                custom["run_hint"] = hint
                if action_type.startswith("run_"):
                    custom.setdefault("create_if_missing", True)
        return custom

    plan_mode_like = any(
        token in q
        for token in ("plan mode", "plan 모드", "계획 모드", "제안 후 확인", "확인 후 실행", "preview mode")
    )
    act_mode_like = any(
        token in q
        for token in ("act mode", "act 모드", "자동 실행 모드", "즉시 실행 모드")
    )
    if plan_mode_like:
        return {
            "type": "set_action_mode",
            "label": "Plan 모드 전환",
            "mode": "plan",
            "run_rel": run_rel or "",
            "safety": "제안 후 확인 실행 모드",
            "summary": "FederHav 실행 정책을 Plan 모드로 전환",
        }
    if act_mode_like:
        allow_artifacts = any(
            token in q
            for token in (
                "파일쓰기허용",
                "파일 쓰기 허용",
                "artifact",
                "바로 실행",
                "즉시 실행",
                "자동 실행",
            )
        )
        return {
            "type": "set_action_mode",
            "label": "Act 모드 전환",
            "mode": "act",
            "allow_artifacts": allow_artifacts,
            "run_rel": run_rel or "",
            "safety": "안전 범위 내 자동 실행 모드",
            "summary": "FederHav 실행 정책을 Act 모드로 전환",
        }

    run_hint = _extract_run_hint(question)
    run_hint_from_history = False
    if not run_hint and followup_execution_like:
        run_hint = _extract_recent_run_hint(history)
        run_hint_from_history = bool(run_hint)
    run_binding_like = bool(run_hint) and (
        any(
            token in q
            for token in (
                "run folder",
                "run 폴더",
                "런 폴더",
                "run을",
                "run 를",
                "런을",
                "으로 설정",
                "로 설정",
                "으로 하고",
                "로 하고",
                "run as",
                "use run",
                "run=",
            )
        )
        or _mentions_run_root_token(q)
        or run_hint_from_history
    )
    run_create_if_missing_like = bool(run_hint) and any(
        token in q
        for token in (
            "run folder",
            "run 폴더",
            "런 폴더",
            "으로 설정",
            "로 설정",
            "으로 하고",
            "로 하고",
            "run as",
            "use run",
            "run=",
            "새 run",
            "새로운 run",
            "new run",
            "신규 run",
            "fresh run",
            "create run",
            "만들",
            "생성",
        )
    )
    switch_run_like = any(
        token in q
        for token in (
            "run 변경",
            "run 전환",
            "run 바꿔",
            "run 선택",
            "switch run",
            "select run",
            "다른 run",
            "런 변경",
            "런 전환",
            "런 바꿔",
        )
    ) or (
        "run" in q
        and any(token in q for token in ("전환", "변경", "바꿔", "선택", "switch", "select", "use"))
    ) or (
        _mentions_run_root_token(q)
        and any(token in q for token in ("열어", "open", "선택", "바꿔", "전환", "use"))
    )
    if switch_run_like:
        if run_hint:
            action = {
                "type": "switch_run",
                "label": f"Run 전환: {run_hint}",
                "run_hint": run_hint,
                "run_rel": run_rel or "",
                "safety": "기존 run 선택만 수행 (파일 변경 없음)",
                "summary": f"대상 run으로 전환: {run_hint}",
            }
            if run_create_if_missing_like:
                action["create_if_missing"] = True
                action["summary"] = f"대상 run으로 전환 (없으면 생성): {run_hint}"
            return action

    stage_hint = _infer_stage_hint(q)
    stage_control_like = any(
        token in q
        for token in ("단계", "stage", "부터", "재시작", "resume", "이어서", "다시", "start from", "시작점")
    )
    if stage_hint and stage_control_like:
        stage_label = stage_hint.capitalize()
        return {
            "type": "preset_resume_stage",
            "label": f"{stage_label}부터 재시작 프리셋",
            "stage": stage_hint,
            "run_rel": run_rel or "",
            "safety": "워크플로우 시작점 프리셋만 변경",
            "summary": f"Federlicht 재시작 단계를 {stage_label}로 설정",
        }

    editor_focus_like = any(
        token in q
        for token in ("열어", "focus", "편집", "수정", "작성", "입력", "update", "채워")
    )
    prompt_like = any(token in q for token in ("prompt", "프롬프트", "inline prompt", "inline"))
    instruction_like = any(token in q for token in ("instruction", "지시문", "요청문", "query", "질문문"))
    if editor_focus_like and (prompt_like or instruction_like):
        target = (
            "federlicht_prompt"
            if (prompt_like or "federlicht" in q or "보고서" in q)
            else "feather_instruction"
        )
        target_label = "Federlicht Inline Prompt" if target == "federlicht_prompt" else "Feather Instruction"
        return {
            "type": "focus_editor",
            "label": f"{target_label} 열기",
            "target": target,
            "run_rel": run_rel or "",
            "safety": "편집기 포커스만 이동 (자동 저장/실행 없음)",
            "summary": f"{target_label} 편집기로 이동",
        }

    def _extract_topic_hint(raw: str) -> str:
        text = str(raw or "").strip()
        if not text:
            return ""
        patterns = [
            r"(?:주제(?:는|:)\s*)(.+)$",
            r"(?:topic\s*[:=]\s*)(.+)$",
            r"(?:about\s+)(.+)$",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if not match:
                continue
            value = str(match.group(1) or "").strip()
            if value:
                value = re.sub(r"[.?!]+$", "", value).strip()
                return value[:120]
        cleaned = re.sub(r"\s+", " ", text).strip()
        return cleaned[:120]

    create_run_like = (
        any(token in q for token in ("run folder", "run 폴더", "런 폴더", "runfolder", "새 run", "새로운 run"))
        and any(token in q for token in ("만들", "생성", "create", "new"))
    )
    explicit_new_run_like = any(
        token in q
        for token in (
            "새 run",
            "새로운 run",
            "new run",
            "신규 run",
            "fresh run",
            "create run",
        )
    )
    if create_run_like and run_hint and not explicit_new_run_like:
        action = {
            "type": "switch_run",
            "label": f"Run 전환: {run_hint}",
            "run_hint": run_hint,
            "run_rel": run_rel or "",
            "safety": "기존 run 선택만 수행 (파일 변경 없음)",
            "summary": f"대상 run으로 전환: {run_hint}",
        }
        action["create_if_missing"] = True
        action["summary"] = f"대상 run으로 전환 (없으면 생성): {run_hint}"
        return action
    if create_run_like:
        topic_hint = _extract_topic_hint(question)
        run_name_hint = run_hint or _extract_run_hint(topic_hint)
        return {
            "type": "create_run_folder",
            "label": "새 Run Folder 생성",
            "run_rel": run_rel or "",
            "topic_hint": topic_hint,
            "run_name_hint": run_name_hint,
            "safety": "configured run root 하위에 안전한 새 run 폴더만 생성",
            "summary": f"새 run 생성 · run={run_name_hint}" if run_name_hint else (
                f"새 run 생성 · topic={topic_hint}" if topic_hint else "새 run 생성"
            ),
        }

    execution_intent_like = _has_explicit_execution_intent(q)
    if run_binding_like and run_hint and not execution_intent_like:
        action = {
            "type": "switch_run",
            "label": f"Run 전환: {run_hint}",
            "run_hint": run_hint,
            "run_rel": run_rel or "",
            "safety": "기존 run 선택만 수행 (파일 변경 없음)",
            "summary": f"대상 run으로 전환: {run_hint}",
        }
        action["create_if_missing"] = True
        action["summary"] = f"대상 run으로 전환 (없으면 생성): {run_hint}"
        return action

    explicit_run = _has_explicit_execution_intent(q) or any(
        token in q for token in ("재작성", "다시 작성")
    )
    analysis_like = any(
        token in q
        for token in (
            "파악",
            "분석",
            "정리",
            "조사",
            "동향",
            "최신 기술",
            "최신 동향",
            "보고서 작성",
            "리포트 작성",
        )
    )
    if analysis_like and not workspace_request and not generic_followup:
        return None
    if not explicit_run:
        return None
    if any(token in q for token in ("feather부터", "연속", "end-to-end", "파이프라인")):
        action = {
            "type": "run_feather_then_federlicht",
            "label": "Feather -> Federlicht 실행",
            "run_rel": run_rel or "",
            "safety": "현재 화면 폼 값만 사용",
            "summary": "수집부터 보고서 생성까지 연속 실행",
        }
        if run_binding_like and run_hint:
            action["run_hint"] = run_hint
            action["create_if_missing"] = True
            action["summary"] = f"수집부터 보고서 생성까지 연속 실행 · run={run_hint}"
        return action
    target_from_history = _infer_recent_execution_target(history)
    feather_requested = "feather" in q or any(token in q for token in ("자료 수집", "검색", "크롤링", "아카이브"))
    federlicht_requested = "federlicht" in q or "보고서" in q
    if feather_requested or (not federlicht_requested and target_from_history == "feather"):
        action = {
            "type": "run_feather",
            "label": "Feather 실행",
            "run_rel": run_rel or "",
            "safety": "현재 화면 폼 값만 사용",
            "summary": "자료 수집/아카이브 실행",
        }
        if run_binding_like and run_hint:
            action["run_hint"] = run_hint
            action["create_if_missing"] = True
            action["summary"] = f"자료 수집/아카이브 실행 · run={run_hint}"
        return action
    if federlicht_requested or (not feather_requested and target_from_history == "federlicht"):
        action = {
            "type": "run_federlicht",
            "label": "Federlicht 실행",
            "run_rel": run_rel or "",
            "safety": "현재 화면 폼 값만 사용",
            "summary": "현재 Run 기준 보고서 생성",
        }
        if run_binding_like and run_hint:
            action["run_hint"] = run_hint
            action["create_if_missing"] = True
            action["summary"] = f"현재 Run 기준 보고서 생성 · run={run_hint}"
        return action
    action = {
        "type": "run_feather_then_federlicht",
        "label": "Feather -> Federlicht 실행",
        "run_rel": run_rel or "",
        "safety": "현재 화면 폼 값만 사용",
        "summary": "질문 의도 기반으로 수집+보고서 연속 실행",
    }
    if run_binding_like and run_hint:
        action["run_hint"] = run_hint
        action["create_if_missing"] = True
        action["summary"] = f"질문 의도 기반으로 수집+보고서 연속 실행 · run={run_hint}"
    return action


def _help_capabilities(root: Path, web_search_enabled: bool) -> dict[str, Any]:
    return runtime_capabilities(root, web_search_enabled=bool(web_search_enabled))


def _new_governor_trace_id() -> str:
    millis = int(time.time() * 1000)
    return f"fh-{millis:x}"


def _estimate_token_count(text: str) -> int:
    raw = str(text or "")
    if not raw:
        return 0
    return max(1, int(len(raw) / 4))


def _trace_step(
    step_id: str,
    status: str,
    *,
    message: str = "",
    tool_id: str = "",
    duration_ms: float | int | None = None,
    token_est: int | None = None,
    cache_hit: bool | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "id": str(step_id or "").strip() or "unknown",
        "status": str(status or "idle").strip().lower() or "idle",
        "tool_id": str(tool_id or step_id or "unknown").strip() or "unknown",
    }
    note = str(message or "").strip()
    if note:
        out["message"] = note[:280]
    if duration_ms is not None:
        try:
            out["duration_ms"] = max(0, int(float(duration_ms)))
        except Exception:
            pass
    if token_est is not None:
        try:
            out["token_est"] = max(0, int(token_est))
        except Exception:
            pass
    if cache_hit is not None:
        out["cache_hit"] = bool(cache_hit)
    if isinstance(details, dict) and details:
        out["details"] = details
    return out


def _trace_activity_event(
    *,
    trace_id: str,
    step_id: str,
    status: str,
    message: str,
    tool_id: str = "",
    duration_ms: float | int | None = None,
    token_est: int | None = None,
    cache_hit: bool | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {
        "event": "activity",
        "id": str(step_id or "").strip() or "unknown",
        "status": str(status or "idle").strip().lower() or "idle",
        "message": str(message or "").strip(),
        "trace_id": str(trace_id or "").strip(),
        "tool_id": str(tool_id or step_id or "unknown").strip() or "unknown",
    }
    if duration_ms is not None:
        try:
            payload["duration_ms"] = max(0, int(float(duration_ms)))
        except Exception:
            pass
    if token_est is not None:
        try:
            payload["token_est"] = max(0, int(token_est))
        except Exception:
            pass
    if cache_hit is not None:
        payload["cache_hit"] = bool(cache_hit)
    if isinstance(details, dict) and details:
        payload["details"] = details
    return payload


def _action_governor_summary(action_details: dict[str, Any] | None) -> str:
    if not isinstance(action_details, dict):
        return ""
    handoff = action_details.get("execution_handoff")
    if not isinstance(handoff, dict):
        return ""
    governor = handoff.get("governor_loop")
    if not isinstance(governor, dict):
        return ""
    attempts = governor.get("attempts")
    max_iter = governor.get("max_iter")
    converged = governor.get("converged")
    candidates = governor.get("candidates")
    candidate_count = len(candidates) if isinstance(candidates, list) else 0
    parts: list[str] = []
    if isinstance(attempts, int) and isinstance(max_iter, int) and max_iter > 0:
        parts.append(f"governor={attempts}/{max_iter}")
    elif isinstance(attempts, int):
        parts.append(f"governor={attempts}")
    if isinstance(converged, bool):
        parts.append("converged" if converged else "non-converged")
    if candidate_count > 0:
        parts.append(f"candidates={candidate_count}")
    return " ".join(parts).strip()


def _clarify_prompt_from_action(action: dict[str, Any] | None) -> tuple[bool, str]:
    if not isinstance(action, dict):
        return False, ""
    required = bool(action.get("clarify_required"))
    prompt = str(action.get("clarify_question") or "").strip()
    if required and prompt:
        return True, prompt[:220]
    return False, ""


def _action_trace_details(action: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(action, dict):
        return None
    action_type = str(action.get("type") or "").strip().lower()
    if not action_type:
        return None
    details: dict[str, Any] = {"type": action_type}
    planner = str(action.get("planner") or "").strip().lower()
    if planner:
        details["planner"] = planner
    confidence = _normalize_action_confidence(action.get("confidence"))
    if confidence is not None:
        details["confidence"] = confidence
    rationale = str(action.get("intent_rationale") or "").strip()
    if rationale:
        details["intent_rationale"] = rationale[:220]
    handoff = _normalize_execution_handoff(action.get("execution_handoff"))
    if handoff:
        details["execution_handoff"] = handoff
    return details


def _action_trace_status_and_message(action: dict[str, Any] | None) -> tuple[str, str, dict[str, Any] | None]:
    details = _action_trace_details(action)
    if not details:
        return "skipped", "no executable action suggested", None
    planner = str(details.get("planner") or "-")
    confidence = details.get("confidence")
    confidence_text = ""
    if isinstance(confidence, (float, int)):
        confidence_text = f" confidence={float(confidence):.2f}"
    governor_summary = _action_governor_summary(details)
    suffix = f" {governor_summary}" if governor_summary else ""
    message = f"action={details.get('type')} planner={planner}{confidence_text}{suffix}".strip()
    return "done", message, details


def answer_help_question(
    root: Path,
    question: str,
    *,
    agent: str | None = None,
    execution_mode: str = "plan",
    allow_artifacts: bool = False,
    model: str | None = None,
    llm_backend: str | None = None,
    reasoning_effort: str | None = None,
    runtime_mode: str | None = None,
    strict_model: bool = False,
    max_sources: int = 8,
    history: list[dict[str, str]] | None = None,
    state_memory: dict[str, Any] | None = None,
    run_rel: str | None = None,
    web_search: bool = False,
    live_log_tail: str | None = None,
) -> dict[str, Any]:
    q = (question or "").strip()
    if not q:
        raise ValueError("question is required")
    effective_run_rel = _effective_run_rel(run_rel, state_memory)
    trace_id = _new_governor_trace_id()
    trace_steps: list[dict[str, Any]] = []
    resolved_mode = _normalize_execution_mode(execution_mode)
    resolved_agent = _normalize_agent_label(agent)
    effective_question = _augment_help_question(
        q,
        execution_mode=resolved_mode,
        agent=resolved_agent,
        allow_artifacts=bool(allow_artifacts),
    )
    web_note = ""
    if web_search:
        web_started = time.perf_counter()
        if _should_run_help_web_search(q, history):
            web_note = _run_help_web_research(root, question=q, run_rel=effective_run_rel, history=history)
        else:
            web_note = "web_search enabled: skipped (query does not require web lookup)."
        web_elapsed_ms = (time.perf_counter() - web_started) * 1000.0
        web_status = "skipped" if "skipped" in web_note.lower() else ("error" if web_note.lower().startswith("web_search failed") else "done")
        trace_steps.append(
            _trace_step(
                "web_research",
                web_status,
                message=web_note or "web research completed",
                tool_id="web_research",
                duration_ms=web_elapsed_ms,
                cache_hit=False,
            )
        )
    else:
        trace_steps.append(
            _trace_step(
                "web_research",
                "disabled",
                message="web_search 옵션이 꺼져 있습니다.",
                tool_id="web_research",
                duration_ms=0,
            )
        )
    source_index_started = time.perf_counter()
    sources, indexed_files = _select_sources(
        root,
        q,
        max_sources=max(3, min(max_sources, 16)),
        run_rel=effective_run_rel,
    )
    source_index_elapsed_ms = (time.perf_counter() - source_index_started) * 1000.0
    trace_steps.append(
        _trace_step(
            "source_index",
            "done",
            message=f"근거 후보 {indexed_files}개 인덱스 완료",
            tool_id="source_index",
            duration_ms=source_index_elapsed_ms,
            token_est=0,
            cache_hit=False,
        )
    )
    error_msg = ""
    used_llm = False
    used_model = ""
    resolved_backend = _resolve_help_llm_backend(llm_backend)
    resolved_reasoning_effort = _resolve_help_reasoning_effort(reasoning_effort)
    resolved_runtime_mode = _resolve_help_runtime_mode(runtime_mode)
    normalized_live_log_tail = _normalize_live_log_tail(live_log_tail)
    normalized_state_memory = _normalize_state_memory(state_memory)
    capabilities = _help_capabilities(root, bool(web_search))
    requested_model, explicit_model = _resolve_requested_model(model, backend=resolved_backend)
    llm_started = time.perf_counter()
    try:
        answer, used_model = _call_llm(
            effective_question,
            sources,
            model=model,
            history=history,
            live_log_tail=normalized_live_log_tail,
            state_memory=normalized_state_memory,
            strict_model=bool(strict_model),
            reasoning_effort=resolved_reasoning_effort,
            runtime_mode=resolved_runtime_mode,
            root=root,
            llm_backend=resolved_backend,
        )
        used_llm = True
        llm_elapsed_ms = (time.perf_counter() - llm_started) * 1000.0
        trace_steps.append(
            _trace_step(
                "llm_generate",
                "done",
                message=f"완료 · model={used_model or requested_model or '-'}",
                tool_id="llm_generate",
                duration_ms=llm_elapsed_ms,
                token_est=_estimate_token_count(answer),
                cache_hit=False,
            )
        )
    except Exception as exc:
        error_msg = str(exc)
        answer = _fallback_answer(q, sources)
        llm_elapsed_ms = (time.perf_counter() - llm_started) * 1000.0
        trace_steps.append(
            _trace_step(
                "llm_generate",
                "error",
                message=error_msg,
                tool_id="llm_generate",
                duration_ms=llm_elapsed_ms,
                token_est=_estimate_token_count(answer),
                cache_hit=False,
            )
        )
    reported_reasoning_effort = _reported_reasoning_effort(
        resolved_reasoning_effort,
        backend=resolved_backend,
        model_name=used_model or requested_model,
    )
    action = _infer_governed_action(
        root,
        q,
        run_rel=effective_run_rel,
        history=history,
        state_memory=normalized_state_memory,
        capabilities=capabilities,
        execution_mode=resolved_mode,
        allow_artifacts=bool(allow_artifacts),
        model=model,
        llm_backend=resolved_backend,
        reasoning_effort=resolved_reasoning_effort,
        runtime_mode=resolved_runtime_mode,
        strict_model=bool(strict_model),
    )
    action_status, action_message, action_details = _action_trace_status_and_message(action)
    trace_steps.append(
        _trace_step(
            "action_plan",
            action_status,
            message=action_message,
            tool_id="action_planner",
            duration_ms=0,
            token_est=0,
            cache_hit=False,
            details=action_details,
        )
    )
    clarify_required, clarify_question = _clarify_prompt_from_action(action)
    return {
        "answer": answer,
        "sources": sources,
        "used_llm": used_llm,
        "model": used_model,
        "requested_model": requested_model,
        "model_selection": "explicit" if explicit_model else "auto",
        "model_fallback": bool(used_llm and requested_model and used_model and requested_model != used_model),
        "llm_backend": resolved_backend,
        "reasoning_effort": reported_reasoning_effort,
        "runtime_mode": resolved_runtime_mode,
        "error": error_msg,
        "indexed_files": indexed_files,
        "web_search": bool(web_search),
        "web_search_note": web_note,
        "live_log_chars": len(normalized_live_log_tail),
        "state_memory_chars": len(normalized_state_memory),
        "agent": resolved_agent,
        "execution_mode": resolved_mode,
        "allow_artifacts": bool(allow_artifacts),
        "action": action,
        "capabilities": capabilities,
        "trace": {
            "trace_id": trace_id,
            "steps": trace_steps,
        },
        "clarify_required": bool(clarify_required),
        "clarify_question": clarify_question,
    }


def stream_help_question(
    root: Path,
    question: str,
    *,
    agent: str | None = None,
    execution_mode: str = "plan",
    allow_artifacts: bool = False,
    model: str | None = None,
    llm_backend: str | None = None,
    reasoning_effort: str | None = None,
    runtime_mode: str | None = None,
    strict_model: bool = False,
    max_sources: int = 8,
    history: list[dict[str, str]] | None = None,
    state_memory: dict[str, Any] | None = None,
    run_rel: str | None = None,
    web_search: bool = False,
    live_log_tail: str | None = None,
) -> Iterator[dict[str, Any]]:
    q = (question or "").strip()
    if not q:
        raise ValueError("question is required")
    effective_run_rel = _effective_run_rel(run_rel, state_memory)
    trace_id = _new_governor_trace_id()
    trace_steps: list[dict[str, Any]] = []
    resolved_mode = _normalize_execution_mode(execution_mode)
    resolved_agent = _normalize_agent_label(agent)
    effective_question = _augment_help_question(
        q,
        execution_mode=resolved_mode,
        agent=resolved_agent,
        allow_artifacts=bool(allow_artifacts),
    )
    web_note = ""
    yield _trace_activity_event(
        trace_id=trace_id,
        step_id="source_index",
        status="running",
        message="코드/문서 인덱스를 탐색 중입니다.",
        tool_id="source_index",
    )
    if web_search:
        yield _trace_activity_event(
            trace_id=trace_id,
            step_id="web_research",
            status="running",
            message="웹 보강 검색을 준비 중입니다.",
            tool_id="web_research",
        )
        web_started = time.perf_counter()
        if _should_run_help_web_search(q, history):
            web_note = _run_help_web_research(root, question=q, run_rel=effective_run_rel, history=history)
        else:
            web_note = "web_search enabled: skipped (query does not require web lookup)."
        web_elapsed_ms = (time.perf_counter() - web_started) * 1000.0
        web_status = "error" if web_note.lower().startswith("web_search failed") else "done"
        if "skipped" in web_note.lower():
            web_status = "skipped"
        web_message = web_note or "web search completed"
        trace_steps.append(
            _trace_step(
                "web_research",
                web_status,
                message=web_message,
                tool_id="web_research",
                duration_ms=web_elapsed_ms,
                cache_hit=False,
            )
        )
        yield _trace_activity_event(
            trace_id=trace_id,
            step_id="web_research",
            status=web_status,
            message=web_message,
            tool_id="web_research",
            duration_ms=web_elapsed_ms,
            cache_hit=False,
        )
    else:
        trace_steps.append(
            _trace_step(
                "web_research",
                "disabled",
                message="web_search 옵션이 꺼져 있습니다.",
                tool_id="web_research",
                duration_ms=0,
            )
        )
        yield _trace_activity_event(
            trace_id=trace_id,
            step_id="web_research",
            status="disabled",
            message="web_search 옵션이 꺼져 있습니다.",
            tool_id="web_research",
            duration_ms=0,
        )
    source_index_started = time.perf_counter()
    sources, indexed_files = _select_sources(
        root,
        q,
        max_sources=max(3, min(max_sources, 16)),
        run_rel=effective_run_rel,
    )
    source_index_elapsed_ms = (time.perf_counter() - source_index_started) * 1000.0
    source_index_message = f"근거 후보 {indexed_files}개 인덱스 완료"
    trace_steps.append(
        _trace_step(
            "source_index",
            "done",
            message=source_index_message,
            tool_id="source_index",
            duration_ms=source_index_elapsed_ms,
            token_est=0,
            cache_hit=False,
        )
    )
    yield _trace_activity_event(
        trace_id=trace_id,
        step_id="source_index",
        status="done",
        message=source_index_message,
        tool_id="source_index",
        duration_ms=source_index_elapsed_ms,
        token_est=0,
        cache_hit=False,
    )
    resolved_backend = _resolve_help_llm_backend(llm_backend)
    resolved_reasoning_effort = _resolve_help_reasoning_effort(reasoning_effort)
    resolved_runtime_mode = _resolve_help_runtime_mode(runtime_mode)
    normalized_live_log_tail = _normalize_live_log_tail(live_log_tail)
    normalized_state_memory = _normalize_state_memory(state_memory)
    capabilities = _help_capabilities(root, bool(web_search))
    requested_model, explicit_model = _resolve_requested_model(model, backend=resolved_backend)
    reported_reasoning_effort = _reported_reasoning_effort(
        resolved_reasoning_effort,
        backend=resolved_backend,
        model_name=requested_model,
    )
    yield {
        "event": "meta",
        "requested_model": requested_model,
        "model_selection": "explicit" if explicit_model else "auto",
        "llm_backend": resolved_backend,
        "reasoning_effort": reported_reasoning_effort,
        "runtime_mode": resolved_runtime_mode,
        "indexed_files": indexed_files,
        "web_search": bool(web_search),
        "web_search_note": web_note,
        "live_log_chars": len(normalized_live_log_tail),
        "state_memory_chars": len(normalized_state_memory),
        "agent": resolved_agent,
        "execution_mode": resolved_mode,
        "allow_artifacts": bool(allow_artifacts),
        "capabilities": capabilities,
        "trace_id": trace_id,
    }
    error_msg = ""
    used_llm = False
    used_model = ""
    answer_parts: list[str] = []
    yield _trace_activity_event(
        trace_id=trace_id,
        step_id="llm_generate",
        status="running",
        message="답변 생성 중입니다.",
        tool_id="llm_generate",
    )
    llm_started = time.perf_counter()
    try:
        chunk_iter, used_model = _call_llm_stream(
            effective_question,
            sources,
            model=model,
            history=history,
            live_log_tail=normalized_live_log_tail,
            state_memory=normalized_state_memory,
            strict_model=bool(strict_model),
            reasoning_effort=resolved_reasoning_effort,
            runtime_mode=resolved_runtime_mode,
            root=root,
            llm_backend=resolved_backend,
        )
        used_llm = True
        for chunk in chunk_iter:
            token = str(chunk or "")
            if not token:
                continue
            answer_parts.append(token)
            yield {"event": "delta", "text": token}
    except Exception as exc:
        error_msg = str(exc)
        llm_elapsed_ms = (time.perf_counter() - llm_started) * 1000.0
        trace_steps.append(
            _trace_step(
                "llm_generate",
                "error",
                message=error_msg,
                tool_id="llm_generate",
                duration_ms=llm_elapsed_ms,
                token_est=0,
                cache_hit=False,
            )
        )
        yield _trace_activity_event(
            trace_id=trace_id,
            step_id="llm_generate",
            status="error",
            message=error_msg,
            tool_id="llm_generate",
            duration_ms=llm_elapsed_ms,
            token_est=0,
            cache_hit=False,
        )
    answer = "".join(answer_parts).strip()
    if not answer:
        answer = _fallback_answer(q, sources)
        if used_llm:
            used_llm = False
            if not error_msg:
                error_msg = "LLM returned empty content"
    if not error_msg:
        model_note = used_model or requested_model or "configured default"
        llm_elapsed_ms = (time.perf_counter() - llm_started) * 1000.0
        llm_message = f"완료 · model={model_note}"
        token_est = _estimate_token_count(answer)
        trace_steps.append(
            _trace_step(
                "llm_generate",
                "done",
                message=llm_message,
                tool_id="llm_generate",
                duration_ms=llm_elapsed_ms,
                token_est=token_est,
                cache_hit=False,
            )
        )
        yield _trace_activity_event(
            trace_id=trace_id,
            step_id="llm_generate",
            status="done",
            message=llm_message,
            tool_id="llm_generate",
            duration_ms=llm_elapsed_ms,
            token_est=token_est,
            cache_hit=False,
        )
    yield {"event": "sources", "sources": sources}
    action = _infer_governed_action(
        root,
        q,
        run_rel=effective_run_rel,
        history=history,
        state_memory=normalized_state_memory,
        capabilities=capabilities,
        execution_mode=resolved_mode,
        allow_artifacts=bool(allow_artifacts),
        model=model,
        llm_backend=resolved_backend,
        reasoning_effort=resolved_reasoning_effort,
        runtime_mode=resolved_runtime_mode,
        strict_model=bool(strict_model),
    )
    action_status, action_message, action_details = _action_trace_status_and_message(action)
    trace_steps.append(
        _trace_step(
            "action_plan",
            action_status,
            message=action_message,
            tool_id="action_planner",
            duration_ms=0,
            token_est=0,
            cache_hit=False,
            details=action_details,
        )
    )
    yield _trace_activity_event(
        trace_id=trace_id,
        step_id="action_plan",
        status=action_status,
        message=action_message,
        tool_id="action_planner",
        duration_ms=0,
        token_est=0,
        cache_hit=False,
        details=action_details,
    )
    clarify_required, clarify_question = _clarify_prompt_from_action(action)
    yield {
        "event": "done",
        "answer": answer,
        "sources": sources,
        "used_llm": used_llm,
        "model": used_model,
        "requested_model": requested_model,
        "model_selection": "explicit" if explicit_model else "auto",
        "model_fallback": bool(used_llm and requested_model and used_model and requested_model != used_model),
        "llm_backend": resolved_backend,
        "reasoning_effort": _reported_reasoning_effort(
            resolved_reasoning_effort,
            backend=resolved_backend,
            model_name=used_model or requested_model,
        ),
        "runtime_mode": resolved_runtime_mode,
        "error": error_msg,
        "indexed_files": indexed_files,
        "web_search": bool(web_search),
        "web_search_note": web_note,
        "live_log_chars": len(normalized_live_log_tail),
        "state_memory_chars": len(normalized_state_memory),
        "agent": resolved_agent,
        "execution_mode": resolved_mode,
        "allow_artifacts": bool(allow_artifacts),
        "action": action,
        "capabilities": capabilities,
        "trace": {
            "trace_id": trace_id,
            "steps": trace_steps,
        },
        "clarify_required": bool(clarify_required),
        "clarify_question": clarify_question,
    }
