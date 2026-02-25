from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
import re
from pathlib import Path

from federnett.filesystem import clear_help_history

from .core import FederHavChatConfig, ask_question, normalize_run_relpath, stream_question


def _configure_stdio_utf8() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            continue


def _resolve_run_dir(run: str) -> Path:
    path = Path(run).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    return path.resolve()


def _next_update_path(run_dir: Path) -> Path:
    notes_dir = run_dir / "report_notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d")
    base = notes_dir / f"update_request_{stamp}.txt"
    if not base.exists():
        return base
    idx = 1
    while True:
        candidate = notes_dir / f"update_request_{stamp}_{idx}.txt"
        if not candidate.exists():
            return candidate
        idx += 1


def _build_update_prompt(base_report: str, update: str, second: str | None) -> str:
    lines = [f"Base report: {base_report}", "", "Update request:"]
    if update:
        lines.append(update.strip())
    if second:
        lines.append("")
        lines.append("Second prompt:")
        lines.append(second.strip())
    return "\n".join(lines).strip() + "\n"


def _default_output(run_dir: Path) -> Path:
    return run_dir / "report_full.html"


def _coerce_command_argv(argv: list[str]) -> list[str]:
    if not argv:
        return ["chat"]
    if argv[0] in {"-h", "--help"}:
        return argv
    first = str(argv[0]).strip().lower()
    if first in {"chat", "update"}:
        return argv
    legacy_update_flags = {"--base-report", "--update", "--second", "--template", "--agent-profile", "--lang"}
    if any(token in legacy_update_flags for token in argv):
        return ["update", *argv]
    return ["chat", *argv]


def _sanitize_profile_token(raw: str | None) -> str:
    token = str(raw or "").strip()
    cleaned = "".join(ch for ch in token if ch.isalnum() or ch in {"_", "-"})
    return cleaned[:80]


def _sanitize_agent_token(raw: str | None) -> str:
    token = str(raw or "").strip()
    cleaned = "".join(ch for ch in token if ch.isalnum() or ch in {"_", "-", "."})
    return cleaned[:80]


def _parse_prefixed_mode_question(line: str) -> tuple[str | None, str]:
    text = str(line or "").strip()
    if not text.startswith("/"):
        return None, text
    match = re.match(r"^/(plan|act)\b(?:\s+(.*))?$", text, flags=re.IGNORECASE)
    if not match:
        return None, text
    mode = str(match.group(1) or "").strip().lower()
    question = str(match.group(2) or "").strip()
    return mode, question


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="FederHav CLI: interactive operator chat + report update runner.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    chat = sub.add_parser("chat", help="Interactive FederHav chat (uses federnett.help_agent core).")
    chat.add_argument("--root", default=".", help="Workspace root (default: current directory).")
    chat.add_argument("--run", help="Run folder hint/path (optional).")
    chat.add_argument("--profile-id", default="default", help="History profile id (default: default).")
    chat.add_argument("--agent", default="federhav", help="FederHav operator agent label/id (default: federhav).")
    chat.add_argument(
        "--execution-mode",
        choices=["plan", "act"],
        default="plan",
        help="Execution policy for orchestration responses (default: plan).",
    )
    chat.add_argument(
        "--allow-artifacts",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Allow side-effectful artifact write actions in Act mode (default: false).",
    )
    chat.add_argument("--model", help="Model override (optional).")
    chat.add_argument("--llm-backend", choices=["openai_api", "codex_cli"], help="LLM backend override.")
    chat.add_argument(
        "--reasoning-effort",
        choices=["off", "low", "medium", "high", "extra_high"],
        help="Reasoning effort override.",
    )
    chat.add_argument(
        "--runtime-mode",
        choices=["auto", "deepagent", "off"],
        default="auto",
        help="FederHav runtime mode (default: auto).",
    )
    chat.add_argument(
        "--strict-model",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Fail instead of fallback when explicit model cannot be used.",
    )
    chat.add_argument(
        "--web-search",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Enable web search augmentation.",
    )
    chat.add_argument("--max-sources", type=int, default=8, help="Max source chunks (3-16).")
    chat.add_argument("--history-turns", type=int, default=14, help="History turns for context window.")
    chat.add_argument("--live-log-tail", help="Optional live log tail text to inject.")
    chat.add_argument(
        "--stream",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Use streaming output (default: true).",
    )
    chat.add_argument("--show-sources", action="store_true", help="Print cited sources after answers.")
    chat.add_argument("--verbose", action="store_true", help="Print stream activity telemetry.")
    chat.add_argument("--question", help="One-shot question mode (no interactive loop).")

    update = sub.add_parser("update", help="Profile-guided report revision runner (legacy federhav behavior).")
    update.add_argument("--run", required=True, help="Run directory (site/runs/...)")
    update.add_argument("--base-report", required=True, help="Base report path (relative or absolute)")
    update.add_argument("--update", required=True, help="Update request / revision instructions")
    update.add_argument("--second", help="Optional second prompt to append")
    update.add_argument("--output", help="Output report path (default: report_full.html in run)")
    update.add_argument("--model", help="Model name (e.g., gpt-4o-mini)")
    update.add_argument("--depth", help="Report depth (brief|standard|deep|extreme)")
    update.add_argument("--lang", default="ko", help="Report language (default: ko)")
    update.add_argument("--template", help="Template name/path override")
    update.add_argument("--agent-profile", default="federhav", help="Agent profile to apply")
    return parser


