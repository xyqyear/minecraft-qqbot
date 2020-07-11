from plugins.mc.permissions import permission_manager
from plugins.mc import chosen_server, get_id
from config import SERVER_RCON

permission_manager.register('select')


def get_command(session, args: str):
    if permission_manager.validate(session, 'select'):
        server_name = args.strip()
        if server_name in SERVER_RCON.keys():
            chosen_server[get_id(session)] = server_name
