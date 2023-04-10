from aiogram.dispatcher.filters.state import StatesGroup, State


class EmotionListReport(StatesGroup):
    report_start = State()
    daily_report_start = State()
    hard_to_diff_emotions = State()
    mood = State()
    not_sending_emotions = State()
    emotions_report_read = State()
    was_hard_to_identify_emotion = State()
    had_intense_emotions = State()
    questions_helped = State()
    kpt_questions = State()
