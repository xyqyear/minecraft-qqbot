permissions = ('unban', )
commands = ('unban', 'pardon', )


def get_command(session, args: str):
    return f'pardon {args}', 'unban'


def parse_response(permission, response):
    return response
