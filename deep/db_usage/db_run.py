"""Инициализация бд"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

print('db run!')

engine = create_engine(os.getenv('DB_URL'))

Session = sessionmaker(bind=engine)

Base = declarative_base()