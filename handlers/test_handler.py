from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from services.db_interaction import DB
from aiogram.dispatcher.filters.state import StatesGroup, State

keyboard = types.InlineKeyboardMarkup()
btns = ['a', 'b', 'c']
button1 = types.InlineKeyboardButton(text='a', callback_data='a')
button2 = types.InlineKeyboardButton(text='b', callback_data='b')
button3 = types.InlineKeyboardButton(text='c', callback_data='c')
keyboard.add(button1, button2, button3)

async def button_callback_handler(query: types.CallbackQuery):
    print(1)
    # Get the current state of the button
    current_state = query.data.split(':')[1]

    # Invert the state of the button
    new_state = "checked_in" if current_state == "checked_out" else "checked_out"

    # Generate the new inline keyboard markup
    inline_kb = InlineKeyboardMarkup(row_width=3)
    button1_text = "Checked In" if new_state == "checked_in" else "Check In"
    button1_callback_data = f"checkinout:{new_state}"
    button1 = InlineKeyboardButton(text=button1_text, callback_data=button1_callback_data)
    inline_kb.add(button1)

    button2_text = "Checked In" if new_state == "checked_in" else "Check In"
    button2_callback_data = f"checkinout:{new_state}"
    button2 = InlineKeyboardButton(text=button2_text, callback_data=button2_callback_data)
    inline_kb.add(button2)

    button3_text = "Checked In" if new_state == "checked_in" else "Check In"
    button3_callback_data = f"checkinout:{new_state}"
    button3 = InlineKeyboardButton(text=button3_text, callback_data=button3_callback_data)
    inline_kb.add(button3)

    # Update the message with the new inline keyboard markup
    await query.message.edit_reply_markup(reply_markup=inline_kb)


async def test_handle(message: Message, state: FSMContext, db: DB):
    inline_kb = InlineKeyboardMarkup(row_width=3)

    # Define the initial state of the buttons as "checked_out"
    button1_text = "Check In"
    button1_callback_data = "checkinout:checked_out"
    button1 = InlineKeyboardButton(text=button1_text, callback_data=button1_callback_data)
    inline_kb.add(button1)

    button2_text = "Check In"
    button2_callback_data = "checkinout:checked_out"
    button2 = InlineKeyboardButton(text=button2_text, callback_data=button2_callback_data)
    inline_kb.add(button2)

    button3_text = "Check In"
    button3_callback_data = "checkinout:checked_out"
    button3 = InlineKeyboardButton(text=button3_text, callback_data=button3_callback_data)
    inline_kb.add(button3)

    await message.answer("Please check in or check out using the buttons below:", reply_markup=inline_kb)


def test_handler(dp: Dispatcher):
    pass
    # dp.register_message_handler(test_handle, commands=['test'], state="*")
    # dp.register_message_handler(test_handle, Text(equals='test'), state = "*")
    # dp.register_callback_query_handler(button_callback_handler, state = "*")