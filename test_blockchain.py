from blockchain.chain import Blockchain
from blockchain.verifier import (
    verify_evidence
)


# ============================================================
# CREATE / LOAD BLOCKCHAIN
# ============================================================

blockchain = Blockchain()


print("\n==============================")
print("BLOCKCHAIN STARTED")
print("==============================\n")


# ============================================================
# CREATE MOCK EVIDENCE
# ============================================================

evidence = {
    "input_image_hash":
        "abc123examplehash",

    "matched_page_url":
        "https://example.com/person",

    "matched_image_url":
        "https://example.com/image.jpg",

    "source":
        "example.com",

    "similarity_score":
        0.87,

    "search_provider":
        "test_provider",

    "timestamp":
        "2026-09-03T12:00:00+00:00"
}


# ============================================================
# ADD BLOCK
# ============================================================

new_block = blockchain.add_block(
    evidence
)


print("NEW BLOCK CREATED:\n")

print(new_block)


# ============================================================
# VALIDATE CHAIN
# ============================================================

print("\n==============================")
print("CHAIN VALIDATION")
print("==============================\n")


is_valid = blockchain.is_chain_valid()


print(
    "CHAIN VALID:",
    is_valid
)


# ============================================================
# VERIFY EVIDENCE
# ============================================================

print("\n==============================")
print("EVIDENCE VERIFICATION")
print("==============================\n")


result = verify_evidence(
    new_block,
    evidence
)


print(result)


# ============================================================
# TAMPER TEST
# ============================================================

print("\n==============================")
print("TAMPER TEST")
print("==============================\n")


print(
    "Changing similarity score..."
)


blockchain.chain[-1]["evidence"][
    "similarity_score"
] = 0.99


print(
    "CHAIN VALID AFTER TAMPERING:",
    blockchain.is_chain_valid()
)