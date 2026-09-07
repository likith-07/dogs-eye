from typing import Dict, Any, List


class EvidenceBuilder:
    """
    Builds the canonical evidence payload that will be hashed and
    registered on the blockchain.

    Username expansion/discovery data should NOT be included here.
    """

    @staticmethod
    def build(
        investigation_result: Dict[str, Any]
    ) -> Dict[str, Any]:

        raw_results: List[Dict[str, Any]] = (
            investigation_result.get("results") or []
        )

        evidence_results = []

        for item in raw_results:

            evidence_results.append(
                {
                    "page_url": item.get("page_url"),
                    "image_url": item.get("image_url"),
                    "source": item.get("source"),
                    "provider": item.get("provider"),
                    "title": item.get("title"),
                    "search_rank": item.get("search_rank"),
                    "author": item.get("author"),
                    "verified": item.get("verified"),
                    "similarity_score": item.get(
                        "similarity_score"
                    ),
                }
            )

        evidence = {
            "target_image": investigation_result.get(
                "target_image"
            ),

            "total_candidates_found": investigation_result.get(
                "total_candidates_found",
                0
            ),

            "results": evidence_results,
        }

        return evidence