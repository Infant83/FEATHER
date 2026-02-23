#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from federlicht.quality_profiles import quality_profile_choices, resolve_quality_gate_targets

METRIC_FIELDS = (
    "overall",
    "claim_support_ratio",
    "unsupported_claim_count",
    "evidence_density_score",
    "section_coherence_score",
)


def _run_command(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=False, text=True, capture_output=True)


def _to_float(value: object, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def extract_quality_contract_metrics(contract_payload: dict) -> dict[str, float]:
    selected_eval = contract_payload.get("selected_eval")
    final_signals = contract_payload.get("final_signals")
    metric_source = selected_eval if isinstance(selected_eval, dict) else final_signals
    metric_source = metric_source if isinstance(metric_source, dict) else {}
    return {key: _to_float(metric_source.get(key), 0.0) for key in METRIC_FIELDS}


def build_quality_contract_consistency(
    summary_payload: dict,
    contract_payload: dict,
    *,
    max_overall_delta: float = 2.5,
    max_claim_support_delta: float = 8.0,
    max_unsupported_delta: float = 8.0,
    max_evidence_density_delta: float = 8.0,
    max_section_coherence_delta: float = 8.0,
) -> dict:
    summary = dict(summary_payload.get("summary") or {})
    benchmark_metrics = {key: _to_float(summary.get(key), 0.0) for key in METRIC_FIELDS}
    contract_metrics = extract_quality_contract_metrics(contract_payload)
    delta = {
        key: round(benchmark_metrics.get(key, 0.0) - contract_metrics.get(key, 0.0), 4)
        for key in METRIC_FIELDS
    }
    abs_delta = {key: round(abs(value), 4) for key, value in delta.items()}
    thresholds = {
        "overall": float(max_overall_delta),
        "claim_support_ratio": float(max_claim_support_delta),
        "unsupported_claim_count": float(max_unsupported_delta),
        "evidence_density_score": float(max_evidence_density_delta),
        "section_coherence_score": float(max_section_coherence_delta),
    }
    failed_checks = [
        f"{metric} abs_delta={abs_delta[metric]:.2f} > {thresholds[metric]:.2f}"
        for metric in METRIC_FIELDS
        if abs_delta[metric] > thresholds[metric]
    ]
    metric_source = (
        "selected_eval"
        if isinstance(contract_payload.get("selected_eval"), dict)
        else "final_signals"
    )
    return {
        "pass": len(failed_checks) == 0,
        "metric_source": metric_source,
        "benchmark_summary": benchmark_metrics,
        "quality_contract_metrics": contract_metrics,
        "delta": delta,
        "abs_delta": abs_delta,
        "thresholds": thresholds,
        "failed_checks": failed_checks,
    }


def build_gate_report_markdown(
    summary_payload: dict,
    gate_stdout: str,
    gate_rc: int,
    *,
    contract_consistency: dict | None = None,
    gate_policy: dict | None = None,
) -> str:
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
    ]
    if isinstance(gate_policy, dict):
        targets = dict(gate_policy.get("thresholds") or {})
        lines.extend(
            [
                f"- gate_profile: {gate_policy.get('profile') or 'none'}",
                f"- gate_effective_band: {gate_policy.get('effective_band') or 'custom'}",
                f"- gate_source: {gate_policy.get('source') or 'custom'}",
                f"- gate_targets: {targets}",
            ]
        )
    lines.extend(
        [
            "",
            "## Summary",
            f"- overall: {float(summary.get('overall', 0.0)):.2f}",
            f"- claim_support_ratio: {float(summary.get('claim_support_ratio', 0.0)):.2f}",
            f"- unsupported_claim_count: {float(summary.get('unsupported_claim_count', 0.0)):.2f}",
            f"- evidence_density_score: {float(summary.get('evidence_density_score', 0.0)):.2f}",
            f"- section_coherence_score: {float(summary.get('section_coherence_score', 0.0)):.2f}",
        ]
    )
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
    if isinstance(contract_consistency, dict):
        lines.extend(
            [
                "",
                "## Quality Contract Consistency",
                f"- pass: {'PASS' if contract_consistency.get('pass') else 'FAIL'}",
                f"- metric_source: {contract_consistency.get('metric_source') or 'unknown'}",
            ]
        )
        checks = contract_consistency.get("failed_checks")
        if isinstance(checks, list) and checks:
            lines.append("- failed_checks:")
            lines.extend(
                f"  - {item}" for item in checks if isinstance(item, str) and item.strip()
            )
        else:
            lines.append("- failed_checks: (none)")
        lines.extend(
            [
                "",
                "### Metric Delta (benchmark - quality_contract)",
                "| metric | benchmark | quality_contract | delta | abs_delta | threshold |",
                "| --- | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        benchmark_summary = contract_consistency.get("benchmark_summary") or {}
        contract_metrics = contract_consistency.get("quality_contract_metrics") or {}
        deltas = contract_consistency.get("delta") or {}
        abs_deltas = contract_consistency.get("abs_delta") or {}
        thresholds = contract_consistency.get("thresholds") or {}
        for metric in METRIC_FIELDS:
            lines.append(
                f"| {metric} | {float(benchmark_summary.get(metric, 0.0)):.2f} | "
                f"{float(contract_metrics.get(metric, 0.0)):.2f} | "
                f"{float(deltas.get(metric, 0.0)):+.2f} | "
                f"{float(abs_deltas.get(metric, 0.0)):.2f} | "
                f"{float(thresholds.get(metric, 0.0)):.2f} |"
            )
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
    parser.add_argument(
        "--quality-contract",
        default="",
        help="Optional quality_contract.latest.json path for metric consistency checks.",
    )
    parser.add_argument(
        "--contract-consistency-output",
        default="",
        help="Optional JSON output path for quality-contract consistency result.",
    )
    parser.add_argument(
        "--strict-contract-consistency",
        action="store_true",
        help="Fail run when quality_contract consistency check fails.",
    )
    parser.add_argument("--max-contract-overall-delta", type=float, default=2.5)
    parser.add_argument("--max-contract-claim-support-delta", type=float, default=8.0)
    parser.add_argument("--max-contract-unsupported-delta", type=float, default=8.0)
    parser.add_argument("--max-contract-evidence-density-delta", type=float, default=8.0)
    parser.add_argument("--max-contract-section-coherence-delta", type=float, default=8.0)
    parser.add_argument(
        "--quality-profile",
        default="baseline",
        choices=list(quality_profile_choices()),
        help=(
            "Gate threshold preset: none/smoke/baseline/professional/world_class "
            "(default: baseline)."
        ),
    )
    parser.add_argument("--min-overall", type=float, default=0.0)
    parser.add_argument("--min-claim-support", type=float, default=0.0)
    parser.add_argument("--max-unsupported", type=float, default=-1.0)
    parser.add_argument("--min-section-coherence", type=float, default=0.0)
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

    gate_policy = resolve_quality_gate_targets(
        profile=args.quality_profile,
        min_overall=float(args.min_overall),
        min_claim_support=float(args.min_claim_support),
        max_unsupported=float(args.max_unsupported),
        min_section_coherence=float(args.min_section_coherence),
    )
    gate_targets = dict(gate_policy.get("thresholds") or {})

    gate_cmd = [
        sys.executable,
        "tools/report_quality_regression_gate.py",
        "--input",
        str(args.summary_output),
        "--quality-profile",
        str(gate_policy.get("profile") or "none"),
        "--min-overall",
        str(float(gate_targets.get("min_overall", 0.0))),
        "--min-claim-support",
        str(float(gate_targets.get("min_claim_support", 0.0))),
        "--max-unsupported",
        str(float(gate_targets.get("max_unsupported", -1.0))),
        "--min-section-coherence",
        str(float(gate_targets.get("min_section_coherence", 0.0))),
    ]
    gate_proc = _run_command(gate_cmd)
    print(
        "gate-policy | "
        f"profile={gate_policy.get('profile')} | "
        f"effective_band={gate_policy.get('effective_band')} | "
        f"source={gate_policy.get('source')} | "
        f"targets={gate_targets}"
    )
    print(gate_proc.stdout, end="")
    if gate_proc.stderr:
        print(gate_proc.stderr, file=sys.stderr, end="")

    summary_payload = json.loads(Path(args.summary_output).read_text(encoding="utf-8"))
    contract_consistency: dict | None = None
    contract_fail = False
    quality_contract_path = Path(str(args.quality_contract or "").strip())
    if str(args.quality_contract or "").strip():
        if not quality_contract_path.exists():
            contract_consistency = {
                "pass": False,
                "metric_source": "missing",
                "benchmark_summary": {},
                "quality_contract_metrics": {},
                "delta": {},
                "abs_delta": {},
                "thresholds": {},
                "failed_checks": [f"quality_contract missing: {quality_contract_path.as_posix()}"],
            }
            contract_fail = True
        else:
            contract_payload = json.loads(quality_contract_path.read_text(encoding="utf-8"))
            contract_consistency = build_quality_contract_consistency(
                summary_payload,
                contract_payload if isinstance(contract_payload, dict) else {},
                max_overall_delta=float(args.max_contract_overall_delta),
                max_claim_support_delta=float(args.max_contract_claim_support_delta),
                max_unsupported_delta=float(args.max_contract_unsupported_delta),
                max_evidence_density_delta=float(args.max_contract_evidence_density_delta),
                max_section_coherence_delta=float(args.max_contract_section_coherence_delta),
            )
            contract_fail = not bool(contract_consistency.get("pass"))
        if args.contract_consistency_output:
            output_path = Path(str(args.contract_consistency_output))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                json.dumps(contract_consistency, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"Wrote quality contract consistency: {output_path.as_posix()}")
    report_md = build_gate_report_markdown(
        summary_payload,
        gate_proc.stdout,
        gate_proc.returncode,
        contract_consistency=contract_consistency,
        gate_policy=gate_policy,
    )
    report_path = Path(args.report_md)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_md, encoding="utf-8")
    print(f"Wrote quality gate report: {report_path.as_posix()}")
    if gate_proc.returncode != 0:
        return gate_proc.returncode
    if bool(args.strict_contract_consistency) and contract_fail:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
