from keyboards.common import reaction_buttons, create_inline_keyboard
from messages.common import *
from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from services.common import check_tries
from states.user_start import UserMain
from services.db_interaction import DB
from handlers.user_start import user_start
from services.db_interaction_raw import add_reaction_to_db


async def choose_from_keyboard(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    if await check_tries(state) > 3:
        await state.finish()
        await state.set_state(UserMain.on_start)
        await message.reply(main_menu_redirect_message, reply=False)
        await user_start(message=message, state=state, db=db)
    else:
        await message.reply(choose_from_keyboard_message, reply=False)


def create_reaction_keyboard(data):
    loc_buttons = reaction_buttons.copy()
    if data in loc_buttons:
        loc_buttons[loc_buttons.index(data)] = '✅' + loc_buttons[loc_buttons.index(data)]
    return create_inline_keyboard(loc_buttons, row_width=4)


async def inline_keyboard_callback_handler(query: CallbackQuery):
    await query.message.edit_reply_markup(create_reaction_keyboard(query.data))
    await add_reaction_to_db(query)
    return


def common_handler(dp: Dispatcher):
    dp.register_message_handler(choose_from_keyboard, state='*')
    dp.register_callback_query_handler(inline_keyboard_callback_handler, state='*')
