permissions = ('restart', )
commands = ('restart', )


def get_command(raw_message, parsed_message):
    return 'stop', 'restart'


def parse_response(permission, response):
    return response
