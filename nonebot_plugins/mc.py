import inspect
from nonebot import on_command, CommandSession

from nonebot_plugins.mc.permissions import permission_manager
from nonebot_plugins.mc.utils import send_command, get_server
from mc_commands import list, whitelist, restart, ban, unban, banlist, say

commands = {'ping': list,
            'list': list,
            'whitelist': whitelist,
            'restart': restart,
            'ban': ban,
            'unban': unban,
            'pardon': unban,
            'banlist': banlist,
            's': say,
            'say': say}

# registering permissions
permissions = set()
for _, command in commands.items():
    for permission in command.permissions:
        permissions.add(permission)

for permission in permissions:
    permission_manager.register(permission)

permission_manager.load_user_permissions()

# binding commands
for command in commands.keys():
    @on_command(command,  only_to_me=False)
    async def _(session: CommandSession):
        chat_command = session.cmd.name[0]
        chat_args, server_names = get_server(session.current_arg_text.strip())
        if inspect.iscoroutinefunction(commands[chat_command].get_command):
            mc_command, permission = await commands[chat_command].get_command(session, chat_args)
        else:
            mc_command, permission = commands[chat_command].get_command(session, chat_args)

        # if mc_command is empty, it means permission string is an error string
        if not mc_command:
            if permission:
                await session.send(permission)
            return

        for server_name in server_names:
            # permission string returned does not include server name
            s_permission = f'{server_name}.{permission}'
            # if the person has the required permission, then perform the command on corresponding server
            # and parse the response from the server and send it to the source
            if permission_manager.validate(session, s_permission):
                response = await send_command(server_name, mc_command)
                parsed_response = commands[chat_command].parse_response(permission, response)
                if parsed_response:
                    await session.send(parsed_response)
            # could be used for no permission exception
            else:
                await session.send('You have no permission to run this command.')
