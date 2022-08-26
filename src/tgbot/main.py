import asyncio
import logging
import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.config import BotConfig, load_bot_config
from tgbot.filters.role import AdminFilter, RoleFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.common import register_common
from tgbot.handlers.users import register_user
from tgbot.middlewares.role import RoleMiddleware
from tgbot.utils.default_commands import set_default_commands

logger = logging.getLogger(__name__)


async def main():

    logging.basicConfig(level=logging.INFO)
    logger.info("Startinug bot")
    config: BotConfig = load_bot_config("bot.ini")
    storage = MemoryStorage()

    bot = Bot(config.token)
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(RoleMiddleware(config.admins_id))

    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_admin(dp)
    register_common(dp)
    register_user(dp)

    await set_default_commands(dp)
    # starting
    try:
        await dp.start_polling()
    finally:
        await storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


def cli():
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot is stopped")


if __name__ == "__main__":
    cli()
