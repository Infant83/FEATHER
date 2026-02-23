from federlicht import tools


def test_build_claim_evidence_packet_prefers_direct_sources() -> None:
    claims = [
        {
            "claim": "색인은 근거가 약하다",
            "evidence": ["./archive/tavily_search.jsonl"],
            "evidence_strength": "low",
            "flags": ["index_only"],
        },
        {
            "claim": "직접 소스가 있는 주장은 우선되어야 한다",
            "evidence": ["https://example.com/paper", "./archive/web/text/paper.txt"],
            "evidence_strength": "high",
            "flags": [],
        },
    ]

    packet = tools.build_claim_evidence_packet(
        claims,
        focus_text="직접 소스 주장",
        top_k=5,
        max_refs_per_claim=2,
        include_index_only=False,
    )

    selected = packet.get("claims") or []
    assert selected
    assert all("index_only" not in (entry.get("flags") or []) for entry in selected)
    assert any(entry.get("evidence_ids") for entry in selected)
    assert packet.get("schema_version") == "v1"
    assert all("claim_text" in entry for entry in selected)
    assert all("strength" in entry for entry in selected)
    assert all("source_kind" in entry for entry in selected)
    assert all("recency" in entry for entry in selected)


def test_format_claim_evidence_packet_contains_claim_and_evidence_ids() -> None:
    packet = {
        "stats": {"selected_claims": 1, "total_claims": 1, "selected_evidence": 1, "index_only_ratio": 0.0},
        "claims": [
            {
                "claim_id": "C001",
                "claim": "핵심 주장",
                "evidence_strength": "high",
                "flags": [],
                "evidence_ids": ["E001"],
            }
        ],
        "evidence_registry": [{"evidence_id": "E001", "ref": "https://example.com"}],
    }

    text = tools.format_claim_evidence_packet(packet)

    assert "Claim-Evidence Packet" in text
    assert "C001" in text
    assert "E001" in text


def test_normalize_claim_evidence_packet_converts_legacy_claim_fields() -> None:
    legacy_packet = {
        "created_at": "2026-02-22T10:00:00",
        "stats": {"selected_claims": 1, "total_claims": 1, "selected_evidence": 1, "index_only_ratio": 0.0},
        "focus": "legacy",
        "claims": [
            {
                "claim_id": "C007",
                "claim": "legacy claim",
                "evidence_strength": "high",
                "flags": [],
                "evidence_ids": ["E001"],
                "refs": ["https://example.com/paper"],
            }
        ],
        "evidence_registry": [{"evidence_id": "E001", "ref": "https://example.com/paper"}],
    }
    packet = tools.normalize_claim_evidence_packet(legacy_packet)
    assert packet["schema_version"] == "v1"
    assert packet["claims"][0]["claim_text"] == "legacy claim"
    assert packet["claims"][0]["strength"] == "high"
    assert packet["claims"][0]["section_hint"] == "unspecified"


def test_validate_claim_evidence_packet_v1_reports_missing_keys() -> None:
    invalid_packet = {
        "schema_version": "v1",
        "created_at": "2026-02-22T10:00:00",
        "stats": {},
        "focus": "bad",
        "claims": [{"claim_id": "C001", "claim_text": "x"}],
        "evidence_registry": [],
    }
    errors = tools.validate_claim_evidence_packet_v1(invalid_packet)
    assert errors
    assert any("missing key" in err for err in errors)


def test_validate_claim_evidence_packet_v1_accepts_normalized_packet() -> None:
    claims = [
        {
            "claim": "직접 소스가 있는 주장은 우선되어야 한다",
            "evidence": ["https://example.com/paper", "./archive/web/text/paper.txt"],
            "evidence_strength": "high",
            "flags": [],
        },
    ]
    packet = tools.build_claim_evidence_packet(claims, focus_text="직접 소스 주장")
    normalized = tools.normalize_claim_evidence_packet(packet)
    errors = tools.validate_claim_evidence_packet_v1(normalized)
    assert errors == []


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
