from aiogram.types import ReplyKeyboardMarkup
from keyboards.common import create_keyboard, description_button, questionnaire_button, emotions_gather_button, ok_button, skip_button
from localization import _


"""Report period choose"""
period_buttons = [_('1'), _('3'), _('5'), _('7'), _('14'), _('30')]
custom_period_button = _("Другой период")
period_keyboard = create_keyboard(period_buttons + [custom_period_button], row_width=3, with_main=True, one_time=False)

"""start"""
weekly_start_button = _('Хорошо!')
weekly_start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
weekly_start_keyboard.add(weekly_start_button)


"""Want to get report"""
get_report_button = _('Получить отчёт')
skip_report_button = _('Пропустить')
want_report_buttons = [skip_report_button, get_report_button]
want_report_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
want_report_keyboard.add(*want_report_buttons)


"""wow keyboard"""
wow_button = _("""Вау, интересно""")
wow_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
wow_keyboard.add(wow_button)


"""Event reports start keyboard"""
event_reports_start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
event_reports_start_keyboard.add(skip_button, ok_button)

