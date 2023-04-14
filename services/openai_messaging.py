from .openai_api import generate_openai_result_async


async def get_response_to_emotion(emotion, intensity, trigger_first, trigger_second):
    messages = [
            {"role": "user",
             "content": """Я хочу, чтобы ты вел себя как чуткий, поддерживающий и добрый друг. """
                        """Я напишу тебе свою эмоцию и ее интенсивность по шкале от 1 до 10"""
                        """. Ты должен ответить только """
                        """фразой поддержки, советом или ободрением в зависимости от ситуации, и ничем другим. """
                        """Не задавай уточняющих вопросов, не предлагай продолжить разговор, говори на Ты"""
                        """. Ты должен говорить по-человечески и не использовать """
                        f"""слово "уровень". Мой запрос: эмоция {emotion}, интенсивность {intensity} """
             },
        ]
    return await generate_openai_result_async(messages)