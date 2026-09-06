import os
import json
from typing import Dict, Any, List

from search.engine import search_image


class IntegratedPipeline:

    def __init__(
        self,
        max_candidates: int = 100,
        max_evaluations: int = 10,
        verbose: bool = False,
        provider_threshold: float = 0.70
    ):
        self.max_candidates = max_candidates
        self.max_evaluations = max_evaluations
        self.verbose = verbose
        self.provider_threshold = provider_threshold

    def _normalize_provider_score(self, rank_val: Any, provider: str, position: int = 1) -> float:
        """
        Calculates a 0.0 - 1.0 similarity score using provider metadata 
        or sliding list-position confidence.
        """
        if provider == "facefinder":
            try:
                score_float = float(rank_val)
                if score_float > 1.0:
                    return score_float / 100.0
                return score_float
            except (ValueError, TypeError):
                pass
                
        # Position-based sliding score (Index 1 = 0.95, Index 10 = 0.50)
        return max(0.40, 1.0 - (position * 0.05))

    def execute(
        self,
        target_image_path: str
    ) -> Dict[str, Any]:

        print("\n" + "=" * 60)
        print("DOGSEYE SEARCH PIPELINE (PROVIDER SCORING MODE)")
        print("=" * 60)

        if not os.path.exists(target_image_path):
            return {
                "success": False,
                "error": f"Image not found: {target_image_path}",
                "results": []
            }

        print("\n[1/3] Input image validated.")
        print("\n[2/3] Searching providers...")

        try:
            search_response = search_image(
                image_path=target_image_path,
                max_candidates=self.max_candidates,
                verbose=self.verbose
            )
        except Exception as error:
            return {
                "success": False,
                "error": f"Search failed: {error}",
                "results": []
            }

        candidates = search_response.get("candidates", [])
        search_statistics = search_response.get("stats", {})

        print(f"Candidates found: {len(candidates)}")
        print(f"\n[3/3] Evaluating top {self.max_evaluations} candidates via provider scores...")

        evaluated_results: List[Dict[str, Any]] = []

        for index, candidate in enumerate(candidates[:self.max_evaluations], start=1):
            provider = candidate.get("provider", "unknown")
            raw_rank = candidate.get("search_rank")
            
            similarity_score = self._normalize_provider_score(raw_rank, provider, position=index)
            is_verified = bool(similarity_score >= self.provider_threshold)

            candidate["candidate_id"] = index
            candidate["verified"] = is_verified
            candidate["similarity_score"] = similarity_score

            if self.verbose:
                print(
                    f" Candidate #{index} [{provider}]: "
                    f"Score={similarity_score:.2f} -> Verified={is_verified}"
                )

            evaluated_results.append(candidate)

        verified_count = sum(1 for c in evaluated_results if c.get("verified"))
        print(f"\nEvaluation Complete: {verified_count}/{len(evaluated_results)} candidates verified.")

        return {
            "success": search_response.get("success", True),
            "target_image": target_image_path,
            "total_candidates_found": len(candidates),          
            "total_candidates_evaluated": len(evaluated_results), 
            "verified_matches_count": verified_count,
            "search_statistics": search_statistics,
            "results": evaluated_results                        
        }