#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def _run_command(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=False, text=True, capture_output=True)


def build_gate_report_markdown(summary_payload: dict, gate_stdout: str, gate_rc: int) -> str:
    summary = dict(summary_payload.get("summary") or {})
    baseline = dict(summary_payload.get("baseline_summary") or {})
    delta = dict(summary_payload.get("delta_summary") or {})
    suite = dict(summary_payload.get("suite") or {})
    lines = [
        "# Report Quality Gate Result",
        "",
        f"- gate_result: {'PASS' if gate_rc == 0 else 'FAIL'} (rc={gate_rc})",
        f"- suite: {suite.get('suite_id') or '(none)'}",
        f"- rows_count: {summary_payload.get('rows_count')}",
        "",
        "## Summary",
        f"- overall: {float(summary.get('overall', 0.0)):.2f}",
        f"- claim_support_ratio: {float(summary.get('claim_support_ratio', 0.0)):.2f}",
        f"- unsupported_claim_count: {float(summary.get('unsupported_claim_count', 0.0)):.2f}",
        f"- evidence_density_score: {float(summary.get('evidence_density_score', 0.0)):.2f}",
        f"- section_coherence_score: {float(summary.get('section_coherence_score', 0.0)):.2f}",
    ]
    if baseline:
        lines.extend(
            [
                "",
                "## Baseline",
                f"- overall: {float(baseline.get('overall', 0.0)):.2f}",
                f"- claim_support_ratio: {float(baseline.get('claim_support_ratio', 0.0)):.2f}",
                f"- unsupported_claim_count: {float(baseline.get('unsupported_claim_count', 0.0)):.2f}",
                f"- evidence_density_score: {float(baseline.get('evidence_density_score', 0.0)):.2f}",
                f"- section_coherence_score: {float(baseline.get('section_coherence_score', 0.0)):.2f}",
            ]
        )
    if delta:
        lines.extend(
            [
                "",
                "## Delta (current - baseline)",
                f"- overall: {float(delta.get('overall', 0.0)):+.2f}",
                f"- claim_support_ratio: {float(delta.get('claim_support_ratio', 0.0)):+.2f}",
                f"- unsupported_claim_count: {float(delta.get('unsupported_claim_count', 0.0)):+.2f}",
                f"- evidence_density_score: {float(delta.get('evidence_density_score', 0.0)):+.2f}",
                f"- section_coherence_score: {float(delta.get('section_coherence_score', 0.0)):+.2f}",
            ]
        )
    compare_md = str(summary_payload.get("compare_markdown") or "").strip()
    if compare_md:
        lines.extend(["", "## Compare Table", compare_md])
    lines.extend(["", "## Gate Output", "```text", (gate_stdout or "").strip(), "```"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run benchmark + regression gate and emit markdown report.")
    parser.add_argument("--input", nargs="+", required=True, help="Report path(s) or glob pattern(s).")
    parser.add_argument("--suite", default="", help="Optional benchmark suite JSON path.")
    parser.add_argument("--baseline", default="", help="Optional baseline benchmark JSON path.")
    parser.add_argument(
        "--required-sections",
        default="Executive Summary,Scope & Methodology,Key Findings,Risks & Gaps",
    )
    parser.add_argument("--depth", default="deep")
    parser.add_argument("--intent", default="research")
    parser.add_argument("--summary-output", required=True, help="Benchmark summary JSON output path.")
    parser.add_argument("--benchmark-output", default="", help="Optional benchmark row JSON output path.")
    parser.add_argument("--report-md", required=True, help="Markdown gate report output path.")
    parser.add_argument("--min-overall", type=float, default=70.0)
    parser.add_argument("--min-claim-support", type=float, default=40.0)
    parser.add_argument("--max-unsupported", type=float, default=25.0)
    parser.add_argument("--min-section-coherence", type=float, default=60.0)
    args = parser.parse_args()

    benchmark_cmd = [
        sys.executable,
        "tools/report_quality_benchmark.py",
        "--input",
        *[str(item) for item in args.input],
        "--required-sections",
        str(args.required_sections),
        "--depth",
        str(args.depth),
        "--intent",
        str(args.intent),
        "--summary-output",
        str(args.summary_output),
    ]
    if args.suite:
        benchmark_cmd.extend(["--suite", str(args.suite)])
    if args.baseline:
        benchmark_cmd.extend(["--baseline", str(args.baseline)])
    if args.benchmark_output:
        benchmark_cmd.extend(["--output", str(args.benchmark_output)])
    bench_proc = _run_command(benchmark_cmd)
    print(bench_proc.stdout, end="")
    if bench_proc.stderr:
        print(bench_proc.stderr, file=sys.stderr, end="")
    if bench_proc.returncode != 0:
        return bench_proc.returncode

    gate_cmd = [
        sys.executable,
        "tools/report_quality_regression_gate.py",
        "--input",
        str(args.summary_output),
        "--min-overall",
        str(float(args.min_overall)),
        "--min-claim-support",
        str(float(args.min_claim_support)),
        "--max-unsupported",
        str(float(args.max_unsupported)),
        "--min-section-coherence",
        str(float(args.min_section_coherence)),
    ]
    gate_proc = _run_command(gate_cmd)
    print(gate_proc.stdout, end="")
    if gate_proc.stderr:
        print(gate_proc.stderr, file=sys.stderr, end="")

    summary_payload = json.loads(Path(args.summary_output).read_text(encoding="utf-8"))
    report_md = build_gate_report_markdown(summary_payload, gate_proc.stdout, gate_proc.returncode)
    report_path = Path(args.report_md)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_md, encoding="utf-8")
    print(f"Wrote quality gate report: {report_path.as_posix()}")
    return gate_proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
