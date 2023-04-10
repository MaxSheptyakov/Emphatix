from aiogram.dispatcher.filters.state import StatesGroup, State


class TriggersReport(StatesGroup):
    start_trigger_report = State()
    choose_emotion_for_report = State()
    choose_period_for_report = State()
