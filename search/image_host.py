import requests


UPLOAD_URL = "https://uguu.se/upload"


def upload_image(image_path):
    """
    Upload a local image to Uguu and return its public URL.
    """

    with open(image_path, "rb") as image_file:
        response = requests.post(
            UPLOAD_URL,
            files={"files[]": image_file},
            timeout=30,
        )

    response.raise_for_status()

    data = response.json()

    if not data.get("success"):
        raise RuntimeError(f"Image upload failed: {data}")

    file_data = data["files"][0]

    return file_data["url"]
