from __future__ import annotations

import html as html_lib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


_FLOW_DIRECTIONS = {"LR", "RL", "TB", "BT"}
_DEFAULT_D2_OUTPUT = "report_assets/artwork/d2_diagram.svg"
_DEFAULT_DIAGRAMS_OUTPUT = "report_assets/artwork/diagrams_architecture.svg"
_DEFAULT_INFOGRAPHIC_OUTPUT = "report_assets/artwork/infographic.html"
_MERMAID_FORMATS = {"svg", "png", "pdf"}
_DOT_CANDIDATES = (
    Path("C:/Program Files/Graphviz/bin/dot.exe"),
    Path("C:/Program Files (x86)/Graphviz/bin/dot.exe"),
)
_D2_CANDIDATES = (
    Path("C:/Program Files/D2/d2.exe"),
    Path("C:/Program Files (x86)/D2/d2.exe"),
)


def _slugify(value: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "_", str(value or "").strip())
    token = token.strip("_").lower()
    return token or "node"


def _split_lines(spec: str) -> list[str]:
    parts = re.split(r"[\n;]+", str(spec or ""))
    return [part.strip() for part in parts if part and part.strip()]


def _escape_mermaid(text: str) -> str:
    return str(text or "").replace('"', '\\"')


def list_artwork_capabilities() -> str:
    d2_ok = bool(_resolve_d2_command())
    mmdc_ok = bool(_resolve_mmdc_command())
    diagrams_ok = _has_diagrams_package()
    dot_ok = _resolve_dot_command() is not None
    lines = [
        "Artwork toolkit capabilities:",
        "- mermaid_flowchart: process/logic flow diagram from node/edge specs.",
        "- mermaid_timeline: chronology/timeline diagram from date|event specs.",
        f"- mermaid_render: {'available' if mmdc_ok else 'missing Mermaid CLI(mmdc)'} (renders SVG/PNG/PDF artifact).",
        f"- d2_render: {'available' if d2_ok else 'missing d2 CLI'} (architecture diagram SVG rendering).",
        f"- diagrams_render: {'available' if diagrams_ok and dot_ok else 'missing diagrams package or graphviz(dot)'} "
        "(Python diagrams fallback for architecture SVG).",
        "- infographic_spec_builder: available (tabular claim/data -> infographic_spec JSON).",
        "- infographic_claim_packet_builder: available (claim_evidence_map/evidence_packet -> infographic_spec JSON).",
        "- infographic_html: available (Chart.js/Plotly/Tailwind HTML infographic artifact).",
        "",
        "Selection guide:",
        "- Prefer Mermaid for simple process/timeline visuals in Markdown/HTML.",
        "- Prefer D2 for dense architecture/topology.",
        "- Use diagrams_render when provider/icon-style architecture is preferred in Python workflow.",
        "- Use infographic_spec_builder first when only table/text data is available.",
        "- Use infographic_claim_packet_builder for claim-evidence packet driven visuals.",
        "- Use infographic_html for data-driven visuals (comparisons/trends/risk-reward).",
        "",
        "Output rule: return only diagram snippets/artifact links with concise captions.",
    ]
    if not mmdc_ok:
        lines.append("Install Mermaid CLI: npm i -g @mermaid-js/mermaid-cli")
    if not d2_ok:
        lines.append("Install d2: https://d2lang.com/tour/install (or set D2_BIN to d2.exe path)")
    if not diagrams_ok:
        lines.append("Install diagrams package: python -m pip install diagrams graphviz")
    if not dot_ok:
        lines.append("Install Graphviz CLI and expose dot (or set GRAPHVIZ_DOT to dot.exe path)")
    return "\n".join(lines)


def build_mermaid_flowchart(
    nodes_spec: str,
    edges_spec: str,
    *,
    direction: str = "LR",
    title: str = "",
) -> str:
    node_map: dict[str, str] = {}
    node_order: list[str] = []
    lines = _split_lines(nodes_spec)
    for idx, raw in enumerate(lines, start=1):
        label = raw
        node_id = ""
        for marker in ("|", ":", "="):
            if marker in raw:
                left, right = raw.split(marker, 1)
                if left.strip() and right.strip():
                    node_id = _slugify(left)
                    label = right.strip()
                    break
        if not node_id:
            node_id = _slugify(raw)
            if node_id in node_map:
                node_id = f"{node_id}_{idx}"
        if node_id not in node_map:
            node_map[node_id] = label.strip() or node_id
            node_order.append(node_id)

    edge_lines = _split_lines(edges_spec)
    parsed_edges: list[tuple[str, str, str]] = []
    edge_re = re.compile(r"^\s*([^>\-\s][^>]*)\s*->\s*([^|:]+?)(?:\s*[|:]\s*(.+))?$")
    for raw in edge_lines:
        match = edge_re.match(raw)
        if not match:
            continue
        src = _slugify(match.group(1))
        dst = _slugify(match.group(2))
        rel_label = str(match.group(3) or "").strip()
        if src not in node_map:
            node_map[src] = src.replace("_", " ").title()
            node_order.append(src)
        if dst not in node_map:
            node_map[dst] = dst.replace("_", " ").title()
            node_order.append(dst)
        parsed_edges.append((src, dst, rel_label))

    flow_dir = str(direction or "LR").upper().strip()
    if flow_dir not in _FLOW_DIRECTIONS:
        flow_dir = "LR"
    diagram: list[str] = [f"flowchart {flow_dir}"]
    for node_id in node_order:
        diagram.append(f'    {node_id}["{_escape_mermaid(node_map[node_id])}"]')
    for src, dst, rel_label in parsed_edges:
        if rel_label:
            diagram.append(f"    {src} -->|{_escape_mermaid(rel_label)}| {dst}")
        else:
            diagram.append(f"    {src} --> {dst}")
    if len(diagram) == 1:
        diagram.append('    a["Placeholder"]')
    snippet = [
        "```mermaid",
        *diagram,
        "```",
    ]
    if title.strip():
        snippet.append(f"*Figure: {title.strip()}*")
    return "\n".join(snippet)


def build_mermaid_timeline(events_spec: str, *, title: str = "") -> str:
    rows = _split_lines(events_spec)
    timeline_lines = ["timeline"]
    if title.strip():
        timeline_lines.append(f"    title {_escape_mermaid(title.strip())}")
    if not rows:
        timeline_lines.append("    1 : Placeholder event")
    for idx, row in enumerate(rows, start=1):
        date_token = f"Step {idx}"
        event_text = row
        for marker in ("|", ":", "="):
            if marker in row:
                left, right = row.split(marker, 1)
                if left.strip() and right.strip():
                    date_token = left.strip()
                    event_text = right.strip()
                    break
        timeline_lines.append(f"    {_escape_mermaid(date_token)} : {_escape_mermaid(event_text)}")
    return "\n".join(["```mermaid", *timeline_lines, "```"])


