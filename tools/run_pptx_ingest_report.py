#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from federlicht.readers.pptx import extract_pptx_slide_contract


def _build_markdown(payload: dict) -> str:
    slides = [item for item in list(payload.get("slides") or []) if isinstance(item, dict)]
    lines = [
        "# PPTX Ingest Report",
        "",
        f"- schema_version: {payload.get('schema_version') or 'unknown'}",
        f"- source_path: {payload.get('source_path') or '(unknown)'}",
        f"- available: {bool(payload.get('available'))}",
        f"- slide_count_total: {int(payload.get('slide_count_total') or 0)}",
        f"- extracted_slide_count: {int(payload.get('extracted_slide_count') or 0)}",
        f"- truncated: {bool(payload.get('truncated'))}",
        "",
        "## Slides",
    ]
    if not slides:
        lines.append("- (none)")
        return "\n".join(lines) + "\n"
    for slide in slides:
        elements = [item for item in list(slide.get("elements") or []) if isinstance(item, dict)]
        lines.extend(
            [
                f"### {slide.get('slide_id') or '(slide)'}",
                f"- title: {slide.get('slide_title') or '(untitled)'}",
                f"- anchor: {slide.get('anchor') or '(none)'}",
                f"- elements: {len(elements)}",
            ]
        )
        for element in elements[:10]:
            lines.append(
                f"  - {element.get('element_id')}: "
                f"{element.get('shape_type')}/{element.get('content_kind')} @ {element.get('anchor')}"
            )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract a structured PPTX ingest contract and optional markdown report.")
    parser.add_argument("--input", required=True, help="Input .pptx path")
    parser.add_argument("--run-dir", default=".", help="Run root for relative source paths (default: current directory)")
    parser.add_argument("--output-json", required=True, help="Output contract JSON path")
    parser.add_argument("--output-md", default="", help="Optional markdown summary output path")
    parser.add_argument("--max-slides", type=int, default=0, help="Max slides to read (0=all)")
    parser.add_argument("--start-slide", type=int, default=0, help="0-based start slide index")
    parser.add_argument("--no-notes", action="store_true", help="Exclude speaker notes from contract")
    parser.add_argument("--max-text-chars-per-shape", type=int, default=500)
    args = parser.parse_args()

    input_path = Path(str(args.input)).resolve()
    run_dir = Path(str(args.run_dir)).resolve()
    contract = extract_pptx_slide_contract(
        input_path,
        run_dir,
        max_slides=int(args.max_slides),
        start_slide=int(args.start_slide),
        include_notes=not bool(args.no_notes),
        max_text_chars_per_shape=int(args.max_text_chars_per_shape),
    )

    out_json = Path(str(args.output_json))
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(contract, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote pptx ingest contract: {out_json.as_posix()}")

    if str(args.output_md).strip():
        out_md = Path(str(args.output_md))
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(_build_markdown(contract), encoding="utf-8")
        print(f"Wrote pptx ingest markdown: {out_md.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

