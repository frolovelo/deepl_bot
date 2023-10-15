### Инструкция по запуску

1. Установка зависимостей [Poetry](https://python-poetry.org "python package manager")
    ```
    poetry install
    ```
2. Конфигурация переменных окружения - создайте файл с именем `.env` в директории `deep`, с содержимым:
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
   
### Структура проекта:
```
my_project/
│
├── deep/
│   ├── .env
│   ├── main.py - телеграм бот
│   └── db_usage/
│       ├── __init__.py 
│       ├── db_run.py - создание движка, сессий для доступа к БД
│       ├── manage.py - создание БД и таблиц
│       ├── methods.py - методы работы с БД
│       └── models.py - модели таблиц БД
│
├── tests/
│   └── __init__.py
│
├── pyproject.toml
├── poetry.lock
└── README.md
```
