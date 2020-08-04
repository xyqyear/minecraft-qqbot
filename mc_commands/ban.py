permissions = ('ban', )
commands = ('ban', )


def get_command(message):
    return f'ban {message.args}', 'ban'


def parse_response(permission, response):
    return response