def _resolve_under_run(run_dir: Path, rel_path: str) -> Path:
    candidate = (run_dir / str(rel_path or "").replace("\\", "/")).resolve()
    run_root = run_dir.resolve()
    try:
        candidate.relative_to(run_root)
    except Exception as exc:
        raise ValueError("output_rel_path must stay under the run directory") from exc
    return candidate


def _resolve_mmdc_command() -> list[str]:
    mmdc = shutil.which("mmdc")
    if mmdc:
        return [mmdc]
    local_bin_dir = Path.cwd() / "node_modules" / ".bin"
    for filename in ("mmdc.cmd", "mmdc"):
        local_mmdc = local_bin_dir / filename
        if local_mmdc.exists():
            return [str(local_mmdc)]
    npx = shutil.which("npx")
    if npx:
        try:
            probe = subprocess.run(
                [npx, "--no-install", "mmdc", "--version"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=4,
                check=False,
            )
            if probe.returncode == 0:
                return [npx, "--no-install", "mmdc"]
        except Exception:
            pass
    return []


def _resolve_d2_command() -> list[str]:
    env_bin = Path(str(os.getenv("D2_BIN", "")).strip())
    if str(env_bin) and env_bin.exists() and env_bin.is_file():
        return [str(env_bin)]
    d2 = shutil.which("d2")
    if d2:
        return [d2]
    for candidate in _D2_CANDIDATES:
        if candidate.exists() and candidate.is_file():
            return [str(candidate)]
    return []


def _resolve_dot_command() -> str | None:
    env_bin = str(os.getenv("GRAPHVIZ_DOT", "")).strip()
    if env_bin and Path(env_bin).exists() and Path(env_bin).is_file():
        return env_bin
    dot = shutil.which("dot")
    if dot:
        return dot
    for candidate in _DOT_CANDIDATES:
        if candidate.exists() and candidate.is_file():
            return str(candidate)
    return None


def _has_diagrams_package() -> bool:
    try:
        import diagrams  # noqa: F401
    except Exception:
        return False
    return True


def _ensure_graphviz_runtime(dot_bin: str) -> None:
    dot_path = Path(dot_bin)
    os.environ["GRAPHVIZ_DOT"] = str(dot_path)
    bin_dir = str(dot_path.parent)
    current = os.environ.get("PATH", "")
    parts = current.split(os.pathsep) if current else []
    if bin_dir not in parts:
        os.environ["PATH"] = bin_dir + os.pathsep + current


def _normalize_mermaid_format(value: str) -> str:
    token = str(value or "").strip().lower().lstrip(".")
    return token if token in _MERMAID_FORMATS else "svg"


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except Exception:
        return default


def _safe_float(value: object, default: float = 1.0) -> float:
    try:
        return float(str(value).strip())
    except Exception:
        return default


def render_d2_svg(
    run_dir: Path,
    d2_source: str,
    *,
    output_rel_path: str = _DEFAULT_D2_OUTPUT,
    theme: str = "200",
    layout: str = "dagre",
) -> dict[str, str]:
    d2_command = _resolve_d2_command()
    if not d2_command:
        return {
            "ok": "false",
            "error": "d2_cli_missing",
            "message": "D2 CLI is not installed. Install https://d2lang.com/tour/install or set D2_BIN.",
        }
    if not str(d2_source or "").strip():
        return {"ok": "false", "error": "empty_source", "message": "d2_source is empty"}

    out_path = _resolve_under_run(run_dir, output_rel_path or _DEFAULT_D2_OUTPUT)
    if out_path.suffix.lower() != ".svg":
        out_path = out_path.with_suffix(".svg")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    temp_file: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".d2", delete=False) as handle:
            handle.write(d2_source)
            handle.flush()
            temp_file = Path(handle.name)
        cmd = [
            *d2_command,
            "--theme",
            str(theme or "200"),
            "--layout",
            str(layout or "dagre"),
            str(temp_file),
            str(out_path),
        ]
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "d2 render failed").strip()
            return {
                "ok": "false",
                "error": "d2_render_failed",
                "message": detail[:400],
            }
    finally:
        if temp_file and temp_file.exists():
            try:
                temp_file.unlink()
            except Exception:
                pass

    rel_out = f"./{out_path.relative_to(run_dir).as_posix()}"
    return {
        "ok": "true",
        "path": rel_out,
        "markdown": f"![Diagram]({rel_out})",
    }


def render_diagrams_architecture(
    run_dir: Path,
    nodes_spec: str,
    edges_spec: str,
    *,
    output_rel_path: str = _DEFAULT_DIAGRAMS_OUTPUT,
    direction: str = "LR",
    title: str = "",
) -> dict[str, str]:
    if not _has_diagrams_package():
        return {
            "ok": "false",
            "error": "diagrams_missing",
            "message": "Python package 'diagrams' is missing. Install: python -m pip install diagrams graphviz",
        }
    dot_bin = _resolve_dot_command()
    if not dot_bin:
        return {
            "ok": "false",
            "error": "graphviz_dot_missing",
            "message": "Graphviz dot executable is missing. Install Graphviz or set GRAPHVIZ_DOT.",
        }
    _ensure_graphviz_runtime(dot_bin)

    try:
        from diagrams import Diagram, Edge
        from diagrams.generic.blank import Blank
    except Exception as exc:
        return {
            "ok": "false",
            "error": "diagrams_import_failed",
            "message": str(exc)[:400],
        }

    out_path = _resolve_under_run(run_dir, output_rel_path or _DEFAULT_DIAGRAMS_OUTPUT)
    if out_path.suffix.lower() != ".svg":
        out_path = out_path.with_suffix(".svg")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    filename_base = out_path.with_suffix("")

    node_map: dict[str, str] = {}
    node_order: list[str] = []
    for idx, raw in enumerate(_split_lines(nodes_spec), start=1):
        label = raw
        node_id = ""
        for marker in ("|", ":", "="):
            if marker in raw:
                left, right = raw.split(marker, 1)
                if left.strip() and right.strip():
                    node_id = _slugify(left)
                    label = right.strip()
                    break
        if not node_id:
            node_id = _slugify(raw)
            if node_id in node_map:
                node_id = f"{node_id}_{idx}"
        if node_id not in node_map:
            node_map[node_id] = label.strip() or node_id
            node_order.append(node_id)

    edge_re = re.compile(r"^\s*([^>\-\s][^>]*)\s*->\s*([^|:]+?)(?:\s*[|:]\s*(.+))?$")
    parsed_edges: list[tuple[str, str, str]] = []
    for raw in _split_lines(edges_spec):
        match = edge_re.match(raw)
        if not match:
            continue
        src = _slugify(match.group(1))
        dst = _slugify(match.group(2))
        rel_label = str(match.group(3) or "").strip()
        if src not in node_map:
            node_map[src] = src.replace("_", " ").title()
            node_order.append(src)
        if dst not in node_map:
            node_map[dst] = dst.replace("_", " ").title()
            node_order.append(dst)
        parsed_edges.append((src, dst, rel_label))

    if not node_order:
        node_order = ["placeholder_a", "placeholder_b"]
        node_map["placeholder_a"] = "Start"
        node_map["placeholder_b"] = "End"
        parsed_edges = [("placeholder_a", "placeholder_b", "flow")]

    graph_dir = str(direction or "LR").upper().strip()
    if graph_dir not in _FLOW_DIRECTIONS:
        graph_dir = "LR"

    try:
        with Diagram(
            title.strip() or filename_base.name,
            filename=str(filename_base),
            outformat="svg",
            direction=graph_dir,
            show=False,
        ):
            nodes = {node_id: Blank(node_map[node_id]) for node_id in node_order}
            if parsed_edges:
                for src, dst, rel_label in parsed_edges:
                    edge = Edge(label=rel_label) if rel_label else Edge()
                    nodes[src] >> edge >> nodes[dst]
    except Exception as exc:
        return {
            "ok": "false",
            "error": "diagrams_render_failed",
            "message": str(exc)[:400],
        }

    rel_out = f"./{out_path.relative_to(run_dir).as_posix()}"
    return {
        "ok": "true",
        "path": rel_out,
        "format": "svg",
        "markdown": f"![Architecture Diagram]({rel_out})",
    }


