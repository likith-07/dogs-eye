import hashlib
import json


def calculate_hash(
    data
) -> str:
    """
    Creates a deterministic SHA-256 hash
    from Python data.
    """

    serialized_data = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":")
    )

    return hashlib.sha256(
        serialized_data.encode(
            "utf-8"
        )
    ).hexdigest()


def hash_file(
    file_path: str
) -> str:
    """
    Creates a SHA-256 hash of a file.
    """

    sha256 = hashlib.sha256()

    with open(
        file_path,
        "rb"
    ) as file:

        while True:

            chunk = file.read(
                8192
            )

            if not chunk:
                break

            sha256.update(
                chunk
            )

    return sha256.hexdigest()