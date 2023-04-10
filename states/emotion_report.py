from aiogram.dispatcher.filters.state import StatesGroup, State


class EmotionReport(StatesGroup):
    show_report = State()
    custom_period = State()
    weekly_report_start = State()
    weekly_report_start_with_emotions = State()
    weekly_report_start_no_emotions = State()
    flower_sent = State()
    top_3 = State()
    question_for_emotions = State()
    question_for_emotions_handle = State()
    paid_version = State()
    odd_week_questions_recognize = State()
    odd_week_questions_call = State()
    odd_week_questions_describe = State()
    even_week_questions_start = State()
    even_week_questions_recognize = State()
    even_week_questions_call = State()
    even_week_questions_describe = State()
    how_do_you_feel = State()
