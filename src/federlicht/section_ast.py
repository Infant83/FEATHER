from __future__ import annotations

import datetime as dt
from typing import Any


def _clean_text(value: object) -> str:
    return str(value or "").strip()


def _claim_title(entry: dict[str, Any]) -> str:
    text = _clean_text(entry.get("claim_text") or entry.get("claim"))
    if not text:
        return "(empty claim)"
    if len(text) <= 160:
        return text
    return f"{text[:157]}..."


def _choose_claim_ids(claims: list[dict[str, Any]], max_items: int = 4) -> list[str]:
    ids: list[str] = []
    for entry in claims[:max_items]:
        claim_id = _clean_text(entry.get("claim_id"))
        if claim_id:
            ids.append(claim_id)
    return ids


def _section_objective(title: str, intent: str) -> str:
    token = title.lower()
    if any(word in token for word in ("method", "scope", "방법")):
        return "Describe methodology, inclusion/exclusion criteria, and boundaries."
    if any(word in token for word in ("result", "finding", "핵심", "benchmark", "결과")):
        return "Present claim-evidence outcomes with traceable references."
    if any(word in token for word in ("risk", "gap", "critic", "한계", "리스크")):
        return "State uncertainty, limits, and unresolved gaps."
    if intent == "briefing":
        return "Deliver concise takeaways and decisions for operators."
    if intent == "decision":
        return "Compare options and provide recommendation conditions."
    return "Synthesize evidence into a coherent narrative for this section."


def build_section_ast(
    *,
    required_sections: list[str],
    claim_packet: dict[str, Any] | None,
    report_intent: str,
    depth: str,
) -> dict[str, Any]:
    section_titles = [str(item).strip() for item in required_sections if str(item).strip()]
    if not section_titles:
        section_titles = ["Executive Summary", "Key Findings", "Risks & Gaps"]
    claims = list((claim_packet or {}).get("claims") or [])
    claim_registry = {
        _clean_text(entry.get("claim_id")): _claim_title(entry)
        for entry in claims
        if _clean_text(entry.get("claim_id"))
    }
    sections: list[dict[str, Any]] = []
    cursor = 0
    for index, title in enumerate(section_titles, start=1):
        if claims:
            claim_slice = claims[cursor : cursor + 4]
            if not claim_slice:
                cursor = 0
                claim_slice = claims[cursor : cursor + 4]
            cursor += max(1, len(claim_slice))
        else:
            claim_slice = []
        section_claim_ids = _choose_claim_ids(claim_slice)
        sections.append(
            {
                "section_id": f"S{index:02d}",
                "title": title,
                "objective": _section_objective(title, report_intent),
                "claim_ids": section_claim_ids,
                "draft": "",
                "revision": "",
            }
        )
    return {
        "schema_version": "section_ast.v1",
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "report_intent": report_intent or "generic",
        "depth": depth or "normal",
        "sections": sections,
        "claim_registry": claim_registry,
    }


def format_section_ast_outline(section_ast: dict[str, Any], *, max_claims: int = 4) -> str:
    sections = list(section_ast.get("sections") or [])
    claim_registry = dict(section_ast.get("claim_registry") or {})
    if not sections:
        return "(no section ast)"
    lines = [
        "Section AST (v1)",
        f"- intent: {section_ast.get('report_intent') or 'generic'}",
        f"- depth: {section_ast.get('depth') or 'normal'}",
        "",
    ]
    for entry in sections:
        section_id = _clean_text(entry.get("section_id")) or "S??"
        title = _clean_text(entry.get("title")) or "(untitled)"
        objective = _clean_text(entry.get("objective")) or "-"
        claim_ids = [str(item).strip() for item in (entry.get("claim_ids") or []) if str(item).strip()]
        lines.append(f"- {section_id} {title}")
        lines.append(f"  objective: {objective}")
        if not claim_ids:
            lines.append("  claims: (none)")
            continue
        lines.append("  claims:")
        for claim_id in claim_ids[:max_claims]:
            claim_text = _clean_text(claim_registry.get(claim_id)) or "(missing claim text)"
            lines.append(f"    - {claim_id}: {claim_text}")
    return "\n".join(lines)


def apply_section_rewrite(
    section_ast: dict[str, Any],
    *,
    section_id: str,
    revised_text: str,
) -> dict[str, Any]:
    out = dict(section_ast or {})
    sections = [dict(item) for item in list(out.get("sections") or [])]
    target = str(section_id or "").strip()
    for entry in sections:
        if str(entry.get("section_id") or "").strip() == target:
            entry["revision"] = str(revised_text or "")
            break
    out["sections"] = sections
    return out


def build_rewrite_tasks(
    section_ast: dict[str, Any],
    *,
    missing_sections: list[str],
    max_claims: int = 3,
) -> list[dict[str, Any]]:
    missing = {str(item).strip().lower() for item in missing_sections if str(item).strip()}
    if not missing:
        return []
    sections = list(section_ast.get("sections") or [])
    claim_registry = dict(section_ast.get("claim_registry") or {})
    tasks: list[dict[str, Any]] = []
    for entry in sections:
        title = _clean_text(entry.get("title"))
        if not title or title.lower() not in missing:
            continue
        claim_ids = [str(item).strip() for item in (entry.get("claim_ids") or []) if str(item).strip()]
        claims = []
        for claim_id in claim_ids[:max_claims]:
            claim_text = _clean_text(claim_registry.get(claim_id))
            if claim_text:
                claims.append({"claim_id": claim_id, "claim_text": claim_text})
        tasks.append(
            {
                "section_id": _clean_text(entry.get("section_id")),
                "title": title,
                "objective": _clean_text(entry.get("objective")),
                "claims": claims,
            }
        )
    return tasks
