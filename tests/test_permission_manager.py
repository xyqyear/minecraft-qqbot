from permissions import PermissionManager
import nonebot
import pytest


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


def get_dummy_group_session(group_id, sender_role, sender_id):
    event = nonebot.command.CQEvent()
    event['post_type'] = 'message'
    event['message_type'] = 'group'
    event['group_id'] = group_id
    event['sender'] = {'user_id': sender_id, 'role': sender_role}
    return nonebot.CommandSession(nonebot.NoneBot(), event,
                                  nonebot.command.Command(name=('',), func=lambda x: x, permission=0, only_to_me=False,
                                                          privileged=False))


def get_dummy_discuss_session(discuss_id, sender_id):
    event = nonebot.command.CQEvent()
    event['post_type'] = 'message'
    event['message_type'] = 'discuss'
    event['discuss_id'] = discuss_id
    event['sender'] = {'user_id': sender_id}
    return nonebot.CommandSession(nonebot.NoneBot(), event,
                                  nonebot.command.Command(name=('',), func=lambda x: x, permission=0, only_to_me=False,
                                                          privileged=False))


def get_dummy_private_session(sender_id):
    event = nonebot.command.CQEvent()
    event['post_type'] = 'message'
    event['message_type'] = 'private'
    event['sender'] = {'user_id': sender_id}
    return nonebot.CommandSession(nonebot.NoneBot(), event,
                                  nonebot.command.Command(name=('',), func=lambda x: x, permission=0, only_to_me=False,
                                                          privileged=False))


@pytest.mark.asyncio
async def test_permission_validate():
    permission_manager = PermissionManager()
    permission_manager.user_permissions = {
        'group': {1111: {'default': {'vanilla.ping', 'vanilla.whitelist.list', 'gtnh.ping'},
                         'admin': {'vanilla.whitelist.reload', 'vanilla.whitelist.list'}}},
        'private': {2222: {'vanilla.whitelist.reload', 'gtnh.whitelist.list', 'vanilla.ping',
                           'vanilla.whitelist.list', 'gtnh.whitelist.reload', 'gtnh.ping'}}}

    assert permission_manager.validate(get_dummy_group_session(1111, 'member', 2345), 'vanilla.ping')
    assert not permission_manager.validate(get_dummy_group_session(1111, 'member', 2345), 'vanilla.whitelist.reload')
    assert permission_manager.validate(get_dummy_group_session(1111, 'member', 2345), 'gtnh.ping')
    assert not permission_manager.validate(get_dummy_group_session(1234, 'member', 2345), 'vanilla.ping')
    assert permission_manager.validate(get_dummy_group_session(1111, 'member', 2345), 'vanilla.ping')

    assert not permission_manager.validate(get_dummy_group_session(2222, 'member', 2345), 'vanilla.ping')

    assert permission_manager.validate(get_dummy_discuss_session(3333, 2222), 'vanilla.ping')
    assert not permission_manager.validate(get_dummy_discuss_session(3333, 2223), 'vanilla.ping')
    assert permission_manager.validate(get_dummy_discuss_session(3333, 2222), 'vanilla.whitelist.reload')
    assert not permission_manager.validate(get_dummy_discuss_session(3333, 2223), 'vanilla.whitelist.reload')

    assert permission_manager.validate(get_dummy_private_session(2222), 'vanilla.ping')
    assert not permission_manager.validate(get_dummy_private_session(2223), 'vanilla.ping')
    assert permission_manager.validate(get_dummy_private_session(2222), 'vanilla.whitelist.reload')
    assert not permission_manager.validate(get_dummy_private_session(2223), 'vanilla.whitelist.reload')
