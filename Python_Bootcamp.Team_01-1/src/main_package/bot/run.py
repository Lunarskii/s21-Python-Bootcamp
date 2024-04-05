from aiogram import (
    Bot,
    Dispatcher,
    types,
    F,
    html
)
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from contextlib import suppress

from .config import TOKEN
from . import handlers
from ..logger import logging


"""
The module contains the basic configuration settings of the bot.
"""


async def main():
    """
    A function to launch the bot.

    :return: None
    """

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    dp.include_routers(
        handlers.main_router,
        handlers.generator_router,
        handlers.game_router,
        handlers.game_talk_router,
        handlers.game_attack_router,
        handlers.game_trade_router,
        handlers.game_goto_router,
        handlers.game_quest_router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    with suppress(KeyboardInterrupt):
        await dp.start_polling(bot)
