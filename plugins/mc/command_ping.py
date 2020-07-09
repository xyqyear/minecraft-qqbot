from plugins.mc import permissions


def get_command(session, args, permission_list=None):
    if permissions.validate(session, 'ping'):
        return 'list'


def parse_response(response):
    return response
