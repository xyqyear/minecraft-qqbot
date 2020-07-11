from plugins.mc.permissions import permission_manager
from plugins.mc import no_session

permission_manager.register('whitelist.list')
permission_manager.register('whitelist.reload')
permission_manager.register('whitelist.add')
permission_manager.register('whitelist.remove')


@no_session
def get_command(args: str):
    if args.startswith('list'):
        return 'whitelist list', 'whitelist.list'
    elif args.startswith('reload'):
        return 'whitelist reload', 'whitelist.reload'
    elif args.startswith('add'):
        return 'whitelist add', 'whitelist.add'
    elif args.startswith('remove'):
        return 'whitelist remove', 'whitelist.remove'


def parse_response(response):
    return response
