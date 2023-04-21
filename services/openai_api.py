import openai
from config import config

openai.api_key = config.openai.token

def get_ans_from_response(response:openai.openai_object.OpenAIObject) -> str:
    return response['choices'][0]['message']['content']

def get_msg_from_response(response:openai.openai_object.OpenAIObject) -> str:
    return response['choices'][0]['message']

def get_msg_text_from_msg(msg):
    return msg['content']

def get_total_tokens(response:openai.openai_object.OpenAIObject) -> int:
    return response.usage.total_tokens




async def generate_openai_result_async(messages):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo-0301",
        messages=messages,
        # max_tokens=1024,
        #stream=True,
        # temperature=0.99
    )
    return get_ans_from_response(response)


def generate_openai_result_sync(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=messages,
        # max_tokens=1024,
        #stream=True,
        # temperature=0.99
    )
    return response
    # return _get_ans_from_response(response)


async def generate_openai_result_async_return_response(messages):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo-0301",
        messages=messages,
        # max_tokens=1024,
        #stream=True,
        # temperature=0.99
    )
    return response

