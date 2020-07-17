from plugins.mc.permissions import permission_manager

permission_manager.register('whitelist.list')
permission_manager.register('whitelist.reload')
permission_manager.register('whitelist.add')
permission_manager.register('whitelist.remove')


def get_command(session, args: str):
    if args.startswith('list'):
        return 'whitelist list', 'whitelist.list'
    elif args.startswith('reload'):
        return 'whitelist reload', 'whitelist.reload'
    elif args.startswith('add'):
        return f'whitelist {args}', 'whitelist.add'
    elif args.startswith('remove'):
        return f'whitelist {args}', 'whitelist.remove'
    else:
        return '', 'wrong usage'


def parse_response(permission, response):
    return response
