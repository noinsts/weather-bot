from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from .base import BaseHandler
from src.utils.states import CityAwait

from src.keyboards.reply import AllMenu
from src.handlers.common import CommonHandlers



class LocationHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.common_handler = CommonHandlers()

    def register_handlers(self):
        self.router.message.register(self.add_city_button, F.text == '🏙️ Додати місто')
        self.router.message.register(self.process_register_city, CityAwait.waiting_for_city)

    async def add_city_button(self, message: Message, state: FSMContext):
        user_id = message.from_user.id
        if self.db.get_city(user_id) is not None:
            await message.answer('Помилка! Ваше місто вже є в БД')
            await message.answer('Повернення до меню...')
            await self.common_handler.cmd_start(message)
            return
        await state.set_state(CityAwait.waiting_for_city)
        await message.answer('Вкажіть назву міста')

    async def process_register_city(self, message: Message, state: FSMContext):
        user_id = message.from_user.id
        city = message.text

        self.db.add_city(user_id, city)
        await message.answer(
            "Успіх! Ваше місто додано до БД", 
            reply_markup=AllMenu().get_keyboard()
        )
        await state.clear()
