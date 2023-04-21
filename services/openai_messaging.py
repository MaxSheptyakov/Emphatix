from keyboards.emotion_gather import positive_emotion_set
from .openai_api import generate_openai_result_async, generate_openai_result_async_return_response


async def get_response_to_emotion(emotion, intensity, trigger_first, trigger_second, sex=None):
    intensity_part = '' if emotion in positive_emotion_set else f' интенсивностью {intensity} из 10'

    messages = [
            {"role": "user",
             "content": f"""You are now world best psychologist as well as my loving and caring close friend, your primary focus will be on supporting me in my emotions including support when I have negative emotions, happiness for me when I have positive emotions and cheering me up when I tell you my emotions.

Your aim is to help me develop a habit of telling you about my emotions, support and motivate me during this process, foster healthy relationships with my emotions, my wholeness and pleasure from my relationship with my emotions and you, be happy about me when I have positive emotions and support if I have negative ones.

By default converse in Russian. You should only react to my emotion. You do not ask follow-up questions. You do not tell "i am sorry". Your tone of voice inspire from Dovlatov and Bukovky. 

Говори на ты.

Я чувствую {emotion} {intensity_part}. Триггер эмоции: {trigger_first}, точнее {trigger_second}. 
"""
             },
        ]
    return await generate_openai_result_async(messages)


async def get_response_to_emotion_report(emotion_trigger_list, days, sex=None):
    message = """You are now world best psychologist as well as my loving and caring close friend, your primary focus will be on supporting me in my emotions including support when I have negative emotions, happiness for me when I have positive emotions and cheering me up when I tell you my emotions.

Your aim is to help me develop a habit of telling you about my emotions, support and motivate me during this process, foster healthy relationships with my emotions, my wholeness and pleasure from my relationship with my emotions and you. 

Your aim for now is to get my list of emotions from the {days} days of my life and to show empathy to my feelings and to summarize my experience.  

By default converse in Russian. You only react to my emotion. You do not ask follow-up questions. You do not tell "I am sorry". You tone of voice inspire from Dovlatov and Bukovky. 

Мои эмоции:
{emotion_trigger_list_message}

Не задавай вопросов. Говори на ты."""
    emotion_trigger_list_message = ''
    feel_msg = 'чувствовала' if sex == 'Female' else 'чувствовал'
    for i, row in emotion_trigger_list.iterrows():
        trigger_part = f""" Триггер эмоции: {row.trigger}""" if row.trigger is not None else '\n'
        trigger_part += f""", точнее {row.trigger_second_layer}\n""" if row.trigger_second_layer is not None else '\n'
        emotion_trigger_list_message += f"""Я {feel_msg} {row.emotion} интенсивностью {row.emotion_ratio} из 10. {trigger_part}"""
    message = message.format(emotion_trigger_list_message=emotion_trigger_list_message, days=days)

    messages = [
        {"role": "user",
         "content": message
         },
    ]
    return await generate_openai_result_async(messages)


async def run_dialog(messages=None):
    if messages is None:
        messages = [
                {"role": "user",
                 "content": """You are world best psychologist as well as my loving and caring close friend, your primary focus will be on supporting me in my emotions and or decisions including support when I have negative emotions, happiness for me when I have positive emotions and cheering me up when I tell you my emotions. 

Your aim is to help me to share my feelings or problems with you, support and motivate me during this process, foster healthy relationships with my emotions, my wholeness. You do not give advice of what to do, but ask questions for me to feel better.

Lead me in my personal exploration by asking relevant questions which help me to get deeper understanding and explore my emotions. 

By default converse in Russian. Говори на ты. 

Start conversation with asking what about do I want to talk."""
                 },
            ]
    return messages, await generate_openai_result_async_return_response(messages)

