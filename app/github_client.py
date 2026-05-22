import math

import httpx

from app.core.config import GITHUB_SEARCH_API, PER_PAGE


async def search_repositories(
    query: str,
    language: str,
    limit: int,
    min_stars: int,
):
    pages = math.ceil(limit / PER_PAGE)
    all_repos = []

    async with httpx.AsyncClient() as client:
        for page in range(1, pages + 1):
            search_parts = [query]
            if language:
                search_parts.append(f"language:{language}")
            if min_stars > 0:
                search_parts.append(f"stars:>={min_stars}")
            search_query = " ".join(search_parts)
            params = {
                "q": search_query,
                "sort": "stars",
                "order": "desc",
                "per_page": PER_PAGE,
                "page": page,
            }
            try:
                headers = {"Accept": "application/vnd.github+json"}
                response = await client.get(
                    GITHUB_SEARCH_API,
                    params=params,
                    headers=headers,
                    timeout=15.0,
                )
            except httpx.RequestError:
                return None

            if response.status_code != 200:
                return None
            data = response.json()
            repos = data.get("items", [])
            all_repos.extend(repos)

    return data.get("items", [])
