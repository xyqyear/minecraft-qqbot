from mc.permissions import PermissionManager
from tests.utils import get_dummy_group_message_session, get_dummy_private_message_session


def test_register():
    permission_manager = PermissionManager()
    permission_manager.register('ping')
    permission_manager.register('whitelist.list')
    permission_manager.register('whitelist.reload')
    permission_manager.register('perm.node1.node2')
    permission_manager.register('perm.node2')

    permission_dict = {'ping', 'whitelist.list', 'whitelist.reload', 'perm.node1.node2', 'perm.node2'}

    assert permission_manager.all_permissions == permission_dict


def test_expand_permission():
    permission_manager = PermissionManager()
    permission_manager.all_permissions = {'ping', 'whitelist.list', 'whitelist.reload'}
    server_names = ('vanilla', 'gtnh')

    assert permission_manager.expand_permission('*', server_names) == {'vanilla.whitelist.reload',
                                                                       'gtnh.whitelist.list',
                                                                       'vanilla.ping',
                                                                       'vanilla.whitelist.list',
                                                                       'gtnh.whitelist.reload',
                                                                       'gtnh.ping'}

    assert permission_manager.expand_permission('*.whitelist.*', server_names) == {'vanilla.whitelist.reload',
                                                                                   'vanilla.whitelist.list',
                                                                                   'gtnh.whitelist.reload',
                                                                                   'gtnh.whitelist.list'}

    assert permission_manager.expand_permission('vanilla.whitelist.*', server_names) == {
        'vanilla.whitelist.reload',
        'vanilla.whitelist.list'}

    assert permission_manager.expand_permission('vanilla.whitelist.reload', server_names) == {
        'vanilla.whitelist.reload'}


def test_load_user_permission():
    permission_manager = PermissionManager()
    permission_manager.all_permissions = {'ping', 'whitelist.list', 'whitelist.reload'}

    permissions = {'group':
                       {1111:
                            {'default':
                                 ['*.ping',
                                  'vanilla.whitelist.list',
                                  ],
                             'admin':
                                 ['vanilla.whitelist.*',
                                  ]
                             }
                        },
                   'private':
                       {2222:
                            ['*']
                        }
                   }

    permission_dict = {'group': {1111: {'default': {'vanilla.ping', 'vanilla.whitelist.list', 'gtnh.ping'},
                                        'admin': {'vanilla.whitelist.reload', 'vanilla.whitelist.list'}}},
                       'private': {2222: {'vanilla.whitelist.reload', 'gtnh.whitelist.list', 'vanilla.ping',
                                          'vanilla.whitelist.list', 'gtnh.whitelist.reload', 'gtnh.ping'}}}

    permission_manager.load_user_permissions(permissions, ('vanilla', 'gtnh'))

    assert permission_manager.user_permissions == permission_dict


def test_permission_validate():
    permission_manager = PermissionManager()
    permission_manager.user_permissions = {
        'group': {1111: {'default': {'vanilla.ping', 'vanilla.whitelist.list', 'gtnh.ping'},
                         'admin': {'vanilla.whitelist.reload', 'vanilla.whitelist.list'}}},
        'private': {2222: {'vanilla.whitelist.reload', 'gtnh.whitelist.list', 'vanilla.ping',
                           'vanilla.whitelist.list', 'gtnh.whitelist.reload', 'gtnh.ping'}}}

    assert permission_manager.validate(get_dummy_group_message_session(1111, 'member', 2345), 'vanilla.ping')
    assert not permission_manager.validate(get_dummy_group_message_session(1111, 'member', 2345), 'vanilla.whitelist.reload')
    assert permission_manager.validate(get_dummy_group_message_session(1111, 'member', 2345), 'gtnh.ping')
    assert not permission_manager.validate(get_dummy_group_message_session(1234, 'member', 2345), 'vanilla.ping')
    assert permission_manager.validate(get_dummy_group_message_session(1111, 'member', 2345), 'vanilla.ping')

    assert permission_manager.validate(get_dummy_group_message_session(1111, 'admin', 2345), 'vanilla.ping')
    assert permission_manager.validate(get_dummy_group_message_session(1111, 'admin', 2345), 'vanilla.whitelist.reload')
    assert permission_manager.validate(get_dummy_group_message_session(1111, 'admin', 2345), 'gtnh.ping')
    assert not permission_manager.validate(get_dummy_group_message_session(1234, 'admin', 2345), 'vanilla.ping')
    assert permission_manager.validate(get_dummy_group_message_session(1111, 'admin', 2345), 'vanilla.ping')

    assert not permission_manager.validate(get_dummy_group_message_session(2222, 'member', 2345), 'vanilla.ping')

    assert permission_manager.validate(get_dummy_private_message_session(2222), 'vanilla.ping')
    assert not permission_manager.validate(get_dummy_private_message_session(2223), 'vanilla.ping')
    assert permission_manager.validate(get_dummy_private_message_session(2222), 'vanilla.whitelist.reload')
    assert not permission_manager.validate(get_dummy_private_message_session(2223), 'vanilla.whitelist.reload')
