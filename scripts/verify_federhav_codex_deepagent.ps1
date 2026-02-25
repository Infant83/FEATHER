param(
  [string]$RunRel = "site/runs/openclaw",
  [string]$Question = "run feather 실행해줘. openclaw run으로.",
  [string]$Model = "gpt-5.3-codex-spark",
  [int]$MaxSources = 4
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$oldGovernor = $env:FEDERHAV_GOVERNOR_MAX_ITER
$oldToolRounds = $env:FEDERLICHT_CODEX_TOOL_MAX_CALLS
$env:FEDERHAV_GOVERNOR_MAX_ITER = "1"
$env:FEDERLICHT_CODEX_TOOL_MAX_CALLS = "1"

try {
  $env:VERIFY_FH_QUESTION = $Question
  $env:VERIFY_FH_RUN_REL = $RunRel
  $env:VERIFY_FH_MODEL = $Model
  $env:VERIFY_FH_MAX_SOURCES = [string]$MaxSources
  $py = @"
import json
import os
import traceback
from pathlib import Path

from federnett.help_agent import answer_help_question

root = Path(".").resolve()
question = str(os.getenv("VERIFY_FH_QUESTION") or "run feather 실행해줘. openclaw run으로.")
run_rel = str(os.getenv("VERIFY_FH_RUN_REL") or "site/runs/openclaw")
model = str(os.getenv("VERIFY_FH_MODEL") or "gpt-5.3-codex-spark")
max_sources = int(str(os.getenv("VERIFY_FH_MAX_SOURCES") or "4"))

cases = [
    {"name": "deepagent_with_openai_key", "runtime_mode": "deepagent", "drop_openai_key": False},
    {"name": "deepagent_without_openai_key", "runtime_mode": "deepagent", "drop_openai_key": True},
    {"name": "auto_without_openai_key", "runtime_mode": "auto", "drop_openai_key": True},
]

reports = []

for case in cases:
    drop_key = bool(case["drop_openai_key"])
    previous_key = os.environ.pop("OPENAI_API_KEY", None) if drop_key else os.environ.get("OPENAI_API_KEY")
    try:
        result = answer_help_question(
            root,
            question,
            llm_backend="codex_cli",
            runtime_mode=case["runtime_mode"],
            execution_mode="act",
            allow_artifacts=False,
            model=model,
            run_rel=run_rel,
            max_sources=max_sources,
        )
        action = result.get("action") if isinstance(result.get("action"), dict) else {}
        handoff = action.get("execution_handoff") if isinstance(action, dict) else {}
        governor = handoff.get("governor_loop") if isinstance(handoff, dict) else {}
        reports.append(
            {
                "case": case["name"],
                "runtime_mode_requested": case["runtime_mode"],
                "openai_key_present_before": bool(previous_key),
                "openai_key_present_during": bool(os.getenv("OPENAI_API_KEY")),
                "llm_backend": result.get("llm_backend"),
                "runtime_mode_reported": result.get("runtime_mode"),
                "used_llm": bool(result.get("used_llm")),
                "model": result.get("model"),
                "error": str(result.get("error") or ""),
                "action_type": action.get("type") if isinstance(action, dict) else "",
                "action_planner": action.get("planner") if isinstance(action, dict) else "",
                "has_governor_loop": isinstance(governor, dict) and bool(governor),
            }
        )
    except Exception as exc:
        reports.append(
            {
                "case": case["name"],
                "runtime_mode_requested": case["runtime_mode"],
                "openai_key_present_before": bool(previous_key),
                "openai_key_present_during": bool(os.getenv("OPENAI_API_KEY")),
                "error": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc(limit=2),
            }
        )
    finally:
        if drop_key and previous_key is not None:
            os.environ["OPENAI_API_KEY"] = previous_key

print(json.dumps({"reports": reports}, ensure_ascii=False, indent=2))
"@

  $tmp = New-TemporaryFile
  Set-Content -Path $tmp -Value $py -Encoding UTF8
  python $tmp
  Remove-Item $tmp -ErrorAction SilentlyContinue
  Remove-Item Env:VERIFY_FH_QUESTION -ErrorAction SilentlyContinue
  Remove-Item Env:VERIFY_FH_RUN_REL -ErrorAction SilentlyContinue
  Remove-Item Env:VERIFY_FH_MODEL -ErrorAction SilentlyContinue
  Remove-Item Env:VERIFY_FH_MAX_SOURCES -ErrorAction SilentlyContinue
}
finally {
  if ($null -ne $oldGovernor) { $env:FEDERHAV_GOVERNOR_MAX_ITER = $oldGovernor } else { Remove-Item Env:FEDERHAV_GOVERNOR_MAX_ITER -ErrorAction SilentlyContinue }
  if ($null -ne $oldToolRounds) { $env:FEDERLICHT_CODEX_TOOL_MAX_CALLS = $oldToolRounds } else { Remove-Item Env:FEDERLICHT_CODEX_TOOL_MAX_CALLS -ErrorAction SilentlyContinue }
}
