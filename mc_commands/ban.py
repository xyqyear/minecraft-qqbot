permissions = ('ban', )
commands = ('ban', )


def get_command(message, chat_args):
    return f'ban {chat_args}', 'ban'


def parse_response(permission, response):
    return response
