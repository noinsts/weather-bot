import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.utils import setup_logger
from src.middlewares import LoggingMiddleware
from src.handlers import *

load_dotenv()
TOKEN = os.getenv("TOKEN")


class WeatherBot:
    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)

        logging_middleware = LoggingMiddleware()
        self.dp.message.middleware(logging_middleware)
        self.dp.callback_query.middleware(logging_middleware)

        self.log = setup_logger()

        self.register_routers()

    def register_routers(self):
        self.dp.include_router(CommonHandlers().router)
        self.dp.include_router(LocationHandler().router)
        self.dp.include_router(WeatherHandler().router)

    async def run(self):
        try:
            self.log.info('Бот запущено!')
            await self.dp.start_polling(self.bot)
        finally:
            await self.bot.session.close()


if __name__ == "__main__":
    bot = WeatherBot()
    asyncio.run(bot.run())
