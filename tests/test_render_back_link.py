from __future__ import annotations

from federlicht.render.html import wrap_html


def test_render_viewer_html_back_link_prefers_run_relative_report_hub() -> None:
    html = wrap_html("Sample", "<h2>Body</h2><p>Text</p>")
    assert "../../report_hub/index.html" in html
    assert "/site/report_hub/index.html" in html
    assert "const canProbe = String(window.location.protocol || '').startsWith('http');" in html
