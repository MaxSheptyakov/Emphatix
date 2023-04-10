from messages.common import *
from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from services.common import check_tries
from states.user_start import UserMain
from services.db_interaction import DB
from handlers.user_start import user_start


async def choose_from_keyboard(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    if await check_tries(state) > 3:
        await state.finish()
        await state.set_state(UserMain.on_start)
        await message.reply(main_menu_redirect_message, reply=False)
        await user_start(message=message, state=state, db=db)
    else:
        await message.reply(choose_from_keyboard_message, reply=False)


def common_handler(dp: Dispatcher):
    dp.register_message_handler(choose_from_keyboard, state='*')
