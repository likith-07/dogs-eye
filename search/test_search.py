import sys

sys.stdout.reconfigure(encoding="utf-8")

from search.engine import search_image


def main():
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = "search/sample_images/demo.jpg"

    result = search_image(image_path)

    print("\n=== SEARCH RESULT ===")
    print(f"Success: {result['success']}")
    print(f"Candidates: {len(result['candidates'])}")

    print("\n=== FIRST 10 RESULTS ===")

    for index, candidate in enumerate(result["candidates"][:10], start=1):
        print(f"\n{index}. [{candidate['provider']}]")
        print(f"   Source: {candidate['source'] or 'Unknown'}")
        print(f"   Title: {candidate['title'] or 'Unknown'}")
        print(f"   Author: {candidate['author'] or 'Unknown'}")
        print(f"   Rank: {candidate['search_rank']}")
        print(f"   Page: {candidate['page_url']}")


if __name__ == "__main__":
    main()
