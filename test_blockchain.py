from blockchain.chain import Blockchain


def main():

    blockchain = Blockchain()


    evidence = {

        "input_image_hash":
            "abc123examplehash",

        "verified_matches": [
            {

                "candidate_id": 1,

                "title":
                    "Test Person",

                "source":
                    "example.com",

                "matched_page_url":
                    "https://example.com/person",

                "matched_image_url":
                    "https://example.com/image.jpg",

                "similarity_score":
                    0.87
            }
        ],

        "verified_matches_count":
            1,

        "timestamp":
            "2026-09-03T12:00:00+00:00"
    }


    new_block = blockchain.add_block(
        evidence
    )


    print(
        "\nNew Block Created:"
    )

    print(
        new_block
    )


    print(
        "\nBlockchain Valid:"
    )

    print(
        blockchain.is_chain_valid()
    )


if __name__ == "__main__":

    main()