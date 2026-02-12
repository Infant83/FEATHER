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
