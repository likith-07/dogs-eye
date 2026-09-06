from datetime import (
    datetime,
    timezone
)

from blockchain.hashing import (
    calculate_hash
)

from blockchain.storage import (
    load_chain,
    save_chain
)


class Blockchain:

    def __init__(
        self,
        storage_path: str = (
            "data/blockchain.json"
        )
    ):

        self.storage_path = (
            storage_path
        )

        loaded_chain = load_chain(
            self.storage_path
        )


        # --------------------------------
        # LOAD EXISTING CHAIN
        # --------------------------------

        if loaded_chain:

            self.chain = (
                loaded_chain
            )


        # --------------------------------
        # CREATE NEW CHAIN
        # --------------------------------

        else:

            self.chain = []

            self.create_genesis_block()

            self.save()


    # ====================================
    # GENESIS BLOCK
    # ====================================

    def create_genesis_block(
        self
    ) -> dict:

        block = {

            "index": 0,

            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "evidence": {
                "type":
                    "GENESIS_BLOCK"
            },

            "previous_hash": "0"
        }


        block["block_hash"] = (
            calculate_hash(
                block
            )
        )


        self.chain.append(
            block
        )


        return block


    # ====================================
    # ADD BLOCK
    # ====================================

    def add_block(
        self,
        evidence: dict
    ) -> dict:

        previous_block = (
            self.chain[-1]
        )


        block = {

            "index": len(
                self.chain
            ),

            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "evidence": evidence,

            "previous_hash":
                previous_block[
                    "block_hash"
                ]
        }


        block["block_hash"] = (
            calculate_hash(
                block
            )
        )


        self.chain.append(
            block
        )


        self.save()


        return block


    # ====================================
    # SAVE
    # ====================================

    def save(
        self
    ) -> None:

        save_chain(
            self.storage_path,
            self.chain
        )


    # ====================================
    # VALIDATE CHAIN
    # ====================================

    def is_chain_valid(
        self
    ) -> bool:

        for index, block in enumerate(
            self.chain
        ):

            # Create copy without stored hash

            block_data = {
                key: value
                for key, value in block.items()
                if key != "block_hash"
            }


            recalculated_hash = (
                calculate_hash(
                    block_data
                )
            )


            # Check block contents

            if (
                recalculated_hash
                != block["block_hash"]
            ):

                return False


            # Genesis block needs no
            # previous block validation

            if index == 0:

                continue


            previous_block = (
                self.chain[
                    index - 1
                ]
            )


            # Check chain link

            if (
                block["previous_hash"]
                != previous_block[
                    "block_hash"
                ]
            ):

                return False


        return True