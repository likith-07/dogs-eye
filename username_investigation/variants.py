import re
from typing import List, Dict, Any


def generate_username_variants(base_username: str) -> List[Dict[str, Any]]:
    """
    Generates conservative handle variants with calibrated risk confidence scores.
    """
    if not base_username:
        return []

    variants = []
    seen = set()

    def add_variant(handle: str, match_type: str, confidence: str):
        cleaned = handle.lower().strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            variants.append({
                "username": handle,
                "match_type": match_type,
                "confidence": confidence
            })

    # Exact extracted handle (Marked as MEDIUM for cross-platform matches until verified)
    add_variant(base_username, "EXACT HANDLE MATCH", "MEDIUM")

    # Format variation: Dots removed
    no_dots = base_username.replace(".", "")
    if no_dots != base_username:
        add_variant(no_dots, "FORMAT VARIATION (NO DOTS)", "MEDIUM")

    # Format variation: Underscores removed
    no_underscores = base_username.replace("_", "")
    if no_underscores != base_username:
        add_variant(no_underscores, "FORMAT VARIATION (NO UNDERSCORES)", "MEDIUM")

    # Format variation: Both removed
    no_delimiters = base_username.replace(".", "").replace("_", "")
    if no_delimiters not in [base_username, no_dots, no_underscores]:
        add_variant(no_delimiters, "FORMAT VARIATION (CLEAN)", "LOW")

    # Similar handle: Trailing numbers removed
    base_no_nums = re.sub(r"\d+$", "", base_username)
    if base_no_nums and base_no_nums != base_username and len(base_no_nums) >= 3:
        add_variant(base_no_nums, "BASE HANDLE HYPOTHESIS", "LOW")

    return variants