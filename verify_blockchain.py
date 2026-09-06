from blockchain.chain import Blockchain
from blockchain.integrity import verify_chain_detailed


def main():
    print("\n" + "=" * 65)
    print("DOGSEYE BLOCKCHAIN TAMPER DETECTION")
    print("=" * 65)

    blockchain = Blockchain()

    result = verify_chain_detailed(blockchain.chain)

    print(f"\nTotal blocks: {len(blockchain.chain)}")

    print("\n--- CHECKING BLOCKCHAIN INTEGRITY ---\n")

    if result["valid"]:

        print("STATUS: VALID")
        print(result["message"])

        print("\nChecks performed:")
        print("[PASS] Block contents match stored hashes")
        print("[PASS] Previous-hash links are intact")
        print("[PASS] Blockchain integrity verified")

    else:

        print("STATUS: INVALID / POSSIBLE TAMPERING DETECTED")

        print(f"\nAffected block: {result.get('tampered_block')}")
        print(f"Reason: {result.get('reason')}")

        if "stored_hash" in result:
            print("\nStored Hash:")
            print(result["stored_hash"])

            print("\nRecalculated Hash:")
            print(result["calculated_hash"])

        if "expected_previous_hash" in result:
            print("\nExpected Previous Hash:")
            print(result["expected_previous_hash"])

            print("\nActual Previous Hash:")
            print(result["actual_previous_hash"])


if __name__ == "__main__":
    main()