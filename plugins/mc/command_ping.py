from plugins.mc.permissions import permission_manager

permission_manager.register('ping')


def get_command(session, args):
    return 'list', 'ping'


def parse_response(permission, response):
    return response
