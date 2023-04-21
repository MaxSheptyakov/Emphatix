import asyncio
# from aioyookassa.core.client import YooKassa
# from aioyookassa.types import Confirmation
# from aioyookassa.types.payment import PaymentAmount
from config import load_config
from datetime import datetime
from typing import Optional
import aiohttp
import json
from services.common import generate_random_string

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

