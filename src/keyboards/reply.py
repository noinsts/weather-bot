from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .base import BaseKeyboard


class MainMenuKeyboard(BaseKeyboard):
    def get_keyboard(self):
        kb = [
            [KeyboardButton(text='🗒️ Допомога')],
            [KeyboardButton(text='🏙️ Додати місто')]
        ]
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

class MainMenuKeyboardRegister(BaseKeyboard):
    def get_keyboard(self):
        kb = [
            [KeyboardButton(text='🗒️ Допомога')],
            [KeyboardButton(text='☀️ Дізнатись погоду')]
        ]
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


class HelpMenuKeyboard(BaseKeyboard):
    def get_keyboard(self):
        kb = [
            [KeyboardButton(text='🏁 Меню')],
            [KeyboardButton(text='🏙️ Додати місто')],
            [KeyboardButton(text='☀️ Дізнатись погоду')]
        ]
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


class WeatherMenuKeyboard(BaseKeyboard):
    def get_keyboard(self):
        kb = [
            [KeyboardButton(text='🏁 Меню')],
            [KeyboardButton(text='☀️ Дізнатись погоду')]
        ]
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
