import nonebot
from os import path

import bot_config
from config_manager import config

if __name__ == '__main__':
    # config init
    config.load()

    # nonebot init
    nonebot.init(bot_config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'nonebot_plugins'),
        'nonebot_plugins'
    )

    nonebot.run()
