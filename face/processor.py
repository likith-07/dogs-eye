import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import os
import cv2
import numpy as np
from typing import Dict, Any
import insightface
from insightface.app import FaceAnalysis
from face.models import format_process_output

class FaceProcessor:
    def __init__(self, output_crop_dir: str = "data/inputs/face_crops"):
        self.output_crop_dir = output_crop_dir
        os.makedirs(self.output_crop_dir, exist_ok=True)

        # Initialize InsightFace using Buffalo_l model (ArcFace)
        self.app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def process_image(self, image_path: str) -> Dict[str, Any]:
        """
        Detects faces, selects primary face, crops it, and extracts ArcFace embedding.
        Matches project contract interface.
        """
        if not os.path.exists(image_path):
            return format_process_output(
                success=False, 
                face_detected=False, 
                error=f"File not found: {image_path}"
            )

        img = cv2.imread(image_path)
        if img is None:
            return format_process_output(
                success=False, 
                face_detected=False, 
                error="Failed to decode image file."
            )

        try:
            faces = self.app.get(img)

            if not faces:
                return format_process_output(
                    success=True,
                    face_detected=False,
                    face_crop_path=None,
                    embedding=None
                )

            # Select primary (largest) face by bounding box area
            primary_face = max(
                faces,
                key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1])
            )

            bbox = primary_face.bbox.astype(int)
            h, w, _ = img.shape
            x1, y1 = max(0, bbox[0]), max(0, bbox[1])
            x2, y2 = min(w, bbox[2]), min(h, bbox[3])

            cropped_img = img[y1:y2, x1:x2]

            crop_filename = f"crop_{os.path.basename(image_path)}"
            crop_path = os.path.join(self.output_crop_dir, crop_filename)
            cv2.imwrite(crop_path, cropped_img)

            return format_process_output(
                success=True,
                face_detected=True,
                face_crop_path=crop_path,
                embedding=primary_face.embedding.tolist()
            )

        except Exception as e:
            return format_process_output(
                success=False,
                face_detected=False,
                error=str(e)
            )