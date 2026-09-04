from blockchain.hashing import (
    hash_file
)


def verify_input_image(
    image_path: str,
    block: dict
) -> bool:

    current_image_hash = hash_file(
        image_path
    )


    stored_image_hash = (
        block["evidence"].get(
            "input_image_hash"
        )
    )


    return (
        current_image_hash
        == stored_image_hash
    )