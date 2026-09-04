import os
from typing import List, Optional, Dict, Any

def format_process_output(
    success: bool, 
    face_detected: bool, 
    face_crop_path: Optional[str] = None, 
    embedding: Optional[List[float]] = None,
    error: Optional[str] = None
) -> Dict[str, Any]:
    """Ensures exact compliance with the team's module contract."""
    res = {
        "success": success,
        "face_detected": face_detected,
        "face_crop_path": face_crop_path,
        "embedding": embedding
    }
    if error:
        res["error"] = error
    return res

def format_verify_output(
    verified: bool, 
    similarity_score: float,
    error: Optional[str] = None
) -> Dict[str, Any]:
    """Ensures exact compliance with the verification output contract."""
    res = {
        "verified": verified,
        "similarity_score": round(float(similarity_score), 4)
    }
    if error:
        res["error"] = error
    return res