from __future__ import annotations

import datetime as dt
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

SLIDE_OUTLINE_SCHEMA_VERSION = "slide_outline.v1"
SLIDE_AST_SCHEMA_VERSION = "slide_ast.v1"

_VALID_DEPTH = {"brief", "normal", "deep", "exhaustive"}
_VALID_VISUAL_TYPES = {"table", "diagram", "image", "bullets", "chart"}
_VALID_INTENTS = {"intro", "methodology", "evidence", "analysis", "risk", "recommendation", "summary"}
_SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"
_SLIDE_OUTLINE_SCHEMA_PATH = _SCHEMA_DIR / "slide_outline_v1.schema.json"
_SLIDE_AST_SCHEMA_PATH = _SCHEMA_DIR / "slide_ast_v1.schema.json"


def _clean_text(value: object) -> str:
    return str(value or "").strip()


def _normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def _truncate_text(text: str, max_len: int) -> str:
    normalized = _normalize_spaces(text)
    if len(normalized) <= max_len:
        return normalized
    if max_len <= 3:
        return normalized[:max_len]
    return f"{normalized[: max_len - 3].rstrip()}..."


def _to_positive_int(value: object, default: int, *, minimum: int = 1, maximum: int = 120) -> int:
    try:
        parsed = int(value)
    except Exception:
        parsed = default
    parsed = max(minimum, parsed)
    return min(maximum, parsed)


def _normalize_depth(value: object) -> str:
    token = _clean_text(value).lower()
    if token in _VALID_DEPTH:
        return token
    return "normal"


def _normalize_section_hint(value: object) -> str:
    token = _clean_text(value).lower()
    if not token:
        return "unspecified"
    token = re.sub(r"[^a-z0-9_]+", "_", token)
    token = re.sub(r"_+", "_", token).strip("_")
    return token or "unspecified"


def _intent_from_section_hint(section_hint: str) -> str:
    token = _normalize_section_hint(section_hint)
    if token in {"executive_summary"}:
        return "intro"
    if token in {"scope_methodology"}:
        return "methodology"
    if token in {"key_findings"}:
        return "evidence"
    if token in {"risks_gaps"}:
        return "risk"
    if token in {"decision_recommendation"}:
        return "recommendation"
    return "analysis"


def _visual_type_for_claim(*, section_hint: str, source_kind: str) -> str:
    section_token = _normalize_section_hint(section_hint)
    source_token = _clean_text(source_kind).lower()
    if section_token == "scope_methodology":
        return "diagram"
    if section_token == "risks_gaps":
        return "bullets"
    if source_token in {"doi", "arxiv"}:
        return "chart"
    if source_token in {"pdf", "image"}:
        return "image"
    return "table"


def _slug_token(value: str) -> str:
    token = re.sub(r"[^a-z0-9]+", "-", _clean_text(value).lower()).strip("-")
    return token or "slide"


def _new_slide_id(index: int) -> str:
    return f"SLIDE-{index:02d}"


def _build_evidence_ref_map(claim_packet: dict[str, Any] | None) -> dict[str, str]:
    mapping: dict[str, str] = {}
    registry = list((claim_packet or {}).get("evidence_registry") or [])
    for item in registry:
        if not isinstance(item, dict):
            continue
        evidence_id = _clean_text(item.get("evidence_id"))
        ref = _clean_text(item.get("ref"))
        if evidence_id and ref:
            mapping[evidence_id] = ref
    return mapping


def _resolve_claim_refs(entry: dict[str, Any], evidence_ref_map: dict[str, str], max_refs: int = 3) -> list[str]:
    refs: list[str] = []
    for evidence_id in list(entry.get("evidence_ids") or []):
        token = _clean_text(evidence_id)
        if not token:
            continue
        resolved = _clean_text(evidence_ref_map.get(token))
        if resolved and resolved not in refs:
            refs.append(resolved)
        if len(refs) >= max_refs:
            break
    if refs:
        return refs
    for ref in list(entry.get("refs") or []):
        token = _clean_text(ref)
        if token and token not in refs:
            refs.append(token)
        if len(refs) >= max_refs:
            break
    return refs


