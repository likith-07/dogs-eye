<div align="center">

<pre>
██████╗  ██████╗  ██████╗ ███████╗███████╗██╗   ██╗███████╗
██╔══██╗██╔═══██╗██╔════╝ ██╔════╝██╔════╝╚██╗ ██╔╝██╔════╝
██║  ██║██║   ██║██║  ███╗███████╗█████╗   ╚████╔╝ █████╗
██║  ██║██║   ██║██║   ██║╚════██║██╔══╝    ╚██╔╝  ██╔══╝
██████╔╝╚██████╔╝╚██████╔╝███████║███████╗   ██║   ███████╗
╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚══════╝
</pre>

# DogsEye

### Image-Based Open Web Investigation & Evidence Verification System

```text
┌──────────────────────────────────────────────────────────────┐
│                        INVESTIGATION FLOW                    │
└──────────────────────────────────────────────────────────────┘

                         INPUT IMAGE
                              │
                              ▼
                    REVERSE IMAGE SEARCH
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                SEARCHAPI          FACEFINDER
                    │                   │
                    └─────────┬─────────┘
                              ▼
                       NORMALIZATION
                              │
                              ▼
                    FILTER + DEDUPLICATION
                              │
                              ▼
                    RESULT CLASSIFICATION
                              │
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
           PROFILES         POSTS         EXTERNAL
               │              │              │
               └──────────────┼──────────────┘
                              ▼
                       EVIDENCE LOGGING
                              │
                              ▼
                         BLOCKCHAIN
                              │
                              ▼
                      INTEGRITY CHECK
```

</div>

---

# `> WHOAMI`

**DogsEye** is an image-based open web investigation and evidence verification system.

The system accepts an input image and attempts to discover visually related or matching images available through supported reverse image search providers. Search results are collected, normalized, filtered, deduplicated, and classified into social media profiles, social media posts, and external web links.

Investigation evidence can then be recorded in a tamper-evident local blockchain.

DogsEye is built around the following workflow:

```text
SEARCH
   +
NORMALIZE
   +
CLASSIFY
   +
VERIFY
   +
PRESERVE EVIDENCE
```

The objective is to create a transparent investigation pipeline where search results and evidence can be reviewed and where historical evidence records can be checked for tampering.

---

# `> WHAT DOES DogsEye DO?`

Given an input image, DogsEye performs the following operations:

```text
                    ┌─────────────────┐
                    │   INPUT IMAGE   │
                    └────────┬────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │ REVERSE IMAGE SEARCH    │
                └────────────┬────────────┘
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
        ┌────────────────┐       ┌────────────────┐
        │   SEARCHAPI    │       │  FACEFINDERAI  │
        └───────┬────────┘       └───────┬────────┘
                │                        │
                └────────────┬───────────┘
                             ▼
                    ┌────────────────┐
                    │ NORMALIZATION  │
                    └────────┬───────┘
                             ▼
                    ┌────────────────┐
                    │   FILTERING    │
                    └────────┬───────┘
                             ▼
                    ┌────────────────┐
                    │ DEDUPLICATION  │
                    └────────┬───────┘
                             ▼
                    ┌────────────────┐
                    │ CLASSIFICATION │
                    └────────┬───────┘
                             │
                ┌────────────┼────────────┐
                ▼            ▼            ▼
             PROFILES      POSTS       EXTERNAL
                │            │            │
                └────────────┼────────────┘
                             ▼
                    ┌────────────────┐
                    │ EVIDENCE STORE │
                    └────────┬───────┘
                             ▼
                    ┌────────────────┐
                    │   BLOCKCHAIN   │
                    └────────────────┘
```

The system provides:

- Reverse image search using multiple providers.
- Parallel execution of search providers.
- Candidate aggregation.
- Candidate normalization.
- URL filtering.
- Candidate deduplication.
- Social media profile detection.
- Social media post detection.
- External link detection.
- Optional face verification using InsightFace.
- Cryptographic hashing of investigation evidence.
- Tamper-evident blockchain storage.
- Blockchain integrity verification.
- A minimal terminal-style investigation dashboard.

