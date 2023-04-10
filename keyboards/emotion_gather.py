from keyboards.common import create_keyboard, main_page_button, skip_button, create_keyboard, back_button
from localization import _

dont_know_button = _('Не знаю')

"""New emotion choose buttons"""

show_more_emotions_button = _('Покажи еще')
first_emotion_list = emotions = [
    _("Радость"),
    _("Грусть"),
    _("Страх"),
    _("Тревога"),
    _("Интерес"),
    _('Безмятежность'),
    _("Ярость"),
    _("Предвкушение"),
    _("Удивление"),
    _("Стыд"),
    _("Счастье"),
    _("Восхищение"),
    _("Разочарование"),
]
first_emotions_buttons =  first_emotion_list + [show_more_emotions_button]

write_own_emotion_button = _('Напишу свою')
second_emotion_list = [_("Безразличие"),
    _("Беспокойство"),
    _("Сожаление"),
    _("Ненависть"),
    _("Злость"),
    _("Отчаяние"),
    _("Облегчение"),
    _("Надежда"),
    _("Симпатия"),
    _("Ревность"),
    _("Самодовольство")]
second_emotions_buttons = [write_own_emotion_button, back_button]

positive_emotions = [
    _("Радость"),
    _("Счастье"),
    _("Восхищение"),
    _("Облегчение"),
    _("Надежда"),
    _("Симпатия"),
    _("Самодовольство"),
    _("Интерес"),
    _("Предвкушение"),
]
positive_emotion_set = set(positive_emotions)

negative_emotion_set = (set(first_emotion_list) | set(second_emotion_list)) - positive_emotion_set


"""Choose intensity keyboard"""
low_intensity_buttons = ['1', '2', '3', '4']
mid_intensity_buttons = ['5', '6']
high_intensity_buttons = ['7', '8', '9', '10']
dont_know_intensity_buttons = [dont_know_button]
intensity_buttons = low_intensity_buttons + mid_intensity_buttons + high_intensity_buttons + dont_know_intensity_buttons
choose_intensity_keyboard = create_keyboard(intensity_buttons, row_width=5)


"""Triggers keyboard"""
triggers_dict = {
    _("Межличностные отношения"): (
        _("Близкие люди"),
        _("Друзья"),
        _("Коллеги"),
        _("Незнакомые люди"),
        _("Общение в Интернете"),
    ),
    _("Работа и учеба"): (
        _("Офис"),
        _("Удалённая работа"),
        _("Школа/Университет"),
    ),
    _("Домашние дела"): (
        _("Уборка"),
        _("Ремонт"),
    ),
    _("Финансы"): (
        _("Покупки"),
        _("Инвестиции"),
        _("Работа и бизнес"),
        _("Сбережения"),
    ),
    _("Здоровье"): (
        _("Спорт"),
        _("Питание"),
        _("Сон и отдых"),
    ),
    _("События"): (
        _("Праздники"),
        _("Мероприятия"),
        _("Путешествия"),
        _("Экстренные ситуации"),
    ),
    _("Искусство и культура"): (
        _("Кино"),
        _("Музыка"),
        _("Искусство"),
        _("Литература"),
        _("Театр"),
        _("Выставки и музеи"),
    ),
    _("Технологии и наука"): (
        _("Научные открытия"),
        _("Технические новинки"),
        _("Программирование"),
        _("Компьютерные игры"),
        _("Интернет и социальные сети"),
    ),
    _("Еда и напитки"): (
        _("Рестораны"),
        _("Кулинария"),
        _("Алкоголь"),
        _("Вкус еды"),
    ),
    _("Рутина"): (
        _("Учёба"),
        _("Работа"),
        _("Уборка"),
    ),
}


triggers_start_gather_buttons = list(triggers_dict.keys())