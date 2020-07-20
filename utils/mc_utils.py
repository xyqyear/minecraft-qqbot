import re
from mcrcon import MCRcon

log_pattern = re.compile(r'\[\d\d:\d\d:\d\d\] \[Server thread/INFO\]: <(.*)> (.*)')


async def send_command(server_name, mc_command: str):
    """send command to the server specified"""
    from bot_config import SERVER_PROPERTIES
    with MCRcon(SERVER_PROPERTIES[server_name]['address'],
                port=SERVER_PROPERTIES[server_name]['rcon_port'],
                password=SERVER_PROPERTIES[server_name]['rcon_password']) as mcr:
        return mcr.command(mc_command)


def get_server(chat_args: str, default_server='', server_properties=None):
    """
    get which server we should run the command on from chat command args
    :param chat_args: the chopped chat
    :param default_server: used for test
    :param server_properties: used for test
    :return chat command args without server specification and server_names as a list
    """
    if not default_server:
        from bot_config import DEFAULT_SERVER
        default_server = DEFAULT_SERVER
    if not server_properties:
        from bot_config import SERVER_PROPERTIES
        server_properties = SERVER_PROPERTIES
    for server_name, server_properties in server_properties.items():
        name_pool = [server_name]
        if 'aka' in server_properties:
            name_pool += server_properties['aka']
        for aka_name in name_pool:
            if chat_args.endswith(f'@{aka_name}'):
                return re.sub(rf'@{aka_name}$', '', chat_args).strip(), [server_name]

    # if the code above didn't return, it means there is no server specification
    # so the command should be executed in default server
    return chat_args, [default_server]


def parse_logs(logs, startswith=None):
    if startswith is None:
        startswith = (r'\\', '、、')
    for name, message in log_pattern.findall(logs):
        for start in startswith:
            if message.startswith(start):
                yield name, message[len(start):]
                break
