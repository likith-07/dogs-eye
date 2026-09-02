import os
import requests
from dotenv import load_dotenv


load_dotenv()


def search(image_url):
    """
    Search the web using SearchAPI's Google Lens engine.

    Args:
        image_url (str): Publicly accessible URL of the image.

    Returns:
        list: Candidate results in the project's standard format.
    """

    api_key = os.getenv("SEARCHAPI_KEY")

    if not api_key:
        raise RuntimeError("SEARCHAPI_KEY not found in .env")

    response = requests.get(
        "https://www.searchapi.io/api/v1/search",
        params={
            "engine": "google_lens",
            "url": image_url,
            "api_key": api_key,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    candidates = []

    for result in data.get("visual_matches", []):
        page_url = result.get("link")

        if not page_url:
            continue

        image_data = result.get("image", {})

        candidates.append(
            {
                "page_url": page_url,
                "image_url": image_data.get("link"),
                "title": result.get("title"),
                "source": result.get("source"),
                "provider": "searchapi_google_lens",
                "search_rank": result.get("position"),
            }
        )

    return candidates