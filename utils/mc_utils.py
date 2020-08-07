import re
from mcstatus.server import MinecraftServer
from mcstatus.pinger import PingResponse
from asyncrcon import AsyncRCON

from config_manager import config
from utils.network_utils import is_ipv4
from utils.aio_utils import to_async
from message import Message

player_message_pattern = re.compile(r'\[\d\d:\d\d:\d\d\] \[Server thread/INFO\]: <(.*)> (.*)')

async_server_lookup = to_async(MinecraftServer.lookup)


@to_async
def async_get_status_from_server(server: MinecraftServer):
    return server.status()


async def async_get_status(address: str, port: int = 25565) -> PingResponse:
    if is_ipv4(address):
        server = MinecraftServer(address, port)
    else:
        server = await async_server_lookup(f'{address}:{port}')

    return await async_get_status_from_server(server)


async def async_get_player_list(address: str, port: int = 25565) -> tuple:
    status = await async_get_status(address, port)
    if status.players.online > 0:
        return tuple(player.name for player in status.players.sample)
    else:
        return tuple()


async def send_command(server_name, mc_command: str):
    """send command to the server specified"""
    server_properties = config.server_properties

    rcon = AsyncRCON(f'{server_properties[server_name]["address"]}:{server_properties[server_name]["rcon_port"]}',
                     server_properties[server_name]['rcon_password'])

    try:
        await rcon.open_connection()
    except OSError:
        return 'Failed to connect to the server'

    try:
        response = await rcon.command(mc_command)
    except OSError:
        return 'Failed to connect to the server'

    rcon.close()
    return response


def get_server(message: Message, private_properties: dict = None, group_properties: dict = None,
               server_properties: dict = None, default_server: str = None):
    """
    get which server we should run the command on from chat command args
    :param message: the chopped chat
    :param private_properties: used for test
    :param group_properties: used for test
    :param server_properties: used for test
    :param default_server: used for test
    :return chat command args without server specification and server_names as a list
    """
    if not default_server:
        default_server = config.default_server

    # if the message is from group, then read group's default server
    # if the group does not have a default server in config file
    # then assign the default server to the group config
    if message.type == 'group':
        source_id = message.group_id
        if group_properties is None:
            properties = config.group_properties
        else:
            properties = group_properties
        if source_id not in properties:
            properties[source_id] = dict()
            properties[source_id]['default_server'] = default_server
            # if not in test environment
            if group_properties is None:
                config.group_properties[source_id] = dict()
                config.group_properties[source_id]['default_server'] = default_server

    # same for private messages
    else:
        source_id = message.sender_id
        if private_properties is None:
            properties = config.private_properties
        else:
            properties = private_properties
        if source_id not in properties:
            properties[source_id] = dict()
            properties[source_id]['default_server'] = default_server
            if private_properties is None:
                config.private_properties[source_id] = dict()
                config.private_properties[source_id]['default_server'] = default_server

    if server_properties is None:
        server_properties = config.server_properties

    for server_name, server_properties in server_properties.items():
        name_pool = [server_name]
        if 'aka' in server_properties:
            name_pool += server_properties['aka']
        for aka_name in name_pool:
            if message.args.endswith(f'/{aka_name}'):
                return re.sub(rf'/{aka_name}$', '', message.args).strip(), [server_name]

    # if the code above didn't return, it means there is no server specification
    # so the command should be executed in default server
    return message.args, [properties[source_id]['default_server']]


def parse_logs(logs, startswith=None):
    if startswith is None:
        startswith = (r'\\', '、、')
    for name, message in player_message_pattern.findall(logs):
        for start in startswith:
            if message.startswith(start):
                yield name, message[len(start):]
                break
