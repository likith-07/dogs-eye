from typing import Dict, Any

def score_identity(target_handle: str, discovered_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates OSINT evidence to determine if the discovered profile 
    belongs to the original target.
    """
    profile = discovered_profile.copy()
    score = 0
    evidence_tags = []

    # 1. Base Username Match (Low Evidence)
    if profile["username"].lower() == target_handle.lower():
        score += 20
        evidence_tags.append("EXACT HANDLE MATCH")

    # Future integration: If metadata (Display Name, Location, Linktree) was scraped:
    # if profile.get('metadata', {}).get('display_name') == target_metadata['display_name']:
    #     score += 30
    #     evidence_tags.append("DISPLAY NAME MATCH")

    # Determine OSINT Confidence
    if score >= 80:
        confidence = "HIGH"
    elif score >= 50:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"
        if not evidence_tags:
            evidence_tags.append("UNVERIFIED HANDLE HYPOTHESIS")

    profile["evidence"] = " + ".join(evidence_tags)
    profile["confidence"] = confidence
    
    return profile