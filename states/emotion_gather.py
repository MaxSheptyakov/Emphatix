from aiogram.dispatcher.filters.state import StatesGroup, State


class EmotionGatherStates(StatesGroup):
    waiting_for_emotion = State()
    waiting_for_emotion_pt2 = State()
    write_own_emotion_state = State()
    waiting_for_intensity = State()
    waiting_for_intensity_finish = State()
    waiting_for_read_more = State()
    exersice = State()
    exersice_finish = State()
    all_done = State()
    triggers_start = State()
    triggers_second_layer = State()
    gather_finish = State()
    meditation = State()
    try_pro = State()
    gather_finish_no_premium = State()
    functions_description = State()