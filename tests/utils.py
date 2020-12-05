import nonebot

from nonebot.command import CommandSession, Command
from aiocqhttp import Event as CQEvent


def get_dummy_group_message_session(group_id: int, sender_role: str = None,
                                    sender_id: int = None, message_text: str = '') -> CommandSession:
    command = ''
    args = ''
    if message_text:
        command_args = message_text.split(' ', 1)
        command = command_args[0][1:]
        if len(command_args) > 1:
            args = command_args[1]
    event = CQEvent()
    event['post_type'] = 'message'
    event['message_type'] = 'group'
    event['group_id'] = group_id
    event['user_id'] = sender_id
    event['sender'] = {'role': sender_role}

    return CommandSession(nonebot.NoneBot(), event, Command(name=(command, ), func=lambda x: x,
                                                            only_to_me=False, privileged=False,
                                                            perm_checker_func=lambda x: x,
                                                            session_class=CommandSession),
                          current_arg=args)


def get_dummy_private_message_session(sender_id: int, message_text: str = '') -> CommandSession:
    command = ''
    args = ''
    if message_text:
        command_args = message_text.split(' ', 1)
        command = command_args[0][1:]
        if len(command_args) > 1:
            args = command_args[1]
    event = CQEvent()
    event['post_type'] = 'message'
    event['message_type'] = 'private'
    event['user_id'] = sender_id

    return CommandSession(nonebot.NoneBot(), event, Command(name=(command, ), func=lambda x: x,
                                                            only_to_me=False, privileged=False,
                                                            perm_checker_func=lambda x: x,
                                                            session_class=CommandSession),
                          current_arg=args)
