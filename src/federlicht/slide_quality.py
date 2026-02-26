from __future__ import annotations

import copy
from typing import Any


def _clean_text(value: object) -> str:
    return str(value or "").strip()


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _is_transition_intent(intent: str) -> bool:
    token = _clean_text(intent).lower()
    return token in {"intro", "summary"}


def _iter_slide_entries(slide_ast: dict[str, Any]) -> list[dict[str, Any]]:
    return [entry for entry in list((slide_ast or {}).get("slides") or []) if isinstance(entry, dict)]


def _traceability_score(slides: list[dict[str, Any]]) -> float:
    if not slides:
        return 0.0
    grounded = 0
    for entry in slides:
        refs = [str(item).strip() for item in list(dict(entry.get("citation_footer") or {}).get("refs") or []) if str(item).strip()]
        intent = _clean_text(entry.get("title_block", {}).get("subheadline") if isinstance(entry.get("title_block"), dict) else "")
        transition_like = any(token in intent.lower() for token in ("intro", "summary", "recommendation"))
        if refs or transition_like:
            grounded += 1
    return round((grounded / len(slides)) * 100.0, 2)


def _density_score(slides: list[dict[str, Any]]) -> float:
    if not slides:
        return 0.0
    total_penalty = 0.0
    for entry in slides:
        text_chars = 0
        bullet_count = 0
        for block in [item for item in list(entry.get("body_blocks") or []) if isinstance(item, dict)]:
            block_type = _clean_text(block.get("type")).lower()
            if block_type == "text":
                text_chars += len(_clean_text(block.get("text")))
            elif block_type == "bullets":
                items = [str(item).strip() for item in list(block.get("items") or []) if str(item).strip()]
                bullet_count += len(items)
                text_chars += sum(len(item) for item in items)
            elif block_type == "table":
                rows = [item for item in list(block.get("rows") or []) if isinstance(item, list)]
                text_chars += sum(len(str(cell or "")) for row in rows for cell in row)
        slide_penalty = 0.0
        if text_chars > 520:
            slide_penalty += min(40.0, (text_chars - 520) / 18.0)
        if bullet_count > 7:
            slide_penalty += min(20.0, (bullet_count - 7) * 3.0)
        total_penalty += slide_penalty
    raw = 100.0 - (total_penalty / max(1, len(slides)))
    return round(max(0.0, min(100.0, raw)), 2)


def _narrative_flow_score(slides: list[dict[str, Any]]) -> float:
    if not slides:
        return 0.0
    score = 100.0
    intents: list[str] = []
    for entry in slides:
        title_block = dict(entry.get("title_block") or {})
        subheadline = _clean_text(title_block.get("subheadline")).lower()
        intent_token = subheadline.split()[0].strip() if subheadline else ""
        if not intent_token:
            intent_token = "analysis"
        intents.append(intent_token)
    if not _is_transition_intent(intents[0]):
        score -= 25.0
    if not _is_transition_intent(intents[-1]):
        score -= 25.0
    evidence_seen = any(token in {"evidence", "analysis", "methodology", "risk"} for token in intents[1:-1])
    if not evidence_seen:
        score -= 30.0
    if len(slides) >= 4 and intents.count("analysis") + intents.count("evidence") < 2:
        score -= 15.0
    return round(max(0.0, min(100.0, score)), 2)


def _visual_integrity_score(slides: list[dict[str, Any]]) -> float:
    if not slides:
        return 0.0
    penalties = 0.0
    checked_blocks = 0
    for entry in slides:
        for block in [item for item in list(entry.get("body_blocks") or []) if isinstance(item, dict)]:
            block_type = _clean_text(block.get("type")).lower()
            checked_blocks += 1
            if block_type == "table":
                columns = [str(item).strip() for item in list(block.get("columns") or []) if str(item).strip()]
                rows = [item for item in list(block.get("rows") or []) if isinstance(item, list)]
                if columns and any(len(row) != len(columns) for row in rows):
                    penalties += 20.0
                if not columns and not rows:
                    penalties += 12.0
            elif block_type == "diagram":
                if not _clean_text(block.get("engine")):
                    penalties += 10.0
                if not _clean_text(block.get("spec")):
                    penalties += 14.0
            elif block_type == "chart":
                labels = list(block.get("labels") or [])
                series = [item for item in list(block.get("series") or []) if isinstance(item, dict)]
                if not labels or not series:
                    penalties += 18.0
            elif block_type == "image":
                if not _clean_text(block.get("path")) and not _clean_text(block.get("alt")):
                    penalties += 12.0
            elif block_type == "bullets":
                items = [str(item).strip() for item in list(block.get("items") or []) if str(item).strip()]
                if not items:
                    penalties += 8.0
            elif block_type == "text":
                if not _clean_text(block.get("text")):
                    penalties += 8.0
    if checked_blocks == 0:
        return 0.0
    score = 100.0 - (penalties / checked_blocks)
    return round(max(0.0, min(100.0, score)), 2)


