permissions = ('banlist', )
commands = ('banlist', )


def get_command(raw_message, parsed_message):
    return 'banlist', 'banlist'


def parse_response(permission, response):
    return response