def _print_sources(sources: list[dict]) -> None:
    rows = sources if isinstance(sources, list) else []
    if not rows:
        return
    print("\n[sources]")
    for src in rows[:8]:
        sid = str(src.get("id") or "-")
        path = str(src.get("path") or "-")
        start = int(src.get("start_line") or 0)
        end = int(src.get("end_line") or 0)
        if start > 0 and end >= start:
            span = f"{start}-{end}"
        elif start > 0:
            span = f"{start}"
        else:
            span = "-"
        print(f"- [{sid}] {path}:{span}")


def _run_chat_once(args: argparse.Namespace, config: FederHavChatConfig, question: str) -> int:
    q = str(question or "").strip()
    if not q:
        raise SystemExit("question is required")
    if args.stream:
        printed = False
        done_payload: dict = {}
        gathered_sources: list[dict] = []
        for event in stream_question(config, q):
            name = str(event.get("event") or "").strip().lower()
            if name == "activity" and args.verbose:
                eid = str(event.get("id") or "activity")
                status = str(event.get("status") or "-")
                msg = str(event.get("message") or "").strip()
                print(f"[{eid}] {status} {msg}".strip())
            elif name == "delta":
                text = str(event.get("text") or "")
                if text:
                    print(text, end="", flush=True)
                    printed = True
            elif name == "sources":
                raw = event.get("sources")
                gathered_sources = raw if isinstance(raw, list) else gathered_sources
            elif name == "done":
                done_payload = dict(event)
                if not gathered_sources:
                    raw = done_payload.get("sources")
                    gathered_sources = raw if isinstance(raw, list) else gathered_sources
        print()
        if not printed:
            answer = str(done_payload.get("answer") or "").strip()
            if answer:
                print(answer)
        if args.show_sources:
            _print_sources(gathered_sources)
        err = str(done_payload.get("error") or "").strip()
        if err:
            print(f"[warning] {err}", file=sys.stderr)
            return 1
        return 0

    result = ask_question(config, q)
    print(str(result.get("answer") or "").strip())
    if args.show_sources:
        _print_sources(result.get("sources") if isinstance(result.get("sources"), list) else [])
    err = str(result.get("error") or "").strip()
    if err:
        print(f"[warning] {err}", file=sys.stderr)
        return 1
    return 0


def _run_chat_interactive(args: argparse.Namespace, config: FederHavChatConfig) -> int:
    root = config.root.resolve()
    run_rel = normalize_run_relpath(root, config.run_rel)
    profile_id = _sanitize_profile_token(config.profile_id) or "default"
    agent_id = _sanitize_agent_token(config.agent) or "federhav"
    execution_mode = "act" if str(config.execution_mode).strip().lower() == "act" else "plan"
    allow_artifacts = bool(config.allow_artifacts)
    print("[federhav] interactive chat mode")
    runtime_mode = str(config.runtime_mode or "auto").strip().lower() or "auto"
    print("[federhav] commands: /help, /run <path>, /profile <id>, /agent <id>, /runtime <auto|deepagent|off>, /plan [질문], /act [질문], /clear, /exit")
    while True:
        run_token = run_rel or "-"
        try:
            raw = input(f"[{run_token}|{profile_id}|{execution_mode}|{runtime_mode}] you> ")
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print()
            return 0
        line = str(raw or "").strip()
        if not line:
            continue
        lower = line.lower()
        if lower in {"/exit", "/quit"}:
            return 0
        if lower == "/help":
            print("commands:")
            print("- /help")
            print("- /run <path>")
            print("- /profile <id>    : history scope")
            print("- /agent <id>      : operator agent label")
            print("- /runtime <mode>  : auto|deepagent|off")
            print("- /plan [질문]      : plan-confirm mode")
            print("- /act [질문]       : act mode")
            print("- /clear")
            print("- /exit")
            continue
        if lower.startswith("/run "):
            next_run = line.split(" ", 1)[1].strip()
            run_rel = normalize_run_relpath(root, next_run)
            print(f"[federhav] run context -> {run_rel or '-'}")
            continue
        if lower.startswith("/profile"):
            next_profile = line.split(" ", 1)[1].strip() if " " in line else ""
            if not next_profile:
                print(f"[federhav] profile -> {profile_id}")
                continue
            profile_id = _sanitize_profile_token(next_profile) or profile_id
            print(f"[federhav] profile -> {profile_id}")
            continue
        if lower.startswith("/agent"):
            next_agent = line.split(" ", 1)[1].strip() if " " in line else ""
            if not next_agent:
                print(f"[federhav] agent -> {agent_id}")
                continue
            agent_id = _sanitize_agent_token(next_agent) or agent_id
            print(f"[federhav] agent -> {agent_id}")
            continue
        if lower.startswith("/runtime"):
            next_mode = line.split(" ", 1)[1].strip().lower() if " " in line else ""
            if not next_mode:
                print(f"[federhav] runtime mode -> {runtime_mode}")
                continue
            if next_mode not in {"auto", "deepagent", "off"}:
                print("[federhav] invalid runtime mode. use: auto | deepagent | off")
                continue
            runtime_mode = next_mode
            print(f"[federhav] runtime mode -> {runtime_mode}")
            continue
        mode_from_command, inline_question = _parse_prefixed_mode_question(line)
        if mode_from_command:
            execution_mode = mode_from_command
            print(
                "[federhav] execution mode -> "
                f"{execution_mode} (allow_artifacts={'true' if allow_artifacts else 'false'})"
            )
            if not inline_question:
                continue
            line = inline_question
        if lower == "/clear":
            clear_help_history(root, run_rel, profile_id=profile_id)
            print("[federhav] chat history cleared.")
            continue

        question_cfg = FederHavChatConfig(
            root=root,
            run_rel=run_rel,
            profile_id=profile_id,
            agent=agent_id,
            execution_mode=execution_mode,
            allow_artifacts=allow_artifacts,
            model=config.model,
            llm_backend=config.llm_backend,
            reasoning_effort=config.reasoning_effort,
            runtime_mode=runtime_mode,
            strict_model=config.strict_model,
            max_sources=config.max_sources,
            web_search=config.web_search,
            live_log_tail=config.live_log_tail,
            history_turns=config.history_turns,
        )
        exit_code = _run_chat_once(args, question_cfg, line)
        if exit_code != 0:
            print(f"[federhav] response finished with warning (code={exit_code}).")


