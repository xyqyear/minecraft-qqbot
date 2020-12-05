import ruamel.yaml

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True


class ConfigManager:
    def __init__(self):
        self.config = None

    def load_from_file(self, path: str = 'config.yml', force: bool = False):
        if not self.config or force:
            with open(path) as f:
                self.config = yaml.load(f.read())

    def load_from_string(self, string: str, force: bool = False):
        if not self.config or force:
            self.config = yaml.load(string)

    def save_to_file(self, path: str = 'config.yml'):
        with open(path, 'w') as f:
            yaml.dump(self.config, f)

    def reload(self, path: str = None):
        if path:
            self.load_from_file(path, force=True)
        else:
            self.load_from_file(force=True)

    load = load_from_file
    save = save_to_file

    @property
    def bot_listen_host(self) -> str:
        return self.config['bot_listen_host']

    @bot_listen_host.setter
    def bot_listen_host(self, bot_listen_host: str):
        self.config['bot_listen_host'] = bot_listen_host

    @property
    def bot_listen_port(self) -> int:
        return self.config['bot_listen_port']

    @bot_listen_port.setter
    def bot_listen_port(self, bot_listen_port: int):
        self.config['bot_listen_port'] = bot_listen_port

    @property
    def server_properties(self):
        return self.config['server_properties']

    @server_properties.setter
    def server_properties(self, server_properties):
        self.config['server_properties'] = server_properties

    @property
    def group_properties(self):
        return self.config['group_properties']

    @group_properties.setter
    def group_properties(self, group_properties):
        self.config['group_properties'] = group_properties

    @property
    def private_properties(self):
        return self.config['private_properties']

    @private_properties.setter
    def private_properties(self, private_properties):
        self.config['private_properties'] = private_properties

    @property
    def default_server(self) -> str:
        return self.config['default_server']

    @default_server.setter
    def default_server(self, default_server: str):
        self.config['default_server'] = default_server

    @property
    def default_group(self):
        return self.config['default_group']

    @default_group.setter
    def default_group(self, default_group):
        self.config['default_group'] = default_group

    @property
    def command_say_bindings(self):
        return self.config['command_say_bindings']

    @command_say_bindings.setter
    def command_say_bindings(self, command_say_bindings):
        self.config['command_say_bindings'] = command_say_bindings

    @property
    def permissions(self):
        return self.config['permissions']

    @permissions.setter
    def permissions(self, permissions):
        self.config['permissions'] = permissions


config = ConfigManager()
