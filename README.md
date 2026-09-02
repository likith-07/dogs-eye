# Dogs Eye — Dynamic Search Module

## Overview

This module performs dynamic reverse-image searches across external web search providers and returns social-media candidates for downstream face verification.

The module currently uses:

- SearchAPI with Google Lens
- FaceFinderAI
- Uguu for temporary public image hosting required by SearchAPI

Results from both providers are merged, deduplicated, and filtered to supported social-media platforms.

## Project Structure

search/
├── engine.py
├── normalizer.py
├── image_host.py
├── test_search.py
├── sample_images/
│   └── demo.jpg
└── providers/

## Main Function

The main entry point is:

```python
from search.engine import search_image

result = search_image("input.jpg")
```

It returns candidates in the standard format:

```python
{
    "success": True,
    "candidates": [
        {
            "page_url": "...",
            "image_url": "...",
            "title": "...",
            "source": "...",
            "provider": "...",
            "search_rank": 1
        }
    ]
}
```

An empty candidate list is valid. If all providers fail, success is False and candidates is an empty list.

## Providers

### SearchAPI — Google Lens

SearchAPI is used through its Google Lens engine. It requires a publicly accessible image URL, so the local image is temporarily uploaded to Uguu before being searched.

### FaceFinderAI

FaceFinderAI accepts the local image directly. The provider uploads the image, polls for the search result, and converts the returned results into the standard candidate format.

## Candidate Normalization

Results from all providers are passed through normalizer.py.

The normalizer:

- Removes results without a page URL.
- Keeps only supported social-media platforms.
- Removes duplicate URLs.
- Ensures optional fields have consistent values.

Supported platforms currently include X / Twitter, Instagram, Facebook, TikTok, Threads, and YouTube.

## API Keys

API keys are loaded from environment variables using .env.

Required variables:

```text
SEARCHAPI_KEY
FACEFINDER_API_KEY
```

The .env file must not be committed to Git.

## Installation

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Testing

Run the test script with:

```bash
python -m search.test_search
```

The pipeline has been tested with:

- **Cristiano Ronaldo** — exact target X post retrieved through SearchAPI.
- **Virat Kohli** — exact target Instagram post retrieved through FaceFinderAI.
- **A non-famous person** — the known Instagram post was not retrieved by either provider.

The non-famous-person result demonstrates a limitation of external reverse-image search: providers depend on their existing web and social-media indexing. Failure to retrieve a known post does not mean that the post does not exist online.

## Known Limitations

Reverse-image search providers do not guarantee that an exact social-media post will be returned.

Public figures and widely indexed images are more likely to produce exact matches. Less-indexed individuals may produce relevant but incorrect results or no results.

The module does not force a match when external search fails. Downstream face verification is responsible for determining whether a returned candidate is actually the same person.

This helps avoid false positives and allows the final system to return **NO VERIFIED MATCH** when no candidate can be verified.

Provider results can vary between runs due to external indexing changes; the module always searches live rather than caching or hardcoding results.
