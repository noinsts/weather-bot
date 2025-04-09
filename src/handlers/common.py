from aiogram import F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.enums.parse_mode import ParseMode

from .base import BaseHandler
from src.keyboards.reply import MainMenuKeyboard, MainMenuKeyboardRegister
from src.keyboards.reply import HelpMenuKeyboard


class CommonHandlers(BaseHandler):
    def register_handlers(self):
        self.router.message.register(self.cmd_start, CommandStart())
        self.router.message.register(self.cmd_start, F.text == '🏁 Меню')
        self.router.message.register(self.cmd_help, Command('help'))
        self.router.message.register(self.cmd_help, F.text == '🗒️ Допомога')

    async def cmd_start(self, message: Message):
        if self.db.get_city(message.from_user.id):
            rm = MainMenuKeyboardRegister().get_keyboard()
        else:
            rm = MainMenuKeyboard().get_keyboard()

        await message.answer(
            "👋 <b>Вітаємо в боті з погодою!</b>\n\n"
            "Дізнайтесь прогноз для вашого міста — просто надішліть <code>/weather</code>.\n\n"
            "Місто можна не вказувати, якщо ви вже його додали раніше.",
            reply_markup=rm,
            parse_mode=ParseMode.HTML
        )

    async def cmd_help(self, message: Message):
        await message.answer(
            "🆘 <b>Допомога</b>\n\n"
            "➕ Щоб додати місто до бази даних — натисніть кнопку нижче.\n"
            "🌤 Щоб дізнатися прогноз погоди — напишіть команду <code>/weather</code>.\n"
            "📍 Назву міста можна не вказувати, якщо воно вже додане у вашу БД.",
            parse_mode=ParseMode.HTML,
            reply_markup=HelpMenuKeyboard().get_keyboard()
        )
