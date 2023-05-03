from keyboards.common import skip_button
from keyboards.emotion_gather import positive_emotion_set, negative_emotion_set
from .common import get_sex_promt_part_ru
from .openai_api import generate_openai_result_async, generate_openai_result_async_return_response


async def get_response_to_emotion(emotion, intensity, trigger_first, trigger_second, sex=None):
    sex_part = get_sex_promt_part_ru(sex)
    trigger_second_part = f', {trigger_second}' if trigger_second != skip_button else ''
    trigger_part = f' Вызвало эмоцию: {trigger_first}{trigger_second_part}.' if trigger_first != skip_button else ''
    messages = [
            {"role": "user",
             "content": f"""You are now world best psychologist as well as my loving and caring close friend, your primary focus will be on supporting me in my emotions including support when I have negative emotions, happiness and cheering for me when I have positive or neutral emotions.

Your aim is to foster healthy relationships with my emotions, my wholeness and pleasure from my relationship with my emotions.
Your tone of voice inspire from Carl Rogers and Martin Seligman. 

Instructions for your first answer are located below, delimited by triple backticks. Each instructions starts from the new row. 
```Start with support for negative emotion, cheer for positive emotion, interest for neutral emotion.
By default converse in Russian.
Try to not give advice.
Do not tell you are sorry. 
If you want to get additional information, use question but not sentence.
От себя говори в мужском роде. 
Обращайся ко мне на ты. 
{sex_part}
Do not greet me.```

Now I will tell you what I feel and what caused this emotion. My request is delimeted by <>.
<Я чувствую {emotion}.{trigger_part}>"""
             },
        ]
    return messages, await generate_openai_result_async_return_response(messages)


async def get_response_to_emotion_report(emotion_trigger_list, days, sex=None):
    sex_part = get_sex_promt_part_ru(sex)
    message = """You are now world best psychologist as well as my loving and caring close friend, your primary focus will be on supporting me in my emotions including support when I have negative emotions, happiness and cheering for me when I have positive or neutral emotions.

Your aim is to foster healthy relationships with my emotions, my wholeness and pleasure from my relationship with my emotions.
Your tone of voice inspire from Carl Rogers and Martin Seligman. 

Instructions for your first answer are located below, delimited by triple backticks. Each instructions starts from the new row. 
```Show empathy to my feelings.
Summarize my experience for the period.
By default converse in Russian.
Try to not give advice.
Do not tell you are sorry. 
If you want to get additional information, use question but not sentence.
От себя говори в мужском роде. 
Обращайся ко мне на ты. 
{sex_part}
Do not greet me.```

Now I will tell you what I felt for the last {days} days and what caused this emotions in the format of "emotion: what caused it". My request is delimeted by <>. 
<{emotion_trigger_list_message}>
"""
    emotion_trigger_list_message = ''
    feel_msg = 'чувствовала' if sex == 'Женский' else 'чувствовал'
    for i, row in emotion_trigger_list.iterrows():
        trigger_second_part = f', {row.trigger_second_layer}' if row.trigger_second_layer != skip_button else ''
        trigger_part = f' Вызвало эмоцию: {row.trigger}{trigger_second_part}.' if row.trigger != skip_button else ''
        # emotion_trigger_list_message += f"""Я {feel_msg} {row.emotion}. {trigger_part}"""
        emotion_trigger_list_message += f"""{row.emotion}: {trigger_part}"""
    message = message.format(emotion_trigger_list_message=emotion_trigger_list_message, days=days, sex_part=sex_part)

    messages = [
        {"role": "user",
         "content": message
         },
    ]
    return messages, await generate_openai_result_async_return_response(messages)


async def run_dialog(messages=None, sex=None):
    sex_part = get_sex_promt_part_ru(sex)
    if messages is None:
        messages = [
                {"role": "user",
                 "content": f"""You are world best psychologist as well as my loving and caring close friend, your primary focus will be on supporting me in my emotions and or decisions including support when I have negative emotions, happiness for me when I have positive emotions and cheering me up when I tell you my emotions. 

Your aim is to help me to share my feelings or problems with you, support and motivate me during this process, foster healthy relationships with my emotions, my wholeness. Lead me in my personal exploration by asking relevant questions which help me to get deeper understanding and explore my emotions. 

By default converse in Russian. От себя говори в мужском роде. Говори на ты.{sex_part} Respond with 75 words or less. Your tone of voice inspire from Carl Rogers and Martin Seligman.

Start conversation with asking what about do I want to talk or what feelings do I want to share."""
                 },
            ]
    return messages, await generate_openai_result_async_return_response(messages)

