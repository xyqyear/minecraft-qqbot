from plugins.mc.permissions import permission_manager
from plugins.mc import no_session

permission_manager.register('ping')


@no_session
def get_command(args):
    return 'list', 'ping'


def parse_response(response):
    return response