def _default_blueprint(prompt: str, target_slide_count: int) -> list[dict[str, Any]]:
    prompt_line = _truncate_text(prompt or "", 220)
    if not prompt_line:
        prompt_line = "Summarize context, evidence, and decision implications."
    base = [
        {
            "intent": "intro",
            "title": "Problem Framing",
            "key_claim": prompt_line,
            "evidence_refs": [],
            "visual_type": "bullets",
            "section_hint": "executive_summary",
        },
        {
            "intent": "methodology",
            "title": "Scope and Methodology",
            "key_claim": "Define scope boundaries, assumptions, and selection criteria.",
            "evidence_refs": [],
            "visual_type": "diagram",
            "section_hint": "scope_methodology",
        },
        {
            "intent": "evidence",
            "title": "Evidence Snapshot",
            "key_claim": "Summarize strongest evidence and benchmark outcomes.",
            "evidence_refs": [],
            "visual_type": "table",
            "section_hint": "key_findings",
        },
        {
            "intent": "risk",
            "title": "Risks and Gaps",
            "key_claim": "List uncertainty and unresolved validation gaps.",
            "evidence_refs": [],
            "visual_type": "bullets",
            "section_hint": "risks_gaps",
        },
        {
            "intent": "recommendation",
            "title": "Recommendation and Next Step",
            "key_claim": "Provide decision recommendation with execution guardrails.",
            "evidence_refs": [],
            "visual_type": "bullets",
            "section_hint": "decision_recommendation",
        },
    ]
    slides = base[: max(3, target_slide_count)]
    while len(slides) < target_slide_count:
        slides.append(
            {
                "intent": "analysis",
                "title": f"Deep Dive {len(slides) - 1}",
                "key_claim": "Expand evidence interpretation and implications for stakeholders.",
                "evidence_refs": [],
                "visual_type": "chart",
                "section_hint": "unspecified",
            }
        )
    return slides


def _claims_for_outline(claim_packet: dict[str, Any] | None, max_items: int) -> list[dict[str, Any]]:
    claims = [item for item in list((claim_packet or {}).get("claims") or []) if isinstance(item, dict)]
    if not claims:
        return []
    scored_claims: list[tuple[float, dict[str, Any]]] = []
    for entry in claims:
        try:
            score = float(entry.get("score") or 0.0)
        except Exception:
            score = 0.0
        scored_claims.append((score, entry))
    scored_claims.sort(key=lambda row: row[0], reverse=True)
    return [row[1] for row in scored_claims[: max(1, max_items)]]


