# 🔍 GitHub Repository Search API

Асинхронный API на FastAPI для поиска популярных GitHub репозиториев с фильтрацией и аналитикой.
Может быть использован для поиска интересных идей и новой информации для Python проектов.

---

## 🚀 Возможности

- Поиск репозиториев через GitHub Search API
- Фильтрация по:
  - языку программирования
  - минимальному количеству stars
- Пагинация: до 100 результатов на странице, максимум до 1000 результатов всего
- Асинхронные запросы (httpx + asyncio.gather)
- Агрегация данных:
  - total stars
  - average stars
  - top repository
- Экспорт результатов:
  - JSON
  - CSV

---

## 📡 API

### GET /search
```
Пример запроса:

/search?query=fastapi&language=python&limit=200&min_stars=10

Пример ответа (json):

{
  "query": "fastapi",
  "repos_count": 200,
  "total_stars": 120000,
  "average_stars": 600,
  "top_repo": "tiangolo/fastapi",
  "repos": [...]
}
```
---

## ⚙️ Запуск проекта

### Запуск через Docker

1. Создать .env (опционально):

GITHUB_TOKEN=your_github_token_here

2. Сборка

docker-compose build

3. Запуск

docker-compose up

4. Открыть документацию API

http://localhost:8000/docs

### Локальный запуск
```
pip install -r requirements.txt

uvicorn app.main:app --reload
```

### GitHub Token (опционально)

- Используется для увеличения лимитов API.
- Не влияет на SSH и git-ключи.

---

## Структура проекта

    app/
     ├── main.py
     ├── github_client.py  # API запросы
     ├── services.py       # обработка данных
     ├── schemas.py        # pydantic схемы
     ├── storage.py        # сохранение данных в файлы
     ├── core
     ├──── config.py
     ├──── logging.py      # настройки логирования
    data                   # файлы с данными
     ├
    logs
     ├
    .env.example
     ├
    docker-compose.yaml
     ├
    Dockerfile
     ├
    Makefile
     ├
    README.md
     ├
    requirements.txt

---

## Дополнительно

- Документация API: используется `drf-spectacular`:
  - автоматическая генерация OpenAPI схемы,
  - Swagger UI для тестирования API.
- Конфигурация через переменные окружения.
- Реализовано структурированное логирование.
- Контейнеризация (используется Docker)
- Прекоммит-хуки (pre-commit) для поддержания качества кода.

---

## Возможные улучшения

- Redis кэширование.
- Добавление новых запросов (поиск репозиториев по имени пользователя и др.).
- Добавление метрик для анализа данных.
- Web UI (создание дашбордов со статистикой).

---

## Автор

Разработано в рамках тестового задания.

Надежда Попова

Python Developer

📧 nadezhdapopova13@yandex.ru

🔗 GitHub: simbarilion
