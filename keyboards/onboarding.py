from localization import _
from keyboards.common import create_keyboard#, try_pro_button
from keyboards.common import main_page_button, quantity_buttons
from aiogram.types import ReplyKeyboardMarkup


onboarding_first_button = _("Интересно")
onboarding_first_keyboard = create_keyboard(onboarding_first_button, with_main=False, row_width=1, one_time=False,
                                            with_back_button=False)

onboarding_second_button = _("Да, это правда")
onboarding_second_keyboard = create_keyboard(onboarding_second_button, with_main=False, row_width=1, one_time=False,
                                            with_back_button=False)

onboarding_third_button = _("""Отлично 👌""")
onboarding_third_keyboard = create_keyboard(onboarding_third_button, with_main=False, row_width=1, one_time=False,
                                            with_back_button=False)
#
# try_free_button = _('Попробовать бесплатную версию')
# onboarding_forth_keyboard = create_keyboard([try_free_button, try_pro_button], with_main=False, row_width=1,
#                                           one_time=False, with_back_button=False)

thanks_button = _("Спасибо 🙏")
thanks_keyboard = create_keyboard([thanks_button], with_main=False, row_width=1, one_time=False, with_back_button=False)

continue_onboarding_button = _('Продолжить онбординг')


'''Choose genders'''
choose_genders = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
genders = [_("Мужской"),_("Женский"),_("Неопределенный"),_("Трансгендерный"),_("Бигендерный"),
           _("Гендерфлюидный"),_("Небинарный"),_("Андрогинный")]

choose_genders.add(*genders)




"""Choose time for questionnaire keyboard"""
choose_time_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=6)
available_times = ['00', '01', '02', '03', '04', '05', '06', '07', '08',
           '09', '10', '11', '12', '13', '14', '15', '16', '17',
           '18', '19', '20', '21', '22', '23',
           ]
choose_time_keyboard.add(*available_times)
choose_time_keyboard_with_main = ReplyKeyboardMarkup(resize_keyboard=True, row_width=6)
choose_time_keyboard_with_main.add(*available_times)
choose_time_keyboard_with_main.add(main_page_button)

"""Choose frequency of asking"""
setup_manually_button = _('Настроить вручную')
dont_want_to_recieve_button = _('Я буду отмечать эмоции самостоятельно')
once_a_day_button = _('Раз в день')
three_times_a_day_button = _('3 раза в день')
once_in_three_hours_button = _('Раз в 3 часа в течение дня')
base_setup_buttons = [once_a_day_button, three_times_a_day_button, once_in_three_hours_button]
choose_frequency_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
choose_frequency_buttons = base_setup_buttons + [dont_want_to_recieve_button, setup_manually_button]
choose_frequency_keyboard.row(*choose_frequency_buttons[:-2])
choose_frequency_keyboard.row(*choose_frequency_buttons[-2:])


"""Custom frequency"""
all_variants_chosen_button = _('Всё выбрано')
custom_frequency_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=6)
custom_frequency_keyboard.add(*available_times)
custom_frequency_keyboard.row(all_variants_chosen_button)


"""Additional Questions"""
skip_button = _('Пропустить')
reply_to_additional_questions_button = _('Хорошо')
additional_questions_buttons = [skip_button, reply_to_additional_questions_button]
additional_questions_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
additional_questions_keyboard.add(*additional_questions_buttons)


"""Choose sex"""
choose_sex_buttons = [_('Мужской'), _('Женский'), _('Другое'), skip_button]
choose_sex_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
choose_sex_keyboard.add(*choose_sex_buttons)


"""Choose age"""
choose_age_buttons = ['>18', '19-21', '22-25', '26-30', '31-35', '35-40', '41-50', '>51', skip_button]
choose_age_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
choose_age_keyboard.add(*choose_age_buttons[:-1])
choose_age_keyboard.add(*choose_age_buttons[-1:])


#
# """Want to read about emotions"""
# want_to_read_buttons = [_('Да, хочу'), _('Нет, не хочу')]
# want_to_read_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
# want_to_read_keyboard.add(*want_to_read_buttons)


"""Questionnaire ended"""
mark_first_emotion_button = _('✨Отметить первую эмоцию')
mark_first_emotion_keyboard = create_keyboard(mark_first_emotion_button, with_main=False, row_width=1, one_time=False,
                                       with_back_button=False)


