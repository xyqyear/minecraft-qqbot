from utils.mc_utils import parse_logs


def test_parse_logs():
    logs = r'''
[22:55:47] [Server thread/INFO]: <player0> \\hi
[23:08:54] [Server thread/WARN]: player1 moved wrongly!
[23:14:33] [Server thread/INFO]: <player2> hi @player0!
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
