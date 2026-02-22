from federlicht import tools


def test_evidence_packet_schema_v1_contract_loaded() -> None:
    schema = tools.evidence_packet_schema_v1()
    required = set(schema.get("required") or [])
    assert "schema_version" in required
    claim_required = set(
        ((schema.get("properties") or {}).get("claims") or {}).get("items", {}).get("required", [])
    )
    assert "claim_text" in claim_required
    assert "evidence_ids" in claim_required


def test_build_claim_evidence_packet_infers_section_hint_from_claim_text() -> None:
    claims = [
        {
            "claim": "방법론과 scope를 먼저 공개해야 한다",
            "evidence": ["./archive/openalex/works.jsonl"],
            "evidence_strength": "medium",
            "flags": [],
        }
    ]
    packet = tools.build_claim_evidence_packet(claims, focus_text="research")
    selected = packet.get("claims") or []
    assert selected
    assert selected[0].get("section_hint") == "scope_methodology"
