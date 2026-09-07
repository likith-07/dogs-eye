# DogsEye

### Image-Based Open Web Investigation & Evidence Verification System

```text
██████╗  ██████╗  ███████╗███████╗███████╗██╗   ██╗███████╗
██╔══██╗██╔═══██╗██╔════╝ ██╔════╝██╔════╝╚██╗ ██╔╝██╔════╝
██║  ██║██║   ██║██║  ███╗███████╗█████╗   ╚████╔╝ █████╗
██║  ██║██║   ██║██║   ██║╚════██║██╔══╝    ╚██╔╝  ██╔══╝
██████╔╝╚██████╔╝╚██████╔╝███████║███████╗   ██║   ███████╗
╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚══════╝
```

```text
┌──────────────────────────────────────────────────────────────┐
│                      INVESTIGATION FLOW                      │
└──────────────────────────────────────────────────────────────┘

                         INPUT IMAGE
                              │
                              ▼
                  REVERSE IMAGE SEARCH
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
             SEARCHAPI                 OPENNINJA
                 │                         │
                 └────────────┬────────────┘
                              ▼
                       RESULT MERGING
                              │
                              ▼
                        NORMALIZATION
                              │
                              ▼
                    FILTER + DEDUPLICATION
                              │
                              ▼
                    RESULT CLASSIFICATION
                              │
                  ┌───────────┼───────────┐
                  ▼           ▼           ▼
              PROFILES      POSTS      EXTERNAL
                  │           │           │
                  └───────────┼───────────┘
                              ▼
                       EVIDENCE BUILDER
                              │
                              ▼
                       SHA-256 HASHING
                              │
                              ▼
                     ETHEREUM SEPOLIA
                              │
                              ▼
                     INTEGRITY CHECK
```

---

# `> WHOAMI`

**DogsEye** is an image-based open web investigation and evidence verification system.

The system accepts an input image and uses supported reverse image search providers to discover potentially related or matching images available on the open web.

Search results from multiple providers are aggregated and passed through a common processing pipeline that performs:

```text
SEARCH
   ↓
NORMALIZE
   ↓
FILTER
   ↓
DEDUPLICATE
   ↓
CLASSIFY
   ↓
BUILD EVIDENCE
   ↓
HASH
   ↓
REGISTER
   ↓
VERIFY
```

The goal is to provide an investigation workflow where discovered results can be reviewed and the resulting evidence can be cryptographically committed to a blockchain.

---

# `> WHAT DOES DOGSEYE DO?`

Given an input image, DogsEye performs the following operations:

```text
                    ┌─────────────────┐
                    │   INPUT IMAGE   │
                    └────────┬────────┘
                             │
                             ▼
                 ┌────────────────────────┐
                 │ REVERSE IMAGE SEARCH   │
                 └────────────┬───────────┘
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          ┌────────────────┐       ┌────────────────┐
          │    SEARCHAPI   │       │   OPENNINJA    │
          └───────┬────────┘       └───────┬────────┘
                  │                        │
                  └────────────┬───────────┘
                               ▼
                      ┌────────────────┐
                      │ RESULT MERGING │
                      └────────┬───────┘
                               ▼
                      ┌────────────────┐
                      │ NORMALIZATION  │
                      └────────┬───────┘
                               ▼
                      ┌────────────────┐
                      │    FILTERING   │
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
                   ┌───────────┼───────────┐
                   ▼           ▼           ▼
                PROFILES      POSTS      EXTERNAL
                   │           │           │
                   └───────────┼───────────┘
                               ▼
                      ┌────────────────┐
                      │ EVIDENCE BUILD │
                      └────────┬───────┘
                               ▼
                      ┌────────────────┐
                      │   SHA-256 HASH │
                      └────────┬───────┘
                               ▼
                      ┌────────────────┐
                      │ ETHEREUM       │
                      │ SEPOLIA        │
                      └────────────────┘
```

### Core capabilities

