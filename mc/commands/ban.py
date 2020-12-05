permissions = ('ban', )
commands = ('ban', )


def get_command(session, parsed_message):
    return f'ban {parsed_message.args}', 'ban'


def parse_response(permission, response):
    return response
