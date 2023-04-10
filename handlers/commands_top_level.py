
from handlers.emotion_list_report import *
from handlers.emotion_gather import *
from handlers.onboarding import *
from handlers.emotion_report import *
from handlers.user_start import *



def top_handler(dp: Dispatcher):
    dp.register_message_handler(emotion_list_report_variants, commands=["daily_report"], state="*")
    dp.register_message_handler(emotion_list_report_variants, Text(emotions_recap_button), state="*")
    dp.register_message_handler(weekly_report, Text(equals=get_weekly_report_button), state="*")
    dp.register_message_handler(emotion_gather_start, Text(equals=emotions_gather_button), state="*")
    dp.register_message_handler(emotion_gather_start, Text(equals=mark_first_emotion_button), state="*")
    dp.register_message_handler(emotion_gather_start, commands=['gather_emotion'], state="*")
    dp.register_message_handler(leave_feedback, Text(equals=feedback_button), state="*")
    dp.register_message_handler(user_start, commands=["start"], state="*")
    #dp.register_message_handler(user_start, callback=main_page_button, state="*")
    dp.register_message_handler(user_stop, commands=['stop'], state='*')
    dp.register_message_handler(user_start, Text(equals=main_page_button), state="*")
    dp.register_message_handler(show_description, Text(equals=description_button), state="*")
    dp.register_message_handler(show_description, commands=['description'], state="*")
    dp.register_message_handler(emotion_report_variants, Text(equals=report_button),
                                state="*")
    dp.register_message_handler(emotion_report_variants, commands=["emotion_report"], state="*")