def build_slide_outline(
    *,
    report_prompt: str,
    depth: str = "normal",
    audience: str = "general",
    time_budget_minutes: int = 20,
    target_slide_count: int = 10,
    claim_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    slide_target = _to_positive_int(target_slide_count, default=10, minimum=3, maximum=40)
    budget_minutes = _to_positive_int(time_budget_minutes, default=20, minimum=5, maximum=240)
    meta = {
        "depth": _normalize_depth(depth),
        "audience": _clean_text(audience) or "general",
        "time_budget_minutes": budget_minutes,
        "target_slide_count": slide_target,
        "source": "claim_packet" if list((claim_packet or {}).get("claims") or []) else "prompt_only",
    }
    slides: list[dict[str, Any]] = []
    evidence_ref_map = _build_evidence_ref_map(claim_packet)
    claims = _claims_for_outline(claim_packet, max_items=max(1, slide_target - 2))
    if claims:
        intro_claim = _truncate_text(report_prompt or "", 220) or "Frame problem and decision objective."
        slides.append(
            {
                "slide_id": _new_slide_id(1),
                "intent": "intro",
                "title": "Executive Framing",
                "key_claim": intro_claim,
                "evidence_refs": [],
                "visual_type": "bullets",
                "section_hint": "executive_summary",
            }
        )
        for claim in claims:
            section_hint = _normalize_section_hint(claim.get("section_hint"))
            intent = _intent_from_section_hint(section_hint)
            claim_text = _truncate_text(_clean_text(claim.get("claim_text") or claim.get("claim")), 240)
            if not claim_text:
                continue
            refs = _resolve_claim_refs(claim, evidence_ref_map)
            slide_title = _truncate_text(f"{section_hint.replace('_', ' ').title()}: {claim_text}", 84)
            slides.append(
                {
                    "slide_id": _new_slide_id(len(slides) + 1),
                    "intent": intent,
                    "title": slide_title,
                    "key_claim": claim_text,
                    "evidence_refs": refs,
                    "visual_type": _visual_type_for_claim(
                        section_hint=section_hint,
                        source_kind=_clean_text(claim.get("source_kind") or "unknown"),
                    ),
                    "section_hint": section_hint,
                }
            )
            if len(slides) >= max(2, slide_target - 1):
                break
        all_refs: list[str] = []
        for item in slides:
            for ref in list(item.get("evidence_refs") or []):
                token = _clean_text(ref)
                if token and token not in all_refs:
                    all_refs.append(token)
                if len(all_refs) >= 4:
                    break
            if len(all_refs) >= 4:
                break
        slides.append(
            {
                "slide_id": _new_slide_id(len(slides) + 1),
                "intent": "summary",
                "title": "Decision Summary",
                "key_claim": "Summarize decision, expected impact, and immediate next actions.",
                "evidence_refs": all_refs,
                "visual_type": "bullets",
                "section_hint": "decision_recommendation",
            }
        )
    else:
        for slide in _default_blueprint(report_prompt, slide_target):
            slides.append(
                {
                    "slide_id": _new_slide_id(len(slides) + 1),
                    **slide,
                }
            )
    if len(slides) > slide_target:
        slides = slides[:slide_target]
    return {
        "schema_version": SLIDE_OUTLINE_SCHEMA_VERSION,
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "meta": meta,
        "slides": slides,
    }


def _split_key_claim_to_bullets(text: str, *, max_items: int = 3) -> list[str]:
    normalized = _normalize_spaces(text)
    if not normalized:
        return []
    parts = [item.strip() for item in re.split(r"[.;]|(?<=[!?])\s+", normalized) if item.strip()]
    bullets: list[str] = []
    for part in parts:
        item = _truncate_text(part, 120)
        if item and item not in bullets:
            bullets.append(item)
        if len(bullets) >= max_items:
            break
    if bullets:
        return bullets
    return [_truncate_text(normalized, 120)]


def _compose_visual_block(*, visual_type: str, title: str, key_claim: str, evidence_refs: list[str]) -> dict[str, Any]:
    token = _clean_text(visual_type).lower()
    if token == "diagram":
        return {
            "type": "diagram",
            "engine": "mermaid",
            "spec": (
                "flowchart LR\n"
                f'  A["{_truncate_text(title, 50)}"] --> B["{_truncate_text(key_claim, 60)}"]\n'
                '  B --> C["Decision / Action"]'
            ),
        }
    if token == "table":
        return {
            "type": "table",
            "columns": ["Claim", "Evidence"],
            "rows": [[_truncate_text(key_claim, 90), _truncate_text(evidence_refs[0], 90) if evidence_refs else "TBD"]],
        }
    if token == "image":
        return {
            "type": "image",
            "path": "",
            "alt": f"Placeholder image for {_truncate_text(title, 80)}",
        }
    if token == "chart":
        return {
            "type": "chart",
            "library": "chartjs",
            "kind": "bar",
            "labels": [_truncate_text(title, 60)],
            "series": [{"label": "Evidence references", "data": [max(0, len(evidence_refs))]}],
        }
    return {"type": "bullets", "items": _split_key_claim_to_bullets(key_claim)}


def _layout_for_visual_type(visual_type: str) -> str:
    token = _clean_text(visual_type).lower()
    if token in {"table", "chart", "diagram", "image"}:
        return "title_two_column"
    return "title_body"


def build_slide_ast(
    outline: dict[str, Any],
    *,
    style_pack: str = "default",
) -> dict[str, Any]:
    slides: list[dict[str, Any]] = []
    for entry in list((outline or {}).get("slides") or []):
        if not isinstance(entry, dict):
            continue
        slide_id = _clean_text(entry.get("slide_id"))
        if not slide_id:
            continue
        title = _truncate_text(_clean_text(entry.get("title")) or "Untitled Slide", 120)
        key_claim = _truncate_text(_clean_text(entry.get("key_claim")), 300)
        intent = _clean_text(entry.get("intent")).lower() or "analysis"
        evidence_refs = [str(item).strip() for item in list(entry.get("evidence_refs") or []) if str(item).strip()]
        visual_type = _clean_text(entry.get("visual_type")).lower() or "bullets"
        body_blocks: list[dict[str, Any]] = [
            {"type": "text", "text": key_claim or "Claim placeholder."},
            _compose_visual_block(
                visual_type=visual_type,
                title=title,
                key_claim=key_claim,
                evidence_refs=evidence_refs,
            ),
        ]
        slide_ast = {
            "slide_id": slide_id,
            "source_outline_id": slide_id,
            "layout": _layout_for_visual_type(visual_type),
            "title_block": {
                "headline": title,
                "subheadline": _truncate_text(intent.replace("_", " ").title(), 80),
            },
            "body_blocks": body_blocks,
            "citation_footer": {
                "refs": evidence_refs,
                "source_policy": "claim-evidence-source",
            },
        }
        slides.append(slide_ast)
    return {
        "schema_version": SLIDE_AST_SCHEMA_VERSION,
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "outline_schema_version": _clean_text(outline.get("schema_version") if isinstance(outline, dict) else ""),
        "style_pack": _clean_text(style_pack) or "default",
        "slides": slides,
    }


def _matches_json_type(value: object, expected_type: str) -> bool:
    token = str(expected_type or "").strip().lower()
    if token == "object":
        return isinstance(value, dict)
    if token == "array":
        return isinstance(value, list)
    if token == "string":
        return isinstance(value, str)
    if token == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if token == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if token == "boolean":
        return isinstance(value, bool)
    if token == "null":
        return value is None
    return True


def _validate_types_by_schema(
    payload: dict[str, Any],
    schema_properties: dict[str, Any],
    *,
    prefix: str,
    errors: list[str],
) -> None:
    for key, spec in schema_properties.items():
        if key not in payload:
            continue
        if not isinstance(spec, dict):
            continue
        expected_type = _clean_text(spec.get("type")).lower()
        if expected_type and not _matches_json_type(payload.get(key), expected_type):
            errors.append(f"{prefix}{key} must be {expected_type}")


def _load_json_schema(path: Path, fallback: dict[str, Any]) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return fallback


@lru_cache(maxsize=1)
def load_slide_outline_schema_v1() -> dict[str, Any]:
    fallback = {
        "required": ["schema_version", "created_at", "meta", "slides"],
        "properties": {
            "schema_version": {"type": "string"},
            "created_at": {"type": "string"},
            "meta": {"type": "object"},
            "slides": {"type": "array"},
        },
    }
    return _load_json_schema(_SLIDE_OUTLINE_SCHEMA_PATH, fallback)


@lru_cache(maxsize=1)
def load_slide_ast_schema_v1() -> dict[str, Any]:
    fallback = {
        "required": ["schema_version", "created_at", "outline_schema_version", "style_pack", "slides"],
        "properties": {
            "schema_version": {"type": "string"},
            "created_at": {"type": "string"},
            "outline_schema_version": {"type": "string"},
            "style_pack": {"type": "string"},
            "slides": {"type": "array"},
        },
    }
    return _load_json_schema(_SLIDE_AST_SCHEMA_PATH, fallback)


def slide_outline_schema_path_v1() -> Path:
    return _SLIDE_OUTLINE_SCHEMA_PATH


def slide_ast_schema_path_v1() -> Path:
    return _SLIDE_AST_SCHEMA_PATH


def validate_slide_outline(outline: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    data = outline if isinstance(outline, dict) else {}
    schema = load_slide_outline_schema_v1()
    schema_required = list(schema.get("required") or [])
    schema_properties = dict(schema.get("properties") or {})
    for key in schema_required:
        if key not in data:
            errors.append(f"missing outline key: {key}")
    _validate_types_by_schema(data, schema_properties, prefix="", errors=errors)
    if _clean_text(data.get("schema_version")) != SLIDE_OUTLINE_SCHEMA_VERSION:
        errors.append(f"schema_version must be {SLIDE_OUTLINE_SCHEMA_VERSION}")
    meta = data.get("meta")
    if not isinstance(meta, dict):
        errors.append("meta must be object")
        meta = {}
    else:
        if _normalize_depth(meta.get("depth")) != _clean_text(meta.get("depth")).lower():
            errors.append("meta.depth must be one of brief|normal|deep|exhaustive")
        if not _clean_text(meta.get("audience")):
            errors.append("meta.audience must be non-empty")
        for field in ("time_budget_minutes", "target_slide_count"):
            value = meta.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                errors.append(f"meta.{field} must be positive integer")
    slides = data.get("slides")
    if not isinstance(slides, list):
        errors.append("slides must be list")
        return errors
    if not slides:
        errors.append("slides must not be empty")
        return errors
    seen_ids: set[str] = set()
    required_slide_fields = ("slide_id", "intent", "title", "key_claim", "evidence_refs", "visual_type")
    for idx, entry in enumerate(slides, start=1):
        if not isinstance(entry, dict):
            errors.append(f"slides[{idx}] must be object")
            continue
        for key in required_slide_fields:
            if key not in entry:
                errors.append(f"slides[{idx}] missing key: {key}")
        slide_id = _clean_text(entry.get("slide_id"))
        if not slide_id:
            errors.append(f"slides[{idx}] empty slide_id")
        elif slide_id in seen_ids:
            errors.append(f"slides[{idx}] duplicate slide_id: {slide_id}")
        else:
            seen_ids.add(slide_id)
        intent = _clean_text(entry.get("intent")).lower()
        if intent not in _VALID_INTENTS:
            errors.append(f"slides[{idx}] intent must be one of {sorted(_VALID_INTENTS)}")
        title = _clean_text(entry.get("title"))
        if not title:
            errors.append(f"slides[{idx}] empty title")
        key_claim = _clean_text(entry.get("key_claim"))
        if not key_claim:
            errors.append(f"slides[{idx}] empty key_claim")
        visual_type = _clean_text(entry.get("visual_type")).lower()
        if visual_type not in _VALID_VISUAL_TYPES:
            errors.append(f"slides[{idx}] visual_type must be one of {sorted(_VALID_VISUAL_TYPES)}")
        refs = entry.get("evidence_refs")
        if not isinstance(refs, list):
            errors.append(f"slides[{idx}] evidence_refs must be list")
            continue
        for ref in refs:
            if not _clean_text(ref):
                errors.append(f"slides[{idx}] evidence_refs contains empty item")
                break
    return errors


def validate_slide_ast(slide_ast: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    data = slide_ast if isinstance(slide_ast, dict) else {}
    schema = load_slide_ast_schema_v1()
    schema_required = list(schema.get("required") or [])
    schema_properties = dict(schema.get("properties") or {})
    for key in schema_required:
        if key not in data:
            errors.append(f"missing slide_ast key: {key}")
    _validate_types_by_schema(data, schema_properties, prefix="", errors=errors)
    if _clean_text(data.get("schema_version")) != SLIDE_AST_SCHEMA_VERSION:
        errors.append(f"schema_version must be {SLIDE_AST_SCHEMA_VERSION}")
    if not _clean_text(data.get("outline_schema_version")):
        errors.append("outline_schema_version must be non-empty")
    if not _clean_text(data.get("style_pack")):
        errors.append("style_pack must be non-empty")
    slides = data.get("slides")
    if not isinstance(slides, list):
        errors.append("slides must be list")
        return errors
    if not slides:
        errors.append("slides must not be empty")
        return errors
    required_slide_fields = ("slide_id", "layout", "title_block", "body_blocks", "citation_footer")
    for idx, entry in enumerate(slides, start=1):
        if not isinstance(entry, dict):
            errors.append(f"slides[{idx}] must be object")
            continue
        for key in required_slide_fields:
            if key not in entry:
                errors.append(f"slides[{idx}] missing key: {key}")
        if not _clean_text(entry.get("slide_id")):
            errors.append(f"slides[{idx}] empty slide_id")
        if not _clean_text(entry.get("layout")):
            errors.append(f"slides[{idx}] empty layout")
        title_block = entry.get("title_block")
        if not isinstance(title_block, dict):
            errors.append(f"slides[{idx}].title_block must be object")
        else:
            if not _clean_text(title_block.get("headline")):
                errors.append(f"slides[{idx}].title_block.headline must be non-empty")
        body_blocks = entry.get("body_blocks")
        if not isinstance(body_blocks, list):
            errors.append(f"slides[{idx}].body_blocks must be list")
        elif not body_blocks:
            errors.append(f"slides[{idx}].body_blocks must not be empty")
        else:
            for block_idx, block in enumerate(body_blocks, start=1):
                if not isinstance(block, dict):
                    errors.append(f"slides[{idx}].body_blocks[{block_idx}] must be object")
                    continue
                if not _clean_text(block.get("type")):
                    errors.append(f"slides[{idx}].body_blocks[{block_idx}] missing type")
        footer = entry.get("citation_footer")
        if not isinstance(footer, dict):
            errors.append(f"slides[{idx}].citation_footer must be object")
            continue
        refs = footer.get("refs")
        if not isinstance(refs, list):
            errors.append(f"slides[{idx}].citation_footer.refs must be list")
        else:
            for ref in refs:
                if not _clean_text(ref):
                    errors.append(f"slides[{idx}].citation_footer.refs contains empty item")
                    break
        if not _clean_text(footer.get("source_policy")):
            errors.append(f"slides[{idx}].citation_footer.source_policy must be non-empty")
    return errors


def format_slide_outline(outline: dict[str, Any], *, max_items: int = 16) -> str:
    meta = dict((outline or {}).get("meta") or {})
    slides = [entry for entry in list((outline or {}).get("slides") or []) if isinstance(entry, dict)]
    if not slides:
        return "(no slide outline)"
    lines = [
        "Slide Outline (v1)",
        f"- depth: {_clean_text(meta.get('depth')) or 'normal'}",
        f"- audience: {_clean_text(meta.get('audience')) or 'general'}",
        f"- time budget: {_clean_text(meta.get('time_budget_minutes')) or '-'} min",
        f"- target slides: {_clean_text(meta.get('target_slide_count')) or len(slides)}",
        "",
    ]
    for entry in slides[: max(1, max_items)]:
        slide_id = _clean_text(entry.get("slide_id")) or "SLIDE-??"
        title = _clean_text(entry.get("title")) or "(untitled)"
        intent = _clean_text(entry.get("intent")) or "analysis"
        visual_type = _clean_text(entry.get("visual_type")) or "bullets"
        refs = [str(item).strip() for item in list(entry.get("evidence_refs") or []) if str(item).strip()]
        lines.append(f"- {slide_id} [{intent}/{visual_type}] {title}")
        lines.append(f"  claim: {_truncate_text(_clean_text(entry.get('key_claim')), 150)}")
        lines.append(f"  refs: {', '.join(refs[:3]) if refs else '(none)'}")
    return "\n".join(lines)


def format_slide_ast(slide_ast: dict[str, Any], *, max_items: int = 16) -> str:
    slides = [entry for entry in list((slide_ast or {}).get("slides") or []) if isinstance(entry, dict)]
    if not slides:
        return "(no slide ast)"
    lines = [
        "Slide AST (v1)",
        f"- style pack: {_clean_text(slide_ast.get('style_pack')) or 'default'}",
        f"- slides: {len(slides)}",
        "",
    ]
    for entry in slides[: max(1, max_items)]:
        slide_id = _clean_text(entry.get("slide_id")) or "SLIDE-??"
        layout = _clean_text(entry.get("layout")) or "title_body"
        title_block = dict(entry.get("title_block") or {})
        headline = _clean_text(title_block.get("headline")) or "(untitled)"
        body_blocks = [block for block in list(entry.get("body_blocks") or []) if isinstance(block, dict)]
        block_types = ",".join(_clean_text(block.get("type")) for block in body_blocks if _clean_text(block.get("type")))
        footer = dict(entry.get("citation_footer") or {})
        refs = [str(item).strip() for item in list(footer.get("refs") or []) if str(item).strip()]
        lines.append(f"- {slide_id} [{layout}] {headline}")
        lines.append(f"  blocks: {block_types or '(none)'}")
        lines.append(f"  refs: {', '.join(refs[:3]) if refs else '(none)'}")
    return "\n".join(lines)

