permissions = ('whitelist.list', 'whitelist.reload', 'whitelist.add', 'whitelist.remove')
commands = ('whitelist', )


def get_command(session, parsed_message):
    if parsed_message.args == 'list':
        return 'whitelist list', 'whitelist.list'
    elif parsed_message.args == 'reload':
        return 'whitelist reload', 'whitelist.reload'
    elif parsed_message.args.startswith('add '):
        return f'whitelist {parsed_message.args}', 'whitelist.add'
    elif parsed_message.args.startswith('remove '):
        return f'whitelist {parsed_message.args}', 'whitelist.remove'
    else:
        return '', 'wrong usage'


def parse_response(permission, response):
    return response
