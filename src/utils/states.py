from aiogram.fsm.state import State, StatesGroup


class CityAwait(StatesGroup):
    waiting_for_city = State()
