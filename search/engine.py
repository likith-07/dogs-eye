from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Set

from search.image_host import upload_image
from search.normalizer import normalize_candidates

from search.providers.provider_primary import search as searchapi_search
from search.providers.provider_secondary import search as facefinder_search
import time
import requests 

def get_candidate_url(candidate: Any) -> str:
    """
    Extract a usable image URL or fallback to page URL from a normalized candidate.
    """
    if isinstance(candidate, str):
        return candidate.strip()

    if not isinstance(candidate, dict):
        return ""

    possible_keys = [
        "image_url",
        "image",
        "base64",
        "thumbnail",
        "thumbnail_url",
        "url",
        "src",
        "imageUrl",
        "imageURL",
        "page_url"  # Fallback to page URL if image is missing
    ]

    for key in possible_keys:
        value = candidate.get(key)
        if isinstance(value, str):
            value = value.strip()
            if value.startswith(("http://", "https://", "data:image/")):
                return value

    return ""


def is_valid_candidate(candidate: Any) -> bool:
    """
    Check whether a candidate has a usable URL or page link.
    """
    if not isinstance(candidate, dict):
        return False
    
    # Accept if it has either a valid image link or a valid page profile link
    img_url = get_candidate_url(candidate)
    page_url = candidate.get("page_url", "")

    has_valid_img = img_url.startswith(("http://", "https://", "data:image/"))
    has_valid_page = page_url.startswith(("http://", "https://"))

    return has_valid_img or has_valid_page


def deduplicate_candidates(candidates: List[Any]) -> List[Any]:
    seen_urls: Set[str] = set()
    unique_candidates = []

    for candidate in candidates:
        image_url = get_candidate_url(candidate)
        if not image_url:
            continue

        normalized_url = image_url.strip().rstrip("/")
        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)
        unique_candidates.append(candidate)

    return unique_candidates


def filter_candidates(candidates: List[Any]) -> List[Any]:
    valid_candidates = [
        candidate for candidate in candidates if is_valid_candidate(candidate)
    ]
    return deduplicate_candidates(valid_candidates)


def interleave_candidates(
    searchapi_candidates: List[Any],
    facefinder_candidates: List[Any],
    max_candidates: int,
) -> List[Any]:
    combined = []
    max_length = max(len(searchapi_candidates), len(facefinder_candidates))

    for index in range(max_length):
        if index < len(searchapi_candidates) and len(combined) < max_candidates:
            combined.append(searchapi_candidates[index])
        if index < len(facefinder_candidates) and len(combined) < max_candidates:
            combined.append(facefinder_candidates[index])
        if len(combined) >= max_candidates:
            break

    return combined






def run_facefinder(image_path: str, max_retries: int = 3, max_poll_attempts: int = 15) -> List[Any]:
    """
    FaceFinderAI search with:
    1. Retry logic for 522/Cloudflare timeouts.
    2. Asynchronous status polling until progress reaches 100%.
    """
    response = None
    delay = 2

    # ----------------------------------------------------
    # PHASE 1: Initiate Search with Network Retry Logic
    # ----------------------------------------------------
    for attempt in range(1, max_retries + 1):
        try:
            response = facefinder_search(image_path)
            break
        except Exception as error:
            error_str = str(error)
            if "522" in error_str or "timed out" in error_str.lower() or "Connection" in error_str:
                if attempt < max_retries:
                    print(f"[Search] FaceFinder 522/Timeout on start (Attempt {attempt}/{max_retries}). Retrying in {delay}s...")
                    time.sleep(delay)
                    delay *= 2
                    continue
            print(f"[Search] FaceFinder initialization failed: {error}")
            return []

    if not isinstance(response, dict):
        return response if isinstance(response, list) else []

    # ----------------------------------------------------
    # PHASE 2: Asynchronous Polling Loop (Wait for 100%)
    # ----------------------------------------------------
    search_id = response.get("id_search")
    progress = response.get("progress", 0)

    poll_attempts = 0
    while progress < 100 and poll_attempts < max_poll_attempts:
        poll_attempts += 1
        time.sleep(3)  # Wait 3 seconds between status checks

        try:
            # If the provider module exposes a status checker, use it. 
            # Otherwise, re-trigger or check status via available method.
            if search_id and hasattr(facefinder_search, "get_status"):
                response = facefinder_search.get_status(search_id)
            elif search_id and hasattr(facefinder_search, "poll"):
                response = facefinder_search.poll(search_id)
            else:
                # Fallback: if no dedicated poll method exists, break out with current response
                break

            if isinstance(response, dict):
                progress = response.get("progress", 100)
                if verbose := True:
                    print(f"[Search] FaceFinder polling... Status: {response.get('message', 'Processing')} ({progress}%)")
        except Exception as poll_error:
            # Swallow minor polling network blips and try next poll cycle
            continue

    # ----------------------------------------------------
    # PHASE 3: Extract Final Items
    # ----------------------------------------------------
    if isinstance(response, dict):
        output = response.get("output", {})
        if isinstance(output, dict):
            return output.get("items", [])

    return []

def run_searchapi(image_path: str) -> List[Any]:
    image_url = upload_image(image_path)
    return searchapi_search(image_url)


def search_image(
    image_path: str,
    max_candidates: int = 150,
    verbose: bool = True,
) -> Dict[str, Any]:

    provider_results = {"searchapi": [], "facefinder": []}
    provider_success = {"searchapi": False, "facefinder": False}
    provider_errors = {}

    provider_tasks = {
        "facefinder": run_facefinder,
        "searchapi": run_searchapi,
    }

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(provider_function, image_path): provider_name
            for provider_name, provider_function in provider_tasks.items()
        }

        for future in as_completed(futures):
            provider_name = futures[future]
            try:
                results = future.result() or []
                provider_results[provider_name] = results
                provider_success[provider_name] = True

                if verbose:
                    print(f"[Search] {provider_name} returned {len(results)} raw candidates.")
            except Exception as error:
                provider_errors[provider_name] = str(error)
                if verbose:
                    print(f"[Search] {provider_name} failed: {error}")

    searchapi_normalized = normalize_candidates(provider_results["searchapi"])
    facefinder_normalized = normalize_candidates(provider_results["facefinder"])

    searchapi_filtered = filter_candidates(searchapi_normalized)
    facefinder_filtered = filter_candidates(facefinder_normalized)

    candidates = interleave_candidates(
        searchapi_filtered, facefinder_filtered, max_candidates
    )
    candidates = deduplicate_candidates(candidates)[:max_candidates]

    searchapi_final_count = sum(1 for c in candidates if c.get("provider", "").startswith("searchapi"))
    facefinder_final_count = sum(1 for c in candidates if c.get("provider", "").startswith("facefinder"))

    result = {
        "success": any(provider_success.values()),
        "candidates": candidates,
        "stats": {
            "searchapi": {
                "success": provider_success["searchapi"],
                "raw_candidates": len(provider_results["searchapi"]),
                "after_normalization": len(searchapi_normalized),
                "after_filtering": len(searchapi_filtered),
                "final_candidates": searchapi_final_count,
            },
            "facefinder": {
                "success": provider_success["facefinder"],
                "raw_candidates": len(provider_results["facefinder"]),
                "after_normalization": len(facefinder_normalized),
                "after_filtering": len(facefinder_filtered),
                "final_candidates": facefinder_final_count,
            },
            "total_final_candidates": len(candidates),
        },
    }

    if verbose:
        result["provider_errors"] = provider_errors

    return result