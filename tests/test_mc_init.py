from plugins.mc import get_server


def test_get_server():
    assert get_server('add') == ['add', ['vanilla', 'gtnh']]
    assert get_server('add @vanilla') == ['add', ['vanilla']]
    assert get_server('add @v') == ['add', ['vanilla']]
