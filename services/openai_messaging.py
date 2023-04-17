from .openai_api import generate_openai_result_async


async def get_response_to_emotion(emotion, intensity, trigger_first, trigger_second):
    messages = [
            {"role": "user",
             "content": """Я хочу, чтобы ты вел себя как чуткий, поддерживающий и добрый друг. """
                        """Я напишу тебе свою эмоцию и ее интенсивность по шкале от 1 до 10"""
                        """. Ты должен ответить только """
                        """фразой поддержки, одобрением, успокоением или ободрением."""
                        """Не задавай уточняющих вопросов. Не предлагай продолжить разговор. Говори на Ты"""
                        """. Не давай советов. Не предлагай ничего тебе рассказать."""
                        """ Ты должен говорить по-человечески и не использовать """
                        f"""слово "уровень". Мой запрос: эмоция {emotion}, интенсивность {intensity} """
             },
        ]
    return await generate_openai_result_async(messages)


async def get_response_to_emotion_report(emotion_list, days, sex=None):
    template = f"""Ты - чуткий, поддерживающий и любящий друг. Ты говоришь как друг, а не как ассистент. Я напишу список эмоций твоего друга, их количество и интенсивность по шкале от 1 до 10 за последнее время. Ты должен проэмпатировать чувствам твоего друга и поддержать его в его эмоциях. Не задавай уточняющих вопросов. Не предлагай продолжить разговор. Говори на ты.\n"""+\
    f"""Список эмоций твоего друга за {days} дней:"""
    for i, emotion in emotion_list.iterrows():
        template += f"""\n{emotion.emotion_count} раз {emotion.emotion} на {emotion.emotion_ratio}"""
    messages = [
        {"role": "user",
         "content": template
         },
    ]
    template += '\nОтреагируй на эмоции из списка выше. Не продолжай этот список.'
    print(template)
    resp = await generate_openai_result_async(messages)
    print(resp)
    return resp#await generate_openai_result_async(messages)
