import json

from search.engine import search_image


def main():

    image_path = "data/inputs/nihal2.jpg"

    result = search_image(
        image_path=image_path,
        max_candidates=100,
        verbose=True
    )

    print("\n" + "=" * 60)
    print("SEARCH TEST RESULT")
    print("=" * 60)

    print(
        json.dumps(
            result,
            indent=2
        )
    )

    print("\n" + "=" * 60)
    print("CANDIDATE SUMMARY")
    print("=" * 60)

    candidates = result.get(
        "candidates",
        []
    )

    print(f"Total candidates: {len(candidates)}")

    for index, candidate in enumerate(
        candidates[:20],
        start=1
    ):

        print(f"\nCandidate {index}")

        print(
            f"Title: "
            f"{candidate.get('title')}"
        )

        print(
            f"Source: "
            f"{candidate.get('source')}"
        )

        print(
            f"Page URL: "
            f"{candidate.get('page_url')}"
        )

        print(
            f"Image URL: "
            f"{candidate.get('image_url')}"
        )

        print(
            f"Social Media: "
            f"{candidate.get('is_social_media')}"
        )


if __name__ == "__main__":
    main()