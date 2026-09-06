import json
import sys
import os

from pipeline.integrated_pipeline import IntegratedPipeline
from pipeline.evidence_builder import build_evidence
from blockchain.chain import Blockchain


def process_image(image_path: str):

    print("\n==============================")
    print("STARTING COMPLETE PIPELINE")
    print("==============================\n")

    # --------------------------------
    # 1. RUN SEARCH PIPELINE
    # --------------------------------
    try:
        pipeline = IntegratedPipeline(
            max_candidates=100,
            max_evaluations=10,
            verbose=True,
            provider_threshold=0.80  # Score threshold for matches
        )

        pipeline_result = pipeline.execute(image_path)
    except Exception as e:
        print(f"\n[Main Error] Pipeline failed with exception: {e}")
        return {"success": False, "error": str(e)}

    # --------------------------------
    # 2. STOP IF PIPELINE FAILED
    # --------------------------------
    if not pipeline_result.get("success"):
        print("\n[Main] Pipeline search failed or returned no results.")
        return pipeline_result

    # --------------------------------
    # 3. BUILD BLOCKCHAIN EVIDENCE
    # --------------------------------
    print("\n[Main] Building evidence record...")
    try:
        evidence = build_evidence(image_path, pipeline_result)
    except Exception as e:
        print(f"\n[Main Error] Evidence building failed: {e}")
        return {"success": False, "error": f"Evidence build error: {e}"}

    # --------------------------------
    # 4. LOAD BLOCKCHAIN
    # --------------------------------
    print("[Main] Loading blockchain...")
    try:
        blockchain = Blockchain()
    except Exception as e:
        print(f"\n[Main Error] Failed to initialize blockchain: {e}")
        return {"success": False, "error": f"Blockchain init error: {e}"}

    # --------------------------------
    # 5. ADD EVIDENCE BLOCK & SAVE
    # --------------------------------
    print("[Main] Adding evidence to blockchain...")
    try:
        new_block = blockchain.add_block(evidence)
    except Exception as e:
        print(f"\n[Main Error] Failed to add block: {e}")
        return {"success": False, "error": f"Add block error: {e}"}

    # --------------------------------
    # 6. VALIDATE BLOCKCHAIN
    # --------------------------------
    chain_valid = blockchain.is_chain_valid()

    # --------------------------------
    # 7. ATTACH BLOCKCHAIN RESULT
    # --------------------------------
    pipeline_result["blockchain"] = {
        "block_index": new_block.get("index"),
        "block_hash": new_block.get("block_hash"),
        "chain_valid": chain_valid,
    }

    print("\n==============================")
    print("PIPELINE COMPLETE")
    print("==============================\n")

    return pipeline_result


# ====================================
# COMMAND LINE ENTRY
# ====================================
if __name__ == "__main__":

    image_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "data/inputs/sample_test.jpg"
    )

    if not os.path.exists(image_path):
        print(f"[Error] Target image file does not exist at path: '{image_path}'")
        sys.exit(1)

    output = process_image(image_path)

    print("\n=== FINAL OUTPUT ===")
    print(json.dumps(output, indent=2))