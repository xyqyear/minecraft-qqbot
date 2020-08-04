permissions = ('unban', )
commands = ('unban', 'pardon', )


def get_command(message):
    return f'pardon {message.args}', 'unban'


def parse_response(permission, response):
    return response
