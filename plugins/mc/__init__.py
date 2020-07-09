from nonebot import on_command, CommandSession
from config import SERVER_RCON, DEFAULT_SERVER
from mcrcon import MCRcon

from plugins.mc import command_ping, command_whitelist, command_select
from utils.coolq_utils import *

commands = {'ping': command_ping,
            'whitelist': command_whitelist,
            'select': command_select}

chosen_server = {}


for command in commands.keys():
    @on_command(command, only_to_me=False)
    async def _(session: CommandSession):
        source_id = get_id(session)
        pre_choose_server(source_id)

        command = session.cmd.name[0]
        mc_command = commands[command].get_command(session, session.current_arg_text.strip())
        if mc_command:
            response = await send_command(mc_command)
            await session.send(source_id, commands[command].parse_response(response))


def pre_choose_server(source_id):
    if source_id not in chosen_server:
        chosen_server[source_id] = DEFAULT_SERVER


def get_id(session):
    if get_detail_type(session) == 'private':
        return get_sender_id(session)
    elif get_detail_type(session) == 'group':
        return get_sender_id(session)
    elif get_detail_type(session) == 'discuss':
        return get_discuss_id(session)


async def send_command(source_id, mc_command: str):
    server_name = chosen_server[source_id]
    with MCRcon(SERVER_RCON[server_name]['host'],
                port=SERVER_RCON[server_name]['port'],
                password=SERVER_RCON[server_name]['password']) as mcr:
        return mcr.command(mc_command)
