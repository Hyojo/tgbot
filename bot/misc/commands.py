from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Starts the bot",
        ),
        BotCommand(
            command="help",
            description="Help",
        ),
        BotCommand(
            command="menu",
            description="bot menu",
        ),
        BotCommand(
            command="dice",
            description="dice x2",
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