---

# `> SYSTEM ARCHITECTURE`

```text
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                            │
│                                                             │
│                      DogsEye Terminal                       │
│                                                             │
│        Upload Image → Execute Investigation → Results       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               │ HTTP
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                         BACKEND                             │
│                                                             │
│                     FastAPI Application                     │
│                                                             │
│                  POST /api/investigate                      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    INTEGRATED PIPELINE                      │
│                                                             │
│   Input Validation → Search → Processing → Evidence         │
└───────────────┬───────────────────────┬─────────────────────┘
                │                       │
                ▼                       ▼
┌────────────────────────┐   ┌──────────────────────────────┐
│      SEARCH ENGINE     │   │      FACE VERIFICATION       │
│                        │   │                              │
│ SearchAPI              │   │ InsightFace                  │
│ FaceFinderAI           │   │ ONNX Runtime                 │
│ Image Hosting          │   │ Similarity Evaluation        │
└──────────────┬─────────┘   └──────────────┬───────────────┘
               │                            │
               └──────────────┬─────────────┘
                              ▼
                 ┌────────────────────────┐
                 │   NORMALIZED RESULTS   │
                 └────────────┬───────────┘
                              ▼
                 ┌────────────────────────┐
                 │   RESULT CLASSIFIER    │
                 └────────────┬───────────┘
                              ▼
                 ┌────────────────────────┐
                 │       BLOCKCHAIN       │
                 └────────────┬───────────┘
                              ▼
                 ┌────────────────────────┐
                 │   INTEGRITY VERIFIER   │
                 └────────────────────────┘
```

---

# `> COMPONENTS`

## `[01] SEARCH ENGINE`

Location:

```text
search/
```

The search engine is responsible for discovering possible online occurrences of the input image.

DogsEye can query multiple reverse image search providers.

```text
                         INPUT IMAGE
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
           FACEFINDERAI                 IMAGE HOST
                 │                         │
                 │                         ▼
                 │                     SEARCHAPI
                 │                         │
                 └────────────┬────────────┘
                              ▼
                         RAW RESULTS
                              │
                              ▼
                         NORMALIZATION
                              │
                              ▼
                          FILTERING
                              │
                              ▼
                        DEDUPLICATION
                              │
                              ▼
                       FINAL CANDIDATES
```

The providers may return different response structures. The search engine passes these results through a normalization layer so the rest of the system receives a consistent format.

Example candidate:

```json
{
    "page_url": "https://example.com/page",
    "image_url": "https://example.com/image.jpg",
    "title": "Example Result",
    "source": "example.com",
    "provider": "search_provider",
    "search_rank": 1,
    "author": null
}
```

---

## `[02] SEARCH PROVIDERS`

Location:

```text
search/providers/
```

DogsEye uses provider modules to keep external search APIs isolated from the rest of the application.

Each provider is responsible for:

```text
INPUT
  │
  ▼
PROVIDER REQUEST
  │
  ▼
PROVIDER RESPONSE
  │
  ▼
EXTRACT RESULTS
  │
  ▼
RETURN RAW CANDIDATES
```

The provider architecture allows additional reverse image search services to be added without redesigning the entire application.

---

## `[03] IMAGE HOSTING`

Location:

```text
search/image_host.py
```

Some reverse image search providers require the input image to be accessible through a public URL.

The image hosting component handles this workflow.

```text
LOCAL IMAGE
     │
     ▼
UPLOAD IMAGE
     │
     ▼
PUBLIC IMAGE URL
     │
     ▼
SEARCH PROVIDER
```

Providers that can directly accept a local image do not require this step.

---

## `[04] CANDIDATE NORMALIZATION`

Location:

```text
search/normalizer.py
```

