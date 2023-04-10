from keyboards.onboarding import *
from messages.onboarding import *


async def generate_final_reply_message(state):
    user_data = await state.get_data()
    user_chosen_times = user_data.get('user_chosen_times').split('; ') if 'user_chosen_times' in user_data else []
    if len(user_chosen_times) > 0:
        reply_message = all_set_chosen_times_message.format(len(user_chosen_times))
    else:
        reply_message = all_set_no_chosen_times_message
    return reply_message


async def set_base_frequency_setup(message, state):
    if message.text == once_a_day_button:
        await state.update_data(user_chosen_times='16:00')
    elif message.text == three_times_a_day_button:
        await state.update_data(user_chosen_times='09:00; 16:00; 21:00')
    elif message.text == once_in_three_hours_button:
        await state.update_data(user_chosen_times='09:00; 12:00; 15:00; 18:00; 21:00')