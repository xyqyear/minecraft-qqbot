import nonebot

from config_manager import config
from utils.file_utils import async_get_new_content
from utils.mc_utils import parse_logs, send_command


@nonebot.scheduler.scheduled_job('interval', seconds=1)
async def _():
    bot = nonebot.get_bot()
    for server_name, server_property in config.server_properties.items():
        if server_property['server2group']['enable']:
            new_logs = await async_get_new_content(server_property['server2group']['log_path'])
            if not new_logs:
                continue

            new_messages = parse_logs(new_logs)
            if not new_messages:
                continue

            for name, message in new_messages:
                try:
                    await bot.send_group_msg(group_id=server_property['server2group']['default_group'],
                                             message=f'[{server_name}] <{name}> {message}')
                except:
                    await send_command(server_name, f'say message "{message}" failed to be sent')
