permissions = ('restart', )
commands = ('restart', )


def get_command(message):
    return 'stop', 'restart'


def parse_response(permission, response):
    return response
