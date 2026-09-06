import re
from urllib.parse import urlparse

PLATFORM_PATTERNS = {
    "instagram": r"instagram\.com/(?:p/|reel/|reels/|stories/|tv/)?@?([a-zA-Z0-9_.]+)",
    "x": r"(?:twitter\.com|x\.com)/(?:status/|i/)?@?([a-zA-Z0-9_]+)",
    "tiktok": r"tiktok\.com/@([a-zA-Z0-9_.]+)",
    "threads": r"threads\.(?:com|net)/(?:post/)?@?([a-zA-Z0-9_.]+)",
    "youtube": r"youtube\.com/(?:@|user/|c/|channel/)?([a-zA-Z0-9_.-]+)",
    "facebook": r"facebook\.com/(?:people/|pg/|posts/|videos/)?([a-zA-Z0-9_.]+)",
    "github": r"github\.com/([a-zA-Z0-9_-]+)",
}

RESERVED_PATH_WORDS = {
    "home", "explore", "search", "settings", "login", "p", "reel", "reels",
    "shorts", "watch", "status", "posts", "post", "video", "videos", "stories",
    "tv", "comments", "channel", "user", "c", "in", "people", "feed", "pub",
    "packages", "package", "docs", "about", "contact", "privacy", "terms", "api"
}

def extract_target_handle(url: str) -> str:
    if not url: return ""
    url_str = url.strip()

    for platform, pattern in PLATFORM_PATTERNS.items():
        match = re.search(pattern, url_str, re.IGNORECASE)
        if match:
            username = match.group(1).rstrip("/").lstrip("@")
            if username.lower() not in RESERVED_PATH_WORDS and len(username) >= 3:
                return username

    try:
        parsed = urlparse(url_str)
        path_parts = [p for p in parsed.path.split("/") if p]
        if path_parts:
            candidate = path_parts[0].replace("@", "")
            if (candidate.lower() not in RESERVED_PATH_WORDS 
                and len(candidate) >= 3 
                and re.match(r"^[a-zA-Z0-9_.]+$", candidate)):
                return candidate
    except Exception:
        pass

    return ""