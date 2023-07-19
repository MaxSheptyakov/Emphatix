from aiogram.types import ReplyKeyboardMarkup
from keyboards.common import description_button, questionnaire_button, emotions_gather_button, main_page_button
from localization import _

"""Start Keyboard"""
start_buttons = [description_button, questionnaire_button, emotions_gather_button]
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
start_keyboard.add(*start_buttons)

start_keyboard_no_questionnaire = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard_no_questionnaire.add(questionnaire_button)



