import asyncio
import math
import os

import httpx

from app.core.config import GITHUB_SEARCH_API, PER_PAGE

TOKEN_FOR_GITHUB_API = os.getenv("TOKEN_FOR_GITHUB_API")


async def fetch_page(
    client: httpx.AsyncClient,
    query: str,
    language: str,
    min_stars: int,
    page: int,
) -> list[dict]:
    """
    Выполняет запрос одной страницы GitHub Search API.
    Args:
        client (httpx.AsyncClient): асинхронный HTTP клиент
        query (str): поисковый запрос пользователя
        language (str): язык программирования для фильтрации
        min_stars (int): минимальное количество stars
        page (int): номер страницы результата
    Returns:
        list[dict]: список репозиториев GitHub (items из API ответа)
    Raises:
        httpx.HTTPStatusError: при ошибке HTTP ответа
    """
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
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "FastAPI-GitHub-Searcher",
    }
    if TOKEN_FOR_GITHUB_API:
        headers["Authorization"] = f"Bearer {TOKEN_FOR_GITHUB_API}"

    response = await client.get(
        GITHUB_SEARCH_API,
        params=params,
        headers=headers,
        timeout=15.0,
    )

    response.raise_for_status()
    data = response.json()

    return data.get("items", [])


async def search_repositories(
    query: str,
    language: str,
    limit: int,
    min_stars: int,
) -> list[dict] | None:
    """
    Асинхронно выполняет поиск GitHub репозиториев с поддержкой пагинации.
    Функциональность:
    - поиск по ключевому слову
    - фильтрация по языку программирования
    - фильтрация по минимальному количеству stars
    - автоматическая пагинация (до limit)
    - параллельные запросы через asyncio.gather
    Args:
        query (str): поисковый запрос
        language (str): язык программирования
        limit (int): максимальное количество репозиториев (до 1000)
        min_stars (int): минимальное количество stars
    Returns:
        list[dict] | None: список найденных репозиториев или None при ошибке
    """
    pages = math.ceil(limit / PER_PAGE)
    async with httpx.AsyncClient() as client:
        tasks = [
            fetch_page(
                client=client,
                query=query,
                language=language,
                min_stars=min_stars,
                page=page,
            )
            for page in range(1, pages + 1)
        ]

        try:
            results = await asyncio.gather(*tasks)
        except httpx.RequestError:
            return None

        all_repos = []
        for repos in results:
            if repos:
                all_repos.extend(repos)

        return all_repos[:limit]
