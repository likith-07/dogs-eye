import hashlib
import os
from typing import Dict, Any, List


class EvidenceBuilder:
    """
    Builds the canonical evidence payload that will be hashed
    and registered on the blockchain.

    The uploaded evidence file is hashed separately and that
    hash becomes part of the canonical evidence payload.

    This allows the system to detect modifications to the
    original evidence file after blockchain registration.
    """

    @staticmethod
    def hash_file(file_path: str) -> str:
        """
        Calculate the SHA-256 hash of the actual evidence file.
        """

        sha256 = hashlib.sha256()

        try:
            with open(file_path, "rb") as file:
                while True:
                    chunk = file.read(8192)

                    if not chunk:
                        break

                    sha256.update(chunk)

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Evidence file not found: {file_path}"
            )

        return sha256.hexdigest()

    @staticmethod
    def build(
        investigation_result: Dict[str, Any],
        file_path: str
    ) -> Dict[str, Any]:
        """
        Build the canonical evidence payload.

        Args:
            investigation_result:
                Result produced by the DogsEye investigation pipeline.

            file_path:
                Path to the original uploaded evidence file.

        Returns:
            Deterministic evidence dictionary containing the
            investigation results and SHA-256 hash of the
            original evidence file.
        """

        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                f"Evidence file does not exist: {file_path}"
            )

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

        # Hash the actual uploaded evidence file.
        file_hash = EvidenceBuilder.hash_file(file_path)

        evidence = {
            "target_image": investigation_result.get(
                "target_image"
            ),

            "evidence_file": {
                "filename": os.path.basename(file_path),
                "sha256": file_hash,
            },

            "total_candidates_found": investigation_result.get(
                "total_candidates_found",
                0
            ),

            "results": evidence_results,
        }

        return evidence