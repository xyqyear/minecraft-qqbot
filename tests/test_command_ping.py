from plugins.mc.command_list import parse_response


def test_parse_response():
    assert parse_response('v.ping', 'There are 0 of a max of 20 players online:') == '0 player is online'
    assert parse_response('v.ping', 'There are 1 of a max of 20 players online: player1') == 'Only player1 is online'
    assert parse_response('v.ping', 'There are 2 of a max of 20 players online: player1 player2') == \
           '2 players are online: player1 player2'
    assert parse_response('v.ping', 'There are 3 of a max of 20 players online: player1 player2 player3') == \
           '3 players are online: player1 player2 player3'
