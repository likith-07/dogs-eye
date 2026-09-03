from face.processor import FaceProcessor
from face.verifier import FaceVerifier

_processor = FaceProcessor()
_verifier = FaceVerifier()

def process_image(image_path: str):
    """Module contract method for processing single images."""
    return _processor.process_image(image_path)

def verify_faces(input_face_path: str, candidate_face_path: str):
    """Module contract method for verifying two face images."""
    return _verifier.verify_faces(input_face_path, candidate_face_path)