import openai
from config import config

openai.api_key = config.openai.token

def _get_ans_from_response(response:openai.openai_object.OpenAIObject) -> str:
    return response['choices'][0]['message']['content']


async def generate_openai_result_async(messages):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo-0301",
        messages=messages,
        max_tokens=1024,
        #stream=True,
        # temperature=0.99
    )
    return _get_ans_from_response(response)