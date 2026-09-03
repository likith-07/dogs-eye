import hashlib
import json


def calculate_hash(data: dict) -> str:
    """
    Convert a dictionary into canonical JSON and
    return its SHA-256 hash.
    """

    canonical_data = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    )

    return hashlib.sha256(
        canonical_data.encode("utf-8")
    ).hexdigest()


def hash_file(file_path: str) -> str:
    """
    Generate a SHA-256 hash for a file.
    Useful for hashing the original input image.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(8192)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()