* Reverse image search using multiple providers.
* SearchAPI as a primary search provider.
* OpenNinja as a secondary search provider.
* Result aggregation.
* Provider-independent result normalization.
* URL filtering.
* Candidate deduplication.
* Social media profile detection.
* Social media post detection.
* External link detection.
* Cryptographic evidence hashing.
* Evidence registration on Ethereum Sepolia.
* Blockchain-based evidence verification.
* Detection of modifications to the original evidence file.
* Web-based investigation interface.

---

# `> SYSTEM ARCHITECTURE`

```text
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                            │
│                                                             │
│                    DogsEye Investigation UI                 │
│                                                             │
│       Upload Image → Investigate → Review Results           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               │ HTTP
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                          BACKEND                            │
│                                                             │
│                       FastAPI Application                   │
│                                                             │
│                  POST /api/investigate                      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    INVESTIGATION PIPELINE                   │
│                                                             │
│ Input → Search → Normalize → Filter → Deduplicate           │
│                              → Classify → Evidence           │
└───────────────────────┬───────────────────┬─────────────────┘
                        │                   │
                        ▼                   ▼
              ┌─────────────────┐   ┌─────────────────┐
              │    SEARCHAPI    │   │    OPENNINJA    │
              │    PRIMARY      │   │    SECONDARY    │
              └────────┬────────┘   └────────┬────────┘
                       │                     │
                       └──────────┬──────────┘
                                  ▼
                       ┌────────────────────┐
                       │ NORMALIZED RESULTS │
                       └──────────┬─────────┘
                                  ▼
                       ┌────────────────────┐
                       │ RESULT CLASSIFIER  │
                       └──────────┬─────────┘
                                  ▼
                       ┌────────────────────┐
                       │ EVIDENCE BUILDER   │
                       └──────────┬─────────┘
                                  │
                                  ▼
                       ┌────────────────────┐
                       │ SHA-256 HASHING    │
                       └──────────┬─────────┘
                                  │
                                  ▼
                       ┌────────────────────┐
                       │ ETHEREUM SEPOLIA   │
                       │ EVIDENCE REGISTRY  │
                       └──────────┬─────────┘
                                  │
                                  ▼
                       ┌────────────────────┐
                       │ INTEGRITY VERIFY   │
                       └────────────────────┘
```

---

# `> COMPONENTS`

## `[01] SEARCH ENGINE`

Location:

```text
search/
```

The search engine is responsible for discovering potential online occurrences of the input image.

DogsEye uses multiple providers:

```text
                    INPUT IMAGE
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          SEARCHAPI             OPENNINJA
          PRIMARY               SECONDARY
              │                     │
              └──────────┬──────────┘
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

The multi-provider architecture provides redundancy when one search provider returns incomplete results, fails, or reaches an API limitation.

---

# `[02] SEARCH PROVIDERS`

Location:

```text
search/providers/
```

Provider modules isolate external API-specific logic from the rest of the investigation pipeline.

Current providers:

```text
┌──────────────────────────────┐
│          SEARCHAPI            │
│          PRIMARY              │
└──────────────┬───────────────┘
               │
               │
┌──────────────▼───────────────┐
│          OPENNINJA            │
│          SECONDARY            │
└──────────────────────────────┘
```

Each provider follows the general workflow:

```text
INPUT IMAGE
     │
     ▼
PROVIDER REQUEST
     │
     ▼
PROVIDER RESPONSE
     │
     ▼
RESULT EXTRACTION
     │
     ▼
RAW CANDIDATES
```

The provider abstraction makes it possible to add or replace search services without redesigning the rest of the pipeline.

---

# `[03] IMAGE HOSTING`

Location:

```text
search/image_host.py
```

Some reverse image search services require the input image to be accessible through a public URL.

The image hosting component supports this workflow where required:

```text
LOCAL IMAGE
     │
     ▼
UPLOAD / HOST
     │
     ▼
PUBLIC IMAGE URL
     │
     ▼
