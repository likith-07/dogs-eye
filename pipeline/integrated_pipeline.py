import os
import json
from typing import Dict, Any

from search.engine import search_image


class IntegratedPipeline:

    def __init__(
        self,
        max_candidates_to_scan: int = 100,
        verbose: bool = False
    ):

        self.max_candidates_to_scan = (
            max_candidates_to_scan
        )

        self.verbose = verbose


    def execute(
        self,
        target_image_path: str
    ) -> Dict[str, Any]:

        print("\n" + "=" * 60)
        print("DOGSEYE SEARCH PIPELINE")
        print("=" * 60)


        # ====================================================
        # STEP 1 — VALIDATE INPUT
        # ====================================================

        if not os.path.exists(
            target_image_path
        ):

            return {

                "success": False,

                "error": (
                    f"Image not found: "
                    f"{target_image_path}"
                ),

                "results": []
            }


        print(
            "\n[1/2] Input image validated."
        )


        # ====================================================
        # STEP 2 — SEARCH
        # ====================================================

        print(
            "\n[2/2] Searching providers..."
        )

        try:

            search_response = search_image(

                image_path=target_image_path,

                max_candidates=(
                    self.max_candidates_to_scan
                ),

                verbose=self.verbose
            )

        except Exception as error:

            return {

                "success": False,

                "error": (
                    f"Search failed: {error}"
                ),

                "results": []
            }


        candidates = search_response.get(
            "candidates",
            []
        )

        search_statistics = (
            search_response.get(
                "stats",
                {}
            )
        )


        # ====================================================
        # PRINT SUMMARY
        # ====================================================

        print(
            f"\nCandidates found: "
            f"{len(candidates)}"
        )

        print(
            "\nTop candidates:"
        )

        for index, candidate in enumerate(
            candidates[:10],
            start=1
        ):

            print(
                f"{index}. "
                f"{candidate.get('title', 'Untitled')}"
            )

            print(
                f"   Source: "
                f"{candidate.get('source', 'Unknown')}"
            )

            print(
                f"   Provider: "
                f"{candidate.get('provider', 'Unknown')}"
            )

            print(
                f"   Provider Rank: "
                f"{candidate.get('search_rank', 'N/A')}"
            )

            print(
                f"   Page: "
                f"{candidate.get('page_url', '')}"
            )


        # ====================================================
        # FINAL PAYLOAD
        # ====================================================

        return {

            "success": search_response.get(
                "success",
                True
            ),

            "target_image": (
                target_image_path
            ),

            "total_candidates_found": (
                len(candidates)
            ),

            "search_statistics": (
                search_statistics
            ),

            "results": candidates
        }


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    import sys


    test_image = (

        sys.argv[1]

        if len(sys.argv) > 1

        else (
            "data/inputs/"
            "sample_image.png"
        )

    )


    pipeline = IntegratedPipeline(

        max_candidates_to_scan=100,

        verbose=True
    )


    output = pipeline.execute(
        test_image
    )


    print(
        "\n=== FINAL PIPELINE OUTPUT ==="
    )


    print(
        json.dumps(
            output,
            indent=2
        )
    )