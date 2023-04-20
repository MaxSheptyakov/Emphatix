from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from localization import _

def create_keyboard(buttons, row_width=1, with_main=False, with_back_button=False, one_time=False, with_skip=False,
                    with_add_variant=False, with_dont_know=False, resize_keyboard=True):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, row_width=row_width, one_time_keyboard=one_time)
    buttons = buttons if isinstance(buttons, list) else [buttons]
    if with_dont_know:
        buttons.append(dont_know_button)
    if with_add_variant:
        buttons.append(add_variant_button)
    if with_back_button:
        buttons.append(back_button)
    if with_skip:
        buttons.append(skip_button)
    if with_main:
        buttons.append(main_page_button)
    if isinstance(buttons, list):
        keyboard.add(*buttons)
    else:
        keyboard.add(buttons)
    return keyboard

"""Home keyboard"""
main_page_button = _('🏠На главную')
description_button = _('🤖О боте')
questionnaire_button = _('📝Анкета')
settings_button = _('⚙️Настройка уведомлений')
emotions_gather_button = _('✅️Отметить эмоцию')
emotions_gather_old_button = _('✔️Отметить эмоцию')
do_not_want_button = _('🚫Сейчас не хочу')

emotions_recap_button = _("📄Список эмоций за период")
report_button = _("📈Отчёт по эмоциям")
triggers_report_button = _('⭕Отчёт по триггерам')
feedback_button = _('💬Оставить фидбек')
get_weekly_report_button = _("📊Получить отчёт за неделю")

back_button = _('↩️Назад')
skip_button = _('⏭️Пропустить')
ok_button = _("👌Хорошо")
continue_button = _("➡️Продолжить")
add_variant_button = _("Добавить свой вариант")
dont_know_button = _('Не знаю')

# buy_pro_button = _("🗝️Купить PRO версию")
# try_pro_button = _('🗝️Попробовать PRO версию')

home_buttons = [emotions_gather_button, report_button,
                  emotions_recap_button, triggers_report_button,
                  description_button, settings_button, feedback_button]
home_keyboard = create_keyboard(home_buttons, row_width=2)


"""Quantity keyboard"""
quantity_buttons = [_('Всегда'), _('В большинстве случаев'), _("Иногда"), _('Редко'), _('Никогда')]
quantity_keyboard = create_keyboard(quantity_buttons)


"""Yes no keyboard"""
yes_button = _('Да')
no_button = _('Нет')
yes_no_buttons = [no_button, yes_button]
yes_no_keyboard = create_keyboard(yes_no_buttons)



"""1-10 rating keyboard"""
rating_buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
rating_keyboard = create_keyboard(rating_buttons, row_width=5)


"""1-10 intencity keyboard"""
intensity_buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
intensity_keyboard = create_keyboard(intensity_buttons, row_width=5)


def create_inline_button(x, default_callback=None):
    if default_callback is not None:
        return InlineKeyboardButton(x, callback_data=f"{default_callback}:{x}")
    return InlineKeyboardButton(x, callback_data=f"{x}")

def create_inline_keyboard(buttons, row_width=1, with_main=False, with_back_button=False, one_time=False, with_skip=False,
                    with_add_variant=False, with_dont_know=False, resize_keyboard=True, default_callback_part=None):
    keyboard = InlineKeyboardMarkup(resize_keyboard=resize_keyboard, row_width=row_width, one_time_keyboard=one_time)
    buttons = [create_inline_button(x, default_callback_part)
               for x in (buttons if isinstance(buttons, list) else [buttons])]
    if with_dont_know:
        buttons.append(create_inline_button(dont_know_button, default_callback_part))
    if with_add_variant:
        buttons.append(create_inline_button(add_variant_button, default_callback_part))
    if with_back_button:
        buttons.append(create_inline_button(back_button, default_callback_part))
    if with_skip:
        buttons.append(create_inline_button(skip_button, default_callback_part))
    if with_main:
        buttons.append(create_inline_button(main_page_button, default_callback_part))
    if isinstance(buttons, list):
        keyboard.add(*buttons)
    else:
        keyboard.add(buttons)
    return keyboard


reaction_buttons = [_('🤗'), _('❤️'), _('😐'), _('⛔'), ]
reaction_keyboard = create_inline_keyboard(reaction_buttons, row_width=4)
