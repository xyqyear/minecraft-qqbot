import os
import inspect
import importlib

from adapter import bot
from message import Message
from permissions import permission_manager
from utils.mc_utils import send_command, get_server

# loading commands from .py files
commands = dict()

for module_filename in os.listdir('mc_commands'):
    if module_filename.endswith('.py'):
        module_name = module_filename[:-3]
        module = importlib.import_module(f'mc_commands.{module_name}')
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
    @bot.on_command(command)
    async def _(message: Message):
        chat_command = message.command
        chat_args, server_names = get_server(message.args)
        if inspect.iscoroutinefunction(commands[chat_command].get_command):
            mc_command, permission = await commands[chat_command].get_command(message)
        else:
            mc_command, permission = commands[chat_command].get_command(message)

        # if mc_command is empty, it means permission string is an error string
        if not mc_command:
            if permission:
                await message.send_back(permission)
            return

        for server_name in server_names:
            # permission string returned does not include server name
            s_permission = f'{server_name}.{permission}'
            # if the person has the required permission, then perform the command on corresponding server
            # and parse the response from the server and send it to the source
            if permission_manager.validate(message, s_permission):
                response = await send_command(server_name, mc_command)
                parsed_response = commands[chat_command].parse_response(permission, response)
                if parsed_response:
                    await message.send_back(parsed_response)
            # could be used for no permission exception
            else:
                await message.send_back('You have no permission to run this command.')
