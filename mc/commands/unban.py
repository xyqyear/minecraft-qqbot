permissions = ('unban', )
commands = ('unban', 'pardon', )


def get_command(session, parsed_message):
    return f'pardon {parsed_message.args}', 'unban'


def parse_response(permission, response):
    return response
