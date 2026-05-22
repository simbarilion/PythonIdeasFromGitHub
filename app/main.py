from fastapi import FastAPI, HTTPException, Query
from starlette import status

from app.core.config import (
    DEFAULT_LIMIT,
    DEFAULT_MIN_STARS,
    LOGS_LEVEL,
)
from app.core.logging import setup_logger
from app.github_client import search_repositories
from app.schemas import SearchResponseSchema
from app.services import process_repositories
from app.storage import save_to_csv, save_to_json

logger = setup_logger(__name__, level=LOGS_LEVEL)

app = FastAPI(
    title="GitHub Projects API",
    description="""
    Асинхронный API для поиска популярных GitHub-репозиториев.
    
    Возможности:
    - поиск по ключевым словам
    - фильтрация по языку
    - фильтрация по минимальному количеству stars
    - пагинация GitHub API
    - экспорт результатов в JSON и CSV
    - расчет агрегированных метрик
    
    Powered by FastAPI + httpx.
    """,
    version="1.0.0",
)


@app.get(
    "/health",
    summary="Простая проверка работоспособности API",
    description="Возвращает статус API",
    status_code=status.HTTP_200_OK,
)
async def health_check():
    """Проверка, что API запущено"""
    try:
        logger.info("Health check called")
        return {"status": "ok"}

    except Exception as e:
        logger.exception('Health check failed": %s', e)
        raise HTTPException(status_code=500, detail="Service unhealthy") from e


@app.get(
    "/search",
    response_model=SearchResponseSchema,
    summary="Search GitHub repositories",
    description="""
    Поиск популярных репозиториев GitHub.
    
    Результаты:
    - сортируются по stars
    - фильтруются по языку
    - поддерживают limit до 1000
    - автоматически сохраняются в JSON и CSV
    """,
)
async def search_projects(
    query: str = Query(
        ...,
        description="Ключевое слово для поиска репозиториев",
        examples="fastapi",
    ),
    language: str | None = Query(
        None,
        description="Язык программирования",
        examples="python",
    ),
    limit: int = Query(
        DEFAULT_LIMIT,
        le=1000,
        description="Количество репозиториев",
        examples=200,
    ),
    min_stars: int = Query(
        DEFAULT_MIN_STARS,
        description="Минимальное количество stars",
        examples=500,
    ),
) -> dict[str, SearchResponseSchema]:
    """
    API endpoint для поиска GitHub репозиториев.
    Query params:
        query (str): ключевое слово поиска
        language (str): язык программирования (по умолчанию python)
        limit (int): максимальное количество результатов (до 1000)
        min_stars (int): минимальное количество stars
    Returns:
        SearchResponseSchema: агрегированные данные + список репозиториев
    Side effects:
        - сохраняет результаты в JSON
        - сохраняет результаты в CSV
    """
    logger.info("Search started")
    try:
        repos = await search_repositories(
            query=query,
            language=language,
            limit=limit,
            min_stars=min_stars,
        )
        if repos is None:
            logger.error("GitHub API unavailable")
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

        logger.info("Search completed")
        return result

    except Exception as e:
        logger.exception("Unexpected error in /search: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error") from e
