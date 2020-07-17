from utils.coolq_utils import get_sender_id
from utils.request_utils import uuid2name

permissions = ('say', )


async def get_command(session, args: str, command_say_bindings=None):
    if not command_say_bindings:
        from config import COMMAND_SAY_BINDINGS
        command_say_bindings = COMMAND_SAY_BINDINGS

    sender_id = get_sender_id(session)
    if sender_id in command_say_bindings:
        sender_uuid = command_say_bindings[sender_id]
        player_name = await uuid2name(sender_uuid)

        return f'tellraw @a {{"text": "*<{player_name}> {args}", "color": "yellow"}}', 'say'
    else:
        return '', 'You have no in game character bound'


def parse_response(permission, response):
    if response == 'No player was found':
        return 'No player is online'
    else:
        return response
