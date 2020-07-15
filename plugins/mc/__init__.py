import re

from nonebot import on_command
from config import SERVER_PROPERTIES, DEFAULT_SERVER
from mcrcon import MCRcon

from plugins.mc.permissions import permission_manager
from plugins.mc import command_ping, command_whitelist, command_restart, command_ban, command_unban
from utils.coolq_utils import *

# registering the commands
# get_command: (session, args) -> (mc_command, permission)
commands = {'ping': command_ping,
            'list': command_ping,
            'whitelist': command_whitelist,
            'restart': command_restart,
            'ban': command_ban,
            'unban': command_unban,
            'pardon': command_unban}

# permissions should be loaded after modules registered all the permissions
permission_manager.load_user_permissions()

# binding commands
for command in commands.keys():
    @on_command(command,  only_to_me=False)
    async def _(session: CommandSession):
        chat_command = session.cmd.name[0]
        chat_args, server_names = get_server(session.current_arg_text.strip())
        mc_command, permission = commands[chat_command].get_command(session, chat_args)

        for server_name in server_names:
            # permission string returned does not include server name
            s_permission = f'{server_name}.{permission}'
            # if the person has the required permission, then perform the command on corresponding server
            # and parse the response from the server and send it to the source
            if permission_manager.validate(session, s_permission):
                response = await send_command(server_name, mc_command)
                await session.send(commands[chat_command].parse_response(permission, response))
            # could be used for no permission exception
            else:
                pass


def get_id(session):
    """get sender id from the session"""
    if get_detail_type(session) == 'private':
        return get_sender_id(session)
    elif get_detail_type(session) == 'group':
        return get_sender_id(session)
    elif get_detail_type(session) == 'discuss':
        return get_discuss_id(session)


async def send_command(server_name, mc_command: str):
    """send command to the server specified"""
    with MCRcon(SERVER_PROPERTIES[server_name]['address'],
                port=SERVER_PROPERTIES[server_name]['rcon_port'],
                password=SERVER_PROPERTIES[server_name]['rcon_password']) as mcr:
        return mcr.command(mc_command)


def get_server(chat_args: str):
    """
    get which server we should run the command on from chat command args
    :param chat_args: the chopped chat
    :return chat command args without server specification and server_names as a list
    """
    for server_name, server_properties in SERVER_PROPERTIES.items():
        name_pool = [server_name]
        if 'aka' in server_properties:
            name_pool += server_properties['aka']
        for aka_name in name_pool:
            if chat_args.endswith(f'@{aka_name}'):
                return re.sub(rf'@{aka_name}$', '', chat_args).strip(), [server_name]

    # if the code above didn't return, it means there is no server specification
    # so the command should be executed in default server
    return chat_args, [DEFAULT_SERVER]
