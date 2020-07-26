from utils.coolq_utils import get_detail_type, get_group_id, get_sender_role, get_sender_id
from config_manager import config


class PermissionManager:
    __slots__ = ('all_permissions', 'user_permissions')

    def __init__(self):
        self.all_permissions = set()
        self.user_permissions = dict()

    def load_user_permissions(self, config_user_permissions=None, server_names=None, all_permissions=None):
        """load permission from config file or arguments"""
        if not config_user_permissions:
            config_user_permissions = config.permissions

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
            server_names = (i for i in config.server_properties.keys())
        if not all_permissions:
            all_permissions = self.all_permissions

        if perm_str == '*':
            perm_str = '*.*'

        sub_permissions = perm_str.split('.', 1)

        if sub_permissions[0] == '*':
            needed_server = server_names
        else:
            needed_server = {sub_permissions[0]}

        if sub_permissions[1].endswith('*'):
            sub_permissions[1] = sub_permissions[1][:-1]
            needed_permission = {permission for permission in all_permissions if permission.startswith(sub_permissions[1])}
        else:
            needed_permission = {sub_permissions[1]}

        return {f'{server_name}.{permission}' for server_name in needed_server for permission in needed_permission}

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

    def register(self, perm):
        """register permissions, used by modules"""
        self.all_permissions.add(perm)


permission_manager = PermissionManager()
