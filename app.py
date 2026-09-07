import os
import shutil
from typing import Dict, Any

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from main import process_image

from pipeline.evidence_builder import EvidenceBuilder

from blockchain.evidence_registry import EvidenceRegistry


app = FastAPI(
    title="DogsEye"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)

INPUT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "inputs"
)

os.makedirs(
    INPUT_DIR,
    exist_ok=True
)


# ============================================================
# FRONTEND
# ============================================================

@app.get("/")
async def serve_frontend():

    index_path = os.path.join(
        FRONTEND_DIR,
        "index.html"
    )

    if not os.path.exists(index_path):
        raise HTTPException(
            status_code=404,
            detail="frontend/index.html not found"
        )

    return FileResponse(
        index_path
    )


# ============================================================
# INVESTIGATION
# ============================================================

@app.post("/api/investigate")
async def investigate_image(
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No image selected"
        )

    # Prevent directory traversal.
    safe_filename = os.path.basename(
        file.filename
    )

    file_path = os.path.join(
        INPUT_DIR,
        safe_filename
    )

    # --------------------------------------------------------
    # SAVE ORIGINAL EVIDENCE FILE
    # --------------------------------------------------------

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save evidence file: {error}"
        )


    # --------------------------------------------------------
    # RUN DOGSEYE PIPELINE
    # --------------------------------------------------------

    try:

        investigation_result = process_image(
            file_path
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Pipeline failed: {error}"
        )


    # --------------------------------------------------------
    # BUILD EVIDENCE
    # --------------------------------------------------------

    try:

        evidence = EvidenceBuilder.build(
            investigation_result,
            file_path
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Evidence building failed: {error}"
        )


    # --------------------------------------------------------
    # RETURN INVESTIGATION + EVIDENCE
    # --------------------------------------------------------

    return {
        "success": investigation_result.get(
            "success",
            True
        ),

        "investigation": investigation_result,

        "evidence": evidence
    }


# ============================================================
# REGISTER EVIDENCE ON BLOCKCHAIN
# ============================================================

@app.post("/api/blockchain/register")
async def register_evidence(
    payload: Dict[str, Any]
):

    evidence = payload.get(
        "evidence"
    )

    if not evidence:
        raise HTTPException(
            status_code=400,
            detail="Evidence payload is missing"
        )

    # --------------------------------------------------------
    # Make sure the evidence contains file information.
    # --------------------------------------------------------

    evidence_file = evidence.get(
        "evidence_file"
    )

    if not evidence_file:
        raise HTTPException(
            status_code=400,
            detail="Evidence file information is missing"
        )

    filename = evidence_file.get(
        "filename"
    )

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Evidence filename is missing"
        )

    safe_filename = os.path.basename(
        filename
    )

    file_path = os.path.join(
        INPUT_DIR,
        safe_filename
    )

    if not os.path.isfile(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Evidence file not found: {safe_filename}"
        )

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # Recalculate the file hash instead of trusting the
    # hash supplied by the frontend.
    # --------------------------------------------------------

    try:

        current_file_hash = EvidenceBuilder.hash_file(
            file_path
        )

        evidence["evidence_file"]["sha256"] = (
            current_file_hash
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to hash evidence file: {error}"
        )


    # --------------------------------------------------------
    # REGISTER
    # --------------------------------------------------------

    try:

        registry = EvidenceRegistry()

        blockchain_result = registry.register(
            evidence
        )

        return blockchain_result

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Blockchain registration failed: {error}"
        )


# ============================================================
# VERIFY EVIDENCE
# ============================================================

@app.post("/api/blockchain/verify")
async def verify_evidence(
    payload: Dict[str, Any]
):

    evidence = payload.get(
        "evidence"
    )

    if not evidence:
        raise HTTPException(
            status_code=400,
            detail="Evidence payload is missing"
        )

    # --------------------------------------------------------
    # Get the evidence file information.
    # --------------------------------------------------------

    evidence_file = evidence.get(
        "evidence_file"
    )

    if not evidence_file:
        raise HTTPException(
            status_code=400,
            detail="Evidence file information is missing"
        )

    filename = evidence_file.get(
        "filename"
    )

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Evidence filename is missing"
        )

    # Prevent directory traversal.
    safe_filename = os.path.basename(
        filename
    )

    file_path = os.path.join(
        INPUT_DIR,
        safe_filename
    )

    if not os.path.isfile(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Evidence file not found: {safe_filename}"
        )

    # --------------------------------------------------------
    # CRITICAL TAMPER DETECTION STEP
    #
    # Read the CURRENT file from disk and calculate its
    # SHA-256 hash.
    #
    # We intentionally DO NOT trust the hash sent by the
    # frontend.
    # --------------------------------------------------------

    try:

        current_file_hash = EvidenceBuilder.hash_file(
            file_path
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to hash evidence file: {error}"
        )


    # --------------------------------------------------------
    # Replace the potentially stale/untrusted hash with the
    # hash of the actual file currently on disk.
    # --------------------------------------------------------

    evidence["evidence_file"]["sha256"] = (
        current_file_hash
    )


    # --------------------------------------------------------
    # VERIFY AGAINST BLOCKCHAIN
    # --------------------------------------------------------

    try:

        registry = EvidenceRegistry()

        verification_result = registry.verify(
            evidence
        )

        # Add useful information for the frontend/demo.
        verification_result["file_hash"] = current_file_hash
        verification_result["filename"] = safe_filename

        return verification_result

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Blockchain verification failed: {error}"
        )