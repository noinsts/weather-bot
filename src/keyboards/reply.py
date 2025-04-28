from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .base import BaseKeyboard


class MainMenuKeyboard(BaseKeyboard):
    def get_keyboard(self) -> ReplyKeyboardMarkup:
        kb = [
            [KeyboardButton(text='🗒️ Допомога')],
            [KeyboardButton(text='🏙️ Додати місто')],
            [KeyboardButton(text='⛈️ Погода в іншому місті')]
        ]
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


class MainMenuKeyboardRegister(BaseKeyboard):
    def get_keyboard(self) -> ReplyKeyboardMarkup:
        kb = [
            [KeyboardButton(text='🗒️ Допомога')],
            [KeyboardButton(text='☀️ Погода в рідному місті')],
            [KeyboardButton(text='⛈️ Погода в іншому місті')]
        ]
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


class HelpMenuKeyboard(BaseKeyboard):
    def get_keyboard(self) -> ReplyKeyboardMarkup:
        kb = [
            [KeyboardButton(text='🏁 Меню')],
            [KeyboardButton(text='🏙️ Додати місто')],
            [KeyboardButton(text='⛈️ Погода в іншому місті')]
        ]
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


class HelpMenuKeyboardRegister(BaseKeyboard):
    def get_keyboard(self) -> ReplyKeyboardMarkup:
        kb = [
            [KeyboardButton(text='🏁 Меню')],
            [KeyboardButton(text='☀️ Погода в рідному місті')],
            [KeyboardButton(text='⛈️ Погода в іншому місті')]
        ]
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


class AllMenuRegister(BaseKeyboard):
    def get_keyboard(self) -> ReplyKeyboardMarkup:
        kb = [
            [KeyboardButton(text='🏁 Меню'), KeyboardButton(text='🗒️ Допомога')],
            [KeyboardButton(text='☀️ Погода в рідному місті')],
            [KeyboardButton(text='⛈️ Погода в іншому місті')]
        ]
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

class AllMenu(BaseKeyboard):
    def get_keyboard(self) -> ReplyKeyboardMarkup:
        kb = [
            [KeyboardButton(text='🏁 Меню'), KeyboardButton(text='🗒️ Допомога')],
            [KeyboardButton(text='🏙️ Додати місто')],
            [KeyboardButton(text='⛈️ Погода в іншому місті')]
        ]
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
