import sys

from search.engine import search_image


def main():
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = "search/sample_images/demo.jpg"

    result = search_image(image_path)

    print("\n=== SEARCH RESULT ===")
    print(f"Success: {result['success']}")
    print(f"Candidates found: {len(result['candidates'])}")

    print("\n=== TOP RESULTS ===")

    for candidate in result["candidates"][:10]:
        print("\n---")
        print(f"Provider: {candidate['provider']}")
        print(f"Rank: {candidate['search_rank']}")
        print(f"Title: {candidate['title']}")
        print(f"Source: {candidate['source']}")
        print(f"Page URL: {candidate['page_url']}")


if __name__ == "__main__":
    main()
