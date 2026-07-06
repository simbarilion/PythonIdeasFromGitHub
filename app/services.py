from typing import Any


def process_repositories(
    query: str,
    repos: list[dict[str, Any]],
) -> dict:
    """
    Обрабатывает список GitHub репозиториев и вычисляет агрегированные метрики.
    Функциональность:
    - фильтрация и нормализация данных
    - расчет статистик (sum, avg, median)
    - определение топ-репозитория
    Args:
        query (str): поисковый запрос
        repos (list[dict]): список репозиториев GitHub
    Returns:
        dict: структурированный результат анализа
    """
    processed = [
        {
            "name": repo["name"],
            "owner": repo["owner"]["login"],
            "stars": repo["stargazers_count"],
            "url": repo["html_url"],
        }
        for repo in repos
    ]
    total_stars = sum(repo["stargazers_count"] for repo in repos)
    average_stars = total_stars / len(processed) if processed else 0
    top_repo = max(processed, key=lambda x: x["stars"])["name"] if processed else None
    return {
        "query": query,
        "repos_count": len(processed),
        "total_stars": total_stars,
        "average_stars": round(average_stars, 2),
        "top_repo": top_repo,
        "repos": processed,
    }
