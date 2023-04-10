import asyncio
# from aioyookassa.core.client import YooKassa
# from aioyookassa.types import Confirmation
# from aioyookassa.types.payment import PaymentAmount
from config import load_config
from datetime import datetime
from typing import Optional
import aiohttp
import json
from services.common import generate_random_string, parse_period_from_message

config = load_config('bot.ini')


class NoUserIdException(Exception):
    "No user_id passed to metadata"
    def __init__(self, message="No user_id passed to metadata"):
        self.message = message
        super().__init__(self.message)


class NoPeriodException(Exception):
    "No user_id passed to metadata"
    def __init__(self, message="No period passed to metadata"):
        self.message = message
        super().__init__(self.message)


async def create_payment_yookassa(value, period, metadata):
    if 'user_id' not in metadata:
        raise NoUserIdException

    metadata['period'] = parse_period_from_message(metadata.get('period'))
    async with YooKassa(config.yookassa.token, config.yookassa.shop_id) as client:
        confirmation = Confirmation(type='redirect', return_url='https://t.me/emotional_diary_bot')
        payment = await client.create_payment(amount=PaymentAmount(value=value, currency='RUB'),
                                              description=f'Платёж за Pro версию Emotional Diary Bot. {period}',
                                              confirmation=confirmation,
                                              capture=True,
                                              metadata=metadata)
    return payment


async def get_all_payments(created_at_gte: Optional[datetime] = None, **kwargs):
    if created_at_gte is not None:
        kwargs['created_at.gte'] = created_at_gte if isinstance(created_at_gte, str) \
            else str(created_at_gte.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
    async with YooKassa(config.yookassa.token, config.yookassa.shop_id) as client:
        payments = await client.get_payments(**kwargs)
    return payments


async def get_one_payment(payment_id):
    async with YooKassa(config.yookassa.token, config.yookassa.shop_id) as client:
        payment = await client.get_payment(payment_id)
    return payment


async def cancel_payment(payment_id):
    async with YooKassa(config.yookassa.token, config.yookassa.shop_id) as client:
        payment = await client.cancel_payment(payment_id)
    return payment


async def capture_payment(payment_id):
    async with YooKassa(config.yookassa.token, config.yookassa.shop_id) as client:
        payment = await client.capture_payment(payment_id)
    return payment

async def create_payment_arca(value, period, metadata):
    if 'user_id' not in metadata:
        raise NoUserIdException
    if 'period' not in metadata:
        raise NoPeriodException
    metadata['period'] = parse_period_from_message(metadata.get('period'))
    period = metadata['period']

    async with aiohttp.ClientSession() as session:
        url = f"""https://ipay.arca.am/payment/rest/register.do?userName={config.arca.userName}""" + \
        f"""&password={config.arca.password}&amount={value}&currency=051""" + \
        f"""&language=ru&orderNumber={generate_random_string(5) + str(metadata.get('user_id'))}""" + \
        f"""&returnUrl={config.tg_bot.return_url}&jsonParams={json.dumps(metadata)}""" + \
        f"""&description={f'Pro version of Emotional Diary Bot. {period}'}"""
        async with session.get(url) as resp:
            payment = await resp.json(content_type='text/plain')
    return payment


async def get_one_payment_arca(payment_id):
    url = f"""https://ipay.arca.am/payment/rest/getOrderStatusExtended.do?userName={config.arca.userName}""" + \
        f"""&password={config.arca.password}&orderId={payment_id}"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            payment = await resp.json(content_type='text/plain')
    return payment
