# this module high depends on graia and mirai
# might need to add some feature to adapter
# to ensure it works after changing framework

from graia.application import MessageChain, Image
from graia.application.message.elements.internal import Plain

from bot.adapter import bot
from bot.message import Message
from config_manager import config

last_n_messages = dict()

if config.repeat['enable']:
    @bot.on_message()
    async def repeat(message: Message):
        if message.type != 'group':
            return

        if message.group_id not in last_n_messages:
            last_n_messages[message.group_id] = list()

        last_n_messages[message.group_id].append(message.raw_message)
        last_n_messages_chopped = [to_comparable(i) for i in last_n_messages[message.group_id]]

        if len(last_n_messages_chopped) == config.repeat['threshold'] + 1:
            if last_n_messages_chopped[0] == last_n_messages_chopped[1]:
                del last_n_messages[message.group_id][0]
                return

            repeat_flag = True
            for each_message in last_n_messages_chopped[2:]:
                if each_message != last_n_messages_chopped[1]:
                    repeat_flag = False
            if repeat_flag:
                if config.repeat['reverse']:
                    await message.send_back_raw(message_reverse(message.raw_message))
                else:
                    await message.send_back_raw(message.raw_message)

            del last_n_messages[message.group_id][0]


def message_reverse(message: MessageChain):
    for component in message.__root__[1:]:
        if isinstance(component, Plain):
            component.text = component.text[::-1]

    return MessageChain(__root__=message.__root__[1:][::-1])


def to_comparable(message: MessageChain):
    compare_str = ''
    for component in message.__root__[1:]:
        if isinstance(component, Image):
            compare_str += component.imageId
        elif isinstance(component, Plain):
            compare_str += component.text
        else:
            compare_str += str(component)
    return compare_str
