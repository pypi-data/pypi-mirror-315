# yt_viewfinder
 Python package designed to effortlessly fetch YouTube video view counts based on video titles and artists

## Features
- Fetches view counts for YouTube videos based on titles and optional artists.

## Installation
Install the package directly from PyPI:

```bash
pip install yt-viewfinder
```

## To Use

```
from yt_viewfinder import get_youtube_view_count

# Example: Get view count for "Thriller" by Michael Jackson
view_count = get_youtube_view_count("Thriller", "Michael Jackson")
print(f"View Count: {view_count}")
```
Output: 
if no matching video it returns 0