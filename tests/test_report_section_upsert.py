from federlicht import report


def test_upsert_named_section_md_replaces_existing_section() -> None:
    src = """
## Executive Summary
old summary

## Key Findings
old findings
"""
    out = report.upsert_named_section(src, "md", "Key Findings", "new findings from repair")
    assert "new findings from repair" in out
    assert "old findings" not in out


def test_upsert_named_section_md_appends_when_missing() -> None:
    src = """
## Executive Summary
summary text
"""
    out = report.upsert_named_section(src, "md", "Risks & Gaps", "remaining uncertainty")
    assert "## Risks & Gaps" in out
    assert "remaining uncertainty" in out


def test_upsert_named_section_html_replaces_h2_block() -> None:
    src = "<h2>Executive Summary</h2><p>summary</p><h2>Key Findings</h2><p>old</p>"
    out = report.upsert_named_section(src, "html", "Key Findings", "new html block")
    assert "<h2>Key Findings</h2>" in out
    assert "new html block" in out
    assert "<p>old</p>" not in out


def test_upsert_named_section_tex_replaces_section() -> None:
    src = "\\section{Executive Summary}\nold\n\n\\section{Key Findings}\nlegacy"
    out = report.upsert_named_section(src, "tex", "Key Findings", "fresh tex findings")
    assert "\\section{Key Findings}" in out
    assert "fresh tex findings" in out
    assert "legacy" not in out
