from config_manager import config
from utils.mc_utils import async_get_player_list
from mc.permissions import permission_manager

permissions = ('list', )
commands = ('list', 'ping', )


async def get_command(raw_message, parsed_message):
    server_name = parsed_message.server
    if permission_manager.validate(raw_message, f'{server_name}.list'):
        player_list = await async_get_player_list(config.server_properties[server_name]['address'],
                                                  config.server_properties[server_name]['main_port'])
        player_count = len(player_list)

        response = ''
        if player_count == 0:
            response = 'No player is online'
        elif player_count == 1:
            response = f'Only {player_list[0]} is online'
        else:
            response = f'{player_count} players are online: {", ".join(player_list)}'

        return '', f'[{server_name}] {response}'
    else:
        return '', 'You dont\'t have the permission to run this command.'
