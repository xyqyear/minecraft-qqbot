from plugins.mc.permissions import permission_manager

permission_manager.register('unban')


def get_command(session, args: str):
    return f'pardon {args}', 'unban'


def parse_response(permission, response):
    return response
