from __future__ import annotations

from pathlib import Path
from typing import Any

from .utils import resolve_under_root, safe_rel


def list_templates(root: Path, run: str | None = None, include_site: bool = True) -> list[str]:
    templates_dir = root / "src" / "federlicht" / "templates"
    names: list[str] = []
    if templates_dir.exists():
        names.extend(sorted(p.stem for p in templates_dir.glob("*.md")))
    if include_site:
        site_dir = root / "site" / "custom_templates"
        if site_dir.exists():
            names.extend(safe_rel(p, root) for p in site_dir.glob("*.md"))
    if run:
        run_dir = resolve_under_root(root, run)
        if run_dir:
            custom_dir = run_dir / "custom_templates"
            if custom_dir.exists():
                names.extend(safe_rel(p, root) for p in custom_dir.glob("*.md"))
    return sorted(dict.fromkeys(names))


def list_template_styles(root: Path, run: str | None = None, include_site: bool = True) -> list[str]:
    styles_dir = root / "src" / "federlicht" / "templates" / "styles"
    items: list[str] = []
    if styles_dir.exists():
        items.extend(sorted(p.name for p in styles_dir.glob("*.css")))
    if include_site:
        site_dir = root / "site" / "custom_templates"
        if site_dir.exists():
            items.extend(safe_rel(p, root) for p in site_dir.glob("*.css"))
    if run:
        run_dir = resolve_under_root(root, run)
        if run_dir:
            custom_dir = run_dir / "custom_templates"
            if custom_dir.exists():
                items.extend(safe_rel(p, root) for p in custom_dir.glob("*.css"))
    return sorted(dict.fromkeys(items))


def read_template_style(root: Path, name: str) -> dict[str, Any]:
    styles_dir = root / "src" / "federlicht" / "templates" / "styles"
    if not styles_dir.exists():
        raise ValueError("Template styles directory not found.")
    cleaned = Path(name).name if "/" not in name else name
    if not cleaned:
        raise ValueError("Style name is required.")
    if not cleaned.endswith(".css"):
        cleaned = f"{cleaned}.css"
    if "/" in cleaned:
        path = resolve_under_root(root, cleaned)
        if not path:
            raise ValueError("Invalid style path.")
    else:
        path = (styles_dir / cleaned).resolve()
    if not path.exists():
        raise ValueError(f"Style not found: {cleaned}")
    return {
        "name": path.name,
        "path": safe_rel(path, root),
        "content": path.read_text(encoding="utf-8", errors="replace"),
    }


def _parse_template_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {"meta": {}, "sections": [], "guides": {}, "writer_guidance": []}
    _, raw = text.split("---", 1)
    front, *_ = raw.split("---", 1)
    lines = [line.rstrip() for line in front.splitlines() if line.strip()]
    meta: dict[str, str] = {}
    sections: list[str] = []
    guides: dict[str, str] = {}
    writer_guidance: list[str] = []
    for line in lines:
        if ":" not in line:
            continue
        key, value = [chunk.strip() for chunk in line.split(":", 1)]
        if not key:
            continue
        if key == "section":
            sections.append(value)
        elif key.startswith("guide "):
            guides[key[len("guide ") :].strip()] = value
        elif key == "writer_guidance":
            writer_guidance.append(value)
        else:
            meta[key] = value
    return {
        "meta": meta,
        "sections": sections,
        "guides": guides,
        "writer_guidance": writer_guidance,
    }


def _resolve_template_path(root: Path, name: str) -> Path:
    if "/" in name or name.endswith(".md"):
        path = resolve_under_root(root, name)
        if not path:
            raise ValueError(f"Template not found: {name}")
        return path
    return root / "src" / "federlicht" / "templates" / f"{name}.md"


def template_details(root: Path, name: str) -> dict[str, Any]:
    path = _resolve_template_path(root, name)
    if not path.exists():
        raise ValueError(f"Template not found: {name}")
    parsed = _parse_template_frontmatter(path)
    meta = dict(parsed["meta"])
    if "name" not in meta:
        meta["name"] = path.stem
    return {
        "name": meta.get("name", name),
        "path": safe_rel(path, root),
        "meta": meta,
        "sections": parsed["sections"],
        "guides": parsed["guides"],
        "writer_guidance": parsed["writer_guidance"],
    }
