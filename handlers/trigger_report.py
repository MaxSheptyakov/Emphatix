from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text, Regexp

from services.db_interaction import DB
from services.common import parse_custom_date_period
from states.states import *
from keyboards.trigger_report import *
from keyboards.emotion_report import period_keyboard, custom_period_button
from messages.emotion_report import report_choose_message, custom_period_message, cant_parse_period_message

from messages.trigger_report import *
from keyboards.common import *
from handlers.user_start import user_start
from visualization.trigger_report import get_emotion_triggers_report
import os


async def set_trigger_report_period(message: Message, db: DB, state: FSMContext):
    await db.log_message(message)
    await state.set_state(TriggersReport.choose_period_for_report)
    if message.text == custom_period_button:
        await message.reply(custom_period_message, reply_markup=ReplyKeyboardRemove(), reply=False)
    else:
        await message.reply(report_choose_message, reply_markup=period_keyboard, reply=False)


async def show_emotions_with_triggers(message: Message, db: DB, state: FSMContext):
    await db.log_message(message)
    try:
        date_first, date_second = parse_custom_date_period(message.text)
        await state.update_data(date_first=str(date_first), date_second=str(date_second))
        available_emotions = await db.get_available_emotions_for_report_period(message.from_id, date_first=date_first,
                                                                               date_second=date_second)
    except:
        try:
            days = int(message.text)
            await state.update_data(days_for_report=days)
            available_emotions = await db.get_available_emotions_for_report(message.from_id, days=days)
        except:
            await message.reply(cant_parse_period_message, reply=False)
            return
    if available_emotions is not None:
        await state.set_state(TriggersReport.choose_emotion_for_report)
        await state.update_data(available_emotions=available_emotions)
        keyboard = generate_trigger_report_keyboard(available_emotions)
        await message.reply(choose_emotion_for_report_message, reply_markup=keyboard, reply=False)
    else:
        await message.reply(you_didnt_collect_triggers_message, reply=False)
        await set_trigger_report_period(message, db, state)


async def show_trigger_report(message: Message, db: DB, state: FSMContext):
    await db.log_message(message)
    data = await state.get_data()
    if message.text not in data.get('available_emotions'):
        await message.reply(wrong_emotion_message, reply=False)
        return
    emotion_for_report = message.text
    days = data.get('days_for_report')
    date_first = data.get('date_first')
    date_second = data.get('date_second')
    if date_first is not None and date_second is not None:
        trigger_report = await db.get_triggers_report_period(message.from_id, date_first, date_second, emotion_for_report)
    else:
        trigger_report = await db.get_triggers_report(message.from_id, days, emotion_for_report)
    report = await get_emotion_triggers_report(trigger_report, emotion_for_report, days, date_first, date_second)
    await message.reply_photo(open(report, 'rb'), reply=False, reply_markup=home_keyboard)
    try:
        os.remove(report)
    except:
        pass
    await state.finish()




def trigger_report_register(dp: Dispatcher):
    dp.register_message_handler(set_trigger_report_period, commands=["trigger_report"], state="*")
    dp.register_message_handler(set_trigger_report_period, Text(equals=triggers_report_button), state="*")
    dp.register_message_handler(set_trigger_report_period, Text(equals=custom_period_button),
                                state=TriggersReport.choose_period_for_report)
    dp.register_message_handler(user_start, Text(equals=main_page_button), state=TriggersReport.choose_emotion_for_report)
    dp.register_message_handler(show_emotions_with_triggers, Regexp(regexp='\d+'), state=TriggersReport.choose_period_for_report)
    dp.register_message_handler(show_trigger_report, state=TriggersReport.choose_emotion_for_report)


