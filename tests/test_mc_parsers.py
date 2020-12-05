from tests.utils import get_dummy_group_message_session, get_dummy_private_message_session
from mc.parsers import ParsedMessage

get_server = ParsedMessage.get_server


def test_get_server():
    server_properties = {'vanilla':
                             {'aka': ['v']},
                         'gtnh':
                             {'aka': ['g']}}

    private_properties = {11111111: {'default_server': 'vanilla'},
                          22222222: {'default_server': 'gtnh'}}

    assert get_server(get_dummy_private_message_session(11111111, '/whitelist list'),
                      private_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', 'vanilla')
    assert get_server(get_dummy_private_message_session(11111111, '/whitelist list /v'),
                      private_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', 'vanilla')
    assert get_server(get_dummy_private_message_session(11111111, '/whitelist list /vanilla'),
                      private_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', 'vanilla')
    assert get_server(get_dummy_private_message_session(11111111, '/whitelist list /g'),
                      private_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', 'gtnh')
    assert get_server(get_dummy_private_message_session(33333333, '/whitelist list'),
                      private_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', 'vanilla')

    assert private_properties == {11111111: {'default_server': 'vanilla'},
                                  22222222: {'default_server': 'gtnh'},
                                  33333333: {'default_server': 'vanilla'}}

    assert get_server(get_dummy_private_message_session(33333333, '/whitelist list /g'),
                      private_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', 'gtnh')

    group_properties = {12345678: {'default_server': 'vanilla'},
                        87654321: {'default_server': 'gtnh'}}

    assert get_server(get_dummy_group_message_session(12345678, message_text='/whitelist list'),
                      group_properties=group_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', 'vanilla')
    assert get_server(get_dummy_group_message_session(12345678, message_text='/whitelist list /v'),
                      group_properties=group_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', 'vanilla')
    assert get_server(get_dummy_group_message_session(12345678, message_text='/whitelist list /vanilla'),
                      group_properties=group_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', 'vanilla')
    assert get_server(get_dummy_group_message_session(12345678, message_text='/whitelist list /g'),
                      group_properties=group_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', 'gtnh')
    assert get_server(get_dummy_group_message_session(33333333, message_text='/whitelist list'),
                      group_properties=group_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', 'vanilla')
    assert get_server(get_dummy_group_message_session(33333333, message_text='/whitelist list /g'),
                      group_properties=group_properties,
                      server_properties=server_properties,
                      default_server='vanilla') == ('list', 'gtnh')

