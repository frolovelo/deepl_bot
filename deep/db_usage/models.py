"""Модели таблиц бд"""
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from .db_run import Base


class User(Base):
    """БД Пользователей"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(60), nullable=False, unique=True)

    # Отношение к таблице Translate
    translations = relationship('Translate', back_populates='author')


class Translate(Base):
    """БД Переводов"""
    __tablename__ = 'translate'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    language = Column(String(2), nullable=False)
    text_original = Column(String, nullable=False)
    text_translate = Column(String, nullable=False)

    # Отношение к таблице User
    author = relationship('User', back_populates='translations')