SEARCH PROVIDER
```

Providers capable of accepting the required input directly do not need to use this intermediate step.

---

# `[04] CANDIDATE NORMALIZATION`

Location:

```text
search/normalizer.py
```

Different search providers can return different response formats.

The normalization layer converts provider-specific results into a consistent internal representation.

Typical fields include:

```json
{
  "page_url": "https://example.com/page",
  "image_url": "https://example.com/image.jpg",
  "title": "Example Result",
  "source": "example.com",
  "provider": "searchapi",
  "search_rank": 1,
  "author": null
}
```

This allows downstream components to remain independent of individual provider response formats.

---

# `[05] FILTERING AND DEDUPLICATION`

After normalization, candidate results are filtered and deduplicated.

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
FINAL CANDIDATE LIST
```

This reduces redundant results and prevents the same occurrence from being processed multiple times.

---

# `[06] RESULT CLASSIFICATION`

DogsEye classifies discovered URLs into three broad categories:

```text
                       CANDIDATE URL
                             │
                             ▼
                   ┌────────────────────┐
                   │ SOCIAL MEDIA URL?  │
                   └─────────┬──────────┘
                             │
                   ┌─────────┴─────────┐
                   ▼                   ▼
                  YES                  NO
                   │                   │
                   ▼                   ▼
             ┌────────────┐       EXTERNAL
             │  IS POST?  │
             └─────┬──────┘
                   │
             ┌─────┴─────┐
             ▼           ▼
            YES          NO
             │            │
             ▼            ▼
            POST       PROFILE
```

---

## Profiles

Social media URLs that appear to represent an account or profile.

Examples include:

```text
instagram.com/username
x.com/username
linkedin.com/in/username
tiktok.com/@username
youtube.com/@username
```

---

## Posts

URLs that appear to represent individual social media posts or pieces of content.

Examples include:

```text
instagram.com/p/...
instagram.com/reel/...
x.com/username/status/...
youtube.com/shorts/...
tiktok.com/@username/video/...
facebook.com/.../posts/...
```

---

## External Links

Candidate URLs that do not correspond to supported social media profile/post patterns.

Examples include:

```text
News websites
Blogs
Forums
Image hosting services
Public websites
Search-indexed pages
```

---

# `> EVIDENCE BUILDER`

Location:

```text
pipeline/evidence_builder.py
```

The Evidence Builder creates the canonical evidence payload used by the blockchain registry.

It extracts relevant investigation information and associates it with the actual uploaded evidence file.

The evidence includes:

```text
Input / target image information
          │
          ▼
Candidate results
          │
          ▼
Search provider information
          │
          ▼
URLs and metadata
          │
          ▼
Original evidence filename
          │
          ▼
SHA-256 file hash
```

The actual image does not need to be placed on the blockchain.

Instead, DogsEye records its cryptographic fingerprint.

Example:

```json
{
  "target_image": "input.jpg",
  "evidence_file": {
    "filename": "input.jpg",
    "sha256": "..."
  },
  "total_candidates_found": 5,
  "results": [
    {
      "page_url": "https://example.com/page",
      "image_url": "https://example.com/image.jpg",
      "source": "example.com",
      "provider": "searchapi",
      "title": "Example",
      "search_rank": 1,
      "author": null,
      "verified": null,
      "similarity_score": 0.91
    }
  ]
}
```

---

# `> CRYPTOGRAPHIC HASHING`

Location:

```text
blockchain/evidence_hasher.py
```

DogsEye uses SHA-256 to create a deterministic hash of the evidence payload.

The evidence is first serialized into canonical JSON:

```text
Evidence Dictionary
       │
       ▼
Deterministic JSON
       │
       ▼
SHA-256
       │
       ▼
Evidence Hash
```

Canonicalization uses sorted JSON keys and deterministic separators so that equivalent evidence produces the same hash.

Conceptually:

```python
canonical_evidence = json.dumps(
    evidence,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False
)

evidence_hash = SHA256(
    canonical_evidence
)
```

