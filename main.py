from config_manager import config
from bot.adapter import bot
import logging

if __name__ == '__main__':
    config.load()
    bot.init()
    logging.getLogger().setLevel(logging.WARNING)

    from bot_plugins import mc, server2group, repeat

    bot.launch_blocking()
