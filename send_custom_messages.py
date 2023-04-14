from bot_init import bot
from config import config
import psycopg2
import pandas as pd
from tqdm import tqdm
import asyncio


def send_message_to_users(message: str, sql: str, reply_markup=None):
    """
    Sql must return the result with column user_id
    """
    with psycopg2.connect(host=config.db.host, user=config.db.user, password=config.db.password,
                          database=config.db.database, port=config.db.port) as conn:
        user_list = pd.read_sql_query(sql, conn)
        for user_id in tqdm(user_list.user_id):
            try:
                asyncio.run(bot.send_message(chat_id=user_id, text=message))
            except Exception as e:
                print(f'Can not send message to user {user_id}. Error: {e}')
    print('Messages sent')
