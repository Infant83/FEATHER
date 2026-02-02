from __future__ import annotations

import hashlib
import re
import urllib.parse


def slugify_label(label: str, max_len: int = 48) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", label.strip().lower()).strip("_")
    if not cleaned:
        cleaned = "stage"
    return cleaned[:max_len]


def slugify_url(url: str, max_len: int = 80) -> str:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.replace("www.", "")
    path = parsed.path.strip("/").replace("/", "_")
    base = "_".join([part for part in (host, path) if part])
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", base).strip("_")
    if not cleaned:
        cleaned = "resource"
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    trimmed = cleaned[:max_len]
    return f"{trimmed}-{digest}" if digest else trimmed
