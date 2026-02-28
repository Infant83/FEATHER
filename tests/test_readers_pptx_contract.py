from __future__ import annotations

from types import SimpleNamespace
from pathlib import Path

import federlicht.readers.pptx as pptx_reader


class _Cell:
    def __init__(self, text: str) -> None:
        self.text = text


class _Row:
    def __init__(self, cells: list[str]) -> None:
        self.cells = [_Cell(cell) for cell in cells]


class _Table:
    def __init__(self, rows: list[list[str]]) -> None:
        self.rows = [_Row(row) for row in rows]


class _Series:
    def __init__(self, name: str, values: list[object]) -> None:
        self.name = name
        self.values = values


class _Chart:
    def __init__(self, title: str, series: list[_Series]) -> None:
        self.has_title = bool(title)
        self.chart_title = SimpleNamespace(text_frame=SimpleNamespace(text=title))
        self.series = series


class _Paragraph:
    def __init__(self, text: str, level: int = 0) -> None:
        self.text = text
        self.level = level


class _TextFrame:
    def __init__(self, paragraphs: list[_Paragraph]) -> None:
        self.paragraphs = paragraphs


class _Shape:
    def __init__(
        self,
        *,
        has_table: bool = False,
        has_chart: bool = False,
        has_text_frame: bool = False,
        table: _Table | None = None,
        chart: _Chart | None = None,
        text_frame: _TextFrame | None = None,
        shape_type: object = None,
        width: int = 0,
        height: int = 0,
    ) -> None:
        self.has_table = has_table
        self.has_chart = has_chart
        self.has_text_frame = has_text_frame
        self.table = table
        self.chart = chart
        self.text_frame = text_frame
        self.shape_type = shape_type
        self.width = width
        self.height = height


class _Shapes(list):
    def __init__(self, items: list[_Shape], title_text: str = "") -> None:
        super().__init__(items)
        self.title = SimpleNamespace(text=title_text) if title_text else None


class _Slide:
    def __init__(self, shapes: _Shapes, notes_text: str = "") -> None:
        self.shapes = shapes
        self.notes_slide = SimpleNamespace(notes_text_frame=SimpleNamespace(text=notes_text))


class _Presentation:
    def __init__(self, slides: list[_Slide]) -> None:
        self.slides = slides


def test_extract_pptx_slide_contract_returns_structured_elements(monkeypatch, tmp_path: Path) -> None:
    picture_type = "picture"
    slide = _Slide(
        _Shapes(
            [
                _Shape(
                    has_text_frame=True,
                    text_frame=_TextFrame([_Paragraph("Key finding"), _Paragraph("Detail", level=1)]),
                ),
                _Shape(
                    has_table=True,
                    table=_Table([["Metric", "Value"], ["Error", "0.1%"]]),
                ),
                _Shape(
                    has_chart=True,
                    chart=_Chart("Trend", [_Series("Series A", [1, 2, 3])]),
                ),
                _Shape(shape_type=picture_type, width=9525 * 200, height=9525 * 100),
            ],
            title_text="Slide Title",
        ),
        notes_text="Speaker note",
    )
    prs = _Presentation([slide, _Slide(_Shapes([], title_text="Second"))])
    monkeypatch.setattr(pptx_reader, "_pptx_available", lambda: True)
    monkeypatch.setattr(pptx_reader, "pptx", SimpleNamespace(Presentation=lambda _path: prs))
    monkeypatch.setattr(pptx_reader, "MSO_SHAPE_TYPE", SimpleNamespace(PICTURE=picture_type))

    source = tmp_path / "demo.pptx"
    source.write_text("x", encoding="utf-8")
    contract = pptx_reader.extract_pptx_slide_contract(source, tmp_path, max_slides=1)

    assert contract["schema_version"] == "pptx_ingest.v1"
    assert contract["available"] is True
    assert contract["slide_count_total"] == 2
    assert contract["extracted_slide_count"] == 1
    assert contract["truncated"] is True
    slides = contract["slides"]
    assert isinstance(slides, list) and slides
    first = slides[0]
    assert first["slide_id"] == "slide-001"
    elements = first["elements"]
    assert any(item.get("shape_type") == "text" for item in elements)
    assert any(item.get("shape_type") == "table" for item in elements)
    assert any(item.get("shape_type") == "chart" for item in elements)
    assert any(item.get("shape_type") == "picture" for item in elements)
    assert any(item.get("shape_type") == "notes" for item in elements)
    assert all(str(item.get("anchor") or "").startswith("./demo.pptx#slide-1") for item in elements)
    assert all(item.get("source_path") == "./demo.pptx" for item in elements)


def test_extract_pptx_slide_contract_handles_missing_dependency(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(pptx_reader, "_pptx_available", lambda: False)
    contract = pptx_reader.extract_pptx_slide_contract(tmp_path / "missing.pptx", tmp_path)
    assert contract["available"] is False
    assert "error" in contract
