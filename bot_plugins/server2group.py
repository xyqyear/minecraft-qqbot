from config_manager import config
from utils.file_utils import async_get_new_content
from utils.mc_utils import parse_logs, send_command
from adapter import bot


@bot.scheduler.scheduled_job('interval', seconds=1)
async def _():
    new_logs = await async_get_new_content(config.log_path)
    if not new_logs:
        return

    new_messages = parse_logs(new_logs)
    if not new_messages:
        return

    for name, message in new_messages:
        try:
            await bot.send_group_message(config.default_group, f'<{name}> {message}')
        except:
            await send_command(config.default_server, f'say message "{message}" failed to send')