Different search providers may use different names and structures for URLs, titles, sources, and ranking information.

The normalization layer converts these provider-specific responses into a common candidate structure.

```text
RAW PROVIDER RESPONSE
        │
        ▼
EXTRACT PAGE URL
        │
        ▼
EXTRACT IMAGE URL
        │
        ▼
STANDARDIZE FIELDS
        │
        ▼
EXTRACT SOURCE
        │
        ▼
NORMALIZED CANDIDATE
```

This keeps the rest of the pipeline independent from provider-specific response formats.

---

## `[05] FILTERING AND DEDUPLICATION`

The search engine filters malformed candidates and removes duplicate image URLs.

```text
RAW CANDIDATES
      │
      ▼
VALID URL CHECK
      │
      ▼
REMOVE INVALID RESULTS
      │
      ▼
NORMALIZE URL
      │
      ▼
REMOVE DUPLICATES
      │
      ▼
LIMIT RESULT COUNT
      │
      ▼
FINAL CANDIDATE LIST
```

This prevents unnecessary processing and reduces repeated results.

---

## `[06] FACE VERIFICATION`

Location:

```text
face/verifier.py
```

Face verification is an additional verification layer.

It does not perform reverse image search.

Instead, it can evaluate whether a face in the input image is similar to a face found in a candidate image.

```text
INPUT IMAGE                    CANDIDATE IMAGE
     │                                │
     ▼                                ▼
FACE DETECTION                   FACE DETECTION
     │                                │
     └──────────────┬─────────────────┘
                    ▼
              FACE EMBEDDINGS
                    │
                    ▼
             SIMILARITY SCORE
                    │
              ┌─────┴─────┐
              ▼           ▼
            MATCH      NO MATCH
```

The current implementation uses:

```text
InsightFace
    +
ONNX Runtime
```

Face verification is dependent on:

- The candidate image being downloadable.
- The candidate image containing a detectable face.
- The face being sufficiently clear.
- The search provider returning a usable image URL.

---

# `> RESULT CLASSIFICATION`

DogsEye separates results into three categories.

```text
                    CANDIDATE URL
                          │
                          ▼
                 IS SOCIAL MEDIA?
                     │       │
                   YES       NO
                    │         │
                    ▼         ▼
                  IS POST?  EXTERNAL
                   │    │
                  YES   NO
                   │     │
                   ▼     ▼
                 POST   PROFILE
```

---

## `PROFILES`

Social media URLs that appear to represent an account or profile.

Examples:

```text
instagram.com/username
x.com/username
linkedin.com/in/username
tiktok.com/@username
youtube.com/@username
```

---

## `POSTS`

Social media URLs that appear to represent individual posts or content.

Examples:

```text
instagram.com/p/...
instagram.com/reel/...
x.com/username/status/...
youtube.com/shorts/...
tiktok.com/@username/video/...
facebook.com/.../posts/...
```

---

## `EXTERNAL LINKS`

Any candidate URL that does not belong to a supported social media platform.

Examples may include:

```text
News websites
Blogs
Forums
Image hosting websites
Public websites
Search-indexed pages
```

---

# `> BLOCKCHAIN`

## Blockchain Used

DogsEye currently uses a **custom local blockchain implementation**.

It is not connected to a public blockchain network.

The project does not currently use:

```text
Bitcoin Mainnet
Ethereum Mainnet
Polygon
Solana
Hyperledger
```

Instead, DogsEye uses a lightweight blockchain specifically designed to preserve investigation evidence.

```text
┌──────────────────┐
│   GENESIS BLOCK  │
│                  │
│ previous_hash: 0 │
│ block_hash: ...  │
└────────┬─────────┘
         │
         │ block_hash
         ▼
┌──────────────────┐
│     BLOCK #1     │
│                  │
│ evidence: ...    │
│ previous_hash    │
│ block_hash       │
└────────┬─────────┘
         │
         │ block_hash
         ▼
┌──────────────────┐
│     BLOCK #2     │
│                  │
│ evidence: ...    │
│ previous_hash    │
│ block_hash       │
└────────┬─────────┘
         │
         ▼
       ...
```