def render_mermaid_diagram(
    run_dir: Path,
    diagram_source: str,
    *,
    output_rel_path: str = "report_assets/artwork/mermaid_diagram.svg",
    output_format: str = "svg",
    theme: str = "default",
    background_color: str = "transparent",
    width: int = 0,
    height: int = 0,
    scale: float = 1.0,
) -> dict[str, str]:
    command_prefix = _resolve_mmdc_command()
    if not command_prefix:
        return {
            "ok": "false",
            "error": "mmdc_missing",
            "message": "Mermaid CLI(mmdc)가 없습니다. npm i -g @mermaid-js/mermaid-cli 또는 npm i -D @mermaid-js/mermaid-cli",
        }
    source_text = str(diagram_source or "").strip()
    if not source_text:
        return {"ok": "false", "error": "empty_source", "message": "diagram_source is empty"}
    fmt = _normalize_mermaid_format(output_format)
    out_path = _resolve_under_run(run_dir, output_rel_path or "report_assets/artwork/mermaid_diagram.svg")
    if out_path.suffix.lower() != f".{fmt}":
        out_path = out_path.with_suffix(f".{fmt}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    width_px = max(0, _safe_int(width, 0))
    height_px = max(0, _safe_int(height, 0))
    scale_value = _safe_float(scale, 1.0)
    if scale_value <= 0:
        scale_value = 1.0
    temp_file: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".mmd", delete=False) as handle:
            handle.write(source_text)
            handle.flush()
            temp_file = Path(handle.name)
        cmd = [
            *command_prefix,
            "-i",
            str(temp_file),
            "-o",
            str(out_path),
            "-t",
            str(theme or "default"),
            "-b",
            str(background_color or "transparent"),
            "-s",
            str(scale_value),
            "-q",
        ]
        if width_px > 0:
            cmd.extend(["-w", str(width_px)])
        if height_px > 0:
            cmd.extend(["-H", str(height_px)])
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "mmdc render failed").strip()
            return {
                "ok": "false",
                "error": "mmdc_render_failed",
                "message": detail[:400],
            }
    finally:
        if temp_file and temp_file.exists():
            try:
                temp_file.unlink()
            except Exception:
                pass
    rel_out = f"./{out_path.relative_to(run_dir).as_posix()}"
    markdown = f"![Diagram]({rel_out})" if fmt in {"svg", "png"} else f"[Diagram PDF]({rel_out})"
    return {
        "ok": "true",
        "path": rel_out,
        "format": fmt,
        "markdown": markdown,
    }


def _normalize_hex_color(value: object, fallback: str) -> str:
    token = str(value or "").strip()
    if re.fullmatch(r"#[0-9a-fA-F]{6}", token):
        return token.lower()
    if re.fullmatch(r"#[0-9a-fA-F]{3}", token):
        return token.lower()
    return fallback


def _normalize_chart_value(value: object) -> object:
    if isinstance(value, (int, float)):
        return value
    token = str(value or "").strip()
    if re.fullmatch(r"-?\d+", token):
        try:
            return int(token)
        except Exception:
            return token
    if re.fullmatch(r"-?\d+\.\d+", token):
        try:
            return float(token)
        except Exception:
            return token
    return token


def _to_bool(value: object, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    token = str(value or "").strip().lower()
    if not token:
        return bool(default)
    if token in {"1", "true", "yes", "on", "y"}:
        return True
    if token in {"0", "false", "no", "off", "n"}:
        return False
    return bool(default)


def _parse_table_rows(data_table: str) -> list[list[str]]:
    lines = [line.strip() for line in str(data_table or "").splitlines() if line and line.strip()]
    if not lines:
        return []

    markdown_rows: list[list[str]] = []
    for raw in lines:
        if "|" not in raw:
            markdown_rows = []
            break
        row = raw.strip().strip("|")
        cells = [cell.strip() for cell in row.split("|")]
        if not cells or all(not cell for cell in cells):
            continue
        if all(re.fullmatch(r":?-{2,}:?", cell or "") for cell in cells):
            continue
        markdown_rows.append(cells)
    if markdown_rows:
        width = max(len(row) for row in markdown_rows)
        normalized_rows: list[list[str]] = []
        for row in markdown_rows:
            current = list(row[:width])
            if len(current) < width:
                current.extend([""] * (width - len(current)))
            normalized_rows.append(current)
        return normalized_rows

    first = lines[0]
    delimiters = [",", "\t", ";"]
    delimiter = max(delimiters, key=lambda token: first.count(token))
    if first.count(delimiter) > 0:
        rows = [[cell.strip() for cell in row.split(delimiter)] for row in lines]
        width = max(len(row) for row in rows)
        normalized_rows = []
        for row in rows:
            current = list(row[:width])
            if len(current) < width:
                current.extend([""] * (width - len(current)))
            normalized_rows.append(current)
        return normalized_rows

    rows = [re.split(r"\s{2,}", row) for row in lines]
    rows = [[cell.strip() for cell in row if str(cell).strip()] for row in rows]
    return [row for row in rows if row]


def _parse_theme_json(theme_json: str) -> dict[str, str]:
    token = str(theme_json or "").strip()
    if not token:
        return {}
    try:
        payload = json.loads(token)
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}
    out: dict[str, str] = {}
    for key in ("primary", "secondary", "accent", "surface", "ink"):
        if key in payload:
            color = _normalize_hex_color(payload.get(key), "")
            if color:
                out[key] = color
    return out


