import os
import time
import requests
from dotenv import load_dotenv


load_dotenv()


UPLOAD_URL = "https://facefinderai.com/api/public/upload_pic.php"
SEARCH_URL = "https://facefinderai.com/api/public/search.php"


def search(image_path):
    """
    Search FaceFinderAI using a local image file.

    Args:
        image_path (str): Path to the image file.

    Returns:
        list: Candidate results in the project's standard format.
    """

    api_key = os.getenv("FACEFINDER_API_KEY")

    if not api_key:
        raise RuntimeError("FACEFINDER_API_KEY not found in .env")

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    with open(image_path, "rb") as image_file:
        upload_response = requests.post(
            UPLOAD_URL,
            headers=headers,
            files={"images": image_file},
            timeout=30,
        )

    upload_response.raise_for_status()

    upload_data = upload_response.json()
    search_id = upload_data.get("id_search")

    if not search_id:
        raise RuntimeError(
            f"FaceFinder upload failed: {upload_data}"
        )

    for _ in range(30):
        search_response = requests.post(
            SEARCH_URL,
            headers={
                **headers,
                "Content-Type": "application/json",
            },
            json={
                "id_search": search_id,
            },
            timeout=30,
        )

        search_response.raise_for_status()

        data = search_response.json()
        import json
        print("\n========== RAW FACEFINDER API RESPONSE ==========")
        print(json.dumps(data, indent=2)[:10000])
        print("=================================================\n")

        if data.get("status") == "done":
            break

        time.sleep(2)

    else:
        raise TimeoutError("FaceFinder search timed out")

    candidates = []

    for position, item in enumerate(
        data.get("output", {}).get("items", []),
        start=1,
    ):
        page_url = item.get("url")

        if not page_url:
            continue

        candidates.append(
            {
                "page_url": page_url,
                "image_url": None,
                "title": None,
                "source": None,
                "provider": "facefinderai",
                "search_rank": position,
            }
        )

    return candidates