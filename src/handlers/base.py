from abc import ABC, abstractmethod

from aiogram import Router

from src.db.database import Database
from src.utils import setup_logger


class BaseHandler(ABC):
    def __init__(self):
        self.router = Router()
        self.db = Database()
        self.log = setup_logger()
        self.register_handlers()

    @abstractmethod
    def register_handlers(self):
        pass
