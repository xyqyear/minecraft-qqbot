from nonebot import CommandSession
from plugins.mc import permissions


def get_command(session: CommandSession, args: str, permission_list=None):
    permission = ''
    if args.startswith('list'):
        permission = 'whitelist.list'
    elif args.startswith('reload'):
        permission = 'whitelist.reload'
    elif args.startswith('add'):
        permission = 'whitelist.add'
    elif args.startswith('remove'):
        permission = 'whitelist.remove'

    if permissions.validate(session, permission):
        return f'whitelist {args}'


def parse_response(response):
    return response
