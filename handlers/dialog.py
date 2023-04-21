from keyboards.common import main_page_keyboard
from messages.common import *
from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from services.openai_api import get_ans_from_response, get_msg_text_from_msg, get_msg_from_response, get_total_tokens
from services.openai_messaging import run_dialog
from states.user_start import Dialog
from services.db_interaction import DB
import json


async def start_dialog(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.set_state(Dialog.dialog_started)
    dialog_messages = await state.get_data()
    dialog_messages = dialog_messages.get('dialog_messages')
    if dialog_messages is None:
        pass
    else:
        dialog_messages = json.loads(dialog_messages)
        dialog_messages.append({'role':'user', 'content':message.text})
    wait_for_reply = await message.reply(bot_thinking_message, reply_markup=main_page_keyboard, reply=False)
    old_messages, response = await run_dialog(dialog_messages)
    response_text = get_ans_from_response(response)
    await wait_for_reply.delete()
    await message.reply(response_text, reply_markup=main_page_keyboard, reply=False)
    dialog_messages = old_messages + [get_msg_from_response(response)]
    print(get_total_tokens(response))
    if get_total_tokens(response) > 3200:
        dialog_messages = dialog_messages[1:]
    await state.update_data(dialog_messages=json.dumps(dialog_messages))
    data = await state.get_data()


def dialog_handler(dp: Dispatcher):
    dp.register_message_handler(start_dialog, commands=['dialog'], state='*')
    dp.register_message_handler(start_dialog, state=Dialog.dialog_started)
