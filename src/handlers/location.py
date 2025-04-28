from aiogram import F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.handlers import CommonHandlers
from src.keyboards.reply import AllMenuRegister, AllMenu
from src.keyboards.inline import EditHometown
from src.utils import CityAwait
from .base import BaseHandler


class LocationHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.common_handler = CommonHandlers()


    def register_handlers(self):
        self.router.message.register(self.add_city_button, F.text == '🏙️ Додати місто')
        self.router.message.register(self.process_register_city, CityAwait.waiting_for_city)

        self.router.message.register(self.settings_hub, F.text == '⚙️ Налаштування')

        self.router.callback_query.register(self.edit_city_button, F.data == 'change_city')
        self.router.callback_query.register(self.delete_city_button, F.data == "delete_city")

        self.router.message.register(self.process_edit_city, CityAwait.waiting_for_change_city)


    async def add_city_button(self, message: Message, state: FSMContext):
        """Обробник кнопки '🏙️ Додати місто'"""
        user_id = message.from_user.id

        if self.db.get_city(user_id) is not None:
            await message.answer('Помилка! Ваше місто вже є в БД')
            await message.answer('Повернення до меню...')
            await self.common_handler.cmd_start(message)
            return

        await state.set_state(CityAwait.waiting_for_city)
        await message.answer('Вкажіть назву міста')


    async def process_register_city(self, message: Message, state: FSMContext):
        """Обробник вводу назви нового міста"""
        user_id: int = message.from_user.id
        city: str = message.text

        if not city.strip().isalpha():
            await message.answer("Назва міста має містити лише літери. Спробуйте ще раз.")
            return

        self.db.add_city(user_id, city)

        await message.answer(
            "Успіх! Ваше місто додано до БД", 
            reply_markup=AllMenuRegister().get_keyboard()
        )

        await state.clear()


    async def settings_hub(self, message: Message):
        """Обробник кнопки '⚙️ Налаштування'"""
        city = self.db.get_city(message.from_user.id)

        if not city:
            await message.answer("У вас ще немає збереженого міста, спробуйте додати його")
            await self.common_handler.cmd_start(message)
            return

        await message.answer(
            f"⚙️ <b>Керування рідним містом</b>\n\n"
            f"Ваше поточне місто <b>{city}</b>\n\n"
            f"Оберіть дію:",
            reply_markup=EditHometown().get_keyboard(),
            parse_mode=ParseMode.HTML
        )


    async def edit_city_button(self, callback: CallbackQuery, state: FSMContext):
        """Обробник події callback 'change_city'"""
        city = self.db.get_city(callback.from_user.id)

        await callback.answer("Переходимо до зміни міста...")

        await state.set_state(CityAwait.waiting_for_change_city)

        await callback.message.edit_text(
            f"<b>Зміна рідного міста</b>\n\n"
            f"Ваше поточне місто <b>{city}</b>\n\n"
            f"Введіть назву нового міста",
            parse_mode=ParseMode.HTML
        )


    async def process_edit_city(self, message: Message, state: FSMContext):
        user_id: int = message.from_user.id
        old_city: str = self.db.get_city(user_id)
        new_city: str = message.text

        if not new_city.strip().isalpha():
            await message.answer("Назва міста має містити лише літери. Спробуйте ще раз.")
            return

        self.db.edit_city(user_id, new_city)

        await message.answer(
            f"✅ <b>Місто успішно змінено</b>\n\n"
            f"Старе місто: <b>{old_city}</b>\n"
            f"Нове місто: <b>{new_city}</b>",
            parse_mode=ParseMode.HTML
        )

        await message.answer("Повертаємось до меню...")

        await self.common_handler.cmd_start(message)

        await state.clear()


    async def delete_city_button(self, callback: CallbackQuery):
        """Обробник події callback 'delete_city'"""
        user_id = callback.from_user.id
        city = self.db.get_city(user_id)

        self.db.delete_city(user_id)

        await callback.answer("Місто успішно видалено!")

        await callback.message.edit_text(
            f"❌ <b>Місто видалено</b>\n\n"
            f"Ваше рідне місто (<b>{city}</b>) було видалено з бази даних.",
            parse_mode=ParseMode.HTML
        )

        await callback.message.answer(
            "Повертаємось до головного меню...",
            reply_markup=AllMenu().get_keyboard()
        )
