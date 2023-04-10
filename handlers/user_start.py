import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Text#,

from services.db_interaction import DB
from states.user_start import UserMain
from aiogram.types import ReplyKeyboardRemove
from keyboards.user_start import *
from keyboards.common import *

from keyboards.common import main_page_button, description_button
from messages.user_start import *
from handlers.onboarding import onboarding_first_step
from messages.common import *
from states.onboarding import QuestionnaireStates
from keyboards.onboarding import choose_time_keyboard

from services.payment_generation import create_payment_link
from aiogram import types

async def user_start(message: Message, db: DB, state: FSMContext):
    user = await db.add_user(message)
    args = message.get_args()
    if args:
        await db.add_source(message, args)
    await db.log_message(message)
    if '/start' in message.text and not user.completed_questionnaire:
        await onboarding_first_step(message=message, db=db, state=state)
        return
    if '/start' in message.text:
        send_message = welcome_message
    elif message.text == main_page_button:
        send_message = main_page_message
    else:
        send_message = main_page_message
    await state.finish()

    await state.set_state(UserMain.on_start)
    keyboard = home_keyboard
    await message.reply(send_message, reply_markup=keyboard, reply=False)


async def show_description(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    # await state.set_state(UserMain.on_start)
    await message.reply(bot_description_message, reply=False)
    # await user_start(message=message, state=state, db=db)


async def user_stop(message: Message, db: DB, state: FSMContext):
    await db.log_message(message)
    await state.finish()
    await db.stop_user(message)


async def leave_feedback(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.set_state(UserMain.feedback)
    await message.reply(feedback_message, reply_markup=ReplyKeyboardRemove(), reply=False)


async def save_feedback(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await db.save_feedback(message)
    await state.finish()
    await message.reply(feedback_saved_message, reply = False)
    await user_start(message=message, state=state, db=db)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_callback_query_handler(user_start, Text(equals=main_page_button),
                                       state="*")
    dp.register_message_handler(user_stop, commands=['stop'], state='*')

    dp.register_message_handler(user_start, Text(equals=main_page_button), state="*")

    dp.register_message_handler(show_description, Text(equals=description_button), state="*")
    dp.register_message_handler(show_description, commands=['description'], state="*")

    dp.register_message_handler(leave_feedback, Text(equals=feedback_button), state="*")
    dp.register_message_handler(save_feedback, state=UserMain.feedback)
