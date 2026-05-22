from pathlib import Path

GITHUB_SEARCH_API = "https://api.github.com/search/repositories"

DEFAULT_LIMIT = 100
MAX_LIMIT = 1000
PER_PAGE = 100
DEFAULT_MIN_STARS = 0

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)
