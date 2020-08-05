permissions = ('banlist', )
commands = ('banlist', )


def get_command(message, chat_args):
    return 'banlist', 'banlist'


def parse_response(permission, response):
    return response
