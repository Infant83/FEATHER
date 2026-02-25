#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from federlicht import artwork as feder_artwork
from federlicht.quality_contract import (
    QUALITY_CONTRACT_METRIC_VERSION,
    detect_quality_contract_staleness,
)
from federlicht.quality_profiles import quality_profile_choices, resolve_quality_gate_targets

METRIC_FIELDS = (
    "overall",
    "claim_support_ratio",
    "unsupported_claim_count",
    "evidence_density_score",
    "section_coherence_score",
)


def _expand_input_patterns(patterns: list[str]) -> list[Path]:
    resolved: list[Path] = []
    seen: set[Path] = set()
    for token in patterns:
        raw = str(token or "").strip()
        if not raw:
            continue
        path = Path(raw)
        candidates: list[Path]
        if any(char in raw for char in ("*", "?", "[")):
            candidates = sorted(Path(".").glob(raw))
        else:
            candidates = [path]
        for candidate in candidates:
            final = candidate.resolve()
            if final in seen:
                continue
            seen.add(final)
            resolved.append(final)
    return resolved


def evaluate_infographic_lint(spec_paths: list[Path]) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for path in spec_paths:
        row: dict[str, object] = {
            "path": str(path),
            "exists": path.exists(),
            "issues": [],
        }
        if not path.exists():
            row["issues"] = ["spec file not found"]
            rows.append(row)
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except Exception as exc:
            row["issues"] = [f"json parse failed: {exc}"]
            rows.append(row)
            continue
        if not isinstance(payload, dict):
            row["issues"] = ["spec payload is not an object"]
            rows.append(row)
            continue
        issues = feder_artwork.lint_infographic_spec(payload)
        row["issues"] = list(issues)
        charts = payload.get("charts")
        row["chart_count"] = len(charts) if isinstance(charts, list) else 0
        rows.append(row)
    failed_rows = [item for item in rows if isinstance(item.get("issues"), list) and item.get("issues")]
    return {
        "checked_count": len(rows),
        "failed_count": len(failed_rows),
        "pass": len(failed_rows) == 0,
        "rows": rows,
    }


def _run_command(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=False, text=True, capture_output=True)


