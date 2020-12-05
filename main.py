import os
import nonebot
import logging

from config_manager import config

if __name__ == '__main__':
    config.load()
    nonebot.init()
    nonebot.load_plugins(
        os.path.join(os.path.dirname(__file__), 'bot_plugins'),
        'bot_plugins'
    )

    logging.getLogger().setLevel(logging.WARNING)

    nonebot.run(host=config.bot_listen_host, port=config.bot_listen_port)
