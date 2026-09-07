from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Set

from search.image_host import upload_image
from search.normalizer import normalize_candidates

from search.providers.provider_primary import search as searchapi_search
from search.providers.provider_openwebninja import search as openwebninja_search

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
        "page_url"
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
    openwebninja_candidates: List[Any],
    max_candidates: int,
) -> List[Any]:
    combined = []
    max_length = max(len(searchapi_candidates), len(openwebninja_candidates))

    for index in range(max_length):
        if index < len(searchapi_candidates) and len(combined) < max_candidates:
            combined.append(searchapi_candidates[index])

        if index < len(openwebninja_candidates) and len(combined) < max_candidates:
            combined.append(openwebninja_candidates[index])

        if len(combined) >= max_candidates:
            break

    return combined


def run_openwebninja(image_path: str) -> List[Any]:
    image_url = upload_image(image_path)
    return openwebninja_search(image_url)


def run_searchapi(image_path: str) -> List[Any]:
    image_url = upload_image(image_path)
    return searchapi_search(image_url)


def search_image(
    image_path: str,
    max_candidates: int = 150,
    verbose: bool = True,
) -> Dict[str, Any]:

    provider_results = {
        "searchapi": [],
        "openwebninja": []
    }

    provider_success = {
        "searchapi": False,
        "openwebninja": False
    }

    provider_errors = {}

    provider_tasks = {
        "searchapi": run_searchapi,
        "openwebninja": run_openwebninja,
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
                    print(
                        f"[Search] {provider_name} returned "
                        f"{len(results)} raw candidates."
                    )

            except Exception as error:
                provider_errors[provider_name] = str(error)

                if verbose:
                    print(
                        f"[Search] {provider_name} failed: {error}"
                    )

    searchapi_normalized = normalize_candidates(
        provider_results["searchapi"]
    )

    openwebninja_normalized = normalize_candidates(
        provider_results["openwebninja"]
    )

    searchapi_filtered = filter_candidates(
        searchapi_normalized
    )

    openwebninja_filtered = filter_candidates(
        openwebninja_normalized
    )

    candidates = interleave_candidates(
        searchapi_filtered,
        openwebninja_filtered,
        max_candidates
    )

    candidates = deduplicate_candidates(candidates)[:max_candidates]

    searchapi_final_count = sum(
        1
        for c in candidates
        if c.get("provider", "").startswith("searchapi")
    )

    openwebninja_final_count = sum(
        1
        for c in candidates
        if c.get("provider", "").startswith("openwebninja")
    )

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
            "openwebninja": {
                "success": provider_success["openwebninja"],
                "raw_candidates": len(provider_results["openwebninja"]),
                "after_normalization": len(openwebninja_normalized),
                "after_filtering": len(openwebninja_filtered),
                "final_candidates": openwebninja_final_count,
            },
            "total_final_candidates": len(candidates),
        },
    }

    if verbose:
        result["provider_errors"] = provider_errors

    return result