from typing import Dict, Any
from username_investigation.extractor import extract_username
from username_investigation.variants import generate_username_variants
from username_investigation.platform_search import build_platform_candidates


def investigate_username(confirmed_url: str) -> Dict[str, Any]:
    """
    Orchestrates extraction, variant generation, and platform profile lookup.
    """
    extracted_handle = extract_username(confirmed_url)

    if not extracted_handle:
        return {
            "success": False,
            "error": f"Could not extract username from: {confirmed_url}",
            "original_url": confirmed_url,
            "results": []
        }

    variants = generate_username_variants(extracted_handle)
    candidates = build_platform_candidates(variants)

    return {
        "success": True,
        "original_url": confirmed_url,
        "extracted_username": extracted_handle,
        "total_variants": len(variants),
        "total_candidates": len(candidates),
        "results": candidates
    }