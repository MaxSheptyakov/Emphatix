from aiogram.types import ReplyKeyboardMarkup
from keyboards.common import description_button, questionnaire_button, emotions_gather_button, yes_button, no_button
from localization import _


"""Want to get report"""
get_report_button = _('Получить отчёт')
skip_report_button = _('Пропустить')
want_report_buttons = [skip_report_button, get_report_button]
want_report_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
want_report_keyboard.add(*want_report_buttons)



"""Try to check article"""
try_to_check_article_button = _('Хорошо')
try_to_check_article_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
try_to_check_article_keyboard.add(try_to_check_article_button)


"""Want to get analytics"""

want_to_get_analytics_buttons = [no_button, yes_button]
want_to_get_analytics_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
want_to_get_analytics_keyboard.add(*want_to_get_analytics_buttons)


"""How are you"""
mood_buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
mood_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
mood_keyboard.add(*mood_buttons)


"""Was it hard to identify emotions"""
was_it_hard_to_identify_emotions_buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
was_it_hard_to_identify_emotions_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
was_it_hard_to_identify_emotions_keyboard.add(*was_it_hard_to_identify_emotions_buttons)


"""Did you reply to questions"""
did_you_reply_to_questions_buttons = [yes_button, no_button]
did_you_reply_to_questions_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
did_you_reply_to_questions_keyboard.add(*did_you_reply_to_questions_buttons)


"""Did questions help"""
did_questions_help_buttons = [yes_button, no_button]
did_questions_help_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
did_questions_help_keyboard.add(*did_questions_help_buttons)


"""KPT questions"""
kpt_button = _('Хорошо')
kpt_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
kpt_keyboard.add(kpt_button)