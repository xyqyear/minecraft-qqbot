import inspect
from nonebot import on_command, CommandSession

from plugins.mc.permissions import permission_manager
from plugins.mc import command_list, command_whitelist, command_restart, \
    command_ban, command_unban, command_banlist, command_say
from plugins.mc.utils import send_command, get_server

commands = {'ping': command_list,
            'list': command_list,
            'whitelist': command_whitelist,
            'restart': command_restart,
            'ban': command_ban,
            'unban': command_unban,
            'pardon': command_unban,
            'banlist': command_banlist,
            's': command_say,
            'say': command_say}

# permissions should be loaded after modules registered all the permissions
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
