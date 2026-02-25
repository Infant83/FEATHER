from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module():
    path = Path("tools/run_html_pdf_regression.py")
    spec = importlib.util.spec_from_file_location("run_html_pdf_regression", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tool = _load_module()


def test_evaluate_pdf_regression_checks_pass_without_baseline() -> None:
    checks = tool.evaluate_pdf_regression_checks(
        compile_ok=True,
        compile_message="",
        pdf_exists=True,
        pdf_bytes=120000,
        pdf_pages=3,
        min_bytes=10000,
        baseline=None,
    )
    assert isinstance(checks, list)
    assert checks
    assert all(bool(item.get("ok")) for item in checks)


def test_evaluate_pdf_regression_checks_detects_baseline_regression() -> None:
    checks = tool.evaluate_pdf_regression_checks(
        compile_ok=True,
        compile_message="",
        pdf_exists=True,
        pdf_bytes=40000,
        pdf_pages=8,
        min_bytes=10000,
        baseline={"pdf_bytes": 120000, "pdf_pages": 3},
        max_page_delta=1,
        max_bytes_regression_ratio=0.2,
    )
    failed = [item for item in checks if not bool(item.get("ok"))]
    assert failed
    names = {str(item.get("name")) for item in failed}
    assert "baseline_bytes_regression" in names
    assert "baseline_pages_delta" in names
