from .hashing import calculate_hash


def verify_chain_detailed(chain):
    """
    Verify the entire blockchain and return detailed information
    about where integrity failed.
    """

    if not chain:
        return {
            "valid": False,
            "error": "Blockchain is empty"
        }

    # Check every block
    for i, block in enumerate(chain):

        # Recalculate this block's hash
        block_data = {
            "index": block["index"],
            "timestamp": block["timestamp"],
            "evidence": block["evidence"],
            "previous_hash": block["previous_hash"]
        }

        recalculated_hash = calculate_hash(block_data)

        # TEST 1:
        # Has the block's actual content been modified?
        if recalculated_hash != block["block_hash"]:
            return {
                "valid": False,
                "tampered_block": i,
                "reason": "Block contents do not match stored block hash",
                "stored_hash": block["block_hash"],
                "calculated_hash": recalculated_hash
            }

        # TEST 2:
        # Is this block correctly linked to the previous block?
        if i > 0:
            previous_block = chain[i - 1]

            if block["previous_hash"] != previous_block["block_hash"]:
                return {
                    "valid": False,
                    "tampered_block": i,
                    "reason": "Previous hash link is broken",
                    "expected_previous_hash": previous_block["block_hash"],
                    "actual_previous_hash": block["previous_hash"]
                }

    return {
        "valid": True,
        "message": "All blocks passed integrity checks"
    }