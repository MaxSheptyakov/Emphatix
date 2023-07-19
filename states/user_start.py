from aiogram.dispatcher.filters.state import StatesGroup, State


class UserMain(StatesGroup):
    on_start = State()
    additional_info = State()
    feedback = State()
    show_report = State()
    buy_pro = State()

class Dialog(StatesGroup):
    dialog_started = State()
