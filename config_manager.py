import ruamel.yaml

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True


class ConfigManager:
    def __init__(self):
        self.config = None

    def load_from_file(self, path='config.yml', force=False):
        if not self.config or force:
            with open(path) as f:
                self.config = yaml.load(f.read())

    def load_from_string(self, string, force=False):
        if not self.config or force:
            self.config = yaml.load(string)

    def save_to_file(self, path='config.yml'):
        with open(path, 'w') as f:
            yaml.dump(self.config, f)

    def reload(self, path=None):
        if path:
            self.load_from_file(path, force=True)
        else:
            self.load_from_file(force=True)

    load = load_from_file
    save = save_to_file

    @property
    def bot_host(self):
        return self.config['bot_host']

    @bot_host.setter
    def bot_host(self, bot_host):
        self.config['bot_host'] = bot_host

    @property
    def bot_authKey(self):
        return self.config['bot_authKey']

    @bot_authKey.setter
    def bot_authKey(self, bot_authKey):
        self.config['bot_authKey'] = bot_authKey

    @property
    def bot_account(self):
        return self.config['bot_account']

    @bot_account.setter
    def bot_account(self, bot_account):
        self.config['bot_account'] = bot_account

    @property
    def server_properties(self):
        return self.config['server_properties']

    @server_properties.setter
    def server_properties(self, server_properties):
        self.config['server_properties'] = server_properties

    @property
    def default_server(self):
        return self.config['default_server']

    @default_server.setter
    def default_server(self, default_server):
        self.config['default_server'] = default_server

    @property
    def log_path(self):
        return self.config['log_path']

    @log_path.setter
    def log_path(self, log_path):
        self.config['log_path'] = log_path

    @property
    def default_group(self):
        return self.config['default_group']

    @default_group.setter
    def default_group(self, default_group):
        self.default_group['log_path'] = default_group

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
