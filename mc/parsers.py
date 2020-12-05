import re

from config_manager import config
from nonebot import CommandSession
from typing import Tuple, Dict


class ParsedMessage:
    def __init__(self, session: CommandSession):
        self.command = session.cmd.name[0]
        self.args, self.server = self.get_server(session)

    @staticmethod
    def get_server(session: CommandSession, private_properties: dict = None, group_properties: dict = None,
                   server_properties: dict = None, default_server: str = None) -> Tuple[str, str]:
        """
        get which server we should run the command on from chat command args
        :param session: CommandSession from nonebot
        :param private_properties: used for test
        :param group_properties: used for test
        :param server_properties: used for test
        :param default_server: used for test
        :return chat command args without server specification and server_names as a tuple
        """
        if not default_server:
            default_server: str = config.default_server

        # if the message is from group, then read group's default server
        # if the group does not have a default server in config file
        # then assign the default server to the group config
        if session.event.detail_type == 'group':
            source_id: int = session.event.group_id
            if group_properties is None:
                properties = config.group_properties
            else:
                properties = group_properties
            if source_id not in properties:
                properties[source_id]: Dict[str: str] = dict()
                properties[source_id]['default_server'] = default_server
                # if not in test environment
                if group_properties is None:
                    config.group_properties[source_id]: Dict[str: str] = dict()
                    config.group_properties[source_id]['default_server'] = default_server

        # same for private messages
        else:
            source_id: int = session.event.user_id
            if private_properties is None:
                properties = config.private_properties
            else:
                properties = private_properties
            if source_id not in properties:
                properties[source_id]: Dict[str: str] = dict()
                properties[source_id]['default_server'] = default_server
                if private_properties is None:
                    config.private_properties[source_id]: Dict[str: str] = dict()
                    config.private_properties[source_id]['default_server'] = default_server

        if server_properties is None:
            server_properties = config.server_properties

        server_name: str
        for server_name, server_properties in server_properties.items():
            name_pool = [server_name]
            if 'aka' in server_properties:
                name_pool += server_properties['aka']
            for aka_name in name_pool:
                if session.current_arg_text.endswith(f'/{aka_name}'):
                    return re.sub(rf'/{aka_name}$', '', session.current_arg_text).strip(), server_name

        # if the code above didn't return, it means there is no server specification
        # so the command should be executed in default server
        return session.current_arg_text, properties[source_id]['default_server']
