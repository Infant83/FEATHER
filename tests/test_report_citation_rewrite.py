from federlicht import report


def test_rewrite_citations_keeps_unicode_archive_path() -> None:
    text = "핵심 근거는 [./archive/동영상생성AI-index.md]에 정리되어 있습니다."
    rewritten, refs = report.rewrite_citations(text, output_format="md")

    assert refs
    assert refs[0]["kind"] == "path"
    assert refs[0]["target"] == "./archive/동영상생성AI-index.md"
    assert "[\\[1\\]](./archive/동영상생성AI-index.md)" in rewritten


def test_rewrite_citations_detects_unicode_bare_path() -> None:
    text = "근거 파일: ./archive/동영상생성AI-index.md."
    rewritten, refs = report.rewrite_citations(text, output_format="md")

    assert refs
    assert refs[0]["target"] == "./archive/동영상생성AI-index.md"
    assert rewritten.endswith(".")


def test_linkify_html_does_not_nest_archive_anchor() -> None:
    html = "<p>Tavily search index (./archive/tavily_search.jsonl) - selected sources</p>"
    linked = report.linkify_html(html)

    assert linked.count('href="./archive/tavily_search.jsonl"') == 1
    assert "&lt;a href=" not in linked


def test_linkify_html_supports_unicode_archive_path() -> None:
    html = "<p>근거 경로: ./archive/동영상생성AI-index.md</p>"
    linked = report.linkify_html(html)

    assert 'href="./archive/동영상생성AI-index.md"' in linked


def test_scrub_internal_index_mentions_rewrites_plain_filename() -> None:
    text = "근거는 tavily_search.jsonl 과 source_index.jsonl에서 확인했다."
    cleaned = report.scrub_internal_index_mentions(text)

    assert "tavily_search.jsonl" not in cleaned
    assert "source_index.jsonl" not in cleaned
    assert "웹 검색 인덱스" in cleaned
    assert "소스 인덱스" in cleaned


def test_scrub_internal_index_mentions_keeps_citation_path() -> None:
    text = "핵심 인용 [./archive/tavily_search.jsonl]"
    cleaned = report.scrub_internal_index_mentions(text)

    assert "[./archive/tavily_search.jsonl]" in cleaned


def test_report_prompt_block_keeps_section_even_without_prompt() -> None:
    block = report.format_report_prompt_block(None, output_format="md")

    assert "## Report Prompt" in block
    assert "No report prompt provided." in block


def test_reference_section_policy_is_plain_text_not_blockquote() -> None:
    rendered = report.render_reference_section(
        citations=[{"index": 1, "kind": "url", "target": "https://example.com"}],
        refs_meta=[],
        openalex_meta={},
        output_format="md",
        text_meta_index={},
    )

    assert "## References" in rendered
    assert "Citation policy:" in rendered
    assert "> Citation policy" not in rendered


def test_smooth_writer_meta_labels_removes_inline_and_prefix_tags() -> None:
    text = "- (해석) 이 문장은 의미를 전달한다. 다음 문장도 자연스럽다. (리스크)"
    cleaned = report.smooth_writer_meta_labels(text)

    assert "(해석)" not in cleaned
    assert "(리스크)" not in cleaned
    assert "이 문장은 의미를 전달한다." in cleaned