Each block contains:

```json
{
    "index": 1,
    "timestamp": "2026-01-01T00:00:00+00:00",
    "evidence": {},
    "previous_hash": "...",
    "block_hash": "..."
}
```

Each block contains a reference to the previous block through `previous_hash`.

The block's own contents are cryptographically hashed to generate `block_hash`.

---

# `> TAMPER EVIDENCE`

The blockchain is designed to make modifications detectable.

Consider the following chain:

```text
BLOCK 0
   │
   │ HASH_A
   ▼
BLOCK 1
previous_hash = HASH_A
   │
   │ HASH_B
   ▼
BLOCK 2
previous_hash = HASH_B
```

If someone modifies the evidence inside `BLOCK 1`:

```text
ORIGINAL BLOCK 1
       │
       ▼
MODIFIED BLOCK 1
       │
       ▼
BLOCK HASH CHANGES
       │
       ▼
BLOCK 2.previous_hash NO LONGER MATCHES
       │
       ▼
CHAIN INVALID
```

This means historical evidence can be checked for tampering.

The blockchain provides **tamper evidence**, not magical prevention of file modification.

Someone can modify the blockchain file, but the integrity verifier should detect that the chain has been altered.

---

# `> WHAT IS STORED?`

Investigation evidence may contain:

```text
Input image hash
      │
      ▼
Matched page URL
      │
      ▼
Matched image URL
      │
      ▼
Source domain
      │
      ▼
Similarity score
      │
      ▼
Search provider
      │
      ▼
Timestamp
```

Example:

```json
{
    "input_image_hash": "sha256_hash_here",
    "matched_page_url": "https://example.com/page",
    "matched_image_url": "https://example.com/image.jpg",
    "source": "example.com",
    "similarity_score": 0.87,
    "search_provider": "searchapi",
    "timestamp": "2026-01-01T00:00:00+00:00"
}
```

The input image itself does not need to be stored inside the blockchain.

Instead:

```text
IMAGE FILE
    │
    ▼
SHA-256 HASH
    │
    ▼
IMAGE FINGERPRINT
    │
    ▼
BLOCKCHAIN EVIDENCE
```

This makes it possible to associate evidence with a specific input image without storing the entire image inside every block.

---

# `> BLOCKCHAIN INTEGRITY VERIFICATION`

The blockchain verifier checks the integrity of the chain.

```text
START
  │
  ▼
LOAD BLOCKCHAIN
  │
  ▼
CHECK GENESIS BLOCK
  │
  ▼
FOR EACH BLOCK
  │
  ├── RECALCULATE BLOCK HASH
  │
  ├── DOES HASH MATCH?
  │
  ├── CHECK PREVIOUS HASH
  │
  └── DOES IT MATCH PREVIOUS BLOCK?
  │
  ▼
VALID / INVALID
```

Conceptually:

```text
FOR EACH BLOCK:

    calculate_hash(block)

    IF calculated_hash != stored_hash:
        CHAIN INVALID

    IF current.previous_hash != previous.block_hash:
        CHAIN INVALID

    OTHERWISE:
        CONTINUE

CHAIN VALID
```

---

# `> PROJECT STRUCTURE`

```text
DogsEye/
│
├── main.py
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── blockchain.json
│
├── frontend/
│   │
│   └── index.html
│
├── pipeline/
│   │
│   ├── __init__.py
│   │
│   └── integrated_pipeline.py
│
├── search/
│   │
│   ├── __init__.py
│   │
│   ├── engine.py
│   │
│   ├── normalizer.py
│   │
│   ├── image_host.py
│   │
│   └── providers/
│       │
│       ├── __init__.py
│       │
│       ├── provider_primary.py
│       │
│       └── provider_secondary.py
│
├── face/
│   │
│   ├── __init__.py
│   │
│   └── verifier.py
│
├── blockchain/
│   │
│   ├── __init__.py
│   │
│   ├── blockchain.py
│   │
│   └── verifier.py
│
└── data/
    │
    └── inputs/
```

