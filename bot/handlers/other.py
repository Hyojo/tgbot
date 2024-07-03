import json

from aiogram import Dispatcher, F
from aiogram.types import Message


def register_other_handlers(dp: Dispatcher):
    dp.message.register(message_answer, F.dice)


async def message_answer(message: Message):
    await message.answer("Хе-Хе")
