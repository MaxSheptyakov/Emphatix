import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from config import config

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from reload_class_methods import new_send_message
import types


from models.db_model import Base

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
bot = Bot(token=config.tg_bot.token)

# Reload of bot method of sending messages
funcType = type(bot.send_message)
bot.send_message = types.MethodType(new_send_message, bot)


if config.tg_bot.use_redis:
    storage = RedisStorage2(host="redis_bot",pool_size=5)
else:
    storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def create_sessionmaker(user, password, database, host, port, sync=True):
    engine = create_async_engine(f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}",
                                 echo=False, pool_size=30#echo
                                 )

    if sync:
        async with engine.begin() as conn:
            #await conn.run_sync(Base.metadata.drop_all) #TODO
            await conn.run_sync(Base.metadata.create_all)

    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession, future=True
    )

    return async_sessionmaker