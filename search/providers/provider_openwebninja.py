import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.openwebninja.com/reverse-image-search/reverse-image-search"


def search(image_url):
    api_key = os.getenv("OPENWEBNINJA_API_KEY")

    if not api_key:
        raise RuntimeError("OPENWEBNINJA_API_KEY not found in .env")

    response = requests.get(
        API_URL,
        params={
            "url": image_url,
        },
        headers={
            "x-api-key": api_key,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    candidates = []

    for rank, result in enumerate(data.get("data", []), start=1):
        page_url = result.get("link")

        if not page_url:
            continue

        candidates.append({
            "page_url": page_url,
            "image_url": result.get("image"),
            "title": result.get("title"),
            "source": result.get("domain"),
            "provider": "openwebninja_reverse_image",
            "search_rank": rank,
        })

    return candidates