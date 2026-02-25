from __future__ import annotations

import sys
import types
from pathlib import Path

from federlicht import report


def _write_html(path: Path) -> None:
    path.write_text("<!doctype html><html><body><h1>Demo</h1></body></html>", encoding="utf-8")


def test_compile_html_to_pdf_engine_none_disables_export(tmp_path: Path) -> None:
    html_path = tmp_path / "report_full.html"
    _write_html(html_path)

    ok, used_engine, message = report.compile_html_to_pdf(html_path, engine="none")

    assert ok is False
    assert used_engine == "none"
    assert "disabled" in message.lower()


def test_compile_html_to_pdf_auto_falls_back_to_next_engine(monkeypatch, tmp_path: Path) -> None:
    html_path = tmp_path / "report_full.html"
    pdf_path = tmp_path / "report_full.pdf"
    _write_html(html_path)
    calls: list[str] = []

    def fake_playwright(_html: Path, _pdf: Path, **_kwargs) -> tuple[bool, str]:
        calls.append("playwright")
        return False, "playwright unavailable"

    def fake_chrome(_html: Path, target_pdf: Path, **_kwargs) -> tuple[bool, str]:
        calls.append("chrome")
        target_pdf.write_bytes(b"%PDF-1.4\n")
        return True, ""

    def fake_weasy(_html: Path, _pdf: Path, **_kwargs) -> tuple[bool, str]:
        calls.append("weasyprint")
        return False, "should not run"

    monkeypatch.setattr(report, "_compile_html_to_pdf_playwright", fake_playwright)
    monkeypatch.setattr(report, "_compile_html_to_pdf_chrome", fake_chrome)
    monkeypatch.setattr(report, "_compile_html_to_pdf_weasyprint", fake_weasy)

    ok, used_engine, message = report.compile_html_to_pdf(
        html_path,
        pdf_path=pdf_path,
        engine="auto",
        wait_ms=0,
        timeout_sec=10,
    )

    assert ok is True
    assert used_engine == "chrome"
    assert message == ""
    assert calls == ["playwright", "chrome"]


def test_compile_html_to_pdf_specific_engine_does_not_try_others(monkeypatch, tmp_path: Path) -> None:
    html_path = tmp_path / "report_full.html"
    pdf_path = tmp_path / "report_full.pdf"
    _write_html(html_path)
    calls: list[str] = []

    def fake_chrome(_html: Path, _pdf: Path, **_kwargs) -> tuple[bool, str]:
        calls.append("chrome")
        return False, "should not run"

    def fake_weasy(_html: Path, target_pdf: Path, **_kwargs) -> tuple[bool, str]:
        calls.append("weasyprint")
        target_pdf.write_bytes(b"%PDF-1.4\n")
        return True, ""

    monkeypatch.setattr(report, "_compile_html_to_pdf_chrome", fake_chrome)
    monkeypatch.setattr(report, "_compile_html_to_pdf_weasyprint", fake_weasy)

    ok, used_engine, _message = report.compile_html_to_pdf(
        html_path,
        pdf_path=pdf_path,
        engine="weasyprint",
        wait_ms=0,
        timeout_sec=10,
    )

    assert ok is True
    assert used_engine == "weasyprint"
    assert calls == ["weasyprint"]


def test_inspect_pdf_artifact_reports_size_without_parser(tmp_path: Path) -> None:
    pdf_path = tmp_path / "demo.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\nminimal")

    info = report.inspect_pdf_artifact(pdf_path)

    assert int(info.get("pdf_bytes", 0)) > 0


def test_inspect_pdf_artifact_reports_pages_when_fitz_available(monkeypatch, tmp_path: Path) -> None:
    pdf_path = tmp_path / "demo.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\nminimal")

    class _FakeDoc:
        page_count = 7

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    fake_fitz = types.SimpleNamespace(open=lambda _path: _FakeDoc())
    monkeypatch.setitem(sys.modules, "fitz", fake_fitz)

    info = report.inspect_pdf_artifact(pdf_path)

    assert info.get("pdf_pages") == 7


def test_wait_for_playwright_render_settle_reports_ready() -> None:
    class _FakePage:
        def __init__(self) -> None:
            self._count = 0

        def evaluate(self, _script: str) -> dict[str, object]:
            self._count += 1
            return {
                "ready": self._count >= 2,
                "signature": "stable-signature",
                "dom_ready": True,
                "fonts_ready": True,
                "images_pending": 0,
                "iframe_pending": 0,
                "canvas_total": 1,
                "chart_ready_flag": True,
            }

        def wait_for_timeout(self, _ms: int) -> None:
            return None

    ok, reason = report._wait_for_playwright_render_settle(_FakePage(), timeout_ms=1200)

    assert ok is True
    assert reason == ""


def test_wait_for_playwright_render_settle_times_out() -> None:
    class _FakePage:
        def evaluate(self, _script: str) -> dict[str, object]:
            return {
                "ready": False,
                "signature": "moving",
                "dom_ready": False,
                "fonts_ready": False,
                "images_pending": 1,
                "iframe_pending": 1,
                "canvas_total": 1,
                "chart_ready_flag": False,
            }

        def wait_for_timeout(self, _ms: int) -> None:
            return None

    ok, reason = report._wait_for_playwright_render_settle(_FakePage(), timeout_ms=900)

    assert ok is False
    assert "render_settle_timeout" in reason
