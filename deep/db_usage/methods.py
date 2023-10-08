"""Методы для работы с бд"""
from sqlalchemy import desc, func
from .models import User, Translate
from .db_run import Session

__all__ = ['add_new_user', 'set_translation', 'get_user_translations', 'get_translate']


def add_new_user(user_id, nickname):
    """
    Добавляет пользователя в таблицу User.

    :param user_id: telegram id пользователя;
    :param nickname: telegram никнейм пользователя.
    """
    session = Session()

    try:
        # Существует ли пользователь с заданным id
        existing_user = session.query(User).filter_by(id=user_id).first()

        if existing_user is None:
            # Если такого пользователя нет - добавляем в бд
            new_user = User(id=user_id, nickname=nickname)
            session.add(new_user)
            session.commit()
            print(f"Пользователь с id {user_id} добавлен успешно!")
        else:
            print(f"Пользователь с id {user_id} уже существует в базе данных.")
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {str(e)}")
        session.rollback()
    finally:
        session.close()


def set_translation(author_id, language, text_original, text_translate):
    """
    Добавляет перевод в таблицу Translate.

    :param author_id: telegram id пользователя;
    :param language: целевой язык перевода;
    :param text_original: оригинальный текст;
    :param text_translate: переведенный текст.
    """
    new_translation = Translate(author_id=author_id,
                                language=language,
                                text_original=text_original,
                                text_translate=text_translate)
    session = Session()

    try:
        # Добавляет новую запись перевода в сессию
        session.add(new_translation)
        session.commit()
        print("Запись перевода добавлена успешно!")
    except Exception as e:
        print(f"Ошибка при добавлении записи перевода: {str(e)}")
        session.rollback()
    finally:
        session.close()


def get_user_translations(user_id, page_number=1, page_size=6):
    """
    Пагинация для выдачи записей переводов пользователя из Translate.

    :param user_id: telegram id пользователя;
    :param page_number: номер текущей страницы;
    :param page_size: кол-во записей переводов для 1 страницы.

    :return: translations - список объектов Translate;<br>
    total_pages - всего страниц переводов пользователя.
    """
    session = Session()

    try:
        # Общее количество записей для указанного пользователя
        total_count = session.query(func.count(Translate.id)).filter_by(author_id=user_id).scalar()

        # Общее количество страниц
        total_pages = (total_count + page_size - 1) // page_size

        # Смещение (offset) для данной страницы
        offset = (page_number - 1) * page_size

        # Переводы для указанного пользователя с учетом пагинации
        translations = session.query(Translate).filter_by(author_id=user_id).order_by(desc(Translate.id)).limit(
            page_size).offset(offset).all()
        return translations, total_pages

    except Exception as e:
        print(f"Ошибка при получении переводов пользователя: {str(e)}")
    finally:
        session.close()


def get_translate(translate_id):
    """
    Получение перевода из таблицы Translate.

    :param translate_id: id записи перевода;
    :return: translate - объект Translate.
    """
    session = Session()

    try:
        # Запись перевода с заданным id
        translate = session.query(Translate).filter_by(id=translate_id).one()
        return translate

    except Exception as e:
        session.close()
        print(f"Ошибка при получении записи перевода: {str(e)}")
    finally:
        session.close()
