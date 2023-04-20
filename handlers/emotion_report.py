from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text, Regexp

from config import config
from messages.common import bot_thinking_message, evaluate_bot_answer_message
from messages.user_start import main_page_message
from services.db_interaction import DB
from services.openai_messaging import get_response_to_emotion_report
from states.emotion_report import EmotionReport
from keyboards.emotion_report import *

from handlers.user_start import user_start
from keyboards.common import *
from messages.emotion_report import *
from visualization.emotion_report import generate_emotion_flower
import os
from datetime import date
from services.common import parse_custom_date_period


async def emotion_report_variants(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.set_state(EmotionReport.show_report)
    if message.text == custom_period_button:
        await message.reply(custom_period_message, reply_markup=ReplyKeyboardRemove(), reply=False)
    else:
        await message.reply(report_choose_message, reply_markup=period_keyboard, reply=False)


async def set_custom_period(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.set_state(EmotionReport.custom_period)
    await message.reply(custom_period_message, reply=False)


async def weekly_start_days(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    try:
        date_first, date_second = parse_custom_date_period(message.text)
        await send_flower(message, state, db, days=None, date_first=date_first, date_second=date_second)
        return
    except:
        pass
    try:
        days = int(message.text)
        await send_flower(message, state, db, days)
        return
    except Exception as e:
        await message.reply(cant_parse_period_message, reply=False)


async def weekly_report(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    days = 7
    await send_flower(message, state, db, days)


async def send_flower(message: Message, state: FSMContext, db: DB, days: int = None,
                      date_first: date = None, date_second: date = None):
    await state.set_state(EmotionReport.flower_sent)
    if days is None and date_second is None and date_first is None:
        days = 7
    emotions = await db.get_emotions_for_flower(message, days, date_first, date_second)

    if len(emotions) == 0:
        await message.reply(you_didnt_select_emotions_message, reply=False)
        await user_start(message=message, state=state, db=db)
        return
    flower = await generate_emotion_flower(emotions, days, date_first, date_second)
    if days is not None:
        await message.reply(days_you_marked_message.format(days=days), reply=False)
    else:
        await message.reply(period_you_marked_message.format(date_first=date_first, date_second=date_second),
                            reply=False)
    if message.from_id in config.tg_bot.beta_users:
        await message.reply_photo(open(flower, 'rb'), reply=False)
        emotion_trigger_list = await db.get_emotions_for_ai_response(message, days, date_first, date_second)
        if date_first is not None and date_second is not None:
            days = (date_second - date_first).days
        user = await db.return_user_if_exist(message)
        sex = None #user.sex
        msg = await message.reply(bot_thinking_message, reply=False)
        ai_reply_text = await get_response_to_emotion_report(emotion_trigger_list, days, sex)
        await msg.delete()
        await message.reply(ai_reply_text, reply_markup=reaction_keyboard, reply=False)
        await message.reply(evaluate_bot_answer_message, reply_markup=home_keyboard, reply=False, parse_mode='MarkdownV2')
    else:
        await message.reply_photo(open(flower, 'rb'), reply_markup=home_keyboard, reply=False)
    try:
        os.remove(flower)
    except:
        pass
    await state.finish()


def weekly_report_dp(dp: Dispatcher):
    dp.register_message_handler(emotion_report_variants, commands=["emotion_report"], state="*")
    dp.register_message_handler(weekly_report, Text(equals=get_weekly_report_button), state="*")
    dp.register_message_handler(emotion_report_variants, Text(equals=report_button), state="*")
    dp.register_message_handler(emotion_report_variants, Text(equals=custom_period_button),
                                state=EmotionReport.show_report)
    dp.register_message_handler(weekly_start_days, Regexp(regexp='\d+'), state=EmotionReport.show_report)

    dp.register_message_handler(send_flower, Text(equals=yes_button),
                                state=EmotionReport.weekly_report_start_with_emotions)


