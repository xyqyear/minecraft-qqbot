from plugins.mc.permissions import permission_manager

permission_manager.register('restart')


def get_command(session, args):
    return 'stop', 'restart'


def parse_response(permission, response):
    return response