def _run_chat_command(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    run_rel = normalize_run_relpath(root, args.run)
    requested_profile = _sanitize_profile_token(str(args.profile_id or "")) or "default"
    requested_agent = _sanitize_agent_token(str(args.agent or "")) or "federhav"
    execution_mode = "act" if str(args.execution_mode or "").strip().lower() == "act" else "plan"
    config = FederHavChatConfig(
        root=root,
        run_rel=run_rel,
        profile_id=requested_profile,
        agent=requested_agent,
        execution_mode=execution_mode,
        allow_artifacts=bool(args.allow_artifacts),
        model=args.model,
        llm_backend=args.llm_backend,
        reasoning_effort=args.reasoning_effort,
        runtime_mode=args.runtime_mode,
        strict_model=bool(args.strict_model),
        max_sources=max(3, min(int(args.max_sources), 16)),
        web_search=bool(args.web_search),
        live_log_tail=args.live_log_tail,
        history_turns=max(2, int(args.history_turns)),
    )
    if args.question:
        mode_from_prefix, question = _parse_prefixed_mode_question(str(args.question))
        if mode_from_prefix:
            config = FederHavChatConfig(
                **{
                    **config.__dict__,
                    "execution_mode": mode_from_prefix,
                }
            )
        if not question:
            raise SystemExit("question is required")
        return _run_chat_once(args, config, question)
    return _run_chat_interactive(args, config)


def _run_update_command(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(args.run)
    if not run_dir.exists():
        raise SystemExit(f"Run directory not found: {run_dir}")

    base_path = Path(args.base_report).expanduser()
    if not base_path.is_absolute():
        base_path = (run_dir / base_path).resolve()
    if not base_path.exists():
        raise SystemExit(f"Base report not found: {base_path}")

    update_path = _next_update_path(run_dir)
    rel_base = f"./{base_path.relative_to(run_dir).as_posix()}"
    update_text = _build_update_prompt(rel_base, args.update, args.second)
    update_path.write_text(update_text, encoding="utf-8")

    output_path = Path(args.output).expanduser() if args.output else _default_output(run_dir)
    if not output_path.is_absolute():
        output_path = (run_dir / output_path).resolve()

    cmd = [
        sys.executable,
        "-m",
        "federlicht.report",
        "--run",
        str(run_dir),
        "--output",
        str(output_path),
        "--prompt-file",
        str(update_path),
        "--lang",
        args.lang,
    ]
    if args.depth:
        cmd.extend(["--depth", args.depth])
    if args.model:
        cmd.extend(["--model", args.model])
    if args.template:
        cmd.extend(["--template", args.template])
    if args.agent_profile:
        cmd.extend(["--agent-profile", args.agent_profile])

    print(f"[federhav] update prompt: {update_path}")
    print(f"[federhav] output target: {output_path}")
    print(f"[federhav] running: {' '.join(cmd)}")
    return subprocess.call(cmd)


def main(argv: list[str] | None = None) -> int:
    _configure_stdio_utf8()
    raw = list(sys.argv[1:] if argv is None else argv)
    parser = _build_parser()
    args = parser.parse_args(_coerce_command_argv(raw))
    if args.command == "chat":
        return _run_chat_command(args)
    if args.command == "update":
        return _run_update_command(args)
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
