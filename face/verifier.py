import cv2
import numpy as np
from typing import Dict, Any
from face.processor import FaceProcessor
from face.models import format_verify_output

class FaceVerifier:
    def __init__(self, threshold: float = 0.40):
        self.processor = FaceProcessor()
        self.threshold = threshold

    def compute_cosine_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        dot_product = np.dot(emb1, emb2)
        norm_a = np.linalg.norm(emb1)
        norm_b = np.linalg.norm(emb2)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot_product / (norm_a * norm_b))

    def verify_faces(self, img_path_1: str, img_path_2: str) -> Dict[str, Any]:
        res1 = self.processor.process_image(img_path_1)
        res2 = self.processor.process_image(img_path_2)

        if not res1["success"] or not res1["face_detected"]:
            return format_verify_output(
                verified=False,
                similarity_score=0.0,
                error=f"No face detected in primary image: {img_path_1}"
            )

        if not res2["success"] or not res2["face_detected"]:
            return format_verify_output(
                verified=False,
                similarity_score=0.0,
                error=f"No face detected in candidate image: {img_path_2}"
            )

        emb1 = np.array(res1["embedding"], dtype=np.float32)
        emb2 = np.array(res2["embedding"], dtype=np.float32)

        similarity_score = self.compute_cosine_similarity(emb1, emb2)
        is_match = similarity_score >= self.threshold

        return format_verify_output(
            verified=bool(is_match),
            similarity_score=similarity_score
        )
    # In face/verifier.py
    def has_face(self, img_path: str) -> bool:
        """
        Checks if at least one face is present in the target image.
        """
        try:
            # Option A: If your class uses self.app, self.model, or self.detector:
            model = getattr(self, 'app', None) or getattr(self, 'model', None) or getattr(self, 'detector', None)
            
            if model is not None:
                img = cv2.imread(img_path)
                if img is None:
                    return False
                faces = model.get(img)
                return len(faces) > 0
            
            # Option B: Fallback using verify_faces against itself
            result = self.verify_faces(img_path, img_path)
            if result.get("error") and "No face detected" in result["error"]:
                return False
            return True
            
        except Exception:
            return False