import typing
from aiogram.types import base
from aiogram.utils.payload import prepare_arg, generate_payload
from aiogram.bot.base import api
from aiogram import types
import types as t

import random

async def new_send_message(self,
                           chat_id: typing.Union[base.Integer, base.String],
                           text: base.String,
                           parse_mode: typing.Optional[base.String] = None,
                           entities: typing.Optional[typing.List[types.MessageEntity]] = None,
                           disable_web_page_preview: typing.Optional[base.Boolean] = None,
                           message_thread_id: typing.Optional[base.Integer] = None,
                           disable_notification: typing.Optional[base.Boolean] = None,
                           protect_content: typing.Optional[base.Boolean] = None,
                           reply_to_message_id: typing.Optional[base.Integer] = None,
                           allow_sending_without_reply: typing.Optional[base.Boolean] = None,
                           reply_markup: typing.Union[types.InlineKeyboardMarkup,
                           types.ReplyKeyboardMarkup,
                           types.ReplyKeyboardRemove,
                           types.ForceReply, None] = None,
                           ) -> types.Message:
        """
        Use this method to send text messages.

        Source: https://core.telegram.org/bots/api#sendmessage

        :param chat_id: Unique identifier for the target chat or username of the target channel
        :type chat_id: :obj:`typing.Union[base.Integer, base.String]`

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum
            supergroups only
        :type message_thread_id: :obj:`typing.Optional[base.Integer]`

        :param text: Text of the message to be sent
        :type text: :obj:`base.String`

        :param parse_mode: Send Markdown or HTML, if you want Telegram apps to show bold, italic,
            fixed-width text or inline URLs in your bot's message.
        :type parse_mode: :obj:`typing.Optional[base.String]`

        :param entities: List of special entities that appear in message text,
            which can be specified instead of parse_mode
        :type entities: :obj:`typing.Optional[typing.List[types.MessageEntity]]`

        :param disable_web_page_preview: Disables link previews for links in this message
        :type disable_web_page_preview: :obj:`typing.Optional[base.Boolean]`

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound
        :type disable_notification: :obj:`typing.Optional[base.Boolean]`

        :param protect_content: Protects the contents of sent messages
            from forwarding and saving
        :type protect_content: :obj:`typing.Optional[base.Boolean]`

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type reply_to_message_id: :obj:`typing.Optional[base.Integer]`

        :param allow_sending_without_reply: Pass True, if the message should be sent
            even if the specified replied-to message is not found
        :type allow_sending_without_reply: :obj:`typing.Optional[base.Boolean]`

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard,
            custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user
        :type reply_markup: :obj:`typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply, None]`

        :return: On success, the sent Message is returned
        :rtype: :obj:`types.Message`
        """
        if isinstance(text, str):
            text = text
        elif isinstance(text, list):
            text = text[random.randint(0, len(text) - 1)]
        reply_markup = prepare_arg(reply_markup)
        entities = prepare_arg(entities)
        payload = generate_payload(**locals())
        if self.parse_mode and entities is None:
            payload.setdefault('parse_mode', self.parse_mode)
        if self.disable_web_page_preview:
            payload.setdefault('disable_web_page_preview', self.disable_web_page_preview)
        if self.protect_content is not None:
            payload.setdefault('protect_content', self.protect_content)

        result = await self.request(api.Methods.SEND_MESSAGE, payload)
        return types.Message(**result)