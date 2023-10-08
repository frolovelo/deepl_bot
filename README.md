### Инструкция по запуску

1. Установка зависимостей [Poetry](https://python-poetry.org "python package manager")
    ```
    poetry install
    ```
2. Конфигурация переменных окружения - создайте файл с именем `.env`, с содержимым:
    ```
    # токен бота телеграм
    TOKEN_TELEGRAM=your_token
    
    # ключ deepl api
    AUTH_KEY_DEEPL=your_key
    
    # url адрес будущей бд
    DB_URL=postgresql://user:password@localhost/db_name
    ```
3. Запустите `manage.py` для создания БД и таблиц 
(если БД уже создана скрипт добавит только таблицы)
   ```
   poetry run python -m deep.db_usage.manage
   ```

4. Запуск бота в виртуальном окружении (в директории проекта)
    ```
    poetry run python -m deep.main
    ```