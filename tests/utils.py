from graia.application import MessageChain
from graia.application.message.elements.internal import Plain

from bot.message import Message
from bot.adapter import bot


def get_dummy_group_message(group_id: int, sender_role: str = None,
                            sender_id: int = None, message_text: str = '') -> Message:
    command = None
    args = None
    if message_text:
        command, args = bot.parse_command(message_text, ignore_missing_command=True)
    message = Message(
        bot=bot,
        raw_message=MessageChain(__root__=[Plain(message_text)]),
        _type='group',
        message_text=message_text,
        sender_id=sender_id,
        command=command,
        args=args,
        sender_role=sender_role,
        group_id=group_id
    )
    return message


def get_dummy_private_message(sender_id: int, message_text: str = '') -> Message:
    command = None
    args = None
    if message_text:
        command, args = bot.parse_command(message_text, ignore_missing_command=True)
    message = Message(
        bot=bot,
        raw_message=MessageChain(__root__=[Plain(message_text)]),
        _type='private',
        message_text=message_text,
        sender_id=sender_id,
        command=command,
        args=args,
    )
    return message
