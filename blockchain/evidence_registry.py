
from typing import Dict, Any

from blockchain.ethereum_client import EthereumClient
from blockchain.evidence_hasher import hash_evidence


class EvidenceRegistry:

    def __init__(self):
        self.client = EthereumClient()

    # ========================================================
    # REGISTER EVIDENCE
    # ========================================================

    def register(
        self,
        evidence: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Register the SHA-256 hash of the evidence on
        Ethereum Sepolia.
        """

        # ----------------------------------------------------
        # HASH EVIDENCE
        # ----------------------------------------------------

        evidence_hash = hash_evidence(evidence)

        # Convert SHA-256 hex string into bytes32
        evidence_hash_bytes = bytes.fromhex(
            evidence_hash
        )

        # ----------------------------------------------------
        # GET NONCE
        # ----------------------------------------------------

        nonce = self.client.web3.eth.get_transaction_count(
            self.client.account.address
        )

        # ----------------------------------------------------
        # GAS / EIP-1559
        # ----------------------------------------------------
        #
        # maxFeePerGas MUST be >= maxPriorityFeePerGas.
        #
        # Some Sepolia RPC providers can return a gas_price
        # below 1 gwei. Using that directly as maxFeePerGas
        # while setting the priority fee to 1 gwei causes:
        #
        # "max priority fee per gas higher than max fee per gas"
        #
        # ----------------------------------------------------

        gas_price = self.client.web3.eth.gas_price

        priority_fee = self.client.web3.to_wei(
            1,
            "gwei"
        )

        max_fee = max(
            gas_price,
            priority_fee
        )

        # ----------------------------------------------------
        # BUILD TRANSACTION
        # ----------------------------------------------------

        transaction = (
            self.client.contract.functions
            .registerEvidence(
                evidence_hash_bytes
            )
            .build_transaction(
                {
                    "from": self.client.account.address,
                    "nonce": nonce,
                    "chainId": 11155111,
                    "gas": 200000,

                    "maxFeePerGas": max_fee,

                    "maxPriorityFeePerGas": priority_fee,
                }
            )
        )

        # ----------------------------------------------------
        # SIGN TRANSACTION
        # ----------------------------------------------------

        signed_transaction = (
            self.client.account.sign_transaction(
                transaction
            )
        )

        # ----------------------------------------------------
        # SEND TRANSACTION
        # ----------------------------------------------------

        tx_hash = (
            self.client.web3.eth
            .send_raw_transaction(
                signed_transaction.raw_transaction
            )
        )

        # ----------------------------------------------------
        # WAIT FOR CONFIRMATION
        # ----------------------------------------------------

        receipt = (
            self.client.web3.eth
            .wait_for_transaction_receipt(
                tx_hash
            )
        )

        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return {
            "success": True,
            "evidence_hash": evidence_hash,
            "transaction_hash": tx_hash.hex(),
            "block_number": receipt["blockNumber"],
            "contract_address": self.client.contract.address,
            "network": "ethereum-sepolia",
        }

    # ========================================================
    # VERIFY EVIDENCE
    # ========================================================

    def verify(
        self,
        evidence: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Verify whether the exact evidence hash exists
        on Ethereum Sepolia.
        """

        # ----------------------------------------------------
        # HASH CURRENT EVIDENCE
        # ----------------------------------------------------

        evidence_hash = hash_evidence(
            evidence
        )

        # Convert SHA-256 hex string into bytes32
        evidence_hash_bytes = bytes.fromhex(
            evidence_hash
        )

        # ----------------------------------------------------
        # QUERY BLOCKCHAIN
        # ----------------------------------------------------

        result = (
            self.client.contract.functions
            .verifyEvidence(
                evidence_hash_bytes
            )
            .call()
        )

        exists = result[0]
        submitted_by = result[1]
        timestamp = result[2]

        # ----------------------------------------------------
        # RETURN VERIFICATION RESULT
        # ----------------------------------------------------

        return {
            "valid": exists,
            "evidence_hash": evidence_hash,
            "submitted_by": submitted_by,
            "blockchain_timestamp": timestamp,
            "network": "ethereum-sepolia",
        }

