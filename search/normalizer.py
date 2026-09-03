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


def extract_author(url):
    """
    Extract the author/username when it is unambiguously present
    in the social-media URL.

    Returns:
        str | None: Author/username if reliably available, otherwise None.
    """

    try:
        parsed = urlparse(url)
        hostname = parsed.hostname.lower() if parsed.hostname else ""
        parts = [part for part in parsed.path.split("/") if part]

        # X / Twitter:
        # https://x.com/username/status/123456
        if hostname in {"x.com", "twitter.com"}:
            if len(parts) >= 2 and parts[1] == "status":
                if parts[0] not in {"i", "home", "search"}:
                    return parts[0]

        # TikTok:
        # https://www.tiktok.com/@username/video/123456
        if hostname == "tiktok.com" or hostname.endswith(".tiktok.com"):
            if parts and parts[0].startswith("@"):
                return parts[0][1:]

        # Threads:
        # https://www.threads.com/@username/post/123456
        if hostname == "threads.com" or hostname.endswith(".threads.com"):
            if parts and parts[0].startswith("@"):
                return parts[0][1:]

    except Exception:
        pass

    return None


def normalize_candidates(*candidate_lists):
    """
    Merge candidate lists from multiple providers, keep only supported
    social-media results, extract authors where possible, and remove duplicates.
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
                    "author": candidate.get("author") or extract_author(page_url),
                }
            )

    return merged