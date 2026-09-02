from search.image_host import upload_image
from search.normalizer import normalize_candidates
from search.providers.provider_primary import search as searchapi_search
from search.providers.provider_secondary import search as facefinder_search


def search_image(image_path):
    """
    Search for web/social-media candidates using both providers.

    Args:
        image_path (str): Path to the input image.

    Returns:
        dict: Standard search result contract.
    """

    searchapi_candidates = []
    facefinder_candidates = []

    searchapi_success = False
    facefinder_success = False

    # FaceFinderAI searches the local image directly.
    try:
        facefinder_candidates = facefinder_search(image_path)
        facefinder_success = True
    except Exception as error:
        print(f"FaceFinderAI search failed: {error}")

    # SearchAPI requires a publicly accessible image URL.
    try:
        image_url = upload_image(image_path)
        searchapi_candidates = searchapi_search(image_url)
        searchapi_success = True
    except Exception as error:
        print(f"SearchAPI search failed: {error}")

    candidates = normalize_candidates(
        searchapi_candidates,
        facefinder_candidates,
    )

    return {
        "success": searchapi_success or facefinder_success,
        "candidates": candidates,
    }