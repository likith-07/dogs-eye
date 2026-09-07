import hashlib
import json
from typing import Dict, Any


def canonicalize_evidence(
    evidence: Dict[str, Any]
) -> str:
    """
    Convert evidence into deterministic JSON.

    Deterministic serialization is required so that
    the same evidence always produces the same hash.
    """

    return json.dumps(
        evidence,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    )


def hash_evidence(
    evidence: Dict[str, Any]
) -> str:
    """
    Create a SHA-256 hash of canonical evidence.
    """

    canonical_evidence = canonicalize_evidence(
        evidence
    )

    return hashlib.sha256(
        canonical_evidence.encode("utf-8")
    ).hexdigest()