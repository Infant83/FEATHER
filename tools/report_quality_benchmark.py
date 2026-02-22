#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path
from typing import Iterable

from federlicht import report as report_mod

METRIC_FIELDS = (
    "overall",
    "claim_support_ratio",
    "unsupported_claim_count",
    "evidence_density_score",
    "section_coherence_score",
)


def _collect_files(patterns: list[str]) -> list[Path]:
    out: list[Path] = []
    seen: set[str] = set()
    for pattern in patterns:
        if not pattern:
            continue
        if any(token in pattern for token in ("*", "?")):
            for raw_path in glob.glob(pattern):
                path = Path(raw_path)
                if path.is_file():
                    key = str(path.resolve())
                    if key not in seen:
                        seen.add(key)
                        out.append(path)
            continue
        path = Path(pattern)
        if path.is_file():
            key = str(path.resolve())
            if key not in seen:
                seen.add(key)
                out.append(path)
    return out


def _to_float(value: object, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _infer_format(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".html":
        return "html"
    if suffix == ".tex":
        return "tex"
    return "md"


def _run_benchmark(
    files: Iterable[Path],
    *,
    required_sections: list[str],
    depth: str,
    report_intent: str,
) -> list[dict]:
    rows: list[dict] = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        output_format = _infer_format(path)
        signals = report_mod.compute_heuristic_quality_signals(
            text,
            required_sections,
            output_format,
            depth=depth,
            report_intent=report_intent,
        )
        rows.append(
            {
                "path": path.as_posix(),
                "format": output_format,
                "overall": signals.get("overall", 0.0),
                "claim_support_ratio": signals.get("claim_support_ratio", 0.0),
                "unsupported_claim_count": signals.get("unsupported_claim_count", 0.0),
                "evidence_density_score": signals.get("evidence_density_score", 0.0),
                "section_coherence_score": signals.get("section_coherence_score", 0.0),
                "signals": signals,
            }
        )
    return rows


def _compute_summary(rows: list[dict]) -> dict[str, float]:
    if not rows:
        return {field: 0.0 for field in METRIC_FIELDS}
    count = float(len(rows))
    return {
        field: round(sum(_to_float(row.get(field), 0.0) for row in rows) / count, 4)
        for field in METRIC_FIELDS
    }


def _load_rows(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        rows = payload.get("rows")
        if isinstance(rows, list):
            return [item for item in rows if isinstance(item, dict)]
    return []


def _print_table(rows: list[dict]) -> dict[str, float]:
    if not rows:
        print("No report files matched.")
        return _compute_summary(rows)
    print("path | overall | claim_support | unsupported | evidence_density | section_coherence")
    print("--- | ---: | ---: | ---: | ---: | ---:")
    for row in rows:
        print(
            f"{row['path']} | "
            f"{float(row.get('overall', 0.0)):.2f} | "
            f"{float(row.get('claim_support_ratio', 0.0)):.2f} | "
            f"{float(row.get('unsupported_claim_count', 0.0)):.1f} | "
            f"{float(row.get('evidence_density_score', 0.0)):.2f} | "
            f"{float(row.get('section_coherence_score', 0.0)):.2f}"
        )
    summary = _compute_summary(rows)
    print("")
    print(
        "avg | "
        f"{summary['overall']:.2f} | "
        f"{summary['claim_support_ratio']:.2f} | "
        f"{summary['unsupported_claim_count']:.2f} | "
        f"{summary['evidence_density_score']:.2f} | "
        f"{summary['section_coherence_score']:.2f}"
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run heuristic report-quality benchmark on local report files.")
    parser.add_argument(
        "--input",
        nargs="+",
        required=True,
        help="Report files or glob patterns (e.g. site/runs/*/report_full*.html).",
    )
    parser.add_argument(
        "--required-sections",
        default="Executive Summary,Scope & Methodology,Key Findings,Risks & Gaps",
        help="Comma-separated required sections for coverage scoring.",
    )
    parser.add_argument("--depth", default="deep", help="Quality depth hint (brief/normal/deep/exhaustive).")
    parser.add_argument(
        "--intent",
        default="research",
        help="Report intent hint (research/review/decision/briefing/slide/explainer).",
    )
    parser.add_argument("--output", default="", help="Optional JSON output path.")
    parser.add_argument("--summary-output", default="", help="Optional JSON path for summary and delta metadata.")
    parser.add_argument(
        "--baseline",
        default="",
        help="Optional baseline benchmark JSON path. Prints avg delta(current-baseline).",
    )
    args = parser.parse_args()

    files = _collect_files(args.input)
    required_sections = [item.strip() for item in str(args.required_sections).split(",") if item.strip()]
    rows = _run_benchmark(
        files,
        required_sections=required_sections,
        depth=str(args.depth or "deep"),
        report_intent=str(args.intent or "research"),
    )
    summary = _print_table(rows)
    baseline_summary: dict[str, float] | None = None
    delta_summary: dict[str, float] | None = None
    if args.baseline:
        baseline_rows = _load_rows(Path(args.baseline))
        baseline_summary = _compute_summary(baseline_rows)
        delta_summary = {
            key: round(summary.get(key, 0.0) - baseline_summary.get(key, 0.0), 4)
            for key in METRIC_FIELDS
        }
        print("")
        print(
            "delta(current-baseline) | "
            f"overall={delta_summary['overall']:+.2f} | "
            f"claim_support={delta_summary['claim_support_ratio']:+.2f} | "
            f"unsupported={delta_summary['unsupported_claim_count']:+.2f} | "
            f"evidence_density={delta_summary['evidence_density_score']:+.2f} | "
            f"section_coherence={delta_summary['section_coherence_score']:+.2f}"
        )
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote benchmark: {output_path.as_posix()}")
    if args.summary_output:
        summary_path = Path(args.summary_output)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        bundle = {
            "rows_count": len(rows),
            "summary": summary,
            "baseline_summary": baseline_summary,
            "delta_summary": delta_summary,
            "required_sections": required_sections,
            "depth": str(args.depth or "deep"),
            "intent": str(args.intent or "research"),
        }
        summary_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote benchmark summary: {summary_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
