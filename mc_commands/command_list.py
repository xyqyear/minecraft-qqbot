import re
permissions = ('list', )
commands = ('list', 'ping', )


def get_command(message):
    return 'list', 'list'


def parse_response(permission, response):
    player_count, max_player_count, player_list_str = \
        re.findall(r'There are (\d+) of a max of (\d+) players online:(.*)', response)[0]
    if player_count == '0':
        return '0 player is online'
    elif player_count == '1':
        return f'Only{player_list_str} is online'
    else:
        return f'{player_count} players are online:{player_list_str}'
