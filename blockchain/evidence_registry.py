from typing import Dict, Any

from blockchain.ethereum_client import EthereumClient
from blockchain.evidence_hasher import hash_evidence


class EvidenceRegistry:
    def __init__(self):
        self.client = EthereumClient()

    def register(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register evidence hash on Ethereum Sepolia.
        """

        evidence_hash = hash_evidence(evidence)

        # Convert SHA-256 hex string into bytes32
        evidence_hash_bytes = bytes.fromhex(evidence_hash)

        nonce = self.client.web3.eth.get_transaction_count(
            self.client.account.address
        )

        transaction = (
            self.client.contract.functions
            .registerEvidence(evidence_hash_bytes)
            .build_transaction(
                {
                    "from": self.client.account.address,
                    "nonce": nonce,
                    "chainId": 11155111,
                    "gas": 200000,
                    "maxFeePerGas": self.client.web3.eth.gas_price,
                    "maxPriorityFeePerGas": self.client.web3.to_wei(
                        1,
                        "gwei"
                    ),
                }
            )
        )

        signed_transaction = self.client.account.sign_transaction(
            transaction
        )

        tx_hash = self.client.web3.eth.send_raw_transaction(
            signed_transaction.raw_transaction
        )

        receipt = self.client.web3.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return {
            "success": True,
            "evidence_hash": evidence_hash,
            "transaction_hash": tx_hash.hex(),
            "block_number": receipt["blockNumber"],
            "contract_address": self.client.contract.address,
            "network": "ethereum-sepolia",
        }

    def verify(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify whether this exact evidence hash exists on-chain.
        """

        evidence_hash = hash_evidence(evidence)

        evidence_hash_bytes = bytes.fromhex(evidence_hash)

        result = (
            self.client.contract.functions
            .verifyEvidence(evidence_hash_bytes)
            .call()
        )

        exists = result[0]
        submitted_by = result[1]
        timestamp = result[2]

        return {
            "valid": exists,
            "evidence_hash": evidence_hash,
            "submitted_by": submitted_by,
            "blockchain_timestamp": timestamp,
            "network": "ethereum-sepolia",
        }