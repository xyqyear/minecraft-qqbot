from utils.mc_utils import get_server, parse_logs
from tests.utils import get_dummy_group_message, get_dummy_private_message


def test_get_server():
    server_properties = {'vanilla':
                             {'aka': ['v']},
                         'gtnh':
                             {'aka': ['g']}}

    private_properties = {11111111: {'default_server': 'vanilla'},
                          22222222: {'default_server': 'gtnh'}}

    assert get_server(get_dummy_private_message(11111111, '/whitelist list'),
                      private_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', ['vanilla'])
    assert get_server(get_dummy_private_message(11111111, '/whitelist list @v'),
                      private_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', ['vanilla'])
    assert get_server(get_dummy_private_message(11111111, '/whitelist list @vanilla'),
                      private_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', ['vanilla'])
    assert get_server(get_dummy_private_message(11111111, '/whitelist list @g'),
                      private_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', ['gtnh'])
    assert get_server(get_dummy_private_message(33333333, '/whitelist list'),
                      private_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', ['vanilla'])

    assert private_properties == {11111111: {'default_server': 'vanilla'},
                                  22222222: {'default_server': 'gtnh'},
                                  33333333: {'default_server': 'vanilla'}}

    assert get_server(get_dummy_private_message(33333333, '/whitelist list @g'),
                      private_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', ['gtnh'])

    group_properties = {12345678: {'default_server': 'vanilla'},
                        87654321: {'default_server': 'gtnh'}}

    assert get_server(get_dummy_group_message(12345678, message_text='/whitelist list'),
                      group_properties=group_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', ['vanilla'])
    assert get_server(get_dummy_group_message(12345678, message_text='/whitelist list @v'),
                      group_properties=group_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', ['vanilla'])
    assert get_server(get_dummy_group_message(12345678, message_text='/whitelist list @vanilla'),
                      group_properties=group_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', ['vanilla'])
    assert get_server(get_dummy_group_message(12345678, message_text='/whitelist list @g'),
                      group_properties=group_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', ['gtnh'])
    assert get_server(get_dummy_group_message(33333333, message_text='/whitelist list'),
                      group_properties=group_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', ['vanilla'])
    assert get_server(get_dummy_group_message(33333333, message_text='/whitelist list @g'),
                      group_properties=group_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', ['gtnh'])


def test_parse_logs():
    logs = r'''
[22:55:47] [Server thread/INFO]: <player0> \\hi
[23:08:54] [Server thread/WARN]: player1 moved wrongly!
[23:14:33] [Server thread/INFO]: <player2> hi @travelers!
[23:14:43] [Server thread/INFO]: <player2> do you have some magma blocks we can use?
[23:14:44] [Server thread/INFO]: <player0> \\hello
[23:14:54] [Server thread/INFO]: <player0> yes i do
[23:16:09] [Server thread/INFO]: <player1> thx
[23:16:17] [Server thread/INFO]: <player0> my pleasure
[23:16:35] [Server thread/INFO]: <player2> thank you player0 XD
[23:16:42] [Server thread/INFO]: <player0> w
[23:16:54] [Server thread/INFO]: <player1> 、、wood?
[23:17:21] [Server thread/INFO]: <player0> \\what wood?
[23:17:30] [Server thread/INFO]: <player1> its ok
[23:24:27] [Server thread/INFO]: player2 lost connection: Disconnected
[23:24:27] [Server thread/INFO]: player2 left the game
[23:29:49] [Server thread/INFO]: player1 lost connection: Disconnected'''

    assert [i for i in parse_logs(logs)] == [('player0', 'hi'), ('player0', 'hello'), ('player1', 'wood?'),
                                             ('player0', 'what wood?')]
