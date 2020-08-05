from message import Message
from adapter import bot


def get_dummy_group_message(group_id: int, sender_role: str = None,
                            sender_id: int = None, message_text: str = None) -> Message:
    command = None
    args = None
    if message_text:
        command, args = bot.parse_command(message_text, ignore_missing_command=True)
    message = Message(
        bot=bot,
        _type='group',
        message_text=message_text,
        command=command,
        args=args,
        sender_id=sender_id,
        sender_role=sender_role,
        group_id=group_id
    )
    return message


def get_dummy_private_message(sender_id: int, message_text: str = None) -> Message:
    command = None
    args = None
    if message_text:
        command, args = bot.parse_command(message_text, ignore_missing_command=True)
    message = Message(
        bot=bot,
        _type='private',
        message_text=message_text,
        command=command,
        args=args,
        sender_id=sender_id,
    )
    return message
