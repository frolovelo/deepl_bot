"""Инициализация бд"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

try:
    engine = create_engine(os.getenv('DB_URL'))

    Session = sessionmaker(bind=engine)

    Base = declarative_base()
except Exception as ex:
    print('ПРОИЗОШЛА ОШИБКА ПРИ СОЗДАНИИ ДВИЖКА БД - ПРОВЕРЬ <.env> ФАЙЛ:', ex)