def build_infographic_spec_from_table(
    data_table: str,
    *,
    title: str = "",
    subtitle: str = "",
    chart_title: str = "",
    chart_description: str = "",
    chart_type: str = "line",
    library: str = "chartjs",
    source: str = "",
    simulated: bool | str = True,
    theme_json: str = "",
    note: str = "",
    disclaimer: str = "",
) -> str:
    rows = _parse_table_rows(data_table)
    if len(rows) < 2:
        raise ValueError("data_table must contain header + at least one data row")
    header = rows[0]
    if len(header) < 2:
        raise ValueError("data_table must include at least two columns")
    series_labels = [str(col or "").strip() for col in header[1:] if str(col or "").strip()]
    if not series_labels:
        raise ValueError("data_table header must include at least one series column")

    labels: list[str] = []
    values_by_series: list[list[object]] = [[] for _ in series_labels]
    for row in rows[1:]:
        if not row:
            continue
        label = str(row[0] if len(row) > 0 else "").strip()
        if not label:
            continue
        labels.append(label)
        for idx in range(len(series_labels)):
            raw = row[idx + 1] if idx + 1 < len(row) else ""
            values_by_series[idx].append(_normalize_chart_value(raw))
    if not labels:
        raise ValueError("data_table has no valid label rows")

    palette = ["#00bcd4", "#1a237e", "#ff5722", "#94a3b8", "#0ea5e9"]
    datasets = []
    for idx, series_label in enumerate(series_labels):
        datasets.append(
            {
                "label": series_label[:80],
                "data": values_by_series[idx],
                "color": palette[idx % len(palette)],
            }
        )
    title_text = str(title or chart_title or "Auto-generated Infographic").strip()
    chart_title_text = str(chart_title or "Auto-generated chart").strip()
    chart_desc_text = str(chart_description or "Generated from tabular values extracted from report context.").strip()
    library_token = str(library or "chartjs").strip().lower()
    if library_token not in {"chartjs", "plotly"}:
        library_token = "chartjs"
    chart_type_token = str(chart_type or "line").strip().lower() or "line"
    source_text = str(source or "").strip() or "Source: pending mapping"
    note_text = str(note or "").strip()
    simulated_flag = _to_bool(simulated, default=True)
    theme = _parse_theme_json(theme_json)
    if not disclaimer and simulated_flag:
        disclaimer = "Some values are marked as Simulated/Illustrative."
    cards = [
        {
            "label": "Rows",
            "value": str(len(labels)),
            "hint": f"{len(series_labels)} series extracted from table input.",
        }
    ]
    spec = {
        "title": title_text[:180],
        "subtitle": str(subtitle or "").strip()[:260],
        "cards": cards,
        "charts": [
            {
                "id": _slugify(chart_title_text or "auto_chart"),
                "library": library_token,
                "type": chart_type_token,
                "title": chart_title_text[:120],
                "description": chart_desc_text[:280],
                "labels": labels[:240],
                "datasets": datasets,
                "source": source_text[:240],
                "note": note_text[:280],
                "simulated": simulated_flag,
            }
        ],
        "disclaimer": str(disclaimer or "").strip()[:320],
    }
    if theme:
        spec["theme"] = theme
    return json.dumps(spec, ensure_ascii=False, indent=2)


def _claim_strength_to_score(value: object) -> int:
    token = str(value or "").strip().lower()
    if token == "high":
        return 3
    if token == "medium":
        return 2
    if token == "low":
        return 1
    return 0


def _claim_label(entry: dict[str, object], index: int) -> str:
    claim_id = str(entry.get("claim_id") or "").strip()
    claim_text = str(entry.get("claim_text") or entry.get("claim") or "").strip()
    if claim_id:
        return claim_id[:24]
    if claim_text:
        compact = " ".join(claim_text.split())
        return compact[:36] + ("..." if len(compact) > 36 else "")
    return f"Claim {index}"


def _normalize_section_hint(value: object) -> str:
    token = str(value or "").strip().lower().replace("-", "_")
    if not token:
        return "unspecified"
    return token


def _section_hint_label(value: str) -> str:
    token = _normalize_section_hint(value)
    mapping = {
        "key_findings": "Key Findings",
        "scope_methodology": "Scope & Methodology",
        "risks_gaps": "Risks & Gaps",
        "decision_recommendation": "Decision & Recommendation",
        "executive_summary": "Executive Summary",
        "evidence_index": "Evidence Index",
        "unspecified": "Unspecified",
    }
    return mapping.get(token, token.replace("_", " ").title())


def _resolve_claim_chart_type(chart_type: str, section_hint: str) -> str:
    token = str(chart_type or "").strip().lower() or "bar"
    if token not in {"auto", "section_auto", "by_section"}:
        return token
    hint = _normalize_section_hint(section_hint)
    if hint in {"scope_methodology", "risks_gaps"}:
        return "line"
    return "bar"


def _resolve_claim_chart_library(library: str, section_hint: str) -> str:
    token = str(library or "").strip().lower() or "chartjs"
    if token in {"chartjs", "plotly"}:
        return token
    if token in {"mixed", "auto", "section_auto", "by_section"}:
        hint = _normalize_section_hint(section_hint)
        if hint in {"risks_gaps", "decision_recommendation"}:
            return "plotly"
        return "chartjs"
    return "chartjs"


