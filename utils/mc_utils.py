import re
import asyncio
from mcstatus.server import JavaServer
from mcstatus.pinger import PingResponse
from asyncrcon import AsyncRCON

from config_manager import config
from utils.network_utils import is_ipv4

player_message_pattern = re.compile(r'\]: <(.*?)> (.*)')


async def async_get_status(address: str, port: int = 25565) -> PingResponse:
    if is_ipv4(address):
        server = JavaServer(address, port)
    else:
        server = await JavaServer.async_lookup(f'{address}:{port}')

    return await server.async_status()


async def async_get_player_list(address: str, port: int = 25565, timeout: int = 3) -> tuple:
    status = await asyncio.wait_for(async_get_status(address, port), timeout=timeout)
    if status.players.online > 0:
        return tuple(player.name for player in status.players.sample)
    else:
        return tuple()


async def send_command(server_name, mc_command: str, timeout: int = 5):
    """send command to the server specified"""
    server_properties = config.server_properties

    rcon = AsyncRCON(f'{server_properties[server_name]["address"]}:{server_properties[server_name]["rcon_port"]}',
                     server_properties[server_name]['rcon_password'])

    try:
        await asyncio.wait_for(rcon.open_connection(), timeout=timeout)
    except (OSError, asyncio.TimeoutError):
        return 'Failed to connect to the server'

    try:
        response = await asyncio.wait_for(rcon.command(mc_command), timeout=timeout)
    except (OSError, asyncio.TimeoutError):
        return 'Failed to connect to the server'

    rcon.close()
    return response


def parse_logs(logs, startswith=None):
    if startswith is None:
        startswith = (r'\\', '、、')
    for name, message in player_message_pattern.findall(logs):
        for start in startswith:
            if message.startswith(start):
                yield name, message[len(start):]
                break
