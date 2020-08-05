import re
permissions = ('list', )
commands = ('list', 'ping', )


def get_command(message, chat_args):
    return 'list', 'list'


def parse_response(permission, response):
    return response
