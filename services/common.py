import random
import string
from datetime import datetime, time, date, timedelta
from math import ceil
from keyboards.common import yes_no_keyboard, create_keyboard#, buy_pro_keyboard
from keyboards.emotion_report import weekly_start_keyboard
from messages.emotion_report import start_weekly_report_message
from messages.emotion_gather import what_emotion_do_you_feel_message
from models.db_model import SendTypes
from states.emotion_report import EmotionReport
from states.user_start import UserMain
from states.emotion_gather import EmotionGatherStates
from keyboards.user_start import *
from messages.common import *


def parse_custom_date_period(msg: str):
    date_first, date_second = msg.replace(' ', '').split(':')
    date_first = datetime.strptime(date_first, '%Y-%m-%d').date()
    date_second = datetime.strptime(date_second, '%Y-%m-%d').date()
    return date_first, date_second

async def prepare_message_to_send(message, middleware):
    if message.send_type == SendTypes.EMOTION_COLLECT:
        message.from_id = message.user_id
        message_text = what_emotion_do_you_feel_message
        state = EmotionGatherStates.waiting_for_emotion
        buttons_1, buttons_2 = await middleware.db.get_emotions_sorted_list(message)
        keyboard = create_keyboard(buttons_1, with_main=False, one_time=False, row_width=3)
        # keyboard = first_choose_emotion_keyboard
    elif message.send_type == SendTypes.WEEKLY_REPORT:
        if date.today().isoweekday() == 7 or date.today().isoweekday() == 3:
            message_text = start_weekly_report_message
            state = EmotionReport.weekly_report_start
            keyboard = weekly_start_keyboard
        else:
            message_text = None
            state = None
            keyboard = None
    else:
        message_text = None
        state = None
        keyboard = None
    return message_text, state, keyboard


# async def prepare_premium_message_to_send(premium_type):
#     if premium_type == 'Freemium':
#         message_text = premium_freemium_expiring_message
#         keyboard = buy_pro_keyboard
#         #keyboard = create_keyboard(buttons_1, with_main=False, one_time=False, row_width=3)
#         # keyboard = first_choose_emotion_keyboard
#     else:
#         message_text = premium_expiring_message
#         keyboard = buy_pro_keyboard
#     state = UserMain.on_start
#     return message_text, state, keyboard



async def work_with_multiple_selection(message, available_messages, state, parameter):
    user_data = await state.get_data()
    state_data = user_data.get(parameter) if user_data.get(parameter) is not None else ''
    if message.text in available_messages:
        state_data_list = state_data.split('; ') if len(state_data) > 0 else []
        if message.text not in state_data_list:
            state_data_list.append(message.text)
        else:
            state_data_list.remove(message.text)
        state_data = '; '.join(sorted(state_data_list))
        await state.update_data({parameter: state_data})
    return state_data


async def custom_field_chosen(state, field_name):
    user_data = await state.get_data()
    chosen_times = user_data.get(field_name)
    if chosen_times is not None and chosen_times != '':
        return True
    return False


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=length))


def get_hour_diff(end_time: time, start_time: time):
    return ceil((datetime.combine(date.today(), end_time) -
                 datetime.combine(date.today(), start_time)).total_seconds()/60/60)


def add_hours_to_time(t, hours):
    return (datetime.combine(date.today(), t) + timedelta(hours=hours)).time()


async def check_tries(state):
    data = await state.get_data()
    misses = data.get('n_misses')
    if misses is None:
        misses = 1
    else:
        misses = misses + 1
    await state.update_data(n_misses=misses)
    return misses


def string_to_int(x):
    try:
        return (int(x))
    except:
        return False


class UnknownPaymentVariant(Exception):
    "No user_id passed to metadata"
    def __init__(self, message="Unknown payment variant"):
        self.message = message
        super().__init__(self.message)


def flatten(l):
    res = []
    for x in l:
        if isinstance(x, list):
            res = res + x
        else:
            res.append(x)
    return res


def get_sex_promt_part_ru(sex):
    sex_part = ' Обращайся ко мне в мужском роде.' if sex == 'Мужской' \
        else ' Обращайся ко мне в женском роде' if sex == 'Женский' else ''
    return sex_part