from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text

from services.common import parse_custom_date_period
from services.db_interaction import DB
from states.daily_report import EmotionListReport
from datetime import date
from keyboards.common import *
from messages.emotion_list_report import *
from datetime import timedelta
from handlers.user_start import user_start
from messages.emotion_report import report_choose_message, custom_period_message, cant_parse_period_message
from keyboards.emotion_report import custom_period_button, period_keyboard

async def emotion_list_report_variants(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.set_state(EmotionListReport.report_start)
    if message.text == custom_period_button:
        await message.reply(custom_period_message, reply_markup=ReplyKeyboardRemove(), reply=False)
    else:
        await message.reply(report_choose_message, reply_markup=period_keyboard, reply=False)


async def emotion_report_start_days(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    try:
        date_first, date_second = parse_custom_date_period(message.text)
        await emotion_report(message, state, db, days=None, date_first=date_first, date_second=date_second)
        return
    except:
        pass
    try:
        days = int(message.text)
        await emotion_report(message, state, db, days=days)
        return
    except:
        await message.reply(cant_parse_period_message, reply=False)

async def emotion_report(message: Message, state: FSMContext, db: DB,
                         days=None, date_first: date=None, date_second: date=None):
    await db.log_message(message)
    if date_first is not None and date_second is not None:
        emotions = await db.get_emotions_period(message, date_from=date_first, date_to=date_second)
        reply = analytics_start_period_message.format(date_first=date_first, date_second=date_second)
    elif days is not None:
        emotions = await db.get_emotions_last_n_days(message, days)
        reply = analytics_start_days_message.format(days=days)
    else:
        emotions = await db.get_emotions_last_n_days(message)
        reply = analytics_start_message
    user = await db.return_user_if_exist(message)
    hour_diff = user.hour_diff
    for emotion in emotions:
        reply += emotion_template_message.format(emotion=emotion.emotion,
                                                 emotion_ratio=emotion.emotion_ratio,
                                                 timestamp=(emotion.created_at + timedelta(hours=hour_diff)).strftime("%Y-%m-%d %H:%M"))
    await message.reply(reply, reply=False)
    await state.finish()
    await user_start(message=message, state=state, db=db)


def daily_report(dp: Dispatcher):
    dp.register_message_handler(emotion_list_report_variants, commands=["daily_report"], state="*")
    dp.register_message_handler(emotion_list_report_variants, Text(emotions_recap_button), state="*")
    dp.register_message_handler(emotion_list_report_variants, Text(custom_period_button), state=EmotionListReport.report_start)
    dp.register_message_handler(emotion_report_start_days, state=EmotionListReport.report_start)
