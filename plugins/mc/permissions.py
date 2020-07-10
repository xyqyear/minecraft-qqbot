from utils.coolq_utils import *


class PermissionManager:
    def __init__(self):
        self.all_permissions = dict()
        self.user_permissions = dict()
        self.servers = []

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

    # TODO
    def expand_permission(self, general_permission: str):
        pass

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

    def register(self, perm):
        self.put_permission(self.all_permissions, perm.split('.'))


permission_manager = PermissionManager()