---

# `> REQUIREMENTS`

DogsEye uses Python and the following primary dependencies:

```text
requests
python-dotenv

insightface
onnxruntime
opencv-python
numpy

pydantic

fastapi
uvicorn
python-multipart
```

Recommended Python version:

```text
Python 3.11
```

Python 3.11 is recommended because some dependencies, particularly the machine learning and computer vision stack, may not yet provide compatible wheels for newer Python versions.

---

# `> INSTALLATION`

## 1. Clone or Download the Project

```bash
git clone <repository-url>
cd DogsEye
```

If the project was downloaded manually, open a terminal inside the project directory.

---

## 2. Create a Virtual Environment

Windows:

```powershell
py -3.11 -m venv env
```

---

## 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
env\Scripts\activate
```

When activated, your terminal should show something similar to:

```text
(env) PS D:\DogsEye>
```

---

## 4. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. Configure Environment Variables

If the search providers require API keys, create a `.env` file in the project root.

Example:

```text
SEARCHAPI_KEY=your_key_here
FACEFINDER_API_KEY=your_key_here
```

The exact variable names depend on the provider implementations in the project.

Do not commit `.env` files containing private API keys.

---

# `> RUNNING THE PROJECT`

## Start the Backend

From the project root:

```bash
uvicorn app:app --reload
```

The backend should start on:

```text
http://127.0.0.1:8000
```

You can verify that the backend is running using:

```text
http://127.0.0.1:8000/api/health
```

Expected response:

```json
{
    "success": true,
    "status": "online"
}
```

---

# `> RUNNING AN INVESTIGATION`

1. Start the FastAPI backend.

```bash
uvicorn app:app --reload
```

2. Open:

```text
frontend/index.html
```

3. Select an image.

4. Click:

```text
EXECUTE
```

5. DogsEye processes the image.

6. Results are separated into:

```text
┌─────────────────┐
│    PROFILES     │
└─────────────────┘

┌─────────────────┐
│      POSTS      │
└─────────────────┘

┌─────────────────┐
│ EXTERNAL LINKS  │
└─────────────────┘
```

---

# `> RUNNING FROM THE COMMAND LINE`

Depending on your current pipeline configuration, the integrated pipeline can also be tested directly.

Example:

```bash
python -m pipeline.integrated_pipeline data/inputs/sample_image.jpg
```

Or, if configured as a direct script:

```bash
python pipeline/integrated_pipeline.py data/inputs/sample_image.jpg
```

The exact command may depend on your project imports and package structure.

---

# `> TESTING BLOCKCHAIN INTEGRITY`

The blockchain can be tested using the blockchain verifier.

The intended workflow is:

```text
CREATE BLOCKCHAIN
       │
       ▼
ADD EVIDENCE
       │
       ▼
VERIFY CHAIN
       │
       ▼
VALID
```

To test tampering:

```text
CREATE BLOCKCHAIN
       │
       ▼
ADD EVIDENCE
       │
       ▼
VERIFY → VALID
       │
       ▼
MANUALLY MODIFY blockchain.json
       │
       ▼
VERIFY AGAIN
       │
       ▼
INVALID
```

Possible tampering tests include:

```text
[1] Modify evidence data.

[2] Modify a stored similarity score.

[3] Modify a page URL.

[4] Modify an image hash.

[5] Modify a block hash.

[6] Modify a previous_hash value.

[7] Delete a block.

[8] Change a block index.

[9] Insert a fake block.
```

The verifier should detect integrity failures when the hash relationships are broken.

---

# `> KNOWN LIMITATIONS`

DogsEye is a prototype investigation system and has several limitations.

## Search Provider Dependency

Search quality depends heavily on external providers.

```text
DogsEye
   │
   ▼
