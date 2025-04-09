import os
import requests
from dotenv import load_dotenv

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import  Command, CommandObject

from .base import BaseHandler
from src.utils.states import CityAwait
from src.keyboards.reply import WeatherMenuKeyboard


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
        self.router.message.register(self.weather, Command('weather'))
        self.router.message.register(self.weather, F.text == '☀️ Дізнатись погоду')

    async def weather(self, message: Message, state: FSMContext):
        city = self.db.get_city(message.from_user.id)

        if not city:
            await state.set_state(CityAwait.waiting_for_city)
            await message.answer('Введіть назву міста')
            return
        await self.return_city(message, city)


    async def process_get_city(self, message: Message, state: FSMContext):
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

            await message.answer(
                f"Температура в місті {city}: {temp}, вологість: {humid}%.",
                reply_markup=WeatherMenuKeyboard().get_keyboard()
            )
