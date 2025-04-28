from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseKeyboard


class EditHometown(BaseKeyboard):
    def get_keyboard(self) -> InlineKeyboardMarkup:

        kb = [
            [InlineKeyboardButton(text='🏁 Меню', callback_data="back_to_menu")],
            [InlineKeyboardButton(text='🟡 Змінити місто', callback_data="change_city")],
            [InlineKeyboardButton(text='🔴 Видалити місто', callback_data="delete_city")]
        ]

        return InlineKeyboardMarkup(inline_keyboard=kb)
