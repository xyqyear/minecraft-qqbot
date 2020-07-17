permissions = ('unban', )


def get_command(session, args: str):
    return f'pardon {args}', 'unban'


def parse_response(permission, response):
    return response
