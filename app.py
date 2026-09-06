import os
import shutil
from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from main import process_image
from username_investigation.investigator import investigate_identity


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
INPUT_DIR = BASE_DIR / "data" / "inputs"

INPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="DogsEye",
    description="Image-Based Investigation and Verification System"
)


# ============================================================
# CORS & SCHEMAS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UsernameInvestigationRequest(BaseModel):
    target_username: str 


# ============================================================
# SOCIAL MEDIA DOMAINS & CLASSIFICATION
# ============================================================

SOCIAL_MEDIA_DOMAINS = {
    "instagram.com", "facebook.com", "x.com", "twitter.com",
    "tiktok.com", "threads.com", "youtube.com", "youtu.be",
    "linkedin.com", "reddit.com", "clubhouse.com",
}


def get_hostname(url: str) -> str:
    try:
        hostname = (urlparse(url).hostname or "").lower()
        if hostname.startswith("www."):
            hostname = hostname[4:]
        return hostname
    except Exception:
        return ""


def is_social_media(url: str) -> bool:
    hostname = get_hostname(url)
    return any(
        hostname == domain or hostname.endswith("." + domain)
        for domain in SOCIAL_MEDIA_DOMAINS
    )


def classify_url(url: str) -> str:
    if not url:
        return "non_social"

    try:
        parsed = urlparse(url)
        hostname = get_hostname(url)
        path = parsed.path.lower()
    except Exception:
        return "non_social"

    if not is_social_media(url):
        return "non_social"

    if "instagram.com" in hostname:
        if any(marker in path for marker in ["/p/", "/reel/", "/reels/", "/tv/"]):
            return "social_post"
        return "social_profile"

    if "x.com" in hostname or "twitter.com" in hostname:
        if "/status/" in path:
            return "social_post"
        return "social_profile"

    if "tiktok.com" in hostname:
        if "/video/" in path:
            return "social_post"
        return "social_profile"

    if "threads.com" in hostname:
        if "/post/" in path:
            return "social_post"
        return "social_profile"

    if "youtube.com" in hostname or "youtu.be" in hostname:
        if "/watch" in path or "/shorts/" in path or hostname == "youtu.be":
            return "social_post"
        return "social_profile"

    if "facebook.com" in hostname:
        if any(marker in path for marker in ["/posts/", "/videos/", "/reel/", "/photo"]):
            return "social_post"
        return "social_profile"

    if "linkedin.com" in hostname:
        if "/posts/" in path or "/feed/update/" in path:
            return "social_post"
        return "social_profile"

    if "reddit.com" in hostname:
        if "/comments/" in path:
            return "social_post"
        return "social_profile"

    return "social_profile"


def organize_results(results: list) -> dict:
    social_profiles = []
    social_posts = []
    non_social_links = []

    for item in results:
        if not isinstance(item, dict):
            continue

        url = item.get("page_url") or item.get("url") or ""
        category = classify_url(url)
        item["category"] = category

        if category == "social_profile":
            social_profiles.append(item)
        elif category == "social_post":
            social_posts.append(item)
        else:
            non_social_links.append(item)

    return {
        "social_profiles": social_profiles,
        "social_posts": social_posts,
        "non_social_links": non_social_links,
    }


# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/")
async def serve_frontend():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/api/investigate")
async def investigate_image(file: UploadFile = File(...)):
    safe_filename = Path(file.filename).name
    file_path = INPUT_DIR / safe_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = process_image(str(file_path))

    if not result.get("success", False):
        return result

    results = result.get("results", [])
    categorized_results = organize_results(results)

    return {
        **result,
        "categorized_results": categorized_results,
        "summary": {
            "social_profiles": len(categorized_results["social_profiles"]),
            "social_posts": len(categorized_results["social_posts"]),
            "non_social_links": len(categorized_results["non_social_links"]),
        }
    }


@app.post("/api/username-investigate")
async def run_osint_correlation(payload: UsernameInvestigationRequest):
    if not payload.target_username:
        raise HTTPException(status_code=400, detail="Missing target_username parameter.")

    # We now pass the verified username directly to the investigator
    result = investigate_identity(payload.target_username)
    return result