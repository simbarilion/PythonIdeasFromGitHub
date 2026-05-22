from fastapi import FastAPI, HTTPException, Query

from app.core.config import (
    DEFAULT_LIMIT,
    DEFAULT_MIN_STARS,
)
from app.github_client import search_repositories
from app.services import process_repositories
from app.storage import save_to_csv, save_to_json

app = FastAPI(title="GitHub Projects API")


@app.get("/search")
async def search_projects(
    query: str,
    language: str | None = None,
    limit: int = Query(DEFAULT_LIMIT, le=1000),
    min_stars: int = DEFAULT_MIN_STARS,
):
    repos = await search_repositories(
        query=query,
        language=language,
        limit=limit,
        min_stars=min_stars,
    )
    if repos is None:
        raise HTTPException(
            status_code=503,
            detail="GitHub API unavailable",
        )

    result = process_repositories(
        query=query,
        repos=repos,
    )
    save_to_json(result, query)
    save_to_csv(result, query)

    return result
