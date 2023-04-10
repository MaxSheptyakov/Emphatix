import asyncio

from aiogram.utils.exceptions import BotBlocked
from config import config
from middlewares.db import DbMiddleware


from datetime import datetime, timedelta

from bot_init import create_sessionmaker, dp, bot, logger
from services.push_preparation import prepare_push
from pandas import isnull


async def send_pushes():
    logger.info("Push engine started!")
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
        pass ## Some logics to send push and store info about it TODO
        pushes = await db_middleware.db.get_pushes_to_send()
        print(pushes)
        pushes_to_send = pushes.drop_duplicates(['user_id', 'send_type', 'custom_text'])
        for i, push in pushes_to_send.iterrows():
            print(push)
            user_id, push_text, keyboard = prepare_push(push)
            try:
                await bot.send_message(chat_id=user_id, text=push_text, reply_markup=keyboard)
                error = None
            except Exception as e:
                error = str(e)
            finally:
                print(pushes.loc[(isnull(pushes.custom_text)|
                                             (pushes.custom_text == push.custom_text))])
                store_push_ids = pushes.loc[(pushes.user_id == push.user_id)&
                                            (pushes.send_type == push.send_type)&
                                            (isnull(pushes.custom_text)|
                                             (pushes.custom_text == push.custom_text)),
                    'send_schedule_id'].tolist()
                print(store_push_ids)
                await db_middleware.db.store_sent_pushes(push.user_id, store_push_ids, error)
        await db_middleware.post_process_messages()
        await asyncio.sleep(15)


async def cli():
    """Wrapper for command line"""
    try:
        await asyncio.gather(
            send_pushes(),
        )
    except (KeyboardInterrupt, SystemExit):
        logger.error("Push engine stopped!")


if __name__ == '__main__':
    asyncio.run(cli())