This creates a fixed cryptographic fingerprint for the complete evidence record.

---

# `> BLOCKCHAIN EVIDENCE REGISTRY`

DogsEye uses **Ethereum Sepolia** as the blockchain network for evidence registration.

```text
                 EVIDENCE
                     │
                     ▼
              SHA-256 HASH
                     │
                     ▼
              EVIDENCE HASH
                     │
                     ▼
             Ethereum Sepolia
                     │
                     ▼
             Smart Contract
                     │
                     ▼
             REGISTERED HASH
```

The system does not store the complete image on-chain.

Instead, the cryptographic hash of the evidence is registered through the evidence registry smart contract.

The current network configuration is:

```text
Network:        Ethereum Sepolia
Chain ID:       11155111
```

---

# `> EVIDENCE REGISTRATION`

The registration process is:

```text
1. Upload evidence
        │
        ▼
2. Save evidence locally
        │
        ▼
3. Run investigation
        │
        ▼
4. Build evidence payload
        │
        ▼
5. Hash evidence
        │
        ▼
6. Convert hash to bytes32
        │
        ▼
7. Submit transaction
        │
        ▼
8. Ethereum Sepolia
        │
        ▼
9. Evidence hash registered
```

The registry returns information such as:

```json
{
  "success": true,
  "evidence_hash": "...",
  "transaction_hash": "0x...",
  "block_number": 123456,
  "contract_address": "0x...",
  "network": "ethereum-sepolia"
}
```

---

# `> TAMPER DETECTION`

DogsEye uses cryptographic hashing to make modifications to registered evidence detectable.

The original evidence file is hashed before registration:

```text
ORIGINAL IMAGE
      │
      ▼
   SHA-256
      │
      ▼
IMAGE HASH A
      │
      ▼
EVIDENCE PAYLOAD
      │
      ▼
EVIDENCE HASH A
      │
      ▼
ETHEREUM SEPOLIA
```

After the evidence has been registered, the local evidence file can be modified.

For example:

```text
ORIGINAL IMAGE
      │
      │ MODIFY FILE
      ▼
MODIFIED IMAGE
      │
      ▼
   SHA-256
      │
      ▼
IMAGE HASH B
```

Because:

```text
IMAGE HASH A ≠ IMAGE HASH B
```

the resulting evidence hash also changes.

The verifier can therefore detect that the current file no longer corresponds to the evidence committed to the blockchain.

```text
REGISTERED EVIDENCE
        │
        ▼
BLOCKCHAIN HASH
        │
        │
        │ compare
        │
        ▼
CURRENT EVIDENCE
        │
        ▼
CURRENT HASH
        │
        ▼
     MATCH?
      /   \
    YES    NO
     │      │
     ▼      ▼
   VALID  TAMPERED
```

### Important distinction

The blockchain does not physically prevent someone from modifying a local evidence file.

It provides an immutable external reference against which the current evidence can be checked.

Therefore:

```text
Modification prevention     → No
Modification detection      → Yes
Cryptographic verification  → Yes
Blockchain anchoring        → Yes
```

---

# `> TAMPERING DEMO`

The intended demonstration is:

```text
STEP 1
Upload original image
        │
        ▼
STEP 2
Run investigation
        │
        ▼
STEP 3
Build evidence
        │
        ▼
STEP 4
Register evidence on Ethereum Sepolia
        │
        ▼
STEP 5
Verify
        │
        ▼
       VALID
```

Then:

```text
STEP 6
Modify the original image file
        │
        ▼
STEP 7
Verify again
        │
        ▼
Current image hash changes
        │
        ▼
Evidence hash changes
        │
        ▼
Blockchain hash does not match
        │
        ▼
     TAMPERED
```

This demonstrates that the blockchain record can be used as an integrity anchor for the evidence.

---

# `> BLOCKCHAIN VERIFICATION`

The registry verification process is:

