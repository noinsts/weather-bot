import os
import requests
from dotenv import load_dotenv

from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram import Dispatcher
from db.database import Database


class BotHandlers:
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    def api_key(self):
        load_dotenv()
        return os.getenv("WEATHER_API")

    async def start(self, message: Message):
        await message.answer('Вітаємо в боті з погодою! '
        'Ви можете дізнатись погоду за допомогою /weather, '
        'або додати ваше місто за допомогою /add_city')

    async def add_city(self, message: Message, command: CommandObject):
        user_id = message.from_user.id

        if command.args:
            city = command.args
    
            if self.db.add_city(user_id, city):
                await message.answer('Успіх! Ви додали ваше місто')
            else:
                await message.answer('Помилка! Інформація про ваше місто вже записана')
        else:
            await message.answer('Ви не вказали місто')


    async def weather(self, message: Message, command: CommandObject):
        city = command.args or self.db.get_city(message.from_user.id)

        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        api_key = self.api_key() 

        params = {
		    "q" : city, 
		    "appid" : api_key, 
		    "units" : "metric"
	    }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()

            temp = data['main']['temp']
            humid = data['main']['humidity']

            await message.answer(f"Температура в місті {city}: {temp}, вологість: {humid}%.")

        
    def register_handlers(self, dp: Dispatcher):
        dp.message.register(self.start, CommandStart())
        dp.message.register(self.add_city, Command("add_city"))
        dp.message.register(self.weather, Command('weather'))
