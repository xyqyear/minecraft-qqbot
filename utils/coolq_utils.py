from nonebot import CommandSession


def get_detail_type(session: CommandSession):
    return session.event.detail_type


def get_sender(session: CommandSession):
    return session.event.sender


def get_sender_id(session: CommandSession):
    return get_sender(session)['user_id']


def get_sender_role(session: CommandSession):
    if 'role' in get_sender(session):
        return get_sender(session)['role']


def get_group_id(session: CommandSession):
    return session.event.group_id


def get_discuss_id(session: CommandSession):
    return session.event.discuss_id
