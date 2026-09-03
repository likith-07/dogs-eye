import json
import os


DEFAULT_PATH = "data/blockchain.json"


def save_chain(chain: list, path: str = DEFAULT_PATH) -> None:
    """
    Save the blockchain to a JSON file.
    """

    directory = os.path.dirname(path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:

        json.dump(
            chain,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_chain(path: str = DEFAULT_PATH):
    """
    Load an existing blockchain.

    Returns None if no blockchain exists yet.
    """

    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as file:

        return json.load(file)