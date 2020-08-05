permissions = ('unban', )
commands = ('unban', 'pardon', )


def get_command(message, chat_args):
    return f'pardon {chat_args}', 'unban'


def parse_response(permission, response):
    return response
