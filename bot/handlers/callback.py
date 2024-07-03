import requests
from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.exceptions import AiogramError
from requests import HTTPError

from bot.keyboards.inline import get_keyboard_weather_5_days, get_back_main_menu
from bot.misc.stateform import WeatherForm, WeatherDays
from bot.misc.weather import weather_now, weather_5_days, weather_day
from config_reader import config


def register_callback(dp: Dispatcher):
    dp.callback_query.register(cmd_weather, F.data == "weather")
    dp.callback_query.register(weather_info, F.data.startswith("weather_"))
    dp.callback_query.register(get_weather_day, lambda query: query.data in ['0', '1', '2', '3', '4', '5'])


async def cmd_weather(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите город:")
    await state.set_state(WeatherForm.city)


async def weather_info(callback: CallbackQuery, state: FSMContext):
    api = config.api_weather_token.get_secret_value()
    data = await state.get_data()
    action = callback.data
    try:
        match action:
            case "weather_now":
                response = requests.get(
                    f'https://api.openweathermap.org/data/2.5/weather?q={data['city']}&lang=ru&units=metric&appid={api}')
                response.raise_for_status()
                await callback.message.edit_text(weather_now(response.json()), reply_markup=get_back_main_menu())
            case "weather_5_days":
                response = requests.get(
                    f'https://api.openweathermap.org/data/2.5/forecast?q={data['city']}&lang=ru&units=metric&appid={api}')
                response.raise_for_status()
                await state.set_state(WeatherDays.day)
                await callback.message.edit_text(weather_5_days(response.json()),
                                                 reply_markup=get_keyboard_weather_5_days())
                await callback.answer()
    except HTTPError:
        await callback.message.answer("Введите город:")
        await state.set_state(WeatherForm.city)
        await callback.answer()


async def get_weather_day(callback: CallbackQuery, state: FSMContext):
    num = callback.data
    city = await state.get_data()
    await state.update_data(day=callback.data)
    try:
        await callback.message.edit_text(weather_day(int(num), city["city"]),
                                         reply_markup=get_keyboard_weather_5_days())
    except AiogramError:
        await callback.answer()
