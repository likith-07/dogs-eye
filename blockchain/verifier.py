from blockchain.hashing import (
    calculate_hash
)


def verify_evidence(
    block: dict,
    current_evidence: dict
) -> dict:
    """
    Check whether evidence matches the
    evidence originally stored in a block.
    """

    stored_evidence = block.get(
        "evidence"
    )

    stored_hash = calculate_hash(
        stored_evidence
    )

    current_hash = calculate_hash(
        current_evidence
    )


    if stored_hash == current_hash:

        return {
            "verified": True,

            "status":
                "EVIDENCE_MATCHES",

            "stored_evidence_hash":
                stored_hash,

            "current_evidence_hash":
                current_hash
        }


    return {
        "verified": False,

        "status":
            "EVIDENCE_TAMPERED_OR_CHANGED",

        "stored_evidence_hash":
            stored_hash,

        "current_evidence_hash":
            current_hash
    }