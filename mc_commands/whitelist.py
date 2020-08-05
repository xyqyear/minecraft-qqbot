permissions = ('whitelist.list', 'whitelist.reload', 'whitelist.add', 'whitelist.remove')
commands = ('whitelist', )


def get_command(message, chat_args):
    if message.args == 'list':
        return 'whitelist list', 'whitelist.list'
    elif message.args == 'reload':
        return 'whitelist reload', 'whitelist.reload'
    elif message.args.startswith('add '):
        return f'whitelist {chat_args}', 'whitelist.add'
    elif message.args.startswith('remove '):
        return f'whitelist {chat_args}', 'whitelist.remove'
    else:
        return '', 'wrong usage'


def parse_response(permission, response):
    return response
