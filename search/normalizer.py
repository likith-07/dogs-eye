from urllib.parse import urlparse


SOCIAL_MEDIA_DOMAINS = {
    "x.com",
    "twitter.com",
    "instagram.com",
    "facebook.com",
    "tiktok.com",
    "threads.com",
    "youtube.com",
}


def is_social_media_url(url):
    """
    Check whether a URL belongs to a supported social-media platform.
    """

    try:
        hostname = urlparse(url).hostname

        if not hostname:
            return False

        hostname = hostname.lower()

        return any(
            hostname == domain or hostname.endswith("." + domain)
            for domain in SOCIAL_MEDIA_DOMAINS
        )

    except Exception:
        return False


def normalize_candidates(*candidate_lists):
    """
    Merge candidate lists from multiple providers, keep only social-media
    results, and remove duplicates.
    """

    merged = []
    seen_urls = set()

    for candidates in candidate_lists:
        for candidate in candidates:
            page_url = candidate.get("page_url")

            if not page_url:
                continue

            if not is_social_media_url(page_url):
                continue

            normalized_url = page_url.rstrip("/")

            if normalized_url in seen_urls:
                continue

            seen_urls.add(normalized_url)

            merged.append(
                {
                    "page_url": page_url,
                    "image_url": candidate.get("image_url") or "",
                    "title": candidate.get("title") or "",
                    "source": candidate.get("source") or "",
                    "provider": candidate.get("provider") or "",
                    "search_rank": candidate.get("search_rank") or 0,
                }
            )

    return merged