permissions = ('ban', )


def get_command(session, args: str):
    return f'ban {args}', 'ban'


def parse_response(permission, response):
    return response
