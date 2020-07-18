from utils.mc_utils import get_server, parse_logs


def test_get_server():
    server_properties = {
        'vanilla': {'address': 'host', 'rcon_port': 25575, 'rcon_password': 'super secret', 'aka': ['v']}}
    assert get_server('add', 'vanilla', server_properties) == ('add', ['vanilla'])
    assert get_server('add @vanilla', 'vanilla', server_properties) == ('add', ['vanilla'])
    assert get_server('add @v', 'vanilla', server_properties) == ('add', ['vanilla'])


def test_parse_logs():
    logs = '''
[22:55:47] [Server thread/INFO]: <player0> ,s hi
[23:08:54] [Server thread/WARN]: player1 moved wrongly!
[23:14:33] [Server thread/INFO]: <player2> hi @travelers!
[23:14:43] [Server thread/INFO]: <player2> do you have some magma blocks we can use?
[23:14:44] [Server thread/INFO]: <player0> ,s hello
[23:14:54] [Server thread/INFO]: <player0> yes i do
[23:16:09] [Server thread/INFO]: <player1> thx
[23:16:17] [Server thread/INFO]: <player0> my pleasure
[23:16:35] [Server thread/INFO]: <player2> thank you player0 XD
[23:16:42] [Server thread/INFO]: <player0> w
[23:16:54] [Server thread/INFO]: <player1> ,s wood?
[23:17:21] [Server thread/INFO]: <player0> ,s what wood?
[23:17:30] [Server thread/INFO]: <player1> its ok
[23:24:27] [Server thread/INFO]: player2 lost connection: Disconnected
[23:24:27] [Server thread/INFO]: player2 left the game
[23:29:49] [Server thread/INFO]: player1 lost connection: Disconnected'''

    assert [i for i in parse_logs(logs)] == [('player0', 'hi'), ('player0', 'hello'), ('player1', 'wood?'),
                                             ('player0', 'what wood?')]
