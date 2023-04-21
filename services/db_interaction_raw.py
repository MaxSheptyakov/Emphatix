import asyncpg
from config import config
from aiogram.types import CallbackQuery

async def create_db_connection():
    return await asyncpg.connect(host=config.db.host, user=config.db.user, password=config.db.password,
                                 database=config.db.database, port=config.db.port)

async def add_reaction_to_db(query: CallbackQuery):
    conn = await create_db_connection()
    async with conn.transaction():
        try:
            await conn.execute(f"""insert into ai_message_reactions(user_id, bot_text, user_reaction)
    select {query.from_user.id}, '{query.message.text}', '{query.data}'; commit;""")
        except Exception as e:
            print(e)
    return

    # conn = await asyncpg.connect(host=config.db.host, user=config.db.user, password=config.db.password,
    #                              database=config.db.database, port=config.db.port)

