import nonebot
from aiocqhttp.exceptions import Error as CQHttpError

from bot_config import DEFAULT_GROUP, LOG_PATH, DEFAULT_SERVER
from utils.file_utils import async_get_new_content
from utils.mc_utils import parse_logs, send_command


@nonebot.scheduler.scheduled_job('interval', seconds=1)
async def _():
    new_logs = await async_get_new_content(LOG_PATH)
    if not new_logs:
        return

    new_messages = parse_logs(new_logs)
    if not new_messages:
        return

    bot = nonebot.get_bot()
    for name, message in new_messages:
        print(f'<{name}> {message}')
        try:
            await bot.send_group_msg(group_id=DEFAULT_GROUP,
                                     message=f'<{name}> {message}')
        except CQHttpError:
            await send_command(DEFAULT_SERVER, f'message "{message}" failed to send')
