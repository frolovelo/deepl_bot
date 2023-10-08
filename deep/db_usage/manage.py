from sqlalchemy import inspect
from deep.db_usage.db_run import Base, engine
from sqlalchemy_utils import database_exists, create_database
from deep.db_usage.models import User, Translate

if not database_exists(engine.url):
    print(f'БД создана под именем: {engine.url.database}')
    create_database(engine.url)
else:
    print('БД уже существует')


# Создайте экземпляр инспектора базы данных
inspector = inspect(engine)

# Получите список всех существующих таблиц в базе данных
existing_tables = inspector.get_table_names()

# Имя таблицы, которую вы хотите создать
user = User.__tablename__
translate = Translate.__tablename__
# Проверьте, существует ли таблица уже
if user in existing_tables and translate in existing_tables:
    print(f'Таблицы {user} и {translate} уже существуют')
else:
    # Если таблицы нет, создайте её
    Base.metadata.create_all(engine)
    print(f'Таблицы {user} и {translate} успешно созданы')

