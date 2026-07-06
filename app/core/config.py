import os
from datetime import datetime
from pathlib import Path

GITHUB_SEARCH_API = "https://api.github.com/search/repositories"

TOKEN_FOR_GITHUB_API = os.getenv("TOKEN_FOR_GITHUB_API")

DEFAULT_LIMIT = 100
MAX_LIMIT = 1000
PER_PAGE = 100
DEFAULT_MIN_STARS = 0

LOGS_LEVEL = 2

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)


def make_filename(query: str, ext: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_query = query.replace(" ", "_")
    return f"{safe_query}_{timestamp}.{ext}"
