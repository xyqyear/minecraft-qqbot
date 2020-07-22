import nonebot
from aiocqhttp.exceptions import Error as CQHttpError

from config_manager import config
from utils.file_utils import async_get_new_content
from utils.mc_utils import parse_logs, send_command


@nonebot.scheduler.scheduled_job('interval', seconds=1)
async def _():
    new_logs = await async_get_new_content(config.log_path)
    if not new_logs:
        return

    new_messages = parse_logs(new_logs)
    if not new_messages:
        return

    bot = nonebot.get_bot()
    for name, message in new_messages:
        print(f'<{name}> {message}')
        try:
            await bot.send_group_msg(group_id=config.default_group,
                                     message=f'<{name}> {message}')
        except CQHttpError:
            await send_command(config.default_server, f'message "{message}" failed to send')
