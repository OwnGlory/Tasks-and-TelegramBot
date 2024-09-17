from aiogram.types import KeyboardButton  # Кнопки для Reply клавиатуры
from aiogram.types import ReplyKeyboardMarkup  # Клавиатура под полем ввода

from lexicon import lexicon


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=lexicon.buttons.create_task),
            KeyboardButton(text=lexicon.buttons.get_task),
        ],
        [
            KeyboardButton(text=lexicon.buttons.get_task_for_tag),
            KeyboardButton(text=lexicon.buttons.get_all_task),
        ]
    ],
    # Подстраивает размер кнопок под телефон
    resize_keyboard=True,
    # Скрывает клавиатуру после нажатия кнопки
    one_time_keyboard=True,
    # выводит сообщение в поле ввода во время работы с меню
    input_field_placeholder='Выберите действие',
)
