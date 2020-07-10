from plugins.mc.permissions import permission_manager

permission_manager.register('whitelist.list')
permission_manager.register('whitelist.reload')
permission_manager.register('whitelist.add')
permission_manager.register('whitelist.remove')


def get_command(session, args: str):
    permission = ''
    if args.startswith('list'):
        permission = 'whitelist.list'
    elif args.startswith('reload'):
        permission = 'whitelist.reload'
    elif args.startswith('add'):
        permission = 'whitelist.add'
    elif args.startswith('remove'):
        permission = 'whitelist.remove'

    if permission_manager.validate(session, permission):
        return f'whitelist {args}'


def parse_response(response):
    return response
