from nonebot.default_config import *

SUPERUSERS = 11111111

HOST = 'hostname'
PORT = 8080

SERVER_RCON = {'servername1': {'address': 'address1', 'rcon_port': 25575, 'rcon_password': 'secret', 'aka': ['s1']},
               'servername2': {'address': 'address2', 'rcon_port': 25575, 'rcon_password': 'secret', 'aka': ['s2']}}

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
                   },
               'private':
                   {12345679:
                        ['*']
                    }
               }
