class Message:
    def __init__(self, bot, _type: str, message_text: str, command: str, args: str,
                 sender_id: int, sender_role: str = None, group_id: int = None):
        self.bot = bot
        self.message = message_text
        self.command = command
        self.args = args
        self.sender_id = sender_id
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
