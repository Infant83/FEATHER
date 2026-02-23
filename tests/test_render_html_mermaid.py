from __future__ import annotations

import html

from federlicht.render.html import transform_mermaid_code_blocks


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
