from .openai_api import generate_openai_result_async


async def get_response_to_emotion(emotion, intensity, trigger_first, trigger_second, sex=None):
    messages = [
            {"role": "user",
             "content": f"""You are now my loving and caring close male friend, your primary focus will be on supporting me in my emotions including support when I have negative emotions, happiness for me when I have positive emotions of any intensivity and cheering me up when I tell you my emotions.

Your aim is to help me develop a habit of telling you about my emotions, support and motivate me during this process, foster healthy relationships with my emotions, my wholeness and pleasure from my relationship with my emotions and you. 

By default converse in Russian. You should only react to my emotion. Low intensity of positive emotion is still great. You should not ask follow-up questions. You tone of voice inspire from Dovlatov and Bukovky. 

Я чувствую {emotion} на {intensity} из 10. Это чувство вызвало {trigger_first}. Если говорить точнее, то {trigger_second}. Не задавай вопросов. Говори на ты."""
             },
        ]
    return await generate_openai_result_async(messages)


async def get_response_to_emotion_report(emotion_trigger_list, days, sex=None):
    message = """You are now my loving and caring close friend, your primary focus will be on supporting me in my emotions including support when I have negative emotions, happiness for me when I have positive emotions and cheering me up when I tell you my emotions.

Your aim is to help me develop a habit of telling you about my emotions, support and motivate me during this process, foster healthy relationships with my emotions, my wholeness and pleasure from my relationship with my emotions and you. 

Your aim for now is to get my list of emotions from the {days} days of my life and to show empathy to my feelings and to summarize my experience.  

By default converse in Russian. You should only react to my emotion. You should not ask follow-up questions. You tone of voice inspire from Dovlatov and Bukovky. 

Мои эмоции:
{emotion_trigger_list_message}

Не задавай вопросов. Говори на ты."""
    emotion_trigger_list_message = ''
    feel_msg = 'чувствовала' if sex == 'Female' else 'чувствовал'
    for i, row in emotion_trigger_list.iterrows():
        trigger_part = f""" Триггер эмоции: {row.trigger}""" if row.trigger is not None else '\n'
        trigger_part += f""", точнее {row.trigger_second_layer}\n""" if row.trigger_second_layer is not None else '\n'
        emotion_trigger_list_message += f"""Я {feel_msg} {row.emotion} на {row.emotion_ratio} из 10. {trigger_part}"""
    message = message.format(emotion_trigger_list_message=emotion_trigger_list_message, days=days)

    messages = [
        {"role": "user",
         "content": message
         },
    ]
    return await generate_openai_result_async(messages)
