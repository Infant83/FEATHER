from __future__ import annotations

from federlicht import report


def test_normalize_style_pack() -> None:
    assert report.normalize_style_pack("dark") == "dark"
    assert report.normalize_style_pack("JOURNAL") == "journal"
    assert report.normalize_style_pack("none") == "none"
    assert report.normalize_style_pack("off") == "none"
    assert report.normalize_style_pack("unknown-pack") == "none"


def test_resolve_style_pack_css_path() -> None:
    css_path = report.resolve_style_pack_css_path("magazine")
    assert css_path is not None
    assert css_path.name == "style_pack_magazine.css"
    assert css_path.exists()
