from typing import List, Dict, Any

TARGET_PLATFORMS = {
    "instagram": "https://www.instagram.com/{username}/",
    "x": "https://x.com/{username}",
    "tiktok": "https://www.tiktok.com/@{username}",
    "threads": "https://www.threads.net/@{username}",
    "youtube": "https://www.youtube.com/@{username}",
    "facebook": "https://www.facebook.com/{username}",
    "linkedin": "https://www.linkedin.com/in/{username}",
    "github": "https://github.com/{username}"
}


def build_platform_candidates(variants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generates cross-platform links for each username variant.
    """
    candidates = []

    for item in variants:
        username = item["username"]
        match_type = item["match_type"]
        confidence = item["confidence"]

        for platform, url_template in TARGET_PLATFORMS.items():
            profile_url = url_template.format(username=username)
            candidates.append({
                "platform": platform,
                "username": username,
                "profile_url": profile_url,
                "match_type": match_type,
                "confidence": confidence
            })

    return candidates