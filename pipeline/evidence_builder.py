from datetime import datetime, timezone
from typing import Dict, Any

from blockchain.hashing import hash_file


def build_evidence(
    input_image_path: str,
    pipeline_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Converts the output from IntegratedPipeline into a
    standardized blockchain evidence record.
    """

    verified_matches = []

    for result in pipeline_result.get("results", []):

        if result.get("verified"):

            verified_matches.append({
                "candidate_id": result.get("candidate_id"),

                "title": result.get("title"),

                "source": result.get("source"),

                "matched_page_url": result.get(
                    "page_url"
                ),

                "matched_image_url": result.get(
                    "image_url"
                ),

                "similarity_score": result.get(
                    "similarity_score"
                )
            })

    evidence = {
        # Cryptographic identity of the original input image
        "input_image_hash": hash_file(
            input_image_path
        ),

        # Pipeline metadata
        "total_candidates_found": pipeline_result.get(
            "total_candidates_found",
            0
        ),

        "total_candidates_evaluated": pipeline_result.get(
            "total_candidates_evaluated",
            0
        ),

        # Verification results
        "verified_matches": verified_matches,

        "verified_matches_count": len(
            verified_matches
        ),

        # When this evidence record was created
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()
    }

    return evidence