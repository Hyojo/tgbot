import asyncio

from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.inline import get_keyboard_weather, get_keyboard_main
from bot.misc.stateform import WeatherForm


def register_user_handlers(dp: Dispatcher):
    # todo: register all user handlers
    dp.message.register(cmd_start, Command(commands=["start", 'menu']))
    dp.message.register(cmd_dice, Command(commands="dice"))
    dp.message.register(reg_end, WeatherForm.city)


async def cmd_start(message: Message):
    await message.answer("Hello!", reply_markup=get_keyboard_main())


async def reg_end(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()
    await message.answer(f'Ваш город: {data['city']}', reply_markup=get_keyboard_weather())


async def cmd_dice(message: Message, bot: Bot):
    dice_1 = await bot.send_dice(message.chat.id, emoji='🎲')
    dice_2 = await bot.send_dice(message.chat.id, emoji='🎲')
    summ = dice_1.dice.value + dice_2.dice.value
    await asyncio.sleep(3)
    await bot.send_message(message.chat.id, f'значение кубиков {summ}')
