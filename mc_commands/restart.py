permissions = ('restart', )
commands = ('restart', )


def get_command(session, args):
    return 'stop', 'restart'


def parse_response(permission, response):
    return response