```text
CURRENT EVIDENCE
       │
       ▼
CANONICALIZE
       │
       ▼
SHA-256
       │
       ▼
EVIDENCE HASH
       │
       ▼
Ethereum Sepolia
       │
       ▼
verifyEvidence()
       │
       ▼
HASH EXISTS?
     /     \
   YES      NO
    │        │
    ▼        ▼
 VALID     INVALID
```

The smart contract returns information associated with a registered evidence hash, including the submitting address and blockchain timestamp.

Example verification result:

```json
{
  "valid": true,
  "evidence_hash": "...",
  "submitted_by": "0x...",
  "blockchain_timestamp": 1234567890,
  "network": "ethereum-sepolia"
}
```

---

# `> PROJECT STRUCTURE`

```text
DogsEye/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
│
├── frontend/
│   └── index.html
│
├── pipeline/
│   ├── __init__.py
│   └── evidence_builder.py
│
├── search/
│   ├── __init__.py
│   ├── engine.py
│   ├── normalizer.py
│   ├── image_host.py
│   │
│   └── providers/
│       ├── __init__.py
│       ├── searchapi.py
│       └── openninja.py
│
├── blockchain/
│   ├── __init__.py
│   ├── ethereum_client.py
│   ├── evidence_hasher.py
│   └── evidence_registry.py
│
└── data/
    └── inputs/
```

> File names inside `search/providers/` may differ depending on the current provider implementation.

---

# `> REQUIREMENTS`

DogsEye is built primarily with Python.

Core dependencies include:

```text
Python
FastAPI
Uvicorn
Requests
python-dotenv
NumPy
Pydantic
python-multipart
Web3.py
```

The exact dependency versions are defined in:

```text
requirements.txt
```

Recommended Python version:

```text
Python 3.11
```

Python 3.11 is recommended for broad compatibility with the project's dependency stack.

---

# `> INSTALLATION`

## 1. Clone the Repository

```bash
git clone <repository-url>
cd DogsEye
```

---

## 2. Create a Virtual Environment

Windows:

```powershell
py -3.11 -m venv env
```

Linux/macOS:

```bash
python3.11 -m venv env
```

---

## 3. Activate the Environment

### Windows PowerShell

```powershell
env\Scripts\activate
```

### Linux/macOS

```bash
source env/bin/activate
```

---

## 4. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

# `> ENVIRONMENT VARIABLES`

Create a `.env` file in the project root.

The exact variables depend on the provider implementations and Ethereum client configuration.

Typical configuration may include:

```text
SEARCHAPI_KEY=your_searchapi_key
OPENNINJA_API_KEY=your_openninja_key

SEPOLIA_RPC_URL=your_sepolia_rpc_url
PRIVATE_KEY=your_wallet_private_key
CONTRACT_ADDRESS=your_deployed_contract_address
```

Use the variable names expected by the actual implementation.

**Never commit `.env` or private keys to GitHub.**

Add the following to `.gitignore`:

```text
.env
env/
__pycache__/
*.pyc
```

---

# `> RUNNING DOGSEYE`

Start the FastAPI backend from the project root:

```bash
uvicorn app:app --reload
```

The development server will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI also provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

# `> INVESTIGATION API`

## `POST /api/investigate`

Accepts an uploaded image and executes the investigation pipeline.

```text
Upload Image
     │
     ▼
Save Image
     │
     ▼
Run Investigation
     │
     ▼
SearchAPI + OpenNinja
     │
     ▼
Normalize
     │
     ▼
Filter
     │
     ▼
Deduplicate
     │
     ▼
Classify
     │
     ▼
Build Evidence
     │
     ▼
Return Results
```

The endpoint returns both the investigation results and the generated evidence object.

---

# `> BLOCKCHAIN API`

## `POST /api/blockchain/register`

Registers an evidence hash on Ethereum Sepolia.

Request:

```json
{
  "evidence": {}
}
```

The backend:

```text
Evidence
   ↓
SHA-256
   ↓
bytes32
   ↓
Ethereum Transaction
   ↓
Sepolia
```

