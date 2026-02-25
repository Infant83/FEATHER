#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

from federlicht import report


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run HTML->PDF export and evaluate basic regression checks (size/pages/baseline delta).",
    )
    parser.add_argument("--html", required=True, help="Input HTML path.")
    parser.add_argument("--output-pdf", help="Output PDF path (default: <html>.pdf).")
    parser.add_argument("--summary-output", required=True, help="Summary JSON output path.")
    parser.add_argument("--engine", default="auto", help="PDF engine (auto/playwright/chrome/weasyprint/wkhtmltopdf/none).")
    parser.add_argument("--print-profile", default="a4", help="Print profile (a4/letter/screen).")
    parser.add_argument("--wait-ms", type=int, default=1500, help="Extra wait before capture (ms).")
    parser.add_argument("--timeout-sec", type=int, default=120, help="Timeout per engine attempt (sec).")
    parser.add_argument("--baseline-summary", help="Optional previous summary JSON for regression comparison.")
    parser.add_argument("--max-page-delta", type=int, default=1, help="Allowed absolute page-count delta vs baseline.")
    parser.add_argument(
        "--max-bytes-regression-ratio",
        type=float,
        default=0.35,
        help="Allowed relative byte-size drop vs baseline (0.35 means up to -35%%).",
    )
    parser.add_argument("--min-bytes", type=int, default=10_000, help="Minimum expected PDF bytes.")
    return parser.parse_args(argv)


def evaluate_pdf_regression_checks(
    *,
    compile_ok: bool,
    compile_message: str,
    pdf_exists: bool,
    pdf_bytes: int,
    pdf_pages: int,
    min_bytes: int,
    baseline: dict[str, Any] | None = None,
    max_page_delta: int = 1,
    max_bytes_regression_ratio: float = 0.35,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add_check(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "ok": bool(passed), "detail": detail})

    add_check("compile_success", bool(compile_ok and pdf_exists), compile_message or ("ok" if compile_ok else "compile failed"))
    add_check("minimum_bytes", int(pdf_bytes) >= int(min_bytes), f"bytes={int(pdf_bytes)}, min={int(min_bytes)}")
    add_check("nonzero_pages", int(pdf_pages) > 0, f"pages={int(pdf_pages)}")

    payload = dict(baseline or {})
    baseline_bytes = int(payload.get("pdf_bytes", 0) or 0)
    baseline_pages = int(payload.get("pdf_pages", 0) or 0)
    if baseline_bytes > 0:
        min_allowed_bytes = int(round(baseline_bytes * (1.0 - max(0.0, float(max_bytes_regression_ratio)))))
        add_check(
            "baseline_bytes_regression",
            int(pdf_bytes) >= min_allowed_bytes,
            f"bytes={int(pdf_bytes)}, baseline={baseline_bytes}, min_allowed={min_allowed_bytes}",
        )
    if baseline_pages > 0:
        page_delta = abs(int(pdf_pages) - baseline_pages)
        add_check(
            "baseline_pages_delta",
            page_delta <= max(0, int(max_page_delta)),
            f"pages={int(pdf_pages)}, baseline={baseline_pages}, delta={page_delta}",
        )
    return checks


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    html_path = Path(args.html).resolve()
    pdf_path = Path(args.output_pdf).resolve() if args.output_pdf else html_path.with_suffix(".pdf")
    summary_path = Path(args.summary_output).resolve()

    ok, used_engine, message = report.compile_html_to_pdf(
        html_path,
        pdf_path=pdf_path,
        engine=str(args.engine or "auto"),
        print_profile=str(args.print_profile or "a4"),
        wait_ms=max(0, int(args.wait_ms or 0)),
        timeout_sec=max(5, int(args.timeout_sec or 0)),
    )
    artifact = report.inspect_pdf_artifact(pdf_path) if pdf_path.exists() else {}
    pdf_bytes = int(artifact.get("pdf_bytes", 0) or 0)
    pdf_pages = int(artifact.get("pdf_pages", 0) or 0)

    baseline_path = Path(args.baseline_summary).resolve() if args.baseline_summary else None
    baseline: dict[str, Any] = _load_json(baseline_path) if baseline_path and baseline_path.exists() else {}
    checks = evaluate_pdf_regression_checks(
        compile_ok=bool(ok),
        compile_message=str(message or ""),
        pdf_exists=pdf_path.exists(),
        pdf_bytes=pdf_bytes,
        pdf_pages=pdf_pages,
        min_bytes=int(args.min_bytes),
        baseline=baseline,
        max_page_delta=int(args.max_page_delta),
        max_bytes_regression_ratio=float(args.max_bytes_regression_ratio),
    )

    failed = [item for item in checks if not bool(item.get("ok"))]
    status = "PASS" if not failed else "FAIL"
    summary = {
        "status": status,
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "input_html": str(html_path),
        "output_pdf": str(pdf_path),
        "engine_requested": str(args.engine or "auto"),
        "engine_used": used_engine,
        "ok": bool(ok),
        "message": message,
        "pdf_bytes": pdf_bytes,
        "pdf_pages": pdf_pages,
        "baseline_summary": str(baseline_path) if baseline_path else None,
        "checks": checks,
    }
    _write_json(summary_path, summary)

    print(f"HTML PDF regression status={status} engine={used_engine} bytes={pdf_bytes} pages={pdf_pages}")
    if failed:
        for item in failed:
            print(f"- FAIL {item.get('name')}: {item.get('detail')}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
