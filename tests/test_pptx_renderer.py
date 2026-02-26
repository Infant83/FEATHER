from __future__ import annotations

from typing import Any
from pathlib import Path

import federlicht.pptx_renderer as renderer
import federlicht.slide_pipeline as slide_pipeline


def _sample_slide_ast() -> dict:
    outline = slide_pipeline.build_slide_outline(
        report_prompt="Build a compact operational briefing.",
        target_slide_count=4,
    )
    return slide_pipeline.build_slide_ast(outline, style_pack="default")


def test_render_slide_ast_html_writes_file(tmp_path: Path) -> None:
    slide_ast = _sample_slide_ast()
    out_html = tmp_path / "deck.html"
    result = renderer.render_slide_ast_html(slide_ast, output_html=out_html, deck_title="Demo Deck")
    assert result["ok"] is True
    assert out_html.exists()
    text = out_html.read_text(encoding="utf-8")
    assert "Demo Deck" in text
    assert "SLIDE-01" in text


def test_render_slide_ast_pptx_handles_missing_dependency(tmp_path: Path, monkeypatch) -> None:
    slide_ast = _sample_slide_ast()
    out_pptx = tmp_path / "deck.pptx"
    monkeypatch.setattr(renderer, "_pptx_available", lambda: False)
    result = renderer.render_slide_ast_pptx(slide_ast, output_pptx=out_pptx)
    assert result["ok"] is False
    assert result["reason"] == "python-pptx not installed"
    assert out_pptx.exists() is False


def test_render_slide_ast_bundle_generates_html_and_reports_pptx_status(tmp_path: Path, monkeypatch) -> None:
    slide_ast = _sample_slide_ast()
    monkeypatch.setattr(renderer, "_pptx_available", lambda: False)
    result = renderer.render_slide_ast_bundle(
        slide_ast,
        output_dir=tmp_path,
        deck_id="qc_brief",
        deck_title="QC Brief",
        export_html=True,
        export_pptx=True,
    )
    html_result = dict(result.get("html") or {})
    pptx_result = dict(result.get("pptx") or {})
    assert html_result.get("ok") is True
    assert (tmp_path / "qc_brief.html").exists()
    assert pptx_result.get("ok") is False
    assert pptx_result.get("reason") == "python-pptx not installed"


def test_render_slide_ast_bundle_materializes_mermaid_snapshot(tmp_path: Path, monkeypatch) -> None:
    slide_ast = {
        "schema_version": "slide_ast.v1",
        "slides": [
            {
                "slide_id": "SLIDE-01",
                "layout": "title_two_column",
                "title_block": {"headline": "Diagram Slide", "subheadline": "Methodology"},
                "body_blocks": [
                    {"type": "text", "text": "Workflow overview."},
                    {"type": "diagram", "engine": "mermaid", "spec": "flowchart LR\nA-->B"},
                ],
                "citation_footer": {"refs": [], "source_policy": "claim-evidence-source"},
            }
        ],
    }

    def fake_mermaid(run_dir: Path, diagram_source: str, **kwargs: Any) -> dict[str, str]:
        output_rel = str(kwargs.get("output_rel_path") or "deck_assets/demo.svg")
        out_abs = run_dir / output_rel
        out_abs.parent.mkdir(parents=True, exist_ok=True)
        out_abs.write_text("<svg></svg>", encoding="utf-8")
        return {"ok": "true", "path": f"./{output_rel}", "format": "svg"}

    monkeypatch.setattr(renderer.artwork, "render_mermaid_diagram", fake_mermaid)
    monkeypatch.setattr(renderer, "_pptx_available", lambda: False)
    result = renderer.render_slide_ast_bundle(
        slide_ast,
        output_dir=tmp_path,
        deck_id="diagram_demo",
        export_html=True,
        export_pptx=False,
    )
    assert int(result.get("diagram_snapshot_count") or 0) == 1
    paths = [str(item) for item in list(result.get("diagram_snapshot_paths") or []) if str(item).strip()]
    assert paths
    snapshot_abs = tmp_path / paths[0]
    assert snapshot_abs.exists()
    html_text = (tmp_path / "diagram_demo.html").read_text(encoding="utf-8")
    assert "diagram snapshot" in html_text.lower()
    assert paths[0] in html_text
