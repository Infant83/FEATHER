#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from federlicht import report as report_mod
from federlicht.quality_profiles import QUALITY_PROFILES, resolve_quality_gate_targets


PROFILES = ("smoke", "baseline", "professional", "world_class")


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _load_summary(path: Path) -> dict[str, float]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        summary = payload.get("summary")
        if isinstance(summary, dict):
            return {
                "overall": _to_float(summary.get("overall"), 0.0),
                "claim_support_ratio": _to_float(summary.get("claim_support_ratio"), 0.0),
                "unsupported_claim_count": _to_float(summary.get("unsupported_claim_count"), 0.0),
                "section_coherence_score": _to_float(summary.get("section_coherence_score"), 0.0),
            }
    if isinstance(payload, list) and payload:
        rows = [item for item in payload if isinstance(item, dict)]
        if rows:
            n = float(len(rows))
            return {
                "overall": sum(_to_float(r.get("overall"), 0.0) for r in rows) / n,
                "claim_support_ratio": sum(_to_float(r.get("claim_support_ratio"), 0.0) for r in rows) / n,
                "unsupported_claim_count": sum(_to_float(r.get("unsupported_claim_count"), 0.0) for r in rows) / n,
                "section_coherence_score": sum(_to_float(r.get("section_coherence_score"), 0.0) for r in rows) / n,
            }
    raise ValueError("input must be benchmark summary bundle or benchmark row list JSON")


def evaluate_profiles(summary: dict[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for profile in PROFILES:
        policy = resolve_quality_gate_targets(profile=profile)
        targets = dict(policy.get("thresholds") or {})
        failures = report_mod.quality_gate_failures(
            summary,
            min_overall=float(targets.get("min_overall", 0.0)),
            min_claim_support=float(targets.get("min_claim_support", 0.0)),
            max_unsupported=float(targets.get("max_unsupported", -1.0)),
            min_section_coherence=float(targets.get("min_section_coherence", 0.0)),
        )
        rows.append(
            {
                "profile": profile,
                "label": QUALITY_PROFILES[profile].label,
                "pass": len(failures) == 0,
                "targets": targets,
                "failures": failures,
            }
        )
    return rows


def render_markdown(summary: dict[str, float], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Quality Profile Compare",
        "",
        "## Summary",
        f"- overall: {summary['overall']:.2f}",
        f"- claim_support_ratio: {summary['claim_support_ratio']:.2f}",
        f"- unsupported_claim_count: {summary['unsupported_claim_count']:.2f}",
        f"- section_coherence_score: {summary['section_coherence_score']:.2f}",
        "",
        "## Profile Matrix",
        "| profile | pass | min_overall | min_claim_support | max_unsupported | min_section_coherence |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        targets = row["targets"]
        lines.append(
            f"| {row['profile']} | {'PASS' if row['pass'] else 'FAIL'} | "
            f"{float(targets.get('min_overall', 0.0)):.1f} | "
            f"{float(targets.get('min_claim_support', 0.0)):.1f} | "
            f"{float(targets.get('max_unsupported', -1.0)):.1f} | "
            f"{float(targets.get('min_section_coherence', 0.0)):.1f} |"
        )
    lines.append("")
    lines.append("## Failure Details")
    for row in rows:
        lines.append(f"- {row['profile']}: {'PASS' if row['pass'] else '; '.join(row['failures'])}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare one benchmark summary against all quality profiles.")
    parser.add_argument("--input", required=True, help="Benchmark summary JSON or benchmark rows JSON.")
    parser.add_argument("--output-json", default="", help="Optional output JSON path.")
    parser.add_argument("--output-md", default="", help="Optional output markdown path.")
    args = parser.parse_args()

    summary = _load_summary(Path(args.input))
    rows = evaluate_profiles(summary)

    print("profile | pass | failures")
    print("--- | --- | ---")
    for row in rows:
        print(f"{row['profile']} | {'PASS' if row['pass'] else 'FAIL'} | {', '.join(row['failures']) or '-'}")

    if args.output_json:
        out_json = Path(args.output_json)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(
            json.dumps({"summary": summary, "profiles": rows}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Wrote profile compare JSON: {out_json.as_posix()}")
    if args.output_md:
        out_md = Path(args.output_md)
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(render_markdown(summary, rows), encoding="utf-8")
        print(f"Wrote profile compare MD: {out_md.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

