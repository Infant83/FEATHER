#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


def _to_bool(value: object) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    token = str(value).strip().lower()
    if not token:
        return None
    if token in {"1", "true", "yes", "on", "y"}:
        return True
    if token in {"0", "false", "no", "off", "n"}:
        return False
    return None


def _to_int(value: object) -> int | None:
    if value is None:
        return None
    try:
        return int(str(value).strip())
    except Exception:
        return None


def _to_float(value: object) -> float | None:
    if value is None:
        return None
    try:
        return float(str(value).strip())
    except Exception:
        return None


def _normalize_item(item: dict[str, Any]) -> tuple[dict[str, Any], dict[str, int]]:
    row = dict(item)
    stats = {
        "fallback_deck_html": 0,
        "fallback_deck_pptx": 0,
        "quality_promoted": 0,
        "quality_from_legacy_flat": 0,
        "tags_enriched": 0,
    }
    paths_raw = row.get("paths")
    paths = dict(paths_raw) if isinstance(paths_raw, dict) else {}
    report_path = str(paths.get("report") or "").strip()
    fmt = str(row.get("format") or "").strip().lower()
    if not str(paths.get("deck_html") or "").strip():
        if fmt == "pptx" and report_path.lower().endswith(".html"):
            paths["deck_html"] = report_path
            stats["fallback_deck_html"] += 1
    if not str(paths.get("deck_pptx") or "").strip():
        if fmt == "pptx" and report_path.lower().endswith(".pptx"):
            paths["deck_pptx"] = report_path
            stats["fallback_deck_pptx"] += 1
    if paths:
        row["paths"] = paths

    raw_quality = row.get("deck_quality")
    quality = dict(raw_quality) if isinstance(raw_quality, dict) else {}
    had_quality = bool(quality)

    profile = str(quality.get("profile") or row.get("deck_quality_profile") or "").strip()
    effective_band = str(quality.get("effective_band") or row.get("deck_quality_effective_band") or "").strip()
    overall = _to_float(quality.get("overall"))
    if overall is None:
        overall = _to_float(row.get("deck_quality_overall"))
    gate_pass = _to_bool(quality.get("gate_pass"))
    if gate_pass is None:
        gate_pass = _to_bool(row.get("deck_quality_gate_pass"))
    iterations = _to_int(quality.get("iterations"))
    if iterations is None:
        iterations = _to_int(row.get("deck_quality_iterations"))

    normalized_quality: dict[str, Any] = {}
    if profile:
        normalized_quality["profile"] = profile
    if effective_band:
        normalized_quality["effective_band"] = effective_band
    if overall is not None:
        normalized_quality["overall"] = overall
    if gate_pass is not None:
        normalized_quality["gate_pass"] = gate_pass
    if iterations is not None:
        normalized_quality["iterations"] = iterations

    if normalized_quality:
        row["deck_quality"] = normalized_quality
        stats["quality_promoted"] += 1
        if not had_quality:
            stats["quality_from_legacy_flat"] += 1

    tags_raw = row.get("tags")
    tags = [str(item).strip() for item in tags_raw if str(item).strip()] if isinstance(tags_raw, list) else []
    tag_set = set(tags)
    quality_for_tags = row.get("deck_quality") if isinstance(row.get("deck_quality"), dict) else {}
    band_for_tag = str(
        quality_for_tags.get("effective_band") or quality_for_tags.get("profile") or ""
    ).strip()
    gate_for_tag = _to_bool(quality_for_tags.get("gate_pass"))
    derived: list[str] = []
    if band_for_tag:
        derived.append(f"deck:{band_for_tag}")
    if gate_for_tag is True:
        derived.append("deck-pass")
    elif gate_for_tag is False:
        derived.append("deck-fail")
    for token in derived:
        if token not in tag_set:
            tags.append(token)
            tag_set.add(token)
            stats["tags_enriched"] += 1
    if tags:
        row["tags"] = tags
    return row, stats


def normalize_manifest_payload(payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, int]]:
    items_raw = payload.get("items")
    items = list(items_raw) if isinstance(items_raw, list) else []
    normalized_items: list[dict[str, Any]] = []
    stats = {
        "item_count": 0,
        "fallback_deck_html": 0,
        "fallback_deck_pptx": 0,
        "quality_promoted": 0,
        "quality_from_legacy_flat": 0,
        "tags_enriched": 0,
    }
    for raw in items:
        if not isinstance(raw, dict):
            continue
        normalized, row_stats = _normalize_item(raw)
        normalized_items.append(normalized)
        stats["item_count"] += 1
        for key, value in row_stats.items():
            stats[key] = int(stats.get(key, 0) or 0) + int(value or 0)

    out = dict(payload)
    out["items"] = normalized_items
    stamp = dt.datetime.now().isoformat()
    out["generated_at"] = stamp
    out["revision"] = stamp
    return out, stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize report_hub manifest for deck companion paths and quality metadata.")
    parser.add_argument("--hub-root", default="site/report_hub", help="Hub root containing manifest.json (default: site/report_hub)")
    parser.add_argument("--manifest", default="", help="Explicit manifest path override")
    parser.add_argument("--output", default="", help="Optional output manifest path (default: overwrite input when --write)")
    parser.add_argument("--summary-output", default="", help="Optional JSON summary output path")
    parser.add_argument("--write", action="store_true", help="Write normalized manifest to file")
    args = parser.parse_args()

    manifest_path = Path(str(args.manifest).strip()) if str(args.manifest).strip() else Path(str(args.hub_root)) / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"manifest not found: {manifest_path.as_posix()}")
    payload = json.loads(manifest_path.read_text(encoding="utf-8", errors="replace"))
    if not isinstance(payload, dict):
        raise SystemExit("manifest payload must be a JSON object with an items array")

    normalized, stats = normalize_manifest_payload(payload)
    out_path = Path(str(args.output).strip()) if str(args.output).strip() else manifest_path

    if args.write:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote normalized manifest: {out_path.as_posix()}")
    else:
        print("Dry-run mode: normalized payload computed (use --write to persist).")

    summary = {
        "manifest_input": manifest_path.as_posix(),
        "manifest_output": out_path.as_posix(),
        "write": bool(args.write),
        "stats": stats,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if str(args.summary_output).strip():
        summary_path = Path(str(args.summary_output).strip())
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote normalize summary: {summary_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

