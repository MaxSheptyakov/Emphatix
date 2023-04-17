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
    if emotion_list.shape[0] > 3:
        template = f"""Ты - чуткий, поддерживающий и любящий друг. Ты говоришь как друг, а не как ассистент. Я напишу список своих, их количество и интенсивность за последнее время.\n"""+\
        f"""Список моих эмоций за {days} дней:"""
        for i, emotion in emotion_list.iterrows():
            template += f"""\n{emotion.emotion_count} раз {emotion.emotion} на {emotion.emotion_ratio} из 10"""
        template += '\n\nПроэмпатируй моим чувствам и поддержи меня. Не задавай уточняющих вопросов. Не предлагай продолжить разговор. Говори на ты.'
    else:
        template = f"""Ты - чуткий, поддерживающий и любящий друг. Ты говоришь как друг, а не как ассистент. За последнее время я чувствовал \n"""
        for i, emotion in emotion_list.iterrows():
            if i != 0:
                template += ', '
            template += f"""{emotion.emotion_count} раз {emotion.emotion} на {emotion.emotion_ratio} из 10"""
        template += ". Проэмпатируй моим чувствам и поддержи меня. Не задавай уточняющих вопросов. Не предлагай продолжить разговор. Говори на ты."
    messages = [
        {"role": "user",
         "content": template
         },
    ]
    resp = await generate_openai_result_async(messages)
    return resp#await generate_openai_result_async(messages)
