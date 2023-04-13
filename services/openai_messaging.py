from .openai_api import generate_openai_result_async


async def get_response_to_emotion(emotion, intensity, trigger_first, trigger_second):
    messages = [
            {"role": "user",
             "content": """Я хочу, чтобы ты вел себя как чуткий, поддерживающий и добрый друг. """
                        """Я напишу тебе свою эмоцию и ее интенсивность по шкале от 1 до 10, и может быть триггер, """
                        """который вызвал эту эмоцию. Ты должен ответить только """
                        """фразой поддержки, советом или ободрением в зависимости от ситуации, и ничем другим. """
                        """Не задавай уточняющих вопросов, не предлагай поговорить об этом"""
                        """. Ты должен говорить по-человечески и не использовать """
                        f"""слово "уровень". Мой запрос: эмоция {emotion}, интенсивность {intensity} """+
                        (f""", триггер {trigger_first}, а точнее {trigger_second}.""" if trigger_first is not None
                                                                                         and trigger_second is not None
                         else '.')},
        ]
    return await generate_openai_result_async(messages)