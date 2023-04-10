import asyncio
from bot_init import create_sessionmaker, config, logger
from middlewares.db import DbMiddleware




async def check_payments():
    logger.info("Payments checker started!")
    async_sessionmaker = await create_sessionmaker(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
        port=config.db.port,
        sync=False
    )
    while True:

        db_middleware = DbMiddleware(async_sessionmaker)
        await db_middleware.pre_process_messages()
        pass ## Some logics to update payments here #TODO
        await db_middleware.post_process_messages()
        await asyncio.sleep(60)


async def cli():
    """Wrapper for command line"""
    try:
        await asyncio.gather(
            check_payments()
        )
    except (KeyboardInterrupt, SystemExit):
        logger.error("Payments checker stopped!")


if __name__ == '__main__':
    asyncio.run(cli())