Search Provider
   │
   ▼
Provider Index
   │
   ▼
Available Results
```

DogsEye cannot discover an image occurrence that is not available through the provider's searchable index.

---

## API Limits

External APIs may have:

```text
Rate limits
Trial limits
Credit limits
Request quotas
Temporary outages
```

A provider may stop returning results if an account reaches its quota or if the provider is unavailable.

---

## Candidate URL Accuracy

A provider may return:

```text
Correct image URL
        +
Incorrect page URL
```

or:

```text
Relevant page
        +
Missing direct image URL
```

DogsEye displays the information returned by the providers after normalization. Provider-level inaccuracies may therefore affect the final investigation output.

---

## Face Verification Limitations

Face verification may fail when:

```text
Face is too small
Face is rotated
Image quality is poor
Face is partially hidden
Multiple faces are present
Candidate image cannot be downloaded
Candidate URL blocks automated requests
```

Face verification should therefore be considered an additional signal rather than an absolute guarantee.

---

## Social Media Access Restrictions

Some platforms actively restrict automated image downloads.

Examples include restrictions such as:

```text
HTTP 403
Authentication requirements
Anti-bot protection
CDN restrictions
Expired media URLs
```

As a result, a valid social media result may be discovered by a search provider but its image may not be downloadable for local verification.

---

## Custom Local Blockchain

The current blockchain implementation is local.

```text
CURRENT IMPLEMENTATION

DogsEye
   │
   ▼
blockchain.json
```

It does not currently provide:

```text
Distributed consensus
Public decentralization
Mining
Proof of Work
Proof of Stake
Public network validation
Smart contracts
Immutable external storage
```

The blockchain provides a lightweight cryptographically linked evidence ledger suitable for demonstrating tamper detection.

A production system could replace this component with:

```text
Ethereum
Polygon
Hyperledger
IPFS + blockchain anchoring
Cloud timestamping services
Other distributed ledger systems
```

---

## Local Storage

The blockchain is currently stored locally.

If the entire blockchain file is replaced together with all hashes being recalculated by an attacker, a local verifier cannot independently determine which version is historically authentic.

For stronger evidence guarantees, future versions could anchor blockchain hashes to an external immutable or independently controlled system.

---

# `> SECURITY MODEL`

DogsEye currently focuses on:

```text
INTEGRITY
    +
TRACEABILITY
    +
TAMPER DETECTION
```

It does not claim to provide:

```text
Perfect source attribution
Guaranteed identity verification
Complete internet coverage
Public blockchain immutability
Legal proof of identity
```

Search results should be treated as investigation evidence requiring human interpretation.

---

# `> FUTURE IMPROVEMENTS`

Possible future additions include:

```text
[+] More reverse image search providers

[+] Improved candidate ranking

[+] Better social media URL classification

[+] Automatic source confidence scoring

[+] OCR and metadata extraction

[+] Better face verification fallback strategies

[+] Asynchronous processing

[+] Investigation history

[+] Database-backed evidence storage

[+] User authentication

[+] Public blockchain hash anchoring

[+] IPFS evidence storage

[+] Cryptographic timestamps

[+] Docker deployment

[+] Cloud deployment

[+] Advanced forensic reporting
```

---

# `> QUICK COMMAND REFERENCE`

```bash
# Create virtual environment
py -3.11 -m venv env

# Activate environment
env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn app:app --reload

# Test backend health
http://127.0.0.1:8000/api/health

# Run an investigation through the frontend
frontend/index.html
```

---

<div align="center">

```text
┌──────────────────────────────────────────────────────────┐
│                                                          │
│                  DogsEye Investigation System            │
│                                                          │
│     SEARCH  →  VERIFY  →  RECORD  →  DETECT TAMPERING    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

</div>