from keyboards.common import main_page_keyboard, talk_to_me_button
from messages.common import *
from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from services.openai_api import get_ans_from_response, get_msg_text_from_msg, get_msg_from_response, get_total_tokens
from services.openai_messaging import run_dialog
from states.emotion_gather import EmotionGatherStates
from states.emotion_report import EmotionReport
from states.user_start import Dialog
from services.db_interaction import DB
import json
from aiogram.dispatcher.filters import Text


async def start_dialog(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    user = await db.return_user_if_exist(message)
    if not user.completed_questionnaire:
        from handlers.onboarding import onboarding_first_step
        await onboarding_first_step(message=message, state=state, db=db)
        return
    await state.set_state(Dialog.dialog_started)
    if message.text == talk_to_me_button or message.text == '/dialog':
        await state.finish()
        dialog_messages = None
    else:
        data = await state.get_data()
        dialog_messages = data.get('dialog_messages')
    if dialog_messages is None:
        pass
    else:
        dialog_messages = json.loads(dialog_messages)
        dialog_messages.append({'role':'user', 'content':message.text})
    wait_for_reply = await message.reply(bot_thinking_message, reply_markup=main_page_keyboard, reply=False)
    old_messages, response = await run_dialog(dialog_messages, sex=user.sex)
    response_text = get_ans_from_response(response)
    await wait_for_reply.delete()
    await message.reply(response_text, reply_markup=main_page_keyboard, reply=False)
    dialog_messages = old_messages + [get_msg_from_response(response)]
    if get_total_tokens(response) > 3200:
        dialog_messages = dialog_messages[1:]
    await state.update_data(dialog_messages=json.dumps(dialog_messages))


def dialog_handler(dp: Dispatcher):
    dp.register_message_handler(start_dialog, commands=['dialog'], state='*')
    dp.register_message_handler(start_dialog, Text(equals=talk_to_me_button), state='*')
    dp.register_message_handler(start_dialog, state=Dialog.dialog_started)
    dp.register_message_handler(start_dialog, state=EmotionGatherStates.gather_finish)
    dp.register_message_handler(start_dialog, state=EmotionReport.flower_sent)
