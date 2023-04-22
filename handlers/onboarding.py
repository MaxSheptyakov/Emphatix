import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.common import settings_button, home_keyboard
from services.common import work_with_multiple_selection, custom_field_chosen
from services.db_interaction import DB

from keyboards.onboarding import *
from messages.onboarding import *
from services.questionnaire import generate_final_reply_message, set_base_frequency_setup
from states.onboarding import QuestionnaireStates, OnboardingStates
from aiogram.dispatcher.filters import Text

from states.user_start import UserMain
from datetime import datetime

async def onboarding_first_step(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.set_state(OnboardingStates.first)
    await message.reply(onboarding_first_message, reply_markup=onboarding_first_keyboard, reply=False)

async def onboarding_choose_gender(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.set_state(OnboardingStates.gender)
    await message.reply(choose_gender_message, reply_markup=choose_genders, reply=False)

async def how_did_you_know_about_me(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.update_data(sex=message.text)
    await state.set_state(OnboardingStates.how_know_about_me)
    await message.reply(how_did_you_know_about_me_message, reply_markup=ReplyKeyboardRemove(), reply=False)


async def questionnaire_current_time(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.update_data(how_did_you_know_about_us=message.text)
    settings = (message.text == settings_button)
    if message.text == settings_button:
        await state.update_data(settings=True)
    await state.set_state(OnboardingStates.current_time)
    if settings:
        await message.reply(what_is_your_time_message, reply_markup=choose_time_keyboard_with_main, reply=False)
    else:
        await message.reply(what_is_your_time_message, reply_markup=choose_time_keyboard, reply=False)


async def questionnaire_how_many_times_ask(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.update_data(current_time=message.text)
    await state.update_data(server_current_time=str(datetime.now().time()))
    await state.set_state(OnboardingStates.frequency)
    await message.reply(how_often_to_ask_message, reply_markup=choose_frequency_keyboard, reply=False)


async def questionnaire_manual_frequency_choose(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.set_state(OnboardingStates.custom_frequency)
    user_chosen_times = await work_with_multiple_selection(message, available_times, state, 'user_chosen_times')
    if user_chosen_times != '' and user_chosen_times is not None:
        await message.reply(chosen_times_message.format(user_chosen_times), reply_markup=custom_frequency_keyboard,
                            reply=False)
    else:
        await message.reply(choose_time_to_receive_message, reply_markup=custom_frequency_keyboard, reply=False)


async def questionnaire_end_0(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    if message.text in base_setup_buttons:
        await set_base_frequency_setup(message, state)
    if message.text == all_variants_chosen_button and not await custom_field_chosen(state, 'user_chosen_times'):
        await message.reply(choose_at_least_1_variant_message, reply=False)
        await questionnaire_manual_frequency_choose(message, state, db)
        return
    reply_message = await generate_final_reply_message(state)
    await message.reply(reply_message, reply_markup=mark_first_emotion_keyboard, reply=False)
    await db.add_questionnaire_info(message, state)
    await state.finish()



def onboarding(dp: Dispatcher):
    dp.register_message_handler(onboarding_first_step, commands=['onboarding'], state="*")
    dp.register_message_handler(questionnaire_current_time, Text(equals=settings_button), state="*")
    dp.register_message_handler(onboarding_choose_gender, Text(equals=onboarding_first_button),
                                state=OnboardingStates.first)
    dp.register_message_handler(how_did_you_know_about_me, Text(equals=genders),
                                state=OnboardingStates.gender)
    dp.register_message_handler(questionnaire_current_time,
                                state=OnboardingStates.how_know_about_me)
    dp.register_message_handler(questionnaire_how_many_times_ask, Text(equals=available_times),
                                state=OnboardingStates.current_time)
    dp.register_message_handler(questionnaire_manual_frequency_choose, Text(equals=setup_manually_button),
                                state=OnboardingStates.frequency)
    dp.register_message_handler(questionnaire_manual_frequency_choose, Text(equals=available_times),
                                state=OnboardingStates.custom_frequency)
    dp.register_message_handler(questionnaire_end_0, Text(equals=all_variants_chosen_button),
                                state=OnboardingStates.custom_frequency)
    dp.register_message_handler(questionnaire_end_0, Text(equals=base_setup_buttons + [dont_want_to_recieve_button]),
                                state=OnboardingStates.frequency)
    # dp.register_message_handler(onboarding_second_step, Text(equals=onboarding_first_button),
    #                             state=OnboardingStates.first)
