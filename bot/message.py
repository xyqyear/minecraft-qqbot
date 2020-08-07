from graia.application import MessageChain


class Message:
    def __init__(self, bot, raw_message: MessageChain, _type: str, message_text: str, sender_id: int,
                 command: str = None, args: str = None, sender_role: str = None, group_id: int = None):
        self.bot = bot
        self.raw_message = raw_message
        self.message = message_text
        self.sender_id = sender_id
        self.command = command
        self.args = args
        if _type == 'private':
            self.type = 'private'
        elif _type == 'group':
            self.type = 'group'
            self.sender_role = sender_role
            self.group_id = group_id

    async def send_back(self, message: str):
        if self.type == 'private':
            await self.bot.send_private_message(self.sender_id, message)
        elif self.type == 'group':
            await self.bot.send_group_message(self.group_id, message)

    async def send_back_raw(self, message: MessageChain):
        if self.type == 'private':
            await self.bot.send_private_message(self.sender_id, message)
        elif self.type == 'group':
            await self.bot.send_group_message(self.group_id, message)
