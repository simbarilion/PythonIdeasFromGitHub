import csv
import json

from app.core.config import DATA_DIR, make_filename


def save_to_json(data: dict, query: str) -> None:
    """
    Сохраняет результат поиска репозиториев в JSON файл.
    Args:
        data (dict): результат обработки репозиториев
        query (str): поисковый запрос (используется в имени файла)
    Returns:
        None
    """
    filename = make_filename(query, "json")
    path = DATA_DIR / filename

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )


def save_to_csv(data: dict, query: str) -> None:
    """
    Сохраняет список репозиториев в CSV файл.
    Формат:
    - name
    - owner
    - stars
    - forks
    - url
    Args:
        data (dict): результат обработки репозиториев
        query (str): поисковый запрос (для имени файла)
    Returns:
        None
    """
    filename = make_filename(query, "csv")
    path = DATA_DIR / filename

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Repository",
                "Owner",
                "Stars",
                "Forks",
                "URL",
            ]
        )
        for repo in data["repos"]:
            writer.writerow(
                [
                    repo["name"],
                    repo["owner"],
                    repo["stars"],
                    repo["forks"],
                    repo["url"],
                ]
            )