def build_infographic_spec_from_claim_packet(
    claim_packet_json: str,
    *,
    title: str = "",
    subtitle: str = "",
    chart_title: str = "",
    chart_description: str = "",
    source: str = "",
    simulated: bool | str = False,
    library: str = "chartjs",
    chart_type: str = "bar",
    theme_json: str = "",
    note: str = "",
    disclaimer: str = "",
    max_claims: int = 8,
    split_by_section: bool | str = False,
    max_charts: int = 3,
) -> str:
    payload_text = str(claim_packet_json or "").strip()
    if not payload_text:
        raise ValueError("claim_packet_json is empty")
    try:
        payload = json.loads(payload_text)
    except Exception as exc:
        raise ValueError(f"claim_packet_json parse failed: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("claim_packet_json must be a JSON object")

    raw_claims = payload.get("claims")
    if not isinstance(raw_claims, list) or not raw_claims:
        raise ValueError("claim_packet_json.claims must be a non-empty array")

    parsed_rows: list[dict[str, object]] = []
    for idx, raw in enumerate(raw_claims, start=1):
        if not isinstance(raw, dict):
            continue
        claim_text = str(raw.get("claim_text") or raw.get("claim") or "").strip()
        if not claim_text:
            continue
        evidence_ids = raw.get("evidence_ids")
        if isinstance(evidence_ids, list):
            evidence_count = sum(1 for item in evidence_ids if str(item).strip())
        else:
            refs = raw.get("refs")
            evidence_count = sum(1 for item in refs) if isinstance(refs, list) else 0
        score_raw = raw.get("score")
        try:
            relevance = float(score_raw) if score_raw is not None else 0.0
        except Exception:
            relevance = 0.0
        strength_score = _claim_strength_to_score(raw.get("strength") or raw.get("evidence_strength"))
        recency = str(raw.get("recency") or "unknown").strip().lower() or "unknown"
        source_kind = str(raw.get("source_kind") or "unknown").strip().lower() or "unknown"
        parsed_rows.append(
            {
                "label": _claim_label(raw, idx),
                "claim_text": claim_text,
                "evidence_count": evidence_count,
                "strength_score": strength_score,
                "relevance": relevance,
                "section_hint": _normalize_section_hint(raw.get("section_hint")),
                "recency": recency,
                "source_kind": source_kind,
            }
        )
    if not parsed_rows:
        raise ValueError("claim packet has no usable claims")

    parsed_rows.sort(
        key=lambda item: (
            float(item.get("evidence_count") or 0.0),
            float(item.get("strength_score") or 0.0),
            float(item.get("relevance") or 0.0),
        ),
        reverse=True,
    )
    limit = max(1, min(24, int(max_claims) if str(max_claims).strip() else 8))
    selected = parsed_rows[:limit]
    labels = [str(item.get("label") or "") for item in selected]
    evidence_values = [int(item.get("evidence_count") or 0) for item in selected]
    strength_values = [int(item.get("strength_score") or 0) for item in selected]

    stats = payload.get("stats") if isinstance(payload.get("stats"), dict) else {}
    selected_claims = int(stats.get("selected_claims") or len(raw_claims))
    selected_evidence = int(stats.get("selected_evidence") or 0)
    index_only_ratio = float(stats.get("index_only_ratio") or 0.0)
    theme = _parse_theme_json(theme_json)
    simulated_flag = _to_bool(simulated, default=False)

    library_token = str(library or "chartjs").strip().lower() or "chartjs"
    chart_type_token = str(chart_type or "bar").strip().lower() or "bar"

    risk_claim_count = sum(1 for item in selected if str(item.get("section_hint") or "") == "risks_gaps")
    fresh_claim_count = sum(1 for item in selected if str(item.get("recency") or "") in {"new", "recent"})
    fresh_ratio = round((fresh_claim_count / max(1, len(selected))) * 100.0, 1)
    source_kind_counts: dict[str, int] = {}
    for item in selected:
        key = str(item.get("source_kind") or "unknown").strip().lower() or "unknown"
        source_kind_counts[key] = source_kind_counts.get(key, 0) + 1
    dominant_source_kind = "unknown"
    if source_kind_counts:
        dominant_source_kind = sorted(source_kind_counts.items(), key=lambda row: row[1], reverse=True)[0][0]

    title_text = str(title or "Claim-Evidence Snapshot").strip()
    subtitle_text = str(subtitle or "Auto-generated from claim-evidence packet.").strip()
    chart_title_text = str(chart_title or "Claim Strength vs Evidence Coverage").strip()
    chart_description_text = str(
        chart_description
        or "Selected claims are ranked by evidence coverage and claim strength extracted from the evidence packet."
    ).strip()
    source_text = str(source or "./report_notes/claim_evidence_map.json").strip()
    note_text = str(note or "Generated from claim packet fields: evidence_ids, strength, score.").strip()
    if not disclaimer and simulated_flag:
        disclaimer = "Some values are marked as Simulated/Illustrative."
    split_by_section_flag = _to_bool(split_by_section, default=False)
    max_chart_count = max(1, min(8, int(max_charts) if str(max_charts).strip() else 3))

    charts: list[dict[str, object]] = [
        {
            "id": "claim_evidence_snapshot",
            "library": _resolve_claim_chart_library(library_token, "unspecified"),
            "type": _resolve_claim_chart_type(chart_type_token, "unspecified"),
            "title": chart_title_text[:120],
            "description": chart_description_text[:280],
            "labels": labels[:240],
            "datasets": [
                {"label": "Evidence Count", "data": evidence_values, "color": "#00bcd4"},
                {"label": "Strength Score", "data": strength_values, "color": "#1a237e"},
            ],
            "source": source_text[:240],
            "note": note_text[:280],
            "simulated": simulated_flag,
        }
    ]
    if split_by_section_flag and max_chart_count > 1:
        grouped: dict[str, list[dict[str, object]]] = {}
        for item in selected:
            hint = _normalize_section_hint(item.get("section_hint"))
            grouped.setdefault(hint, []).append(item)
        ordered_groups = sorted(
            grouped.items(),
            key=lambda pair: (
                len(pair[1]),
                sum(int(row.get("evidence_count") or 0) for row in pair[1]),
                pair[0] != "key_findings",
            ),
            reverse=True,
        )
        for hint, rows in ordered_groups:
            if len(charts) >= max_chart_count:
                break
            if not rows or hint == "unspecified":
                continue
            labels_hint = [str(row.get("label") or "") for row in rows]
            evidence_hint = [int(row.get("evidence_count") or 0) for row in rows]
            strength_hint = [int(row.get("strength_score") or 0) for row in rows]
            section_label = _section_hint_label(hint)
            charts.append(
                {
                    "id": f"claim_evidence_{_slugify(hint)}",
                    "library": _resolve_claim_chart_library(library_token, hint),
                    "type": _resolve_claim_chart_type(chart_type_token, hint),
                    "title": f"{section_label}: Evidence Profile"[:120],
                    "description": (
                        "Claim-evidence profile grouped by section hint extracted from the claim packet."
                    )[:280],
                    "labels": labels_hint[:240],
                    "datasets": [
                        {"label": "Evidence Count", "data": evidence_hint, "color": "#00bcd4"},
                        {"label": "Strength Score", "data": strength_hint, "color": "#1a237e"},
                    ],
                    "source": source_text[:240],
                    "note": (f"{note_text} | section_hint={hint}")[:280],
                    "simulated": simulated_flag,
                }
            )

    spec: dict[str, object] = {
        "title": title_text[:180],
        "subtitle": subtitle_text[:260],
        "cards": [
            {
                "label": "Selected Claims",
                "value": str(max(0, selected_claims)),
                "hint": f"Top {len(selected)} claims visualized from packet.",
            },
            {
                "label": "Risk-tagged Claims",
                "value": str(max(0, risk_claim_count)),
                "hint": "Claims mapped to Risks & Gaps via section_hint.",
            },
            {
                "label": "Freshness Ratio",
                "value": f"{fresh_ratio:.1f}%",
                "hint": "Share of selected claims marked as new/recent.",
            },
            {
                "label": "Dominant Source Kind",
                "value": dominant_source_kind.replace("_", " ").title(),
                "hint": (
                    f"Evidence={max(0, selected_evidence)} | "
                    f"Index-only={max(0.0, index_only_ratio) * 100:.1f}%"
                ),
            },
        ],
        "charts": charts,
        "disclaimer": str(disclaimer or "").strip()[:320],
    }
    if theme:
        spec["theme"] = theme
    return json.dumps(spec, ensure_ascii=False, indent=2)


def lint_infographic_spec(spec: dict[str, object]) -> list[str]:
    issues: list[str] = []
    if not isinstance(spec, dict):
        return ["spec is not a JSON object."]
    charts = spec.get("charts")
    if not isinstance(charts, list) or not charts:
        return ["charts must be a non-empty array."]
    for idx, raw in enumerate(charts, start=1):
        if not isinstance(raw, dict):
            issues.append(f"charts[{idx}] is not an object.")
            continue
        source = str(raw.get("source") or "").strip()
        if not source:
            issues.append(f"charts[{idx}] source is missing.")
        if "simulated" not in raw:
            issues.append(f"charts[{idx}] simulated flag is missing.")
        elif not isinstance(raw.get("simulated"), bool):
            issues.append(f"charts[{idx}] simulated flag must be boolean.")
        labels = raw.get("labels") if isinstance(raw.get("labels"), list) else []
        datasets = raw.get("datasets") if isinstance(raw.get("datasets"), list) else []
        plotly = raw.get("plotly") if isinstance(raw.get("plotly"), dict) else {}
        has_plotly_data = isinstance(plotly.get("data"), list) and bool(plotly.get("data"))
        if not datasets and not has_plotly_data:
            issues.append(f"charts[{idx}] has no datasets/plotly data.")
        if labels and datasets:
            label_count = len(labels)
            for ds_idx, dataset in enumerate(datasets, start=1):
                if not isinstance(dataset, dict):
                    issues.append(f"charts[{idx}].datasets[{ds_idx}] is not an object.")
                    continue
                values = dataset.get("data")
                if isinstance(values, list) and values and len(values) != label_count:
                    issues.append(
                        f"charts[{idx}].datasets[{ds_idx}] length mismatch: "
                        f"{len(values)} values vs {label_count} labels."
                    )
    return issues


def _normalize_infographic_spec(spec: dict[str, object], page_title: str = "") -> dict[str, object]:
    theme_raw = spec.get("theme") if isinstance(spec.get("theme"), dict) else {}
    theme: dict[str, str] = {
        "primary": _normalize_hex_color((theme_raw or {}).get("primary"), "#1a237e"),
        "secondary": _normalize_hex_color((theme_raw or {}).get("secondary"), "#00bcd4"),
        "accent": _normalize_hex_color((theme_raw or {}).get("accent"), "#ff5722"),
        "surface": _normalize_hex_color((theme_raw or {}).get("surface"), "#f8fafc"),
        "ink": _normalize_hex_color((theme_raw or {}).get("ink"), "#111827"),
    }
    cards: list[dict[str, str]] = []
    for raw in spec.get("cards") if isinstance(spec.get("cards"), list) else []:
        if not isinstance(raw, dict):
            continue
        label = str(raw.get("label") or "").strip()
        value = str(raw.get("value") or raw.get("metric") or "").strip()
        hint = str(raw.get("hint") or raw.get("description") or "").strip()
        if not label:
            continue
        cards.append({"label": label[:80], "value": value[:120], "hint": hint[:180]})

    charts: list[dict[str, object]] = []
    color_cycle = [theme["secondary"], theme["primary"], theme["accent"], "#94a3b8", "#0ea5e9"]
    for idx, raw in enumerate(spec.get("charts") if isinstance(spec.get("charts"), list) else [], start=1):
        if not isinstance(raw, dict):
            continue
        library = str(raw.get("library") or raw.get("engine") or "chartjs").strip().lower()
        if library not in {"chartjs", "plotly"}:
            library = "chartjs"
        chart_type = str(raw.get("type") or "bar").strip().lower()
        chart_id = _slugify(raw.get("id") or f"chart_{idx}")
        title = str(raw.get("title") or f"Chart {idx}").strip()
        description = str(raw.get("description") or "").strip()
        labels = [
            str(item).strip()
            for item in (raw.get("labels") if isinstance(raw.get("labels"), list) else [])
            if str(item).strip()
        ]
        datasets_raw = raw.get("datasets") if isinstance(raw.get("datasets"), list) else []
        datasets: list[dict[str, object]] = []
        for ds_idx, ds in enumerate(datasets_raw, start=1):
            if not isinstance(ds, dict):
                continue
            series_data = ds.get("data") if isinstance(ds.get("data"), list) else []
            datasets.append(
                {
                    "label": str(ds.get("label") or f"Series {ds_idx}").strip()[:80],
                    "data": [_normalize_chart_value(item) for item in series_data],
                    "color": _normalize_hex_color(ds.get("color"), color_cycle[(ds_idx - 1) % len(color_cycle)]),
                }
            )
        if not datasets and isinstance(raw.get("values"), list):
            datasets.append(
                {
                    "label": str(raw.get("series_label") or title or f"Series {idx}").strip()[:80],
                    "data": [_normalize_chart_value(item) for item in raw.get("values") or []],
                    "color": color_cycle[(idx - 1) % len(color_cycle)],
                }
            )
        plotly_raw = raw.get("plotly") if isinstance(raw.get("plotly"), dict) else {}
        source = str(raw.get("source") or raw.get("source_label") or "").strip()
        note = str(raw.get("note") or "").strip()
        simulated_raw = raw.get("simulated")
        simulated = bool(simulated_raw) and str(simulated_raw).strip().lower() not in {"0", "false", "no", "off"}
        charts.append(
            {
                "id": chart_id,
                "dom_id": f"infographic_{chart_id}_{idx}",
                "library": library,
                "type": chart_type,
                "title": title[:120],
                "description": description[:280],
                "labels": labels[:120],
                "datasets": datasets,
                "plotly": plotly_raw,
                "source": source[:240],
                "note": note[:280],
                "simulated": simulated,
            }
        )

    title = str(spec.get("title") or page_title or "Data-Driven Infographic").strip()
    subtitle = str(spec.get("subtitle") or "").strip()
    disclaimer = str(spec.get("disclaimer") or "").strip()
    if not disclaimer:
        if any(bool(chart.get("simulated")) for chart in charts):
            disclaimer = "Some values are marked as Simulated/Illustrative."
    return {
        "title": title[:180],
        "subtitle": subtitle[:260],
        "theme": theme,
        "cards": cards[:12],
        "charts": charts[:12],
        "disclaimer": disclaimer[:320],
    }


def _render_infographic_html(spec: dict[str, object], *, needs_chartjs: bool, needs_plotly: bool) -> str:
    theme = spec.get("theme") if isinstance(spec.get("theme"), dict) else {}
    title = str(spec.get("title") or "Data-Driven Infographic")
    subtitle = str(spec.get("subtitle") or "")
    disclaimer = str(spec.get("disclaimer") or "")
    cards = spec.get("cards") if isinstance(spec.get("cards"), list) else []
    charts = spec.get("charts") if isinstance(spec.get("charts"), list) else []

    lines: list[str] = [
        "<!doctype html>",
        "<html lang=\"ko\">",
        "<head>",
        "  <meta charset=\"utf-8\"/>",
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"/>",
        f"  <title>{html_lib.escape(title)}</title>",
        "  <script src=\"https://cdn.tailwindcss.com\"></script>",
    ]
    if needs_chartjs:
        lines.append("  <script src=\"https://cdn.jsdelivr.net/npm/chart.js\"></script>")
    if needs_plotly:
        lines.append("  <script src=\"https://cdn.plot.ly/plotly-2.30.0.min.js\"></script>")
    lines.extend(
        [
            "  <style>",
            "    :root {",
            f"      --primary: {html_lib.escape(str(theme.get('primary') or '#1a237e'))};",
            f"      --secondary: {html_lib.escape(str(theme.get('secondary') or '#00bcd4'))};",
            f"      --accent: {html_lib.escape(str(theme.get('accent') or '#ff5722'))};",
            f"      --surface: {html_lib.escape(str(theme.get('surface') or '#f8fafc'))};",
            f"      --ink: {html_lib.escape(str(theme.get('ink') or '#111827'))};",
            "    }",
            "    body {",
            "      background: radial-gradient(circle at 10% 0%, rgba(26,35,126,0.10), transparent 45%),",
            "                  radial-gradient(circle at 90% 10%, rgba(0,188,212,0.14), transparent 40%),",
            "                  var(--surface);",
            "      color: var(--ink);",
            "      font-family: \"Pretendard\", \"Noto Sans KR\", \"Segoe UI\", sans-serif;",
            "    }",
            "    .hero {",
            "      background: linear-gradient(120deg, var(--primary), #26369c 50%, var(--secondary));",
            "    }",
            "    .metric-card {",
            "      background: rgba(255,255,255,0.86);",
            "      backdrop-filter: blur(6px);",
            "      border: 1px solid rgba(17,24,39,0.08);",
            "    }",
            "    .chart-card {",
            "      background: #ffffff;",
            "      border-radius: 1rem;",
            "      border: 1px solid rgba(17,24,39,0.08);",
            "      box-shadow: 0 12px 28px rgba(15, 23, 42, 0.09);",
            "    }",
            "    .chart-frame {",
            "      width: 100%;",
            "      min-height: 320px;",
            "      height: 320px;",
            "    }",
            "    @media (max-width: 768px) {",
            "      .chart-frame { min-height: 270px; height: 270px; }",
            "    }",
            "  </style>",
            "</head>",
            "<body class=\"min-h-screen antialiased\">",
            "  <main class=\"max-w-6xl mx-auto px-4 pb-12\">",
            "    <header class=\"hero rounded-2xl text-white p-8 md:p-10 mt-6 shadow-xl\">",
            f"      <h1 class=\"text-2xl md:text-4xl font-black tracking-tight\">{html_lib.escape(title)}</h1>",
            f"      <p class=\"mt-3 text-sm md:text-lg text-cyan-100\">{html_lib.escape(subtitle)}</p>",
            "    </header>",
        ]
    )
    if cards:
        lines.append("    <section class=\"grid grid-cols-1 md:grid-cols-3 gap-4 mt-6\">")
        for card in cards:
            if not isinstance(card, dict):
                continue
            lines.extend(
                [
                    "      <article class=\"metric-card rounded-xl p-4\">",
                    f"        <p class=\"text-xs uppercase tracking-wide text-slate-500\">{html_lib.escape(str(card.get('label') or ''))}</p>",
                    f"        <p class=\"text-2xl font-extrabold mt-1 text-slate-800\">{html_lib.escape(str(card.get('value') or '-'))}</p>",
                    f"        <p class=\"text-xs mt-2 text-slate-500\">{html_lib.escape(str(card.get('hint') or ''))}</p>",
                    "      </article>",
                ]
            )
        lines.append("    </section>")
    lines.append("    <section class=\"space-y-5 mt-6\">")
    for chart in charts:
        if not isinstance(chart, dict):
            continue
        chart_id = html_lib.escape(str(chart.get("dom_id") or ""))
        chart_title = html_lib.escape(str(chart.get("title") or ""))
        chart_desc = html_lib.escape(str(chart.get("description") or ""))
        source = str(chart.get("source") or "").strip()
        note = str(chart.get("note") or "").strip()
        simulated = bool(chart.get("simulated"))
        tokens = []
        if source:
            tokens.append(f"Source: {source}")
        if simulated:
            tokens.append("Label: Simulated/Illustrative")
        if note:
            tokens.append(note)
        meta_text = html_lib.escape(" | ".join(tokens) if tokens else "Source: not specified")
        lines.extend(
            [
                "      <article class=\"chart-card p-5\">",
                f"        <h2 class=\"text-lg font-bold text-slate-900\">{chart_title}</h2>",
                f"        <p class=\"text-sm text-slate-600 mt-1\">{chart_desc}</p>",
            ]
        )
        if str(chart.get("library") or "").lower() == "plotly":
            lines.append(f"        <div id=\"{chart_id}\" class=\"chart-frame mt-3\"></div>")
        else:
            lines.append(f"        <div class=\"chart-frame mt-3\"><canvas id=\"{chart_id}\"></canvas></div>")
        lines.extend(
            [
                f"        <p class=\"text-xs text-slate-500 mt-2\">{meta_text}</p>",
                "      </article>",
            ]
        )
    lines.append("    </section>")
    if disclaimer:
        lines.append(
            "    <p class=\"text-xs text-slate-500 mt-6 bg-white/70 rounded-lg px-3 py-2\">"
            + html_lib.escape(disclaimer)
            + "</p>"
        )
    spec_json = json.dumps(spec, ensure_ascii=False).replace("</", "<\\/")
    lines.extend(
        [
            "  </main>",
            "  <script>",
            f"    const FEDERLICHT_INFOGRAPHIC_SPEC = {spec_json};",
            "    const defaultPalette = [",
            "      FEDERLICHT_INFOGRAPHIC_SPEC.theme?.secondary || '#00bcd4',",
            "      FEDERLICHT_INFOGRAPHIC_SPEC.theme?.primary || '#1a237e',",
            "      FEDERLICHT_INFOGRAPHIC_SPEC.theme?.accent || '#ff5722',",
            "      '#94a3b8',",
            "      '#0ea5e9',",
            "    ];",
            "    const charts = Array.isArray(FEDERLICHT_INFOGRAPHIC_SPEC.charts) ? FEDERLICHT_INFOGRAPHIC_SPEC.charts : [];",
            "    window.__FEDERLICHT_CHARTS_READY__ = false;",
            "    let pendingAsyncRenders = 0;",
            "    const markChartsReady = () => {",
            "      if (pendingAsyncRenders > 0) return;",
            "      if (typeof window.requestAnimationFrame === 'function') {",
            "        window.requestAnimationFrame(() => window.requestAnimationFrame(() => {",
            "          window.__FEDERLICHT_CHARTS_READY__ = true;",
            "        }));",
            "        return;",
            "      }",
            "      window.__FEDERLICHT_CHARTS_READY__ = true;",
            "    };",
            "    charts.forEach((chart) => {",
            "      const library = String(chart.library || 'chartjs').toLowerCase();",
            "      const domId = String(chart.dom_id || '').trim();",
            "      if (!domId) return;",
            "      if (library === 'plotly') {",
            "        if (!window.Plotly) return;",
            "        const host = document.getElementById(domId);",
            "        if (!host) return;",
            "        const plotly = chart.plotly && typeof chart.plotly === 'object' ? chart.plotly : {};",
            "        const traces = Array.isArray(plotly.data) ? plotly.data : [];",
            "        const layout = Object.assign({",
            "          autosize: true,",
            "          margin: { t: 24, r: 16, b: 40, l: 48 },",
            "          paper_bgcolor: '#ffffff',",
            "          plot_bgcolor: '#f8fafc',",
            "          font: { family: 'Pretendard, Noto Sans KR, Segoe UI, sans-serif' },",
            "        }, plotly.layout || {});",
            "        const config = Object.assign({ responsive: true, displayModeBar: false, renderer: 'canvas' }, plotly.config || {});",
            "        if (!traces.length && Array.isArray(chart.datasets) && chart.datasets.length) {",
            "          const fallback = chart.datasets[0] || {};",
            "          traces.push({",
            "            x: Array.isArray(chart.labels) ? chart.labels : [],",
            "            y: Array.isArray(fallback.data) ? fallback.data : [],",
            "            type: chart.type || 'scatter',",
            "            mode: chart.type === 'bar' ? undefined : 'lines+markers',",
            "            marker: { color: fallback.color || defaultPalette[0] },",
            "            name: fallback.label || 'Series',",
            "          });",
            "        }",
            "        if (traces.length) {",
            "          pendingAsyncRenders += 1;",
            "          Promise.resolve(window.Plotly.newPlot(host, traces, layout, config))",
            "            .catch(() => null)",
            "            .finally(() => {",
            "              pendingAsyncRenders -= 1;",
            "              markChartsReady();",
            "            });",
            "        } else {",
            "          markChartsReady();",
            "        }",
            "        return;",
            "      }",
            "      if (!window.Chart) return;",
            "      const canvas = document.getElementById(domId);",
            "      if (!canvas || typeof canvas.getContext !== 'function') return;",
            "      const labels = Array.isArray(chart.labels) ? chart.labels : [];",
            "      const datasetsRaw = Array.isArray(chart.datasets) ? chart.datasets : [];",
            "      if (!datasetsRaw.length) return;",
            "      const datasets = datasetsRaw.map((series, idx) => {",
            "        const color = series.color || defaultPalette[idx % defaultPalette.length];",
            "        return {",
            "          label: String(series.label || `Series ${idx + 1}`),",
            "          data: Array.isArray(series.data) ? series.data : [],",
            "          borderColor: color,",
            "          backgroundColor: color,",
            "          borderWidth: 2,",
            "          tension: 0.25,",
            "          pointRadius: 2,",
            "        };",
            "      });",
            "      const chartType = String(chart.type || 'bar').toLowerCase();",
            "      const options = {",
            "        responsive: true,",
            "        maintainAspectRatio: false,",
            "        plugins: { legend: { position: 'bottom' } },",
            "      };",
            "      if (!['pie', 'doughnut', 'radar', 'polararea'].includes(chartType)) {",
            "        options.scales = { y: { beginAtZero: false } };",
            "      }",
            "      new window.Chart(canvas.getContext('2d'), {",
            "        type: chartType,",
            "        data: { labels, datasets },",
            "        options,",
            "      });",
            "      markChartsReady();",
            "    });",
            "    if (!charts.length) {",
            "      markChartsReady();",
            "    }",
            "    window.setTimeout(markChartsReady, 280);",
            "  </script>",
            "</body>",
            "</html>",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def render_infographic_html(
    run_dir: Path,
    spec_json: str,
    *,
    output_rel_path: str = _DEFAULT_INFOGRAPHIC_OUTPUT,
    page_title: str = "",
) -> dict[str, str]:
    source = str(spec_json or "").strip()
    if not source:
        return {"ok": "false", "error": "empty_spec", "message": "spec_json is empty"}
    try:
        parsed = json.loads(source)
    except Exception as exc:
        return {"ok": "false", "error": "spec_parse_failed", "message": str(exc)[:400]}
    if not isinstance(parsed, dict):
        return {"ok": "false", "error": "invalid_spec", "message": "spec_json must be a JSON object"}

    normalized = _normalize_infographic_spec(parsed, page_title=page_title)
    charts = normalized.get("charts") if isinstance(normalized.get("charts"), list) else []
    if not charts:
        return {"ok": "false", "error": "empty_charts", "message": "spec_json.charts must include at least one chart"}
    out_path = _resolve_under_run(run_dir, output_rel_path or _DEFAULT_INFOGRAPHIC_OUTPUT)
    if out_path.suffix.lower() != ".html":
        out_path = out_path.with_suffix(".html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    run_root = run_dir.resolve()
    run_rel = out_path.relative_to(run_root).as_posix()
    slug = _slugify(Path(run_rel).stem)
    spec_path = run_dir / "report_notes" / f"infographic_spec_{slug}.json"
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")

    needs_chartjs = any(str((item or {}).get("library") or "").lower() == "chartjs" for item in charts if isinstance(item, dict))
    needs_plotly = any(str((item or {}).get("library") or "").lower() == "plotly" for item in charts if isinstance(item, dict))
    html_text = _render_infographic_html(normalized, needs_chartjs=needs_chartjs, needs_plotly=needs_plotly)
    out_path.write_text(html_text, encoding="utf-8")
    rel_out = f"./{run_rel}"
    rel_spec = f"./{spec_path.resolve().relative_to(run_root).as_posix()}"
    title = str(normalized.get("title") or "Data-Driven Infographic")
    caption = f"Infographic: {title}"
    if any(bool((item or {}).get("simulated")) for item in charts if isinstance(item, dict)):
        caption += " (Simulated/Illustrative labels included where applicable)."
    embed_html = (
        '<figure class="report-figure report-infographic">'
        f'<iframe src="{html_lib.escape(rel_out, quote=True)}" loading="lazy" '
        'style="width:100%;min-height:560px;border:0;border-radius:12px;" '
        f'title="{html_lib.escape(title, quote=True)}"></iframe>'
        f"<figcaption>{html_lib.escape(caption)}</figcaption>"
        "</figure>"
    )
    return {
        "ok": "true",
        "path": rel_out,
        "format": "html",
        "data_path": rel_spec,
        "markdown": f"[Infographic HTML]({rel_out})",
        "embed_html": embed_html,
    }
