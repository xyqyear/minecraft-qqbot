from utils.coolq_utils import *
from config import SERVER_RCON


class PermissionManager:
    def __init__(self):
        self.all_permissions = dict()
        self.user_permissions = dict()
        self.servers = []

    def load_user_permissions(self, config_user_permissions: dict):
        # handling group permissions
        self.user_permissions['group'] = dict()
        for group_id, permissions in config_user_permissions['group'].items():
            self.user_permissions['group'][group_id] = {'default': list(), 'admin': list()}
            for role in self.user_permissions['group'][group_id].keys():
                for permission in permissions[role]:
                    self.user_permissions['group'][group_id][role] += self.expand_permission(permission)

        # handling private permissions
        self.user_permissions['private'] = dict()
        for user_id, permissions in config_user_permissions['private']:
            self.user_permissions['private'][user_id] = list()
            for permission in permissions:
                self.user_permissions['private'][user_id] += self.expand_permission(permission)

    # used to parse permission
    def expand_permission(self, perm_str: str, server_names=None, all_permissions=None) -> list:
        # used for test
        if not server_names:
            server_names = [i for i in SERVER_RCON.keys()]
        if not all_permissions:
            all_permissions = self.all_permissions

        perm2process_list = perm_str.split('.')
        servers = []
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

            if isinstance(permissions_pre_left, dict):
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

            else:
                for perm_node in permissions_pre_left:
                    yield f'{string_pre_parsed}.{perm_node}'

        expanded_permissions = list()
        for server in servers:
            for perm in parse_asterisk(perm2process_list[1:], all_permissions):
                expanded_permissions.append(f'{server}.{perm}')

        return expanded_permissions

    def validate(self, session: CommandSession, permission: str):
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

    def add_server(self, server_name):
        self.servers.append(server_name)

    def put_permission(self, node_dict, node_permission):
        if len(node_permission) > 2:
            if node_permission[0] not in node_dict:
                node_dict[node_permission[0]] = dict()
            self.put_permission(node_dict[node_permission[0]], node_permission[1:])

        else:
            if node_permission[0] not in node_dict:
                node_dict[node_permission[0]] = list()

            if len(node_permission) > 1:
                node_dict[node_permission[0]].append(node_permission[1])

    def register(self, perm):
        self.put_permission(self.all_permissions, perm.split('.'))


permission_manager = PermissionManager()
