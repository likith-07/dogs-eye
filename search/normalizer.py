from urllib.parse import urlparse


# ============================================================
# SUPPORTED SOCIAL MEDIA DOMAINS
# ============================================================

SOCIAL_MEDIA_DOMAINS = {
    "x.com",
    "twitter.com",
    "instagram.com",
    "facebook.com",
    "tiktok.com",
    "threads.com",
    "youtube.com",
    "linkedin.com",
}


# ============================================================
# CHECK SOCIAL MEDIA
# ============================================================

def is_social_media_url(url):
    """
    Check whether a URL belongs to a supported
    social-media platform.
    """

    if not url:
        return False

    try:

        hostname = urlparse(url).hostname

        if not hostname:
            return False

        hostname = hostname.lower()

        return any(

            hostname == domain
            or hostname.endswith("." + domain)

            for domain in SOCIAL_MEDIA_DOMAINS
        )

    except Exception:

        return False


# ============================================================
# EXTRACT AUTHOR / USERNAME
# ============================================================

def extract_author(url):
    """
    Extract an author or username when it can be
    reliably determined from a social-media URL.
    """

    if not url:
        return None

    try:

        parsed = urlparse(url)

        hostname = (
            parsed.hostname.lower()
            if parsed.hostname
            else ""
        )

        parts = [

            part

            for part in parsed.path.split("/")

            if part

        ]

        # ----------------------------------------------------
        # X / TWITTER
        #
        # https://x.com/username/status/123
        # ----------------------------------------------------

        if hostname in {
            "x.com",
            "twitter.com"
        }:

            if (
                len(parts) >= 2
                and parts[1] == "status"
            ):

                if parts[0] not in {
                    "i",
                    "home",
                    "search"
                }:

                    return parts[0]

        # ----------------------------------------------------
        # TIKTOK
        #
        # https://www.tiktok.com/@username/video/123
        # ----------------------------------------------------

        if (
            hostname == "tiktok.com"
            or hostname.endswith(
                ".tiktok.com"
            )
        ):

            if (
                parts
                and parts[0].startswith("@")
            ):

                return parts[0][1:]

        # ----------------------------------------------------
        # THREADS
        #
        # https://www.threads.com/@username/post/123
        # ----------------------------------------------------

        if (
            hostname == "threads.com"
            or hostname.endswith(
                ".threads.com"
            )
        ):

            if (
                parts
                and parts[0].startswith("@")
            ):

                return parts[0][1:]

        # ----------------------------------------------------
        # INSTAGRAM
        #
        # https://www.instagram.com/username/
        # ----------------------------------------------------

        if (
            hostname == "instagram.com"
            or hostname.endswith(
                ".instagram.com"
            )
        ):

            if parts:

                username = parts[0]

                # Ignore known Instagram routes
                if username not in {
                    "p",
                    "reel",
                    "explore",
                    "accounts",
                    "direct"
                }:

                    return username

    except Exception:

        pass

    return None


# ============================================================
# NORMALIZE URL
# ============================================================

def normalize_url(url):
    """
    Normalize a URL enough to help remove duplicates.

    Removes trailing slashes and whitespace.
    """

    if not url:
        return ""

    return url.strip().rstrip("/")


# ============================================================
# NORMALIZE CANDIDATES
# ============================================================

def normalize_candidates(*candidate_lists):
    """
    Merge candidates from all providers.

    IMPORTANT:
    This function no longer discards non-social-media
    websites.

    Every candidate with a usable image URL or page URL
    is retained and normalized into one common format.
    """

    merged = []

    seen_keys = set()

    for candidates in candidate_lists:

        if not candidates:
            continue

        for candidate in candidates:

            # ------------------------------------------------
            # HANDLE STRING CANDIDATES
            # ------------------------------------------------

            if isinstance(candidate, str):

                image_url = candidate.strip()

                if not image_url:
                    continue

                dedup_key = (
                    "image:"
                    + normalize_url(
                        image_url
                    )
                )

                if dedup_key in seen_keys:
                    continue

                seen_keys.add(
                    dedup_key
                )

                merged.append(
                    {
                        "page_url": "",
                        "image_url": image_url,
                        "title": "",
                        "source": "",
                        "provider": "",
                        "search_rank": 0,
                        "author": None,
                        "is_social_media": False
                    }
                )

                continue

            # ------------------------------------------------
            # HANDLE INVALID OBJECTS
            # ------------------------------------------------

            if not isinstance(
                candidate,
                dict
            ):

                continue

            # ------------------------------------------------
            # EXTRACT URLS
            # ------------------------------------------------

            page_url = (
                candidate.get("page_url")
                or candidate.get("url")
                or ""
            )

            image_url = (
                candidate.get("image_url")
                or candidate.get("thumbnail_url")
                or candidate.get("thumbnail")
                or candidate.get("image")
                or candidate.get("src")
                or ""
            )

            # ------------------------------------------------
            # KEEP IF AT LEAST ONE URL EXISTS
            # ------------------------------------------------

            if not page_url and not image_url:
                continue

            # ------------------------------------------------
            # VALIDATE URL TYPES
            # ------------------------------------------------

            if page_url and not page_url.startswith(
                ("http://", "https://")
            ):

                page_url = ""

            if image_url and not image_url.startswith(
                ("http://", "https://")
            ):

                image_url = ""

            if not page_url and not image_url:
                continue

            # ------------------------------------------------
            # DEDUPLICATION
            #
            # Prefer image URL because multiple pages can
            # sometimes reference the same image.
            # ------------------------------------------------

            if image_url:

                dedup_key = (
                    "image:"
                    + normalize_url(
                        image_url
                    )
                )

            else:

                dedup_key = (
                    "page:"
                    + normalize_url(
                        page_url
                    )
                )

            if dedup_key in seen_keys:
                continue

            seen_keys.add(
                dedup_key
            )

            # ------------------------------------------------
            # SOCIAL MEDIA INFORMATION
            # ------------------------------------------------

            is_social = (
                is_social_media_url(
                    page_url
                )
                if page_url
                else False
            )

            author = (

                candidate.get("author")

                or extract_author(
                    page_url
                )

                if page_url

                else None

            )

            # ------------------------------------------------
            # STANDARD OUTPUT FORMAT
            # ------------------------------------------------

            merged.append(
                {
                    "page_url":
                        page_url,

                    "image_url":
                        image_url,

                    "title":
                        candidate.get("title")
                        or "",

                    "source":
                        candidate.get("source")
                        or "",

                    "provider":
                        candidate.get("provider")
                        or "",

                    "search_rank":
                        candidate.get(
                            "search_rank"
                        )
                        or 0,

                    "author":
                        author,

                    "is_social_media":
                        is_social
                }
            )

    return merged