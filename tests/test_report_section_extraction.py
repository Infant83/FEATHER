from __future__ import annotations

from federlicht import report


def test_extract_named_section_md_returns_body() -> None:
    text = """
## Executive Summary
summary text

## Key Findings
finding line A
finding line B
"""
    out = report.extract_named_section(text, "md", "Key Findings")
    assert out is not None
    assert "finding line A" in out


def test_extract_named_section_html_returns_body() -> None:
    html = """
<h2>Executive Summary</h2><p>summary</p>
<h2>Key Findings</h2><p>evidence-backed finding</p>
"""
    out = report.extract_named_section(html, "html", "Key Findings")
    assert out is not None
    assert "evidence-backed finding" in out

