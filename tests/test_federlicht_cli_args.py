import pytest

from federlicht import cli_args, report


def test_report_parse_args_matches_cli_args() -> None:
    argv = [
        "--run",
        "sample_run",
        "--output",
        "report_full.md",
        "--no-stream",
        "--max-tool-chars",
        "24000",
        "--temperature-level",
        "balanced",
    ]
    via_report = report.parse_args(argv)
    direct = cli_args.parse_args(argv)
    assert vars(via_report) == vars(direct)


def test_temperature_override_flag_removed() -> None:
    with pytest.raises(SystemExit):
        cli_args.parse_args(["--run", "sample_run", "--temperature", "0.5"])


def test_quality_profile_arg_parses() -> None:
    args = cli_args.parse_args(
        [
            "--run",
            "sample_run",
            "--output",
            "report_full.md",
            "--quality-profile",
            "deep_research",
        ]
    )
    assert args.quality_profile == "deep_research"


def test_quality_profile_legacy_world_class_alias_maps_to_deep_research() -> None:
    args = cli_args.parse_args(
        [
            "--run",
            "sample_run",
            "--output",
            "report_full.md",
            "--quality-profile",
            "world_class",
        ]
    )
    assert args.quality_profile == "deep_research"


def test_reasoning_effort_aliases_normal_and_extended() -> None:
    args_normal = cli_args.parse_args(
        [
            "--run",
            "sample_run",
            "--output",
            "report_full.md",
            "--reasoning-effort",
            "normal",
        ]
    )
    args_extended = cli_args.parse_args(
        [
            "--run",
            "sample_run",
            "--output",
            "report_full.md",
            "--reasoning-effort",
            "extended",
        ]
    )
    assert args_normal.reasoning_effort == "medium"
    assert args_extended.reasoning_effort == "high"
