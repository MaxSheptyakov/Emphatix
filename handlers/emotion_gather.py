import json

from aiogram import Dispatcher, types
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from messages.common import bot_thinking_message, evaluate_bot_answer_message
from messages.user_start import main_page_message
from services.db_interaction import DB
from services.openai_api import get_ans_from_response, get_msg_from_response

from states.emotion_gather import EmotionGatherStates

from keyboards.emotion_gather import *

from messages.emotion_gather import *

from keyboards.common import *
from keyboards.onboarding import mark_first_emotion_button
from config import config

from services.openai_messaging import get_response_to_emotion


async def emotion_gather_start(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    user = await db.return_user_if_exist(message)
    if not user.completed_questionnaire:
        from handlers.onboarding import onboarding_first_step
        await onboarding_first_step(message=message, state=state, db=db)
        return
    await state.set_state(EmotionGatherStates.waiting_for_emotion)
    async with state.proxy() as data:
        if data.get('premium') is None:
            data['premium'] = await db.has_user_premium(message)
        if data.get('emotions_list_first') is None:
            emotions_list_first, emotions_list_second = await db.get_emotions_sorted_list(message)
            data['emotions_list_first'] = emotions_list_first
            data['emotions_list_second'] = emotions_list_second
    if message.text == show_more_emotions_button:
        keyboard = create_keyboard(data.get('emotions_list_second'), with_main=True, one_time=True, row_width=3)
        await message.reply(what_emotion_do_you_feel_pt2_message, reply_markup=keyboard,
                            reply=False)
    else:
        keyboard = create_keyboard(data.get('emotions_list_first'), with_main=True, one_time=True, row_width=3)
        if message.text == back_button:
            await message.reply(first_emotion_list_again_message, reply_markup=keyboard, reply=False)
            return
        await message.reply(choose_emotion_message, reply_markup=keyboard, reply=False)


async def write_own_emotion(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await message.reply(write_own_emotion_message, reply_markup=ReplyKeyboardRemove(), reply=False)
    await state.set_state(EmotionGatherStates.write_own_emotion_state)


async def intensity_gather_start(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.set_state(EmotionGatherStates.waiting_for_intensity)
    await state.update_data(user_emotion=message.text)
    if message.text != dont_know_button:
        await message.reply(which_intensity_message.format(emotion=message.text),
                            reply_markup=choose_intensity_keyboard, reply=False)
    else:
        await message.reply(which_intensity_unknown_emotion_message,
                            reply_markup=choose_intensity_keyboard, reply=False)



async def intensity_gather_finish(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.update_data(emotion_intensity=message.text)
    emotion = await db.write_emotion_info(message, state)
    await state.set_state(EmotionGatherStates.waiting_for_intensity_finish)
    await state.update_data(user_emotion_id=emotion.user_emotion_id)
    await trigger_gather_start(message, state, db)



async def trigger_gather_start(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.set_state(EmotionGatherStates.triggers_start)
    if message.text == add_variant_button:
        await message.reply(triggers_new_variant_message, reply=False)
        return
    triggers_list = await db.get_triggers_sorted_list(message)
    keyboard = create_keyboard(triggers_list, row_width=2, with_add_variant=True, with_skip=True,
                               with_dont_know=True if dont_know_button not in triggers_list else False, one_time=True)
    await message.reply(triggers_start_gather_message, reply_markup=keyboard, reply=False)


async def trigger_gather_second_layer(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    await state.set_state(EmotionGatherStates.triggers_second_layer)
    trigger = message.text
    if trigger == add_variant_button:
        await message.reply(triggers_new_variant_message, reply=False)
        return
    await state.update_data(trigger=trigger)
    if trigger in triggers_dict:
        trigger_buttons = await db.get_triggers_second_layer_sorted_list(message)
        keyboard = create_keyboard(trigger_buttons, row_width=2, with_back_button=True, with_skip=True,
                                   with_add_variant=True, one_time=True)
        await message.reply(triggers_second_layer_message, reply_markup=keyboard, reply=False)
        return
    else:
        await trigger_gather_finish(message, state, db, False)
        return


async def trigger_gather_finish(message: Message, state: FSMContext, db: DB, is_from_second=True):
    await db.log_message(message)
    await state.update_data(trigger_second_layer=message.text if is_from_second else None)
    await db.store_trigger(message, state)
    await emotion_gather_finish(message, state, db)


async def emotion_gather_finish(message: Message, state: FSMContext, db: DB):
    await db.log_message(message)
    user = await db.return_user_if_exist(message)
    await state.set_state(EmotionGatherStates.gather_finish)
    data = await state.get_data()
    emotion = data.get('user_emotion')
    intensity = data.get('emotion_intensity')
    trigger_first = data.get('trigger')
    trigger_second = data.get('trigger_second_layer')
    if emotion is not None and intensity is not None:
        m = await message.reply(bot_thinking_message, reply=False)
        messages, response = await get_response_to_emotion(emotion=emotion, intensity=intensity, trigger_first=trigger_first,
                                                   trigger_second=trigger_second, sex=user.sex)
        reply_text = get_ans_from_response(response)
        dialog_messages = messages + [get_msg_from_response(response)]
        await m.delete()
        await message.reply(reply_text, reply_markup=reaction_keyboard, reply=False)
        await state.update_data(dialog_messages=json.dumps(dialog_messages))
        await message.reply(evaluate_bot_answer_message, reply_markup=home_keyboard, reply=False, parse_mode='MarkdownV2')
    else:
        reply_text = finish_positive_med_high_intensity_message
        await message.reply(reply_text, reply_markup=home_keyboard, reply=False)





def emotions_gather(dp: Dispatcher):
    dp.register_message_handler(emotion_gather_start, Text(equals=emotions_gather_button), state="*")
    dp.register_message_handler(emotion_gather_start, Text(equals=mark_first_emotion_button), state="*")
    dp.register_message_handler(emotion_gather_start, commands=['emotion'], state="*")
    dp.register_message_handler(emotion_gather_start, Text(equals=show_more_emotions_button),
                                state=EmotionGatherStates.waiting_for_emotion)
    dp.register_message_handler(write_own_emotion, Text(equals=write_own_emotion_button),
                                state=EmotionGatherStates.waiting_for_emotion)
    dp.register_message_handler(emotion_gather_start, Text(equals=back_button),
                                state=EmotionGatherStates.waiting_for_emotion)

    dp.register_message_handler(intensity_gather_start,
                                state=EmotionGatherStates.waiting_for_emotion)
    dp.register_message_handler(intensity_gather_start,
                                state=EmotionGatherStates.write_own_emotion_state)

    dp.register_message_handler(intensity_gather_finish, Text(equals=intensity_buttons + dont_know_intensity_buttons),
                                state=EmotionGatherStates.waiting_for_intensity)


    dp.register_message_handler(trigger_gather_start, Text(equals=add_variant_button),
                                state=EmotionGatherStates.triggers_start)
    dp.register_message_handler(emotion_gather_finish, Text(equals=skip_button),
                                state=EmotionGatherStates.triggers_start)
    dp.register_message_handler(trigger_gather_second_layer, Text(equals=add_variant_button),
                                state=EmotionGatherStates.triggers_second_layer)
    dp.register_message_handler(trigger_gather_second_layer,
                                state=EmotionGatherStates.triggers_start)
    dp.register_message_handler(trigger_gather_start, Text(equals=back_button),
                                state=EmotionGatherStates.triggers_second_layer)


    dp.register_message_handler(trigger_gather_finish,
                                state=EmotionGatherStates.triggers_second_layer)
