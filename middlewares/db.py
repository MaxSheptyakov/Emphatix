from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
import asyncio

from services.db_interaction import DB


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, async_sessionmaker, create_session=False):
        super().__init__()
        self.async_sessionmaker = async_sessionmaker
        if create_session:
            self.session = async_sessionmaker()

    async def pre_process(self, obj, data, *args):
        session = self.async_sessionmaker()#self.session
        data["session"] = session
        data["db"] = DB(session)
        # if not getattr(obj, "from_user", None):
        #     data["user"] = None
        # else:
        #     data["user"] = await data['db'].return_user_if_exist(obj.from_user.id)

    async def pre_process_messages(self, *args):
        self.session = self.async_sessionmaker()#self.session
        self.db = DB(self.session)

    async def post_process_messages(self, *args):
        await asyncio.shield(self.session.close())

    async def post_process(self, obj, data, *args):
        del data["db"]
        session = data.get("session")
        if session:
            await asyncio.shield(session.close())
