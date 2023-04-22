from localization import _
from aiogram.utils.markdown import text, bold, italic, code, pre

choose_from_keyboard_message = _("""Пожалуйста, выбери вариант из клавиатуры ниже.
При появлении этого сообщения больше 3х раз произойдёт перенаправление в главное меню.""")

main_menu_redirect_message = _("""Перенаправляю тебя в главное меню.""")

bot_thinking_message = _("""⏳""")

evaluate_bot_answer_message = text(italic(_("""Можешь оценить мой ответ с помощью кнопок выше""")))

evaluate_bot_question_message = text(italic(_("""Можешь оценить мой вопрос с помощью кнопок выше""")))