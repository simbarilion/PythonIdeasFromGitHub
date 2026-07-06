# 🔍 GitHub Repository Search System

Система для поиска популярных GitHub-репозиториев с аналитикой и интеграцией Google Sheets.
Проект включает полноценный аналитический Dashboard внутри Google Sheets.

---

## 🚀 Возможности

**FastAPI backend**
* Поиск GitHub репозиториев через GitHub Search API
* Фильтрация по языку программирования
* Фильтрация по минимальному количеству stars 
* Пагинация: до 100 результатов на странице, максимум до 1000 результатов всего
* Асинхронные запросы (httpx + asyncio.gather)
* Агрегация данных:
  - `total stars` - общее количество звезд (насколько популярная область запроса)
  - `average stars` - среднее количество звезд
  - `top repository` - самый популярный репозиторий
* Вывод данных по каждому репозиторию:
  - `name` - название репозитория (для идентификации проекта)
  - `owner` - автор репозитория
  - `stars` - количество звезд (популярность проекта в мире)
  - `forks` - количество форков (сколько раз проект был скопирован другими разработчиками)
  - `url` - URL репозитория (для быстрого доступа к проекту на GitHub)
* Экспорт результатов в JSON / CSV

**Google Sheets интеграция**
* Кнопка меню: GitHub Loader → Load repos
* Автоматическая загрузка данных в таблицу
* Обновление данных по запросу
* Обработка ошибок API

**Cloudflare Tunnel**
* Используется для публичного HTTPS доступа к локальному FastAPI через туннель
* Не требует деплоя сервера

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

### Запуск через Docker (используется для локального backend)

1. Создать .env (опционально):

GITHUB_TOKEN=your_github_token_here

2. Сборка

docker-compose build

3. Запуск

docker-compose up

4. Открыть документацию API

http://localhost:8000/docs


### GitHub Token (опционально)

- Используется для увеличения лимитов API.
- Не влияет на SSH и git-ключи.


### Запуск проекта через Cloudflare Tunnel
```
pip install -r requirements.txt

uvicorn app.main:app --reload

cloudflared tunnel --url http://localhost:8000

```

---

## Google Sheets интеграция (Apps Script)

### Описание

* Проект интегрирован с Google Sheets через Google Apps Script. 
* При открытии таблицы автоматически создаётся меню:
  - GitHub Loader → Load repos;
  - Apps Script выполняет HTTP запрос к FastAPI backend;
  - Получает JSON с репозиториями;
  - Записывает данные в Google Sheets;
  - Обновляет таблицу по запросу пользователя.
* После запуска системы автоматически создаются 2 листа:
  - DATA — сырые данные репозиториев; используется как источник данных для всех расчетов;
  - DASHBOARD — аналитика и визуализация, включает:
    - Основные метрики,
    - 2 независимых графика: Top 10 Stars, Top 10 Forks.
* Dashboard формируется автоматически после загрузки данных:
  - данные читаются из листа DATA;
  - выполняется сортировка:
    - Top Stars → сортировка по stars,
    - Top Forks → сортировка по forks;
  - создаются временные агрегированные таблицы;
  - строятся диаграммы

### Запуск Google Sheets

1. Открыть таблицу:

https://docs.google.com/spreadsheets/d/1_VuLP7iiecNzHJGHIw6kwYqvJLfPjoeBKRvIFr7fE8c/edit?usp=sharing

2. Перейти:

```angular2html
Extensions → Apps Script
```

3. Для запуска скрипта использовать меню:

```angular2html
GitHub Loader → Load repos
```

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
    google_sheets/         
     ├── Code.gs           # Google App Script
    data                   # файлы с данными (JSON, CSV)
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

- Документация API: используется `FastAPI automatic OpenAPI`:
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
- Интеграция PostgreSQL (хранение данных в БД).

---

## Автор

Разработано в рамках тестового задания.

Надежда Попова

Python Developer

📧 nadezhdapopova13@yandex.ru

🔗 GitHub: simbarilion
