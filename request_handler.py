import asyncio
from aiogram.utils.exceptions import BotBlocked

from bot_init import bot, dp, logger, config, create_sessionmaker

from handlers.user_start import register_user
from handlers.onboarding import onboarding
from handlers.emotion_gather import emotions_gather
from handlers.emotion_report import weekly_report_dp
from handlers.common import common_handler
from handlers.emotion_list_report import daily_report
from handlers.trigger_report import trigger_report_register
from handlers.commands_top_level import top_handler
from handlers.test_handler import test_handler
from middlewares.db import DbMiddleware
from aiogram_dialog import DialogRegistry


async def main():
    logger.info("Bot started!")

    async_sessionmaker = await create_sessionmaker(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
        port=config.db.port
    )

    dp.middleware.setup(DbMiddleware(async_sessionmaker))

    # TODO -- add needed handlers only
    test_handler(dp)
    top_handler(dp)
    onboarding(dp)
    emotions_gather(dp)
    register_user(dp)
    daily_report(dp)
    weekly_report_dp(dp)
    trigger_report_register(dp)
    common_handler(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await asyncio.shield(dp.storage.close())
        await asyncio.shield(dp.storage.wait_closed())
        session = await bot.get_session()
        await session.close()


async def cli():
    """Wrapper for command line"""
    try:
        await asyncio.gather(
            main(),
        )
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    asyncio.run(cli())
