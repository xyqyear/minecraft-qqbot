from plugins.mc.permissions import permission_manager

permission_manager.register('ban')


def get_command(session, args: str):
    return f'ban {args}', 'ban'


def parse_response(permission, response):
    return response
