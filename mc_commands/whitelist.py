permissions = ('whitelist.list', 'whitelist.reload', 'whitelist.add', 'whitelist.remove')


def get_command(session, args: str):
    if args.startswith('list '):
        return 'whitelist list', 'whitelist.list'
    elif args == 'reload':
        return 'whitelist reload', 'whitelist.reload'
    elif args.startswith('add '):
        return f'whitelist {args}', 'whitelist.add'
    elif args.startswith('remove '):
        return f'whitelist {args}', 'whitelist.remove'
    else:
        return '', 'wrong usage'


def parse_response(permission, response):
    return response
