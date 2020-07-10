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

    # TODO
    def load_user_permissions(self, ):
        pass

    # TODO
    def validate(self):
        pass

    def add_server(self, server_name):
        self.servers.append(server_name)

    def register(self, perm):
        self.put_permission(self.all_permissions, perm.split('.'))


permission_manager = PermissionManager()
