import os
from face import process_image, verify_faces

def test_milestone_1():
    test_img = "data/inputs/sample_test.jpg"
    
    # Quick sanity check for dummy file
    if not os.path.exists(test_img):
        print(f"Please place a valid test face image at '{test_img}' to run the test.")
        return

    print("\n=== Testing process_image() ===")
    res = process_image(test_img)
    print(f"Success: {res.get('success')}")
    print(f"Face Detected: {res.get('face_detected')}")
    print(f"Crop Path: {res.get('face_crop_path')}")
    if res.get("embedding"):
        print(f"Embedding Size: {len(res['embedding'])} dimensions")
        print(f"Embedding Sample: {res['embedding'][:5]}...")

    print("\n=== Testing verify_faces() ===")
    v_res = verify_faces(test_img, test_img) # Self-comparison test
    print(f"Verified Match: {v_res.get('verified')}")
    print(f"Similarity Score: {v_res.get('similarity_score')}")

if __name__ == "__main__":
    test_milestone_1()