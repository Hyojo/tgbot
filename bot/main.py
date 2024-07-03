import logging

from aiogram import Bot, Dispatcher

# from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.filters import register_all_filters
from bot.handlers.main import register_all_handlers
from bot.database.models import register_models
from bot.misc.commands import set_commands
from config_reader import config


async def on_start_up(dp: Dispatcher) -> None:
    register_all_filters(dp)
    register_all_handlers(dp)
    register_models()


async def start_bot(bot: Bot):
    await set_commands(bot)


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s"
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )
    bot = Bot(token=config.bot_token.get_secret_value(), HTML='HTML')
    # dp = Dispatcher(storage=MemoryStorage())
    dp = Dispatcher()
    register_all_handlers(dp)
    dp.startup.register(start_bot)
    await on_start_up(dp)
    await dp.start_polling(bot, skip_updates=True)