def _to_float(value: object, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def extract_quality_contract_metrics(contract_payload: dict) -> dict[str, float]:
    metric_source_name = str(contract_payload.get("metric_source") or "").strip().lower()
    selected_eval = contract_payload.get("selected_eval")
    final_signals = contract_payload.get("final_signals")
    metric_source: object
    if metric_source_name == "final_signals":
        metric_source = final_signals if isinstance(final_signals, dict) else selected_eval
    elif metric_source_name == "selected_eval":
        metric_source = selected_eval if isinstance(selected_eval, dict) else final_signals
    else:
        metric_source = selected_eval if isinstance(selected_eval, dict) else final_signals
    metric_source = metric_source if isinstance(metric_source, dict) else {}
    return {key: _to_float(metric_source.get(key), 0.0) for key in METRIC_FIELDS}


def build_quality_contract_consistency(
    summary_payload: dict,
    contract_payload: dict,
    *,
    expected_metric_version: str = QUALITY_CONTRACT_METRIC_VERSION,
    max_overall_delta: float = 2.5,
    max_claim_support_delta: float = 8.0,
    max_unsupported_delta: float = 8.0,
    max_evidence_density_delta: float = 8.0,
    max_section_coherence_delta: float = 8.0,
) -> dict:
    summary = dict(summary_payload.get("summary") or {})
    benchmark_metrics = {key: _to_float(summary.get(key), 0.0) for key in METRIC_FIELDS}
    stale, stale_reason = detect_quality_contract_staleness(
        contract_payload,
        expected_metric_version=expected_metric_version,
    )
    contract_metrics = extract_quality_contract_metrics(contract_payload)
    metric_source = str(contract_payload.get("metric_source") or "").strip() or (
        "selected_eval"
        if isinstance(contract_payload.get("selected_eval"), dict)
        else "final_signals"
    )
    metric_version = str(contract_payload.get("metric_version") or "").strip()
    if stale:
        return {
            "pass": True,
            "skipped": True,
            "stale": True,
            "stale_reason": stale_reason,
            "expected_metric_version": expected_metric_version,
            "metric_version": metric_version or "(missing)",
            "metric_source": metric_source,
            "benchmark_summary": benchmark_metrics,
            "quality_contract_metrics": contract_metrics,
            "delta": {key: 0.0 for key in METRIC_FIELDS},
            "abs_delta": {key: 0.0 for key in METRIC_FIELDS},
            "thresholds": {
                "overall": float(max_overall_delta),
                "claim_support_ratio": float(max_claim_support_delta),
                "unsupported_claim_count": float(max_unsupported_delta),
                "evidence_density_score": float(max_evidence_density_delta),
                "section_coherence_score": float(max_section_coherence_delta),
            },
            "failed_checks": [],
        }
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
    return {
        "pass": len(failed_checks) == 0,
        "skipped": False,
        "stale": False,
        "stale_reason": "",
        "expected_metric_version": expected_metric_version,
        "metric_version": metric_version or "(missing)",
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
    infographic_lint: dict | None = None,
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
                f"- skipped: {'YES' if contract_consistency.get('skipped') else 'NO'}",
                f"- stale: {'YES' if contract_consistency.get('stale') else 'NO'}",
                (
                    f"- stale_reason: {contract_consistency.get('stale_reason')}"
                    if contract_consistency.get("stale_reason")
                    else "- stale_reason: (none)"
                ),
                f"- metric_source: {contract_consistency.get('metric_source') or 'unknown'}",
                f"- metric_version: {contract_consistency.get('metric_version') or 'unknown'}",
                f"- expected_metric_version: {contract_consistency.get('expected_metric_version') or 'unknown'}",
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
    if isinstance(infographic_lint, dict):
        checked_count = int(infographic_lint.get("checked_count", 0) or 0)
        failed_count = int(infographic_lint.get("failed_count", 0) or 0)
        lint_pass = bool(infographic_lint.get("pass"))
        lines.extend(
            [
                "",
                "## Infographic Lint",
                f"- checked_specs: {checked_count}",
                f"- failed_specs: {failed_count}",
                f"- lint_result: {'PASS' if lint_pass else 'FAIL'}",
            ]
        )
        lint_rows = infographic_lint.get("rows")
        if isinstance(lint_rows, list) and lint_rows:
            lines.extend(
                [
                    "",
                    "| spec_path | chart_count | issues |",
                    "| --- | ---: | --- |",
                ]
            )
            for item in lint_rows:
                if not isinstance(item, dict):
                    continue
                path = str(item.get("path") or "").strip() or "(unknown)"
                chart_count = int(item.get("chart_count", 0) or 0)
                issues = item.get("issues")
                if isinstance(issues, list) and issues:
                    issue_text = "; ".join(str(issue) for issue in issues[:4])
                else:
                    issue_text = "-"
                lines.append(f"| {path} | {chart_count} | {issue_text} |")
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
        "--infographic-spec",
        action="append",
        default=[],
        help="Infographic spec JSON path or glob pattern (can be repeated).",
    )
    parser.add_argument(
        "--infographic-lint-output",
        default="",
        help="Optional JSON output path for infographic lint summary.",
    )
    parser.add_argument(
        "--strict-infographic-lint",
        action="store_true",
        help="Fail run when infographic lint finds any issues.",
    )
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
    parser.add_argument(
        "--quality-contract-metric-version",
        default=QUALITY_CONTRACT_METRIC_VERSION,
        help="Expected quality_contract metric version tag for consistency checks.",
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
    infographic_lint: dict | None = None
    infographic_lint_fail = False
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
                expected_metric_version=str(args.quality_contract_metric_version),
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
    if args.infographic_spec:
        spec_paths = _expand_input_patterns([str(item) for item in args.infographic_spec if str(item).strip()])
        infographic_lint = evaluate_infographic_lint(spec_paths)
        infographic_lint_fail = not bool(infographic_lint.get("pass"))
        if args.infographic_lint_output:
            output_path = Path(str(args.infographic_lint_output))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                json.dumps(infographic_lint, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"Wrote infographic lint summary: {output_path.as_posix()}")
        print(
            "infographic-lint | "
            f"checked={int(infographic_lint.get('checked_count', 0) or 0)} | "
            f"failed={int(infographic_lint.get('failed_count', 0) or 0)} | "
            f"result={'PASS' if bool(infographic_lint.get('pass')) else 'FAIL'}"
        )
    report_md = build_gate_report_markdown(
        summary_payload,
        gate_proc.stdout,
        gate_proc.returncode,
        contract_consistency=contract_consistency,
        gate_policy=gate_policy,
        infographic_lint=infographic_lint,
    )
    report_path = Path(args.report_md)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_md, encoding="utf-8")
    print(f"Wrote quality gate report: {report_path.as_posix()}")
    if gate_proc.returncode != 0:
        return gate_proc.returncode
    if bool(args.strict_contract_consistency) and contract_fail:
        return 2
    if bool(args.strict_infographic_lint) and infographic_lint_fail:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
