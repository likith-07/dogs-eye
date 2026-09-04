import os
import json
import urllib.request
import tempfile
from typing import Dict, Any, List

# Import modules from your project structure
from face.verifier import FaceVerifier
from search.engine import search_image


class IntegratedPipeline:
    def __init__(self, threshold: float = 0.40, max_evaluations: int = 30):
        # Initialize Face Verifier (InsightFace)
        self.verifier = FaceVerifier(threshold=threshold)
        self.max_evaluations = max_evaluations

    def execute(self, target_image_path: str) -> Dict[str, Any]:
        print(f"[Pipeline] Processing target image: {target_image_path}")

        # 1. Check if the local image file exists
        if not os.path.exists(target_image_path):
            return {
                "success": False, 
                "error": f"Target image not found at '{target_image_path}'"
            }

        # 2. PRE-CHECK: Detect if the input image actually contains a face
        # 2. PRE-CHECK
        print("[Pipeline] Validating face presence in input image...")
        if not self.verifier.has_face(target_image_path):
            print("[Pipeline] Aborting: No face detected in the input image.")
            return {
                "success": False,
                "error": "No face detected in the provided input image. Please upload an image with a clear face.",
                "total_candidates_found": 0,
                "total_candidates_evaluated": 0,
                "verified_matches_count": 0,
                "results": []
            }

        print(f"[Pipeline] Target face confirmed.")

        # --- STEP A: Reverse Image Search ---
        print("[Pipeline] Executing reverse image search...")
        search_response = search_image(target_image_path)
        candidates = search_response.get("candidates", [])
        print(f"[Pipeline] Found {len(candidates)} candidate match(es).")

        # --- STEP B: Candidate Downloader & ArcFace Verification ---
        print(f"[Pipeline] Verifying up to {self.max_evaluations} candidates with ArcFace...")
        verified_results = []

        # Configure browser headers to bypass HTTP 403 Forbidden on CDNs (Instagram, FB, Twitter)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        evaluated_count = 0

        for idx, candidate in enumerate(candidates, start=1):
            if evaluated_count >= self.max_evaluations:
                print(f"[Pipeline] Reached maximum evaluation cap of {self.max_evaluations} candidates.")
                break

            candidate_url = candidate.get("image_url") if isinstance(candidate, dict) else candidate

            if not candidate_url:
                continue

            temp_dir = tempfile.gettempdir()
            temp_filename = os.path.join(temp_dir, f"candidate_temp_{idx}.jpg")

            # Fix for incomplete evaluations: Add strict 5-second socket timeout to prevent hung requests
            try:
                req = urllib.request.Request(candidate_url)
                with urllib.request.urlopen(req, timeout=5) as response, open(temp_filename, 'wb') as out_file:
                    out_file.write(response.read())
            except Exception as download_err:
                # Silently skip candidates that time out or return 403 blocks
                continue

            evaluated_count += 1

            try:
                # Perform facial verification
                verification = self.verifier.verify_faces(
                    img_path_1=target_image_path,
                    img_path_2=temp_filename
                )

                # Skip candidates where no face was found in the candidate web image
                if verification.get("error") and "No face detected" in verification["error"]:
                    continue

                verified_results.append({
                    "candidate_id": idx,
                    "title": candidate.get("title") if isinstance(candidate, dict) else None,
                    "source": candidate.get("source") if isinstance(candidate, dict) else None,
                    "page_url": candidate.get("page_url") if isinstance(candidate, dict) else None,
                    "image_url": candidate_url,
                    "verified": verification["verified"],
                    "similarity_score": round(verification["similarity_score"], 4)
                })
            except Exception as eval_err:
                print(f"[Pipeline] Error evaluating candidate {idx}: {eval_err}")
            finally:
                # Clean up temporary downloaded file safely on Windows
                if os.path.exists(temp_filename):
                    try:
                        os.remove(temp_filename)
                    except OSError:
                        pass

        # --- STEP C: Output Structured Payload for Blockchain ---
        return {
            "success": search_response.get("success", True),
            "target_image": target_image_path,
            "total_candidates_found": len(candidates),
            "total_candidates_evaluated": evaluated_count,
            "verified_matches_count": sum(1 for r in verified_results if r["verified"]),
            "results": verified_results
        }


if __name__ == "__main__":
    import sys
    
    # Initialize pipeline with max evaluation count
    pipeline = IntegratedPipeline(max_evaluations=30)
    
    # Accept image path as command line arg or use default sample
    test_image = sys.argv[1] if len(sys.argv) > 1 else "data/inputs/sample_test.jpg"
    
    output = pipeline.execute(test_image)
    
    print("\n=== FINAL INTEGRATED PAYLOAD (Ready for Blockchain) ===")
    print(json.dumps(output, indent=2))