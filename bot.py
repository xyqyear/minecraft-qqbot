from config_manager import config
from adapter import bot
import logging

if __name__ == '__main__':
    config.load()
    bot.init()
    logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)

    from bot_plugins import mc, server2group

    bot.launch_blocking()