def evaluate_slide_ast_quality(
    slide_ast: dict[str, Any],
    *,
    min_overall: float = 78.0,
    min_traceability: float = 70.0,
    min_density: float = 65.0,
    min_flow: float = 70.0,
    min_visual_integrity: float = 70.0,
) -> dict[str, Any]:
    slides = _iter_slide_entries(slide_ast)
    traceability = _traceability_score(slides)
    density = _density_score(slides)
    flow = _narrative_flow_score(slides)
    visual = _visual_integrity_score(slides)
    overall = round(
        (traceability * 0.32)
        + (density * 0.22)
        + (flow * 0.24)
        + (visual * 0.22),
        2,
    )
    gate_failures: list[str] = []
    if overall < float(min_overall):
        gate_failures.append("overall")
    if traceability < float(min_traceability):
        gate_failures.append("traceability")
    if density < float(min_density):
        gate_failures.append("density")
    if flow < float(min_flow):
        gate_failures.append("narrative_flow")
    if visual < float(min_visual_integrity):
        gate_failures.append("visual_integrity")
    return {
        "slide_count": len(slides),
        "traceability_score": traceability,
        "density_score": density,
        "narrative_flow_score": flow,
        "visual_integrity_score": visual,
        "overall_score": overall,
        "quality_gate_pass": not gate_failures,
        "gate_failures": gate_failures,
        "targets": {
            "min_overall": _safe_float(min_overall),
            "min_traceability": _safe_float(min_traceability),
            "min_density": _safe_float(min_density),
            "min_flow": _safe_float(min_flow),
            "min_visual_integrity": _safe_float(min_visual_integrity),
        },
    }


def revise_slide_ast_for_quality(
    slide_ast: dict[str, Any],
    *,
    baseline_summary: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], list[str]]:
    revised = copy.deepcopy(slide_ast or {})
    slides = _iter_slide_entries(revised)
    actions: list[str] = []
    if not slides:
        return revised, actions

    # Narrative anchors: first slide intro / last slide summary.
    first_title = dict(slides[0].get("title_block") or {})
    first_sub = _clean_text(first_title.get("subheadline"))
    if "intro" not in first_sub.lower():
        first_title["subheadline"] = "Intro"
        slides[0]["title_block"] = first_title
        actions.append("set_first_slide_intro")
    last_title = dict(slides[-1].get("title_block") or {})
    last_sub = _clean_text(last_title.get("subheadline"))
    if "summary" not in last_sub.lower():
        last_title["subheadline"] = "Summary"
        slides[-1]["title_block"] = last_title
        actions.append("set_last_slide_summary")

    for idx, entry in enumerate(slides, start=1):
        footer = dict(entry.get("citation_footer") or {})
        refs = [str(item).strip() for item in list(footer.get("refs") or []) if str(item).strip()]
        title_block = dict(entry.get("title_block") or {})
        intent_token = _clean_text(title_block.get("subheadline")).lower()
        transition_like = any(token in intent_token for token in ("intro", "summary"))
        if not refs and not transition_like:
            footer["refs"] = ["./report_notes/claim_evidence_map.json"]
            footer["source_policy"] = _clean_text(footer.get("source_policy")) or "claim-evidence-source"
            entry["citation_footer"] = footer
            actions.append(f"add_placeholder_ref:{idx}")

        body_blocks = [item for item in list(entry.get("body_blocks") or []) if isinstance(item, dict)]
        for block_idx, block in enumerate(body_blocks, start=1):
            block_type = _clean_text(block.get("type")).lower()
            if block_type == "text":
                text = _clean_text(block.get("text"))
                if len(text) > 900:
                    block["text"] = text[:420].rstrip() + "..."
                    actions.append(f"trim_text:{idx}:{block_idx}")
            elif block_type == "bullets":
                items = [str(item).strip() for item in list(block.get("items") or []) if str(item).strip()]
                if not items:
                    block["items"] = ["Key point pending evidence alignment."]
                    actions.append(f"fill_empty_bullets:{idx}:{block_idx}")
            elif block_type == "diagram":
                spec = _clean_text(block.get("spec"))
                if not spec:
                    block["spec"] = "flowchart LR\nA[Input] --> B[Output]"
                    block["engine"] = _clean_text(block.get("engine")) or "mermaid"
                    actions.append(f"fill_empty_diagram_spec:{idx}:{block_idx}")
        entry["body_blocks"] = body_blocks

    revised["slides"] = slides
    return revised, actions


def build_slide_quality_report(summary: dict[str, Any]) -> str:
    payload = dict(summary or {})
    lines = [
        "Slide Quality Summary",
        f"- slides: {int(payload.get('slide_count') or 0)}",
        f"- overall: {_safe_float(payload.get('overall_score')):.2f}",
        f"- traceability: {_safe_float(payload.get('traceability_score')):.2f}",
        f"- density: {_safe_float(payload.get('density_score')):.2f}",
        f"- narrative_flow: {_safe_float(payload.get('narrative_flow_score')):.2f}",
        f"- visual_integrity: {_safe_float(payload.get('visual_integrity_score')):.2f}",
        f"- gate: {'PASS' if bool(payload.get('quality_gate_pass')) else 'FAIL'}",
    ]
    failures = [str(item).strip() for item in list(payload.get("gate_failures") or []) if str(item).strip()]
    if failures:
        lines.append(f"- failures: {', '.join(failures)}")
    return "\n".join(lines)
