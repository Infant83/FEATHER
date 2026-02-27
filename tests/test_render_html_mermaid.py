from __future__ import annotations

import html

from federlicht.render.html import markdown_to_html, transform_mermaid_code_blocks


def test_transform_mermaid_quotes_flowchart_labels_with_parentheses() -> None:
    body = (
        '<pre><code class="language-mermaid">'
        "flowchart LR\n"
        "A[compile (routing)] --> B[test]\n"
        "</code></pre>"
    )
    transformed, has_mermaid = transform_mermaid_code_blocks(body)
    assert has_mermaid is True
    decoded = html.unescape(transformed)
    assert 'A["compile (routing)"] --> B["test"]' in decoded


def test_transform_mermaid_keeps_timeline_unchanged() -> None:
    body = (
        '<pre><code class="language-mermaid">'
        "timeline\n"
        "  2024 : milestone\n"
        "</code></pre>"
    )
    transformed, has_mermaid = transform_mermaid_code_blocks(body)
    assert has_mermaid is True
    decoded = html.unescape(transformed)
    assert "timeline" in decoded
    assert "2024 : milestone" in decoded


def test_transform_mermaid_detects_existing_mermaid_div_blocks() -> None:
    body = (
        "<figure>"
        '<div class="mermaid">'
        "flowchart LR\n"
        "A[first pass] --> B[second pass]\n"
        "</div>"
        "</figure>"
    )
    transformed, has_mermaid = transform_mermaid_code_blocks(body)
    assert has_mermaid is True
    decoded = html.unescape(transformed)
    assert 'A["first pass"] --> B["second pass"]' in decoded
    assert 'class="mermaid"' in transformed


def test_transform_mermaid_converts_raw_fenced_blocks_in_html_payload() -> None:
    body = (
        "<section>\n"
        "```mermaid\n"
        "flowchart LR\n"
        "A[collect] --> B[write]\n"
        "```\n"
        "</section>"
    )
    transformed, has_mermaid = transform_mermaid_code_blocks(body)
    assert has_mermaid is True
    decoded = html.unescape(transformed)
    assert "<figure" in transformed
    assert 'A["collect"] --> B["write"]' in decoded


def test_markdown_to_html_unwraps_section_blocks_for_heading_parsing() -> None:
    markdown = (
        "<section>\n"
        "### Scope\n"
        "본문 설명.\n"
        "</section>\n"
    )
    rendered = markdown_to_html(markdown)
    assert "<h3>Scope</h3>" in rendered
