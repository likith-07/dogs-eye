from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Set

from search.image_host import upload_image
from search.normalizer import normalize_candidates

from search.providers.provider_primary import search as searchapi_search
from search.providers.provider_secondary import search as facefinder_search


# ============================================================
# HELPERS
# ============================================================

def is_valid_candidate(candidate: Any) -> bool:
    """
    Check whether a candidate has a usable image URL.
    """

    if isinstance(candidate, str):
        return candidate.startswith(("http://", "https://"))

    if isinstance(candidate, dict):

        image_url = candidate.get("image_url")

        if not image_url:
            return False

        return image_url.startswith(
            ("http://", "https://")
        )

    return False


def get_candidate_url(candidate: Any) -> str:
    """
    Extract the image URL from either a dictionary or string.
    """

    if isinstance(candidate, str):
        return candidate

    if isinstance(candidate, dict):
        return candidate.get("image_url", "")

    return ""


def deduplicate_candidates(
    candidates: List[Any]
) -> List[Any]:
    """
    Remove duplicate candidate image URLs.
    """

    seen_urls: Set[str] = set()

    unique_candidates = []

    for candidate in candidates:

        image_url = get_candidate_url(candidate)

        if not image_url:
            continue

        # Normalise URL slightly before comparing
        normalized_url = image_url.strip()

        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)

        unique_candidates.append(candidate)

    return unique_candidates


def filter_candidates(
    candidates: List[Any],
    max_candidates: int
) -> List[Any]:
    """
    Remove malformed candidates, remove duplicates,
    and limit the number returned.
    """

    valid_candidates = [

        candidate

        for candidate in candidates

        if is_valid_candidate(candidate)

    ]

    unique_candidates = deduplicate_candidates(
        valid_candidates
    )

    return unique_candidates[:max_candidates]


# ============================================================
# PROVIDER FUNCTIONS
# ============================================================

def run_facefinder(
    image_path: str
) -> List[Any]:
    """
    FaceFinderAI searches directly using the local image.
    """

    return facefinder_search(
        image_path
    )


def run_searchapi(
    image_path: str
) -> List[Any]:
    """
    SearchAPI requires a publicly accessible URL.

    The image is uploaded first and the resulting URL
    is passed to the search provider.
    """

    image_url = upload_image(
        image_path
    )

    return searchapi_search(
        image_url
    )


# ============================================================
# MAIN SEARCH ENGINE
# ============================================================

def search_image(
    image_path: str,
    max_candidates: int = 150,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Search for possible online matches using multiple providers.

    Workflow:

        Input Image
            │
            ├── FaceFinderAI
            │
            └── Image Upload
                    │
                    ↓
                 SearchAPI
            │
            └───────────────
                    ↓
               Normalize
                    ↓
               Filter
                    ↓
               Deduplicate
                    ↓
            Ranked Candidate List


    Args:

        image_path:
            Path to the input image.

        max_candidates:
            Maximum number of candidates returned after
            normalization and deduplication.

        verbose:
            Print provider diagnostics.

    Returns:

        Dictionary containing candidates and search statistics.
    """

    provider_results = {

        "searchapi": [],

        "facefinder": []

    }

    provider_success = {

        "searchapi": False,

        "facefinder": False

    }

    provider_errors = {}

    # ========================================================
    # RUN PROVIDERS
    # ========================================================

    # Both searches can be started independently.
    #
    # SearchAPI internally uploads the image first.
    #
    # FaceFinder works directly from the local file.

    provider_tasks = {

        "facefinder": run_facefinder,

        "searchapi": run_searchapi

    }

    with ThreadPoolExecutor(
        max_workers=2
    ) as executor:

        futures = {

            executor.submit(
                provider_function,
                image_path
            ): provider_name

            for provider_name,
            provider_function

            in provider_tasks.items()

        }

        for future in as_completed(
            futures
        ):

            provider_name = futures[
                future
            ]

            try:

                results = future.result()

                provider_results[
                    provider_name
                ] = results or []

                provider_success[
                    provider_name
                ] = True

                if verbose:

                    print(
                        f"[Search] "
                        f"{provider_name} returned "
                        f"{len(results or [])} candidates."
                    )

            except Exception as error:

                provider_errors[
                    provider_name
                ] = str(error)

                if verbose:

                    print(
                        f"[Search] "
                        f"{provider_name} failed: "
                        f"{error}"
                    )

    # ========================================================
    # NORMALIZE RESULTS
    # ========================================================

    normalized_candidates = normalize_candidates(

        provider_results[
            "searchapi"
        ],

        provider_results[
            "facefinder"
        ]

    )

    # ========================================================
    # FILTER + DEDUPLICATE
    # ========================================================

    candidates = filter_candidates(

        normalized_candidates,

        max_candidates

    )

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    result = {

        "success": any(
            provider_success.values()
        ),

        "candidates": candidates,

        "stats": {

            "searchapi": {

                "success":
                    provider_success[
                        "searchapi"
                    ],

                "raw_candidates":
                    len(
                        provider_results[
                            "searchapi"
                        ]
                    )

            },

            "facefinder": {

                "success":
                    provider_success[
                        "facefinder"
                    ],

                "raw_candidates":
                    len(
                        provider_results[
                            "facefinder"
                        ]
                    )

            },

            "total_after_normalization":
                len(
                    normalized_candidates
                ),

            "total_after_filtering":
                len(
                    candidates
                )

        }

    }

    # Only include errors if debugging.
    if verbose:

        result[
            "provider_errors"
        ] = provider_errors

    return result