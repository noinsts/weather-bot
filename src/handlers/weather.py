import os
import requests
from dotenv import load_dotenv

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import  Command
from aiogram.enums import ParseMode

from .base import BaseHandler
from src.utils.states import CityAwait
from src.keyboards.reply import AllMenu
from src.utils.translation import WeatherTranslator


class WeatherHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.load_api_key()

    def load_api_key(self):
        load_dotenv()
        self.api_key = os.getenv("WEATHER_API")
        if not self.api_key:
            self.log.warning("WEATHER API KEY NOT FOUND")

    def register_handlers(self):
        self.router.message.register(self.home_city_weather, Command('home_weather'))
        self.router.message.register(self.home_city_weather, F.text == '☀️ Погода в рідному місті')
        self.router.message.register(self.process_get_city, CityAwait.waiting_for_city)

        self.router.message.register(self.another_city_weather, Command('weather'))
        self.router.message.register(self.another_city_weather, F.text == '⛈️ Погода в іншому місті')
        self.router.message.register(self.process_get_acw, CityAwait.waiting_for_another_city)


    async def home_city_weather(self, message: Message, state: FSMContext):
        city = self.db.get_city(message.from_user.id)

        if not city:
            await state.set_state(CityAwait.waiting_for_city)
            await message.answer('Введіть назву міста')
            return
        await self.return_city(message, city)


    async def process_get_city(self, message: Message, state: FSMContext):
        user_id = message.from_user.id
        city = message.text

        self.db.add_city(user_id, city)
        await message.answer('Успіх! Ваше рідне місто додадо бо БД.')

        await state.clear()
        await self.return_city(message, city)


    async def another_city_weather(self, message: Message, state: FSMContext):
        await state.set_state(CityAwait.waiting_for_another_city)
        await message.answer('Вкажіть назву міста')


    async def process_get_acw(self, message: Message, state: FSMContext):
        city = message.text

        await state.clear()
        await self.return_city(message, city)


    async def return_city(self, message: Message, city: str):
        base_url = 'http://api.openweathermap.org/data/2.5/weather'

        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()

            temp = data['main']['temp']
            humid = data['main']['humidity']
            wind_speed = data['wind']['speed']
            desc = data['weather'][0]['description']

            translator = WeatherTranslator()
            ukr_desc = translator.translations.get(desc.lower()).capitalize()

            forecast_message = (
                f"🌤️ <b>Прогноз погоди для {city}</b>\n\n"
                f"🌡 <b>Температура:</b> {temp}°C\n"
                f"☔ <b>Вологість:</b> {humid}%\n"
                f"🌬 <b>Швидкість вітру:</b> {wind_speed} м/с\n"
                f"☁️ <b>Погода:</b> {ukr_desc}"
            )

            await message.answer(
                forecast_message,
                reply_markup=AllMenu().get_keyboard(),
                parse_mode=ParseMode.HTML
            )
