import os
import shutil
from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from main import process_image


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

FRONTEND_DIR = BASE_DIR / "frontend"

INPUT_DIR = BASE_DIR / "data" / "inputs"

INPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="DogsEye",
    description="Image-Based Investigation and Verification System"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# SOCIAL MEDIA DOMAINS
# ============================================================

SOCIAL_MEDIA_DOMAINS = {

    "instagram.com",

    "facebook.com",

    "x.com",

    "twitter.com",

    "tiktok.com",

    "threads.com",

    "youtube.com",

    "youtu.be",

    "linkedin.com",

    "reddit.com",

    "clubhouse.com",

}


# ============================================================
# URL HELPERS
# ============================================================

def get_hostname(
    url: str
) -> str:
    """
    Extract hostname from URL.
    """

    try:

        hostname = (
            urlparse(url)
            .hostname
            or ""
        )

        hostname = hostname.lower()

        if hostname.startswith(
            "www."
        ):

            hostname = hostname[4:]

        return hostname

    except Exception:

        return ""


def is_social_media(
    url: str
) -> bool:
    """
    Check whether URL belongs to a known
    social media platform.
    """

    hostname = get_hostname(url)

    return any(

        hostname == domain
        or hostname.endswith(
            "." + domain
        )

        for domain
        in SOCIAL_MEDIA_DOMAINS

    )


# ============================================================
# URL CLASSIFICATION
# ============================================================

def classify_url(
    url: str
) -> str:
    """
    Classify URL as:

        social_profile
        social_post
        non_social
    """

    if not url:

        return "non_social"


    try:

        parsed = urlparse(url)

        hostname = get_hostname(url)

        path = (
            parsed.path
            .lower()
        )

    except Exception:

        return "non_social"


    # --------------------------------------------------------
    # NON SOCIAL
    # --------------------------------------------------------

    if not is_social_media(url):

        return "non_social"


    # --------------------------------------------------------
    # INSTAGRAM
    # --------------------------------------------------------

    if "instagram.com" in hostname:

        if any(

            marker in path

            for marker in [

                "/p/",

                "/reel/",

                "/reels/",

                "/tv/"

            ]

        ):

            return "social_post"

        return "social_profile"


    # --------------------------------------------------------
    # X / TWITTER
    # --------------------------------------------------------

    if (

        "x.com" in hostname
        or "twitter.com" in hostname

    ):

        if "/status/" in path:

            return "social_post"

        return "social_profile"


    # --------------------------------------------------------
    # TIKTOK
    # --------------------------------------------------------

    if "tiktok.com" in hostname:

        if "/video/" in path:

            return "social_post"

        return "social_profile"


    # --------------------------------------------------------
    # THREADS
    # --------------------------------------------------------

    if "threads.com" in hostname:

        if "/post/" in path:

            return "social_post"

        return "social_profile"


    # --------------------------------------------------------
    # YOUTUBE
    # --------------------------------------------------------

    if (

        "youtube.com" in hostname
        or "youtu.be" in hostname

    ):

        if (

            "/watch" in path
            or "/shorts/" in path
            or hostname == "youtu.be"

        ):

            return "social_post"

        return "social_profile"


    # --------------------------------------------------------
    # FACEBOOK
    # --------------------------------------------------------

    if "facebook.com" in hostname:

        if any(

            marker in path

            for marker in [

                "/posts/",

                "/videos/",

                "/reel/",

                "/photo"

            ]

        ):

            return "social_post"

        return "social_profile"


    # --------------------------------------------------------
    # LINKEDIN
    # --------------------------------------------------------

    if "linkedin.com" in hostname:

        if (

            "/posts/" in path
            or "/feed/update/" in path

        ):

            return "social_post"

        return "social_profile"


    # --------------------------------------------------------
    # REDDIT
    # --------------------------------------------------------

    if "reddit.com" in hostname:

        if "/comments/" in path:

            return "social_post"

        return "social_profile"


    # --------------------------------------------------------
    # CLUBHOUSE
    # --------------------------------------------------------

    if "clubhouse.com" in hostname:

        return "social_profile"


    # Default for social platforms

    return "social_profile"


# ============================================================
# ORGANIZE RESULTS
# ============================================================

def organize_results(
    results: list
) -> dict:
    """
    Split results into three categories.
    """

    social_profiles = []

    social_posts = []

    non_social_links = []


    for item in results:

        if not isinstance(
            item,
            dict
        ):

            continue


        url = (

            item.get(
                "page_url"
            )

            or

            item.get(
                "url"
            )

            or

            ""

        )


        category = classify_url(url)


        # Add classification so frontend
        # knows exactly what this result is.

        item["category"] = category


        if category == "social_profile":

            social_profiles.append(
                item
            )


        elif category == "social_post":

            social_posts.append(
                item
            )


        else:

            non_social_links.append(
                item
            )


    return {

        "social_profiles":
            social_profiles,

        "social_posts":
            social_posts,

        "non_social_links":
            non_social_links,

    }


# ============================================================
# FRONTEND
# ============================================================

@app.get("/")
async def serve_frontend():

    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


# ============================================================
# INVESTIGATION ENDPOINT
# ============================================================

@app.post(
    "/api/investigate"
)
async def investigate_image(

    file: UploadFile = File(...)

):

    # --------------------------------------------------------
    # SAVE UPLOADED IMAGE
    # --------------------------------------------------------

    safe_filename = (
        Path(
            file.filename
        )
        .name
    )


    file_path = (
        INPUT_DIR
        / safe_filename
    )


    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    # --------------------------------------------------------
    # RUN PIPELINE
    # --------------------------------------------------------

    result = process_image(

        str(file_path)

    )


    # --------------------------------------------------------
    # HANDLE PIPELINE FAILURE
    # --------------------------------------------------------

    if not result.get(

        "success",

        False

    ):

        return result


    # --------------------------------------------------------
    # ORGANIZE RESULTS
    # --------------------------------------------------------

    results = result.get(

        "results",

        []

    )


    categorized_results = organize_results(

        results

    )


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        **result,

        "categorized_results":
            categorized_results,

        "summary": {

            "social_profiles":
                len(
                    categorized_results[
                        "social_profiles"
                    ]
                ),

            "social_posts":
                len(
                    categorized_results[
                        "social_posts"
                    ]
                ),

            "non_social_links":
                len(
                    categorized_results[
                        "non_social_links"
                    ]
                ),

        }

    }