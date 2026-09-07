import json
import os

from dotenv import load_dotenv
from web3 import Web3


load_dotenv()


class EthereumClient:

    def __init__(self):

        self.rpc_url = os.getenv(
            "SEPOLIA_RPC_URL"
        )

        self.private_key = os.getenv(
            "ETHEREUM_PRIVATE_KEY"
        )

        self.contract_address = os.getenv(
            "ETHEREUM_CONTRACT_ADDRESS"
        )

        if not self.rpc_url:
            raise ValueError(
                "SEPOLIA_RPC_URL is missing"
            )

        if not self.private_key:
            raise ValueError(
                "ETHEREUM_PRIVATE_KEY is missing"
            )

        if not self.contract_address:
            raise ValueError(
                "ETHEREUM_CONTRACT_ADDRESS is missing"
            )

        self.web3 = Web3(
            Web3.HTTPProvider(
                self.rpc_url
            )
        )

        if not self.web3.is_connected():
            raise ConnectionError(
                "Could not connect to Sepolia"
            )

        self.account = (
            self.web3.eth.account
            .from_key(self.private_key)
        )

        abi_path = os.path.join(
            os.path.dirname(__file__),
            "abi",
            "EvidenceRegistry.json"
        )

        with open(
            abi_path,
            "r",
            encoding="utf-8"
        ) as file:
            contract_data = json.load(file)

        self.contract = (
            self.web3.eth.contract(
                address=Web3.to_checksum_address(
                    self.contract_address
                ),
                abi=contract_data["abi"]
            )
        )