import re

from bot.message import Message
from config_manager import config


class ParsedMessage:
    def __init__(self, message: Message):
        self.command = message.command
        self.args, self.server = self.get_server(message)

    @staticmethod
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
                    return re.sub(rf'/{aka_name}$', '', message.args).strip(), server_name

        # if the code above didn't return, it means there is no server specification
        # so the command should be executed in default server
        return message.args, properties[source_id]['default_server']
