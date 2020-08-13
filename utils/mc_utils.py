import re
import asyncio
from mcstatus.server import MinecraftServer
from mcstatus.pinger import PingResponse
from asyncrcon import AsyncRCON

from config_manager import config
from utils.network_utils import is_ipv4
from utils.aio_utils import to_async
from bot.message import Message

player_message_pattern = re.compile(r'\[\d\d:\d\d:\d\d\] \[Server thread/INFO\]: <(.*?)> (.*)')

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


async def async_get_player_list(address: str, port: int = 25565, timeout: int = 3) -> tuple:
    status = await asyncio.wait_for(async_get_status(address, port), timeout=timeout)
    if status.players.online > 0:
        return tuple(player.name for player in status.players.sample)
    else:
        return tuple()


async def send_command(server_name, mc_command: str, timeout: int = 3):
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
