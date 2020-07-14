from utils.coolq_utils import *
from config import SERVER_PROPERTIES, PERMISSIONS


class PermissionManager:
    __slots__ = ('all_permissions', 'user_permissions')

    def __init__(self):
        self.all_permissions = dict()
        self.user_permissions = dict()

    def load_user_permissions(self, config_user_permissions=None, server_names=None, all_permissions=None):
        """load permission from config file or arguments"""
        config_user_permissions = PERMISSIONS if not config_user_permissions else config_user_permissions

        # handling group permissions
        self.user_permissions['group'] = dict()
        for group_id, permissions in config_user_permissions['group'].items():
            self.user_permissions['group'][group_id] = {'default': set(), 'admin': set()}
            for role in self.user_permissions['group'][group_id].keys():
                for permission in permissions[role]:
                    self.user_permissions['group'][group_id][role] |= \
                        self.expand_permission(permission, server_names, all_permissions)

        # handling private permissions
        self.user_permissions['private'] = dict()
        for user_id, permissions in config_user_permissions['private'].items():
            self.user_permissions['private'][user_id] = set()
            for permission in permissions:
                self.user_permissions['private'][user_id] |= \
                    self.expand_permission(permission, server_names, all_permissions)

    def expand_permission(self, perm_str: str, server_names=None, all_permissions=None) -> set:
        """ handle asterisks in perm string like 'whitelist.*' """
        # used for test
        if not server_names:
            server_names = (i for i in SERVER_PROPERTIES.keys())
        if not all_permissions:
            all_permissions = self.all_permissions

        perm2process_list = perm_str.split('.')
        servers = list()
        if perm2process_list[0] == '*':
            for server_name in server_names:
                servers.append(server_name)
        else:
            servers.append(perm2process_list[0])

        # the function for parsing asterisks in permission string
        def parse_asterisk(perm2process_left, permissions_pre_left, string_pre_parsed=''):
            if string_pre_parsed.startswith('.'):
                string_pre_parsed = string_pre_parsed[1:]

            if not permissions_pre_left:
                yield string_pre_parsed

            current_node = perm2process_left[0] if perm2process_left else '*'
            if current_node == '*':
                for perm_node, permissions_left in permissions_pre_left.items():
                    for string_parsed in parse_asterisk(['*'],
                                                        permissions_left,
                                                        f'{string_pre_parsed}.{perm_node}'):
                        yield string_parsed
            else:
                for string_parsed in parse_asterisk(perm2process_left[1:],
                                                    permissions_pre_left[current_node],
                                                    f'{string_pre_parsed}.{current_node}'):
                    yield string_parsed

        expanded_permissions = set()
        for server in servers:
            for perm in parse_asterisk(perm2process_list[1:], all_permissions):
                expanded_permissions.add(f'{server}.{perm}')

        return expanded_permissions

    # permission here includes server name
    def validate(self, session, permission: str):
        """
        validates user permission
        :param session: CommandSession got from nonebot
        :param permission: permission string including server name, e.g. 'vanilla.ping'
        :return: if the invoker of the session has the permission, return True, else False
        """
        detail_type = get_detail_type(session)
        if detail_type == 'group':
            group_id = get_group_id(session)
            if group_id in self.user_permissions['group']:
                if permission in self.user_permissions['group'][group_id]['default']:
                    return True
                elif get_sender_role(session) in ('admin', 'owner') and \
                        permission in self.user_permissions[detail_type][group_id]['admin']:
                    return True

        else:
            sender_id = get_sender_id(session)
            if sender_id in self.user_permissions['private']:
                if permission in self.user_permissions['private'][sender_id]:
                    return True

        return False

    def put_permission(self, node_dict, node_permission):
        """parse current registering permission string into dict"""
        if node_permission:
            if node_permission[0] not in node_dict:
                node_dict[node_permission[0]] = dict()
            self.put_permission(node_dict[node_permission[0]], node_permission[1:])

    def register(self, perm):
        """register permissions, used by modules"""
        self.put_permission(self.all_permissions, perm.split('.'))


permission_manager = PermissionManager()
