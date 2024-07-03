from aiogram.fsm.state import State, StatesGroup


class WeatherForm(StatesGroup):
    city = State()


class WeatherDays(StatesGroup):
    day = State()
    info_day = State()
