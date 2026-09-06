import json
import os
from typing import List, Optional


def load_chain(
    storage_path: str
) -> Optional[List[dict]]:

    if not os.path.exists(
        storage_path
    ):
        return None

    try:

        with open(
            storage_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except (
        json.JSONDecodeError,
        OSError
    ):

        return None


def save_chain(
    storage_path: str,
    chain: List[dict]
) -> None:

    directory = os.path.dirname(
        storage_path
    )

    if directory:

        os.makedirs(
            directory,
            exist_ok=True
        )

    with open(
        storage_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chain,
            file,
            indent=4
        )