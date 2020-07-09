from nonebot.default_config import *
import json

SUPERUSERS = 11111111

HOST = 'hostname'
PORT = 8080

SERVER_RCON = {'servername1': {'host': 'hostname1', 'port': 25575, 'password': 'secret'},
               'servername2': {'host': 'hostname2', 'port': 25575, 'password': 'secret'}}

DEFAULT_SERVER = 'servername1'

PERMISSIONS = {'group':
                   {12345678:
                        {'default':
                             ['*.ping',
                              'vanilla.whitelist.list'],
                         'admin':
                             ['vanilla.whitelist.reload',
                              'vanilla.whitelist.add',
                              'vanilla.whitelist.remove',
                              'vanilla.ban',
                              'vanilla.unban',
                              'vanilla.restart']
                         }
                    }
               }
