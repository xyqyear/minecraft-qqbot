from plugins.mc.permissions import permission_manager

permission_manager.register('banlist')


def get_command(session, args):
    return 'banlist', 'banlist'


def parse_response(permission, response):
    return response
