from plugins.mc.permissions import permission_manager

permission_manager.register('ping')


def get_command(session, args):
    if permission_manager.validate(session, 'ping'):
        return 'list'


def parse_response(response):
    return response
