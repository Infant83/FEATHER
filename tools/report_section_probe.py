#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from federlicht import report as report_mod


def _infer_format(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".html":
        return "html"
    if suffix == ".tex":
        return "tex"
    return "md"


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract and quality-probe a single section from a report.")
    parser.add_argument("--report", required=True, help="Report path (.md/.html/.tex).")
    parser.add_argument("--section", required=True, help="Section title to extract.")
    parser.add_argument("--format", default="auto", help="Output format override: auto|md|html|tex")
    parser.add_argument("--depth", default="deep", help="Quality depth hint.")
    parser.add_argument("--intent", default="research", help="Report intent hint.")
    parser.add_argument("--output", default="", help="Optional JSON output path.")
    args = parser.parse_args()

    report_path = Path(args.report)
    output_format = _infer_format(report_path) if str(args.format).lower() == "auto" else str(args.format).lower()
    text = report_path.read_text(encoding="utf-8", errors="replace")
    section_body = report_mod.extract_named_section(text, output_format, str(args.section))
    if not section_body:
        print(f"section-not-found | {args.section}")
        return 1
    signals = report_mod.compute_heuristic_quality_signals(
        section_body,
        [str(args.section)],
        output_format if output_format in {"md", "html", "tex"} else "md",
        depth=str(args.depth or "deep"),
        report_intent=str(args.intent or "research"),
    )
    payload = {
        "report": report_path.as_posix(),
        "section": str(args.section),
        "format": output_format,
        "signals": signals,
        "excerpt": section_body[:2400],
    }
    print(f"section | {args.section}")
    print(json.dumps(signals, ensure_ascii=False))
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"wrote | {output_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

