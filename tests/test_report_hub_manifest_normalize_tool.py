from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module():
    path = Path("tools/normalize_report_hub_manifest.py")
    spec = importlib.util.spec_from_file_location("normalize_report_hub_manifest", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tool = _load_module()


def test_normalize_manifest_promotes_legacy_quality_and_tags() -> None:
    payload = {
        "items": [
            {
                "id": "demo-deck",
                "format": "pptx",
                "paths": {"report": "../runs/demo/deck.html"},
                "deck_quality_profile": "deep_research",
                "deck_quality_effective_band": "deep_research",
                "deck_quality_overall": 91.2,
                "deck_quality_gate_pass": True,
                "deck_quality_iterations": 2,
                "tags": ["demo"],
            }
        ]
    }
    normalized, stats = tool.normalize_manifest_payload(payload)
    items = normalized.get("items")
    assert isinstance(items, list) and items
    row = items[0]
    paths = dict(row.get("paths") or {})
    assert paths.get("deck_html") == "../runs/demo/deck.html"
    quality = dict(row.get("deck_quality") or {})
    assert quality.get("profile") == "deep_research"
    assert quality.get("effective_band") == "deep_research"
    assert quality.get("overall") == 91.2
    assert quality.get("gate_pass") is True
    assert quality.get("iterations") == 2
    tags = list(row.get("tags") or [])
    assert "deck:deep_research" in tags
    assert "deck-pass" in tags
    assert int(stats.get("quality_from_legacy_flat", 0) or 0) == 1


def test_normalize_manifest_keeps_existing_quality_object() -> None:
    payload = {
        "items": [
            {
                "id": "demo2",
                "format": "pptx",
                "paths": {"report": "../runs/demo/deck.pptx"},
                "deck_quality": {
                    "profile": "professional",
                    "effective_band": "professional",
                    "overall": 80.0,
                    "gate_pass": False,
                    "iterations": 1,
                },
                "tags": [],
            }
        ]
    }
    normalized, stats = tool.normalize_manifest_payload(payload)
    row = normalized["items"][0]
    paths = dict(row.get("paths") or {})
    assert paths.get("deck_pptx") == "../runs/demo/deck.pptx"
    quality = dict(row.get("deck_quality") or {})
    assert quality.get("profile") == "professional"
    assert quality.get("gate_pass") is False
    tags = list(row.get("tags") or [])
    assert "deck:professional" in tags
    assert "deck-fail" in tags
    assert int(stats.get("quality_from_legacy_flat", 0) or 0) == 0
