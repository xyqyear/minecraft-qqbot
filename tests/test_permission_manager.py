from plugins.mc.permissions import PermissionManager


def test_register():
    permission_manager = PermissionManager()
    permission_manager.register('ping')
    permission_manager.register('whitelist')
    permission_manager.register('whitelist.list')
    permission_manager.register('whitelist.reload')
    permission_manager.register('perm.node1.node2')
    permission_manager.register('perm.node2')

    permission_dict = {'ping': dict(),
                       'whitelist': {'list': dict(), 'reload': dict()},
                       'perm': {'node1': {'node2': {}}, 'node2': {}}}

    assert permission_manager.all_permissions == permission_dict


def test_expand_permission():
    permission_manager = PermissionManager()
    permission_manager.all_permissions = {'ping': dict(),
                                          'whitelist': {'list': dict(), 'reload': dict()}}

    assert permission_manager.expand_permission('*', ('vanilla', 'gtnh')) == {'vanilla.whitelist.reload',
                                                                              'gtnh.whitelist.list',
                                                                              'vanilla.ping',
                                                                              'vanilla.whitelist.list',
                                                                              'gtnh.whitelist.reload',
                                                                              'gtnh.ping'}

    assert permission_manager.expand_permission('*.whitelist', ('vanilla', 'gtnh')) == {'vanilla.whitelist.reload',
                                                                                        'vanilla.whitelist.list',
                                                                                        'gtnh.whitelist.reload',
                                                                                        'gtnh.whitelist.list'}

    assert permission_manager.expand_permission('*.whitelist.*', ('vanilla', 'gtnh')) == {'vanilla.whitelist.reload',
                                                                                          'vanilla.whitelist.list',
                                                                                          'gtnh.whitelist.reload',
                                                                                          'gtnh.whitelist.list'}

    assert permission_manager.expand_permission('vanilla.whitelist', ('vanilla', 'gtnh')) == {
                                                                                            'vanilla.whitelist.reload',
                                                                                            'vanilla.whitelist.list'}

    assert permission_manager.expand_permission('vanilla.whitelist.*', ('vanilla', 'gtnh')) == {
                                                                                            'vanilla.whitelist.reload',
                                                                                            'vanilla.whitelist.list'}

    assert permission_manager.expand_permission('vanilla.whitelist.reload', ('vanilla', 'gtnh')) == {
                                                                                            'vanilla.whitelist.reload'}


def test_load_user_permission():
    permission_manager = PermissionManager()
    permission_manager.all_permissions = {'ping': dict(),
                                          'whitelist': {'list': dict(), 'reload': dict()}}

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
