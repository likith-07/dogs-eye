from blockchain.evidence_registry import EvidenceRegistry


evidence = {
    "target_image": "data/inputs/test.jpg",
    "results": [
        {
            "page_url": "https://instagram.com/example",
            "source": "searchapi",
            "verified": True
        }
    ]
}


registry = EvidenceRegistry()


print("\nRegistering ORIGINAL evidence...\n")

registration = registry.register(evidence)

print(registration)


print("\nVerifying ORIGINAL evidence...\n")

original_verification = registry.verify(evidence)

print(original_verification)


# ============================================================
# TAMPERING TEST
# ============================================================

tampered_evidence = {
    "target_image": "data/inputs/test.jpg",
    "results": [
        {
            "page_url": "https://instagram.com/TAMPERED_ACCOUNT",
            "source": "searchapi",
            "verified": True
        }
    ]
}


print("\nVerifying TAMPERED evidence...\n")

tampered_verification = registry.verify(tampered_evidence)

print(tampered_verification)