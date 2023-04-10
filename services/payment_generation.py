from aiogram.types import Message
from payments.work_with_payment_api import create_payment_yookassa, create_payment_arca
from keyboards.user_start import *
from services.db_interaction import *
from services.common import *


async def create_payment_link(message: Message, db: DB):
    userid = message.from_id
    period = parse_period_from_message(message.text)
    value = parse_amount_from_message(message.text)
    metadata = {'user_id': userid, 'period': period}
    if message.text in russian_payment_buttons:
        payment = await create_payment_yookassa(value=value, period=period, metadata=metadata)
        await db.add_payment_yookassa(payment, userid=userid)
        return payment.confirmation.url
    elif message.text in foreign_payment_buttons: ## in Drams
        payment = await create_payment_arca(value=value, period=period, metadata=metadata)
        await db.add_payment_arca(payment, userid=userid)
        return payment.get('formUrl')
