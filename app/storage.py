import csv
import json

from app.core.config import DATA_DIR


def save_to_json(data: dict, query: str):
    path = DATA_DIR / f"{query}.json"

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )


def save_to_csv(data: dict, query: str):
    path = DATA_DIR / f"{query}.csv"

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Repository",
                "Owner",
                "Stars",
                "URL",
            ]
        )
        for repo in data["repos"]:
            writer.writerow(
                [
                    repo["name"],
                    repo["owner"],
                    repo["stars"],
                    repo["url"],
                ]
            )
