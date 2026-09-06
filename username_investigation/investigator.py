from typing import Dict, Any
from username_investigation.dorking import sweep_external_endpoints
from username_investigation.correlation import score_identity

def investigate_identity(target_handle: str) -> Dict[str, Any]:
    """Master orchestrator for the identity correlation pipeline."""
    target_handle = target_handle.strip().replace("@", "")

    # 1. Broad Discovery (WhatsMyName External Sweep)
    raw_discovered = sweep_external_endpoints(target_handle)

    # 2. Identity Verification (Correlation Scoring)
    verified_results = [
        score_identity(target_handle, profile) for profile in raw_discovered
    ]

    return {
        "success": True,
        "extracted_username": target_handle,
        "total_discovered": len(verified_results),
        "results": verified_results
    }