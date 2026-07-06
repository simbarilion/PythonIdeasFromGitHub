/**
 * Загружает репозитории GitHub и записывает их в Google Sheet.
 * Использует GitHub API для получения данных о репозиториях, фильтруя по языку и сортируя по количеству звезд.
 * Функция выполняет:
 *  - запрос к GitHub API (Search Repositories)
 *  - обработку JSON-ответа
 *  - фильтрацию и извлечение данных
 *  - запись результата в Google Sheets
 *  - обработку ошибок API и сети
 *
 * @returns {void}
 */
function fetchGitHubRepos() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

  // НАСТРОЙКИ ЗАПРОСА
  const query = "fastapi";
  const language = "python";
  const perPage = 100;

  /**
   * Формирует query параметры отдельно, позволяет легко менять фильтры
   */
  const searchQuery = `${query} language:${language}`;

  const baseUrl = https://farm-contrast-after-comics.trycloudflare.com/docs

  const params = {
    query: query,
    language: language,
    limit: perPage,
    min_stars: 100
  };

  const queryString = Object.keys(params)
    .map(key => `${key}=${encodeURIComponent(params[key])}`)
    .join("&");

  const url = `${baseUrl}?${queryString}`;

  const options = {
    method: "get",
    muteHttpExceptions: true,
    headers: {
      "Accept": "application/vnd.github+json",
      "User-Agent": "GoogleAppsScript"
    }
  };

  // Отправляет запрос к GitHub API и обрабатывает ответ
  try {
    const response = UrlFetchApp.fetch(url, options);
    const statusCode = response.getResponseCode();

    // Проверка статуса ответа от GitHub API, информирование пользователя о возможных ошибках
    if (statusCode !== 200) {
      sheet.getRange("A1").setValue(`GitHub API error: ${statusCode}`);
      return;
    }

    const data = JSON.parse(response.getContentText());
    const repos = data.repos || [];

    // Очистка таблицы перед записью новых данных
    sheet.clear();

    // Запись заголовков столбцов
    sheet.appendRow(["Name", "Stars", "Forks", "URL"]);

    /**
     * Запись данных в таблицу (берется только нужная информация): каждая строка = один репозиторий:
     * - Название репозитория (для идентификации проекта)
     * - Автор репозитория
     * - Количество звезд (популярность проекта в мире)
     * - URL репозитория (для быстрого доступа к проекту на GitHub)
     */
    repos.forEach(repo => {
      sheet.appendRow([
        repo.name,
        repo.owner,
        repo.stars,
        repo.url
      ]);
    });

    // Статус загрузки и количество загруженных репозиториев для информирования пользователя
    sheet.getRange("F1").setValue("Status: OK");
    sheet.getRange("F2").setValue(`Loaded repos: ${repos.length}`);

    // Дополнительная информация о запросе для отладки: запись ошибок в отдельные ячейки
  } catch (error) {
    sheet.getRange("F1").setValue("ERROR");
    sheet.getRange("F2").setValue(error.toString());
  }
}


/**
 * Добавляет меню в Google Sheets для запуска функции загрузки репозиториев из GitHub.
 * Позволяет пользователю легко инициировать процесс загрузки данных, не открывая редактор скриптов.
 *
 * @returns {void}
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("GitHub Loader")
    .addItem("Load repos", "fetchGitHubRepos")
    .addToUi();
}
