from aiogram.dispatcher.filters.state import StatesGroup, State


class OnboardingStates(StatesGroup):
    current_time = State()
    gender = State()
    frequency = State()
    custom_frequency = State()
    on_start = State()
    fifth = State()
    first = State()
    second = State()
    third = State()
    forth = State()
    how_know_about_me = State()
    psychiatrist = State()
    sixth = State()
    seventh = State()
    e = State()
    buy_pro = State()


class QuestionnaireStates(StatesGroup):
    waiting_for_time = State()
    waiting_for_frequency = State()
    waiting_for_selecting_custom_frequency = State()
    waiting_for_fill_data_request = State()
    waiting_for_psych_difficulties = State()
    waiting_for_psych_disorders = State()
    waiting_for_hard_to_diff_emotions = State()
    waiting_for_sad_dont_upderstand_emotions = State()
    attention_gather = State()
    clarity_gather = State()
    communication_gather = State()
    waiting_for_last_messages_clickthrough0 = State()
    waiting_for_last_messages_clickthrough1 = State()
    waiting_for_last_messages_clickthrough2 = State()
    waiting_for_last_messages_clickthrough3 = State()
    waiting_for_choose_sex = State()
    waiting_for_choose_age = State()
    waiting_for_read_emotions_set = State()
    all_done = State()
    #NOT_FILLED_QUESTIONNAIRE = State()
    #SOME_STATE = State()
