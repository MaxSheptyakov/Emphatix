from models.db_model import SendTypes
from messages.emotion_gather import what_emotion_do_you_feel_message
from messages.emotion_report import start_weekly_report_message
from random import randint
from keyboards.common import create_keyboard, emotions_gather_button, get_weekly_report_button, do_not_want_button, \
    reaction_keyboard


def prepare_push(push):
    user_id = push.user_id
    if push.custom_text is not None:
        push_text = push.custom_text
        keyboard = None
    elif push.send_type == SendTypes.EMOTION_COLLECT:
        push_text = what_emotion_do_you_feel_message[randint(0, len(what_emotion_do_you_feel_message) - 1)]
        # keyboard = reaction_keyboard
        keyboard = create_keyboard([emotions_gather_button, do_not_want_button])
    elif push.send_type == SendTypes.WEEKLY_REPORT:
        push_text = start_weekly_report_message
        keyboard = create_keyboard(get_weekly_report_button)
    else:
        push_text = None
        keyboard = None

    return user_id, push_text, keyboard