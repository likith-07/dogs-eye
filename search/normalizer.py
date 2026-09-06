from typing import List, Dict, Any

def normalize_candidates(candidates: List[Any]) -> List[Dict[str, Any]]:
    """
    Standardizes search results from multiple providers into a uniform dictionary structure.
    Handles both SearchAPI formatting and FaceFinder Data URI formatting.
    """
    normalized_list = []

    for item in candidates:
        if not isinstance(item, dict):
            continue

        normalized_item = {}

        # ----------------------------------------------------
        # Detect FaceFinder Formatting
        # (Relies on 'guid', 'base64', and 'score' keys)
        # ----------------------------------------------------
        if "base64" in item and "guid" in item:
            url_val = item.get("url", "")
            source_domain = "FaceFinder"
            if "instagram.com" in url_val.lower():
                source_domain = "Instagram"
            elif "facebook.com" in url_val.lower():
                source_domain = "Facebook"
            elif "twitter.com" in url_val.lower() or "x.com" in url_val.lower():
                source_domain = "Twitter/X"

            normalized_item = {
                "title": f"FaceFinder Match: {item.get('guid', 'Unknown')}",
                "source": source_domain,
                "page_url": url_val,
                # Explicitly capture base64 data URI so filtering doesn't drop it
                "image_url": item.get("base64") or url_val,
                "provider": "facefinder",
                "search_rank": item.get("score", "N/A")
            }

        # ----------------------------------------------------
        # Detect Standard Web SearchAPI Formatting
        # ----------------------------------------------------
        else:
            normalized_item = {
                "title": item.get("title") or item.get("name") or "SearchAPI Result",
                "source": item.get("source") or item.get("domain") or "Web Search",
                "page_url": item.get("link") or item.get("url") or item.get("page_url", ""),
                "image_url": item.get("thumbnail") or item.get("image") or item.get("image_url", ""),
                "provider": item.get("provider", "searchapi"),
                "search_rank": item.get("rank") or item.get("position", "N/A")
            }
        
        normalized_list.append(normalized_item)

    return normalized_list