---

## `POST /api/blockchain/verify`

Verifies whether the evidence hash exists on-chain.

The backend recalculates the hash of the current evidence file before verification.

This is important for the tamper-detection workflow because the verification process should not blindly trust a previously stored file hash.

---

# `> RUNNING AN INVESTIGATION`

1. Start the backend.

```bash
uvicorn app:app --reload
```

2. Open the DogsEye frontend.

3. Select an image.

4. Execute the investigation.

5. Review the discovered candidates.

6. Review the generated evidence.

7. Register the evidence on Ethereum Sepolia.

8. Verify the evidence.

A successful verification should indicate that the calculated evidence hash exists on-chain.

---

# `> SEARCH PROVIDER STRATEGY`

DogsEye uses a primary/secondary provider model:

```text
                    INPUT IMAGE
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
         SEARCHAPI               OPENNINJA
         PRIMARY                SECONDARY
             │                       │
             └───────────┬───────────┘
                         ▼
                  RESULT AGGREGATION
                         │
                         ▼
                    NORMALIZATION
                         │
                         ▼
                   DEDUPLICATION
                         │
                         ▼
                   FINAL RESULTS
```

Using multiple providers reduces dependence on a single external service and allows results from different indexes to be combined.

Provider availability and result quality depend on the external services themselves.

---

# `> SECURITY MODEL`

DogsEye focuses on three primary properties:

```text
INTEGRITY
    +
TRACEABILITY
    +
TAMPER DETECTION
```

The system uses:

```text
SHA-256
   +
Canonical JSON
   +
Ethereum Sepolia
```

to create an externally verifiable integrity reference for investigation evidence.

DogsEye does **not** claim to provide:

```text
Guaranteed identity attribution
Complete internet coverage
Guaranteed reverse-image-search results
Absolute source authenticity
Legal proof of identity
Protection against compromise of the investigator's wallet
```

Search results remain investigative signals that require human interpretation.

---

# `> LIMITATIONS`

## Search Provider Dependency

Search results depend on the indexes and availability of external providers.

An image may exist online without being returned by a particular reverse image search provider.

```text
DOGSEYE
   │
   ▼
SEARCH PROVIDER
   │
   ▼
PROVIDER INDEX
   │
   ▼
AVAILABLE RESULTS
```

---

## API Limits

External providers may impose:

```text
Rate limits
Request quotas
Credit limits
Authentication requirements
Temporary outages
```

A provider becoming unavailable can reduce the number of discovered candidates.

The secondary provider helps provide additional coverage but does not guarantee complete results.

---

## Search Result Accuracy

Providers may return incomplete or imperfect metadata.

For example:

```text
Correct image
     +
Incorrect page URL
```

or:

```text
Relevant page
     +
Missing direct image URL
```

DogsEye normalizes and processes the information returned by the providers but cannot guarantee provider-level accuracy.

---

## Social Media Restrictions

Some platforms restrict automated access to pages or images.

Possible issues include:

```text
HTTP 403
Authentication requirements
Anti-bot protection
CDN restrictions
Expired media URLs
Robots restrictions
```

Consequently, a search provider may identify a relevant page while DogsEye cannot directly retrieve all associated content.

---

## Blockchain Dependency

Evidence registration depends on:

```text
Ethereum Sepolia
     +
RPC provider
     +
Wallet
     +
Smart contract
     +
Sufficient test ETH
```

If the RPC endpoint, wallet, network, or smart contract is unavailable, blockchain registration cannot complete.

---

## Local Evidence Storage

The original uploaded evidence file is stored locally during the investigation.

The blockchain stores the cryptographic evidence reference rather than the complete image.

Therefore, the blockchain alone does not contain the original evidence artifact.

---

# `> WHY BLOCKCHAIN?`

The purpose of the blockchain component is not to store large image files.

Instead, DogsEye uses the blockchain as an external integrity anchor.

