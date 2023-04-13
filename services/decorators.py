import functools
from messages.common import choose_from_keyboard_message


def check_inputs(inputs):
    def decorator(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            if args[0].text not in inputs:
                await args[0].reply(choose_from_keyboard_message)
            else:
                return await func(*args, **kwargs)
        return wrapped
    return decorator


def check_inputs(inputs):
    def decorator(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            if args[0].text not in inputs:
                await args[0].reply(choose_from_keyboard_message)
            else:
                return await func(*args, **kwargs)
        return wrapped
    return decorator