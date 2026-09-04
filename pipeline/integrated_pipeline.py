import os
import json
import urllib.request
import tempfile
from typing import Dict, Any

from face.verifier import FaceVerifier
from search.engine import search_image


class IntegratedPipeline:
    """
    Main integration pipeline.

    Responsibilities:
    1. Validate input image.
    2. Confirm a face exists.
    3. Search for candidate images.
    4. Download candidates.
    5. Verify candidate faces.
    6. Return clean structured results.
    """

    def __init__(
        self,
        threshold: float = 0.35,
        max_evaluations: int = 50,
        max_candidates_to_scan: int = 100,
        verbose: bool = False
    ):
        """
        Args:
            threshold:
                Face similarity threshold required for verification.

            max_evaluations:
                Maximum number of successfully downloaded candidates
                to evaluate.

            max_candidates_to_scan:
                Maximum number of search candidates to inspect.
                This prevents the pipeline from scanning thousands
                of broken URLs.

            verbose:
                Enables detailed debugging output.
        """

        self.verifier = FaceVerifier(threshold=threshold)

        self.max_evaluations = max_evaluations
        self.max_candidates_to_scan = max_candidates_to_scan
        self.verbose = verbose

    # ============================================================
    # LOGGING
    # ============================================================

    def log(self, message: str):
        """
        Print detailed debugging information only when verbose mode
        is enabled.
        """

        if self.verbose:
            print(message)

    # ============================================================
    # MAIN PIPELINE
    # ============================================================

    def execute(self, target_image_path: str) -> Dict[str, Any]:

        print("\n" + "=" * 60)
        print("DOGSEYE INVESTIGATION PIPELINE")
        print("=" * 60)

        # --------------------------------------------------------
        # STEP 1 — CHECK FILE
        # --------------------------------------------------------

        print("\n[1/4] Validating input image...")

        if not os.path.exists(target_image_path):

            print("      FAILED: Image file not found.")

            return {
                "success": False,
                "error": (
                    f"Target image not found at "
                    f"'{target_image_path}'"
                ),
                "results": []
            }

        print("      File found.")

        # --------------------------------------------------------
        # STEP 2 — FACE DETECTION
        # --------------------------------------------------------

        print("\n[2/4] Checking for a face...")

        try:

            has_face = self.verifier.has_face(
                target_image_path
            )

        except Exception as error:

            print("      FAILED: Face detection error.")

            return {
                "success": False,
                "error": (
                    f"Face detection failed: {error}"
                ),
                "results": []
            }

        if not has_face:

            print("      FAILED: No face detected.")

            return {
                "success": False,
                "error": (
                    "No face detected in the provided input image. "
                    "Please upload an image with a clear face."
                ),
                "total_candidates_found": 0,
                "total_candidates_downloaded": 0,
                "candidates_without_faces": 0,
                "download_failures": 0,
                "total_candidates_evaluated": 0,
                "verified_matches_count": 0,
                "results": []
            }

        print("      Face detected.")

        # --------------------------------------------------------
        # STEP 3 — SEARCH
        # --------------------------------------------------------

        print("\n[3/4] Searching for candidate images...")

        try:

            search_response = search_image(
                target_image_path
            )

        except Exception as error:

            print("      FAILED: Search error.")

            return {
                "success": False,
                "error": (
                    f"Image search failed: {error}"
                ),
                "results": []
            }

        candidates = search_response.get(
            "candidates",
            []
        )

        total_candidates_found = len(candidates)

        print(
            f"      Candidates found: "
            f"{total_candidates_found}"
        )

        if not candidates:

            print(
                "      No candidate images were returned."
            )

            return {
                "success": True,
                "target_image": target_image_path,
                "total_candidates_found": 0,
                "total_candidates_downloaded": 0,
                "candidates_without_faces": 0,
                "download_failures": 0,
                "total_candidates_evaluated": 0,
                "verified_matches_count": 0,
                "results": []
            }

        # --------------------------------------------------------
        # STEP 4 — VERIFY CANDIDATES
        # --------------------------------------------------------

        print("\n[4/4] Verifying candidate faces...")

        # Statistics
        downloaded_count = 0
        no_face_count = 0
        download_failed_count = 0
        evaluated_count = 0

        all_evaluated_results = []

        # --------------------------------------------------------
        # Browser-like headers
        # --------------------------------------------------------

        opener = urllib.request.build_opener()

        opener.addheaders = [
            (
                "User-agent",
                (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/120.0.0.0 "
                    "Safari/537.36"
                )
            )
        ]

        urllib.request.install_opener(opener)

        # --------------------------------------------------------
        # Limit number of candidates scanned
        # --------------------------------------------------------

        candidates_to_scan = candidates[
            :self.max_candidates_to_scan
        ]

        # --------------------------------------------------------
        # PROCESS CANDIDATES
        # --------------------------------------------------------

        for idx, candidate in enumerate(
            candidates_to_scan,
            start=1
        ):

            # Stop once enough candidates have been evaluated
            if evaluated_count >= self.max_evaluations:

                self.log(
                    f"Reached evaluation limit "
                    f"({self.max_evaluations})."
                )

                break

            # ----------------------------------------------------
            # EXTRACT IMAGE URL
            # ----------------------------------------------------

            candidate_url = (
                candidate.get("image_url")
                if isinstance(candidate, dict)
                else candidate
            )

            if not candidate_url:

                self.log(
                    f"Candidate {idx} skipped: "
                    f"No image URL."
                )

                continue

            # ----------------------------------------------------
            # TEMP FILE
            # ----------------------------------------------------

            temp_dir = tempfile.gettempdir()

            temp_filename = os.path.join(
                temp_dir,
                f"dogseye_candidate_{idx}.jpg"
            )

            # ----------------------------------------------------
            # DOWNLOAD
            # ----------------------------------------------------

            try:

                req = urllib.request.Request(
                    candidate_url
                )

                with urllib.request.urlopen(
                    req,
                    timeout=8
                ) as response:

                    with open(
                        temp_filename,
                        "wb"
                    ) as out_file:

                        out_file.write(
                            response.read()
                        )

                downloaded_count += 1

                self.log(
                    f"Downloaded candidate {idx}"
                )

            except Exception as download_error:

                download_failed_count += 1

                self.log(
                    f"Candidate {idx} download failed: "
                    f"{download_error}"
                )

                continue

            # ----------------------------------------------------
            # FACE VERIFICATION
            # ----------------------------------------------------

            try:

                verification = (
                    self.verifier.verify_faces(
                        img_path_1=target_image_path,
                        img_path_2=temp_filename
                    )
                )

                # Candidate contains no detectable face
                if (
                    verification.get("error")
                    and "No face detected"
                    in verification["error"]
                ):

                    no_face_count += 1

                    self.log(
                        f"Candidate {idx}: "
                        f"No face detected."
                    )

                    continue

                # Candidate successfully evaluated
                evaluated_count += 1

                similarity_score = round(
                    verification.get(
                        "similarity_score",
                        0.0
                    ),
                    4
                )

                verified = verification.get(
                    "verified",
                    False
                )

                result = {
                    "candidate_id": idx,

                    "title": (
                        candidate.get("title")
                        if isinstance(candidate, dict)
                        else None
                    ),

                    "source": (
                        candidate.get("source")
                        if isinstance(candidate, dict)
                        else None
                    ),

                    "page_url": (
                        candidate.get("page_url")
                        if isinstance(candidate, dict)
                        else None
                    ),

                    "image_url": candidate_url,

                    "verified": verified,

                    "similarity_score": similarity_score
                }

                # Keep ALL evaluated candidates.
                #
                # This lets us inspect the highest similarity
                # candidates even if they don't pass threshold.
                all_evaluated_results.append(
                    result
                )

                self.log(
                    f"Candidate {idx}: "
                    f"Similarity={similarity_score}, "
                    f"Verified={verified}"
                )

            except Exception as evaluation_error:

                self.log(
                    f"Candidate {idx} evaluation error: "
                    f"{evaluation_error}"
                )

            finally:

                # ------------------------------------------------
                # CLEAN UP TEMP FILE
                # ------------------------------------------------

                if os.path.exists(temp_filename):

                    try:

                        os.remove(
                            temp_filename
                        )

                    except OSError:

                        pass

        # ========================================================
        # SORT BY SIMILARITY
        # ========================================================

        all_evaluated_results.sort(
            key=lambda result: result[
                "similarity_score"
            ],
            reverse=True
        )

        # ========================================================
        # VERIFIED RESULTS
        # ========================================================

        verified_results = [

            result

            for result
            in all_evaluated_results

            if result["verified"]

        ]

        # ========================================================
        # CLEAN SUMMARY
        # ========================================================

        print("\n" + "-" * 60)
        print("PIPELINE SUMMARY")
        print("-" * 60)

        print(
            f"Candidates found:        "
            f"{total_candidates_found}"
        )

        print(
            f"Successfully downloaded: "
            f"{downloaded_count}"
        )

        print(
            f"Candidates without face: "
            f"{no_face_count}"
        )

        print(
            f"Download failures:       "
            f"{download_failed_count}"
        )

        print(
            f"Candidates evaluated:    "
            f"{evaluated_count}"
        )

        print(
            f"Verified matches:        "
            f"{len(verified_results)}"
        )

        # ========================================================
        # TOP CANDIDATES
        # ========================================================

        if all_evaluated_results:

            print("\nTOP FACE SIMILARITY RESULTS")

            for rank, result in enumerate(
                all_evaluated_results[:5],
                start=1
            ):

                status = (
                    "VERIFIED"
                    if result["verified"]
                    else "NOT VERIFIED"
                )

                print(
                    f"{rank}. "
                    f"Candidate "
                    f"{result['candidate_id']} "
                    f"| Similarity: "
                    f"{result['similarity_score']} "
                    f"| {status}"
                )

        else:

            print(
                "\nNo candidates could be "
                "successfully evaluated."
            )

        print("=" * 60)

        # ========================================================
        # RETURN STRUCTURED RESULT
        # ========================================================

        return {

            "success": search_response.get(
                "success",
                True
            ),

            "target_image": target_image_path,

            "total_candidates_found":
                total_candidates_found,

            "total_candidates_downloaded":
                downloaded_count,

            "candidates_without_faces":
                no_face_count,

            "download_failures":
                download_failed_count,

            "total_candidates_evaluated":
                evaluated_count,

            "verified_matches_count":
                len(verified_results),

            # Only verified results go to blockchain
            "results":
                verified_results,

            # Top evaluated candidates are useful
            # for debugging but should not necessarily
            # be stored as verified evidence.
            "top_candidates":
                all_evaluated_results[:10]
        }


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    import sys

    test_image = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "data/inputs/sample_test.jpg"
    )

    # --------------------------------------------------------
    # DEBUG SETTINGS
    # --------------------------------------------------------

    pipeline = IntegratedPipeline(

        # Try 0.35 for testing.
        # Do not immediately go much lower.
        threshold=0.35,

        # Number of successfully evaluated candidates.
        max_evaluations=50,

        # Maximum search results to inspect.
        max_candidates_to_scan=100,

        # False = clean demo output
        # True = detailed debugging output
        verbose=True
    )

    output = pipeline.execute(
        test_image
    )

    print(
        "\n=== STRUCTURED PIPELINE RESULT ==="
    )

    print(
        json.dumps(
            output,
            indent=2
        )
    )