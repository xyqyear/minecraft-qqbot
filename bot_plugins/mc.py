import os
import nonebot
import inspect
import importlib

from mc.permissions import permission_manager
from utils.mc_utils import send_command
from mc.parsers import ParsedMessage
from nonebot import on_command, CommandSession

# loading commands from .py files
commands = dict()

for module_filename in os.listdir('mc/commands'):
    if module_filename.endswith('.py'):
        module_name = module_filename[:-3]
        module = importlib.import_module(f'mc.commands.{module_name}')
        for command_name in module.commands:
            commands[command_name] = module


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
    @on_command(command, only_to_me=False)
    async def _(session: CommandSession):
        parsed_message = ParsedMessage(session)
        if inspect.iscoroutinefunction(commands[parsed_message.command].get_command):
            mc_command, permission = await commands[parsed_message.command].get_command(session, parsed_message)
        else:
            mc_command, permission = commands[parsed_message.command].get_command(session, parsed_message)

        # if mc_command is empty, it means permission string is an error or a custom response
        if not mc_command:
            if permission:
                await session.send(permission)
            return

        # permission string returned does not include server name
        full_permission = f'{parsed_message.server}.{permission}'
        # if the person has the required permission, then perform the command on corresponding server
        # and parse the response from the server and send it to the source
        if permission_manager.validate(session, full_permission):
            try:
                response = await send_command(parsed_message.server, mc_command)
            except:
                await session.send(f'"{session.event.message}" failed.')
                return
            parsed_response = commands[parsed_message.command].parse_response(permission, response)
            if parsed_response:
                await session.send(f'[{parsed_message.server}] {parsed_response}')
        # could be used for no permission exception
        else:
            await session.send('You dont\'t have the permission to run this command.')
