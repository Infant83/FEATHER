from pathlib import Path

from federlicht import report


def test_dedupe_repeated_prompt_content_collapses_repeated_blocks() -> None:
    text = (
        "Language: Korean\n\n"
        "Template: acs_review\n\n"
        "핵심 지시문 A\n\n"
        "핵심 지시문 B\n\n"
        "Language: Korean\n\n"
        "Template: acs_review\n\n"
        "핵심 지시문 A\n\n"
        "핵심 지시문 B\n"
    )
    deduped = report.dedupe_repeated_prompt_content(text)

    assert deduped.count("Language: Korean") == 1
    assert deduped.count("핵심 지시문 A") == 1


def test_load_report_prompt_dedupes_within_prompt_file(tmp_path: Path) -> None:
    prompt_path = tmp_path / "prompt.txt"
    prompt_path.write_text("Line A\n\nLine B\n\nLine A\n\nLine B\n", encoding="utf-8")

    loaded = report.load_report_prompt(None, str(prompt_path))

    assert loaded == "Line A\n\nLine B"


def test_find_instruction_file_prefers_base_instruction(tmp_path: Path) -> None:
    run_dir = tmp_path / "openclaw"
    instr = run_dir / "instruction"
    instr.mkdir(parents=True, exist_ok=True)
    (instr / "generated_prompt_openclaw.txt").write_text("generated", encoding="utf-8")
    (instr / "report_prompt_report_full.txt").write_text("report prompt", encoding="utf-8")
    expected = instr / "openclaw.txt"
    expected.write_text("base instruction", encoding="utf-8")

    resolved = report.find_instruction_file(run_dir)

    assert resolved == expected


def test_write_run_overview_uses_clickable_source_links(tmp_path: Path) -> None:
    run_dir = tmp_path / "runs" / "demo"
    instruction = run_dir / "instruction" / "demo.txt"
    index_file = run_dir / "archive" / "demo-index.md"
    instruction.parent.mkdir(parents=True, exist_ok=True)
    index_file.parent.mkdir(parents=True, exist_ok=True)
    instruction.write_text("demo instruction", encoding="utf-8")
    index_file.write_text("# index", encoding="utf-8")

    path = report.write_run_overview(run_dir, instruction, index_file)

    assert path is not None
    text = path.read_text(encoding="utf-8")
    assert "Source: [./instruction/demo.txt](./instruction/demo.txt)" in text
    assert "Source: [./archive/demo-index.md](./archive/demo-index.md)" in text


def test_write_report_overview_uses_clickable_prompt_links(tmp_path: Path) -> None:
    run_dir = tmp_path / "runs" / "demo"
    run_dir.mkdir(parents=True, exist_ok=True)
    output = run_dir / "report_full.html"
    output.write_text("<html></html>", encoding="utf-8")
    prompt_path = run_dir / "instruction" / "report_prompt_report_full.txt"
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text("prompt", encoding="utf-8")
    adjustment = run_dir / "report_notes" / "template_adjustment.txt"
    adjustment.parent.mkdir(parents=True, exist_ok=True)
    adjustment.write_text("adjust", encoding="utf-8")

    overview = report.write_report_overview(
        run_dir=run_dir,
        output_path=output,
        report_prompt="brief prompt",
        template_name="acs_review",
        template_adjustment_path=adjustment,
        output_format="html",
        language="ko",
        quality_iterations=1,
        quality_strategy="none",
        figures_enabled=False,
        figures_mode="none",
        prompt_path=prompt_path,
    )

    assert overview is not None
    text = overview.read_text(encoding="utf-8")
    assert "Source: [./instruction/report_prompt_report_full.txt](./instruction/report_prompt_report_full.txt)" in text
    assert "Source: [./report_notes/template_adjustment.txt](./report_notes/template_adjustment.txt)" in text
