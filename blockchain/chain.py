from datetime import datetime, timezone

from blockchain.hashing import calculate_hash
from blockchain.storage import (
    load_chain,
    save_chain
)


class Blockchain:

    def __init__(
        self,
        storage_path: str = "data/blockchain.json"
    ):

        self.storage_path = storage_path

        loaded_chain = load_chain(
            self.storage_path
        )

        if loaded_chain:

            self.chain = loaded_chain

        else:

            self.chain = []

            self.create_genesis_block()

            self.save()


    # =========================================================
    # GENESIS BLOCK
    # =========================================================

    def create_genesis_block(self):

        block = {
            "index": 0,

            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "evidence": {
                "type": "GENESIS_BLOCK"
            },

            "previous_hash": "0"
        }

        block["block_hash"] = calculate_hash(
            block
        )

        self.chain.append(block)


    # =========================================================
    # ADD BLOCK
    # =========================================================

    def add_block(
        self,
        evidence: dict
    ) -> dict:

        previous_block = self.chain[-1]

        block = {
            "index": len(self.chain),

            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "evidence": evidence,

            "previous_hash":
                previous_block["block_hash"]
        }

        block["block_hash"] = calculate_hash(
            block
        )

        self.chain.append(block)

        self.save()

        return block


    # =========================================================
    # SAVE
    # =========================================================

    def save(self):

        save_chain(
            self.chain,
            self.storage_path
        )


    # =========================================================
    # GET BLOCK
    # =========================================================

    def get_block(
        self,
        index: int
    ):

        if (
            index < 0
            or
            index >= len(self.chain)
        ):
            return None

        return self.chain[index]


    # =========================================================
    # GET LATEST BLOCK
    # =========================================================

    def get_latest_block(self):

        return self.chain[-1]


    # =========================================================
    # VALIDATE CHAIN
    # =========================================================

    def is_chain_valid(self) -> bool:

        for i in range(
            len(self.chain)
        ):

            current_block = self.chain[i]

            stored_hash = current_block.get(
                "block_hash"
            )

            block_copy = current_block.copy()

            block_copy.pop(
                "block_hash",
                None
            )

            recalculated_hash = calculate_hash(
                block_copy
            )

            # Check if block itself was modified

            if (
                stored_hash
                !=
                recalculated_hash
            ):
                return False


            # Genesis block does not have
            # a real previous block

            if i == 0:
                continue


            previous_block = self.chain[
                i - 1
            ]


            # Check previous hash link

            if (
                current_block[
                    "previous_hash"
                ]
                !=
                previous_block[
                    "block_hash"
                ]
            ):
                return False


        return True