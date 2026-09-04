import json
import sys

from pipeline.integrated_pipeline import (
    IntegratedPipeline
)

from pipeline.evidence_builder import (
    build_evidence
)

from blockchain.chain import Blockchain


def process_image(
    image_path: str
):

    print("\n==============================")
    print("STARTING COMPLETE PIPELINE")
    print("==============================\n")

    # --------------------------------
    # 1. RUN SEARCH + FACE PIPELINE
    # --------------------------------

    pipeline = IntegratedPipeline(
        max_evaluations=30
    )

    pipeline_result = pipeline.execute(
        image_path
    )


    # --------------------------------
    # 2. STOP IF PIPELINE FAILED
    # --------------------------------

    if not pipeline_result.get("success"):

        print("\n[Main] Pipeline failed.")

        return pipeline_result


    # --------------------------------
    # 3. BUILD BLOCKCHAIN EVIDENCE
    # --------------------------------

    print(
        "\n[Main] Building evidence record..."
    )

    evidence = build_evidence(
        image_path,
        pipeline_result
    )


    # --------------------------------
    # 4. LOAD BLOCKCHAIN
    # --------------------------------

    print(
        "[Main] Loading blockchain..."
    )

    blockchain = Blockchain()


    # --------------------------------
    # 5. ADD EVIDENCE BLOCK
    # --------------------------------

    print(
        "[Main] Adding evidence to blockchain..."
    )

    new_block = blockchain.add_block(
        evidence
    )


    # --------------------------------
    # 6. VALIDATE BLOCKCHAIN
    # --------------------------------

    chain_valid = blockchain.is_chain_valid()


    # --------------------------------
    # 7. ATTACH BLOCKCHAIN RESULT
    # --------------------------------

    pipeline_result["blockchain"] = {

        "block_index": new_block[
            "index"
        ],

        "block_hash": new_block[
            "block_hash"
        ],

        "chain_valid": chain_valid
    }


    print(
        "\n=============================="
    )

    print(
        "PIPELINE COMPLETE"
    )

    print(
        "==============================\n"
    )


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


    output = process_image(
        image_path
    )


    print(
        "\n=== FINAL OUTPUT ==="
    )

    print(
        json.dumps(
            output,
            indent=2
        )
    )