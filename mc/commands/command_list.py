import asyncio

from config_manager import config
from utils.mc_utils import async_get_player_list
from mc.permissions import permission_manager

permissions = ('list', )
commands = ('list', 'ping', )


async def get_command(session, parsed_message):
    if parsed_message.args == 'all':
        responses = list()
        for server_name in config.server_properties.keys():
            response = (await list_helper(session, server_name))[1]
            if not response.startswith('Y'):
                responses.append(response)
        return '', '\n'.join(responses)

    else:
        return await list_helper(session, parsed_message.server)


async def list_helper(session, server_name):
    if permission_manager.validate(session, f'{server_name}.list'):
        try:
            player_list = await async_get_player_list(config.server_properties[server_name]['address'],
                                                      config.server_properties[server_name]['main_port'])
        except (asyncio.TimeoutError, ConnectionRefusedError):
            return '', f'[{server_name}] Failed to connect to the server'
        player_count = len(player_list)

        if player_count == 0:
            response = 'No player is online'
        elif player_count == 1:
            response = f'Only {player_list[0]} is online'
        else:
            response = f'{player_count} players are online: {", ".join(player_list)}'

        return '', f'[{server_name}] {response}'
    else:
        return '', 'You dont\'t have the permission to run this command.'
