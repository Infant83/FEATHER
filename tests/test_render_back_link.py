from __future__ import annotations

from federlicht.render.html import normalize_html_print_profile, wrap_html


def test_render_viewer_html_back_link_prefers_run_relative_report_hub() -> None:
    html = wrap_html("Sample", "<h2>Body</h2><p>Text</p>")
    assert "../../report_hub/index.html" in html
    assert "/site/report_hub/index.html" in html
    assert "const canProbe = String(window.location.protocol || '').startsWith('http');" in html
    assert "@media print" in html
    assert "size: A4;" in html


def test_wrap_html_print_profile_letter_includes_letter_page_size() -> None:
    html = wrap_html("Sample", "<p>Body</p>", print_profile="letter")
    assert "size: Letter;" in html


def test_normalize_html_print_profile_defaults_to_a4() -> None:
    assert normalize_html_print_profile(None) == "a4"
    assert normalize_html_print_profile("off") == "screen"
