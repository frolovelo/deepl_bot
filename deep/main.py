"""Взаимодействие с Telegram"""

import os
from dotenv import load_dotenv
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import deepl
from deep.db_usage import *



load_dotenv()
bot = TeleBot(os.getenv('TOKEN_TELEGRAM'))
translator = deepl.Translator(os.getenv('AUTH_KEY_DEEPL'))


def markup_start(page=1, text="История переводов"):
    """Формирует стартовую клавиатуру."""
    cal_data = f'HISTORY {page}'
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text=text,
                                    callback_data=cal_data))
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    """Стартовое меню."""
    add_new_user(message.chat.id, message.chat.username)
    bot.send_message(message.chat.id,
                     text="Введите текст на английском для перевода:",
                     reply_markup=markup_start())


@bot.message_handler(func=lambda message: True)
def translate_text(message):
    """Обрабатывает любое текстовое сообщение - переводит текст с англ. на русский."""
    text_to_translate = message.text
    target_language = 'RU'
    translated_text = translator.translate_text(text_to_translate, target_lang=target_language)
    set_translation(message.chat.id, target_language, message.text, translated_text.text)
    bot.send_message(message.chat.id, f"{translated_text.text}")
    bot.send_message(message.chat.id,
                     text="Введите текст на английском для перевода:",
                     reply_markup=markup_start())


@bot.callback_query_handler(lambda call: call.data.startswith('HISTORY'))
def get_history(call):
    """
    История переводов.

    Notes:
        Структура call.data: "HISTORY page",
        где page - номер страницы пагинации.
    """
    page = 1 if not call.data[7:].strip() else int(call.data[7:].strip())
    obj_translate, total_pages = get_user_translations(call.message.chat.id, page_number=page)

    def text_format_markup(lst_obj: list, total_pages: int, current_page: int = 1, start: int = 1):
        """
        Форматирование текста и создание клавиатуры для перехода к отдельной записи перевода.

        :param lst_obj: список объектов Translate;
        :param total_pages: всего страниц;
        :param current_page: текущая страница;
        :param start: старт отсчета для enumerate.

        :return: кортеж (текст, клавиатура).
        """
        lst = []
        markup = InlineKeyboardMarkup(row_width=3)
        lst_button = []

        for ind, obj in enumerate(lst_obj, start=start):
            text_original = obj.text_original[:40] + '...' if len(obj.text_original) > 40 \
                else obj.text_original
            text_translate = obj.text_translate[:40] + '...' if len(obj.text_translate) > 40 \
                else obj.text_translate
            lst.append(f"<b>{ind}.</b> {text_original} - {text_translate}")
            lst_button.append(InlineKeyboardButton(text=f'{ind}',
                                                   callback_data=f'TRANSLATE {obj.id} {page}'))

        markup.add(*lst_button)
        lst_button = []

        # Создание кнопки "назад"
        if current_page > 1:
            lst_button.append(InlineKeyboardButton(text='Назад',
                                                   callback_data=f'HISTORY {current_page - 1}'))

        # Кнопка нового перевода
        lst_button.append(InlineKeyboardButton(text='Скрыть меню',
                                               callback_data='MENU'))

        # Создание кнопки "вперед"
        if current_page < total_pages:
            lst_button.append(InlineKeyboardButton(text='Вперед',
                                                   callback_data=f'HISTORY {current_page + 1}'))

        markup.add(*lst_button)
        text = ';\n'.join(lst)
        return text, markup

    text, markup = text_format_markup(obj_translate, total_pages=total_pages, current_page=page,
                                      start=(page - 1) * 6 + 1)
    preview = "История пуста..." if not text else "Ваша история:"
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=f'<b>{preview}</b>\n\n{text}',
                          reply_markup=markup,
                          parse_mode='html'
                          )


@bot.callback_query_handler(lambda call: call.data.startswith('TRANSLATE'))
def check_translate(call):
    """
    Обработчик обратного вызова для проверки и отображения перевода.

    Notes:
        Структура call.data: "TRANSLATE id page",
        где id - это идентификатор записи, а page - номер страницы пагинации.
    """
    # Извлекаем параметры из call.data
    id_translate, page = int(call.data.split()[1]), int(call.data.split()[2])
    obj = get_translate(id_translate)

    # Создаем клавиатуру
    markup = markup_start(page=page, text="Вернуться к истории переводов")

    # Удаляем сообщение с вызовом
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)

    def send_large_text(chat_id: int, text: str) -> None:
        """
        Отправка сообщений более 4096 символов.

        :param chat_id: id пользователя;
        :param text: строка.
        """
        max_length = 4096
        chunks = [text[i:i + max_length] for i in range(0, len(text), max_length)]

        for chunk in chunks:
            bot.send_message(chat_id=chat_id, text=chunk, parse_mode='html')

    # Отправляем исходный текст
    send_large_text(chat_id=call.message.chat.id,
                    text=f'<b>Исходный текст:</b>\n{obj.text_original}\n\n'
                    )

    # Отправляем перевод
    send_large_text(chat_id=call.message.chat.id,
                    text=f'<b>Перевод:</b>\n{obj.text_translate}'
                    )

    # Отправляем инструкцию для ввода нового текста
    bot.send_message(chat_id=call.message.chat.id,
                     text='Вы можете ввести новый текст для перевода:',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'MENU')
def return_to_main_menu(call):
    """Обработчик обратного вызова для возвращения в главное меню."""
    markup = markup_start()
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text="Введите текст на английском для перевода:",
                          reply_markup=markup)


bot.infinity_polling()