```text
                    ORIGINAL EVIDENCE
                           │
                           ▼
                       SHA-256
                           │
                           ▼
                    EVIDENCE HASH
                           │
                           ▼
                    ETHEREUM SEPOLIA
                           │
                           ▼
                  IMMUTABLE REFERENCE
```

Later, the evidence can be hashed again:

```text
CURRENT EVIDENCE
       │
       ▼
    SHA-256
       │
       ▼
CURRENT HASH
       │
       ▼
COMPARE WITH ON-CHAIN HASH
```

If the hashes match, the evidence corresponds to the registered record.

If they do not match, the evidence has changed or is not the same evidence that was registered.

---

# `> DESIGN PRINCIPLES`

DogsEye is designed around several principles:

### Provider Independence

External search providers are isolated from the core pipeline.

### Deterministic Evidence

Evidence is canonicalized before hashing.

### Cryptographic Integrity

SHA-256 provides a fixed fingerprint for the evidence payload.

### External Anchoring

Evidence hashes are registered on Ethereum Sepolia.

### Detectable Tampering

Changes to the evidence result in a different cryptographic fingerprint.

### Separation of Concerns

```text
SEARCH
   ↓
NORMALIZATION
   ↓
CLASSIFICATION
   ↓
EVIDENCE
   ↓
HASHING
   ↓
BLOCKCHAIN
```

Each stage has a separate responsibility.

---

# `> FUTURE IMPROVEMENTS`

Potential future additions include:

```text
[+] Additional reverse image search providers
[+] Improved candidate ranking
[+] Better result confidence scoring
[+] OCR and metadata extraction
[+] Improved social media classification
[+] Investigation history
[+] Database-backed evidence storage
[+] Object storage for evidence artifacts
[+] Cryptographic timestamps
[+] IPFS evidence storage
[+] Stronger evidence provenance
[+] User authentication
[+] Role-based access control
[+] Automated forensic report generation
[+] Improved blockchain gas management
[+] Mainnet or production-chain deployment
[+] Dockerized deployment
[+] Cloud deployment
```

---

# `> QUICK COMMAND REFERENCE`

```bash
# Clone
git clone <repository-url>

# Enter project
cd DogsEye

# Create virtual environment
py -3.11 -m venv env

# Activate
env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn app:app --reload
```

Development server:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# `> END-TO-END FLOW`

```text
┌──────────────────────────────────────────────────────────────┐
│                         DOGSEYE                              │
└──────────────────────────────────────────────────────────────┘

                         INPUT IMAGE
                              │
                              ▼
                    SAVE EVIDENCE FILE
                              │
                              ▼
                  ┌─────────────────────┐
                  │  REVERSE IMAGE      │
                  │      SEARCH         │
                  └──────────┬──────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
                SEARCHAPI          OPENNINJA
                PRIMARY            SECONDARY
                    │                 │
                    └────────┬────────┘
                             ▼
                      RESULT AGGREGATION
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
                       CLASSIFICATION
                             │
                 ┌───────────┼───────────┐
                 ▼           ▼           ▼
              PROFILES      POSTS      EXTERNAL
                 │           │           │
                 └───────────┼───────────┘
                             ▼
                      EVIDENCE BUILDER
                             │
                             ▼
                     SHA-256 FILE HASH
                             │
                             ▼
                    CANONICAL EVIDENCE
                             │
                             ▼
                     SHA-256 EVIDENCE
                             │
                             ▼
                    ETHEREUM SEPOLIA
                             │
                             ▼
                     EVIDENCE REGISTERED
                             │
                             ▼
                         VERIFY
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
                  MATCH            NO MATCH
                    │                 │
                    ▼                 ▼
                  VALID            TAMPERED
```

---

<div align="center">

```text
┌──────────────────────────────────────────────────────────┐
│                                                          │
│                  DogsEye Investigation System             │
│                                                          │
│       SEARCH → ANALYZE → PRESERVE → VERIFY INTEGRITY     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

</div>
