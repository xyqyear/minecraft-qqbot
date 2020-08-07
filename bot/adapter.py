from graia.application.group import MemberPerm
from graia.application.message.elements.internal import Plain
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session, Member, Group, MessageChain, Friend, GroupMessage, \
    FriendMessage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

from bot.message import Message
from config_manager import config


class Bot:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.command_handlers = dict()
        self.bcc = None
        self.app = None
        self.scheduler = AsyncIOScheduler()

    def init(self):
        self.bcc = Broadcast(loop=self.loop)
        self.app = GraiaMiraiApplication(
            broadcast=self.bcc,
            connect_info=Session(
                host=config.bot_host,
                authKey=config.bot_authKey,
                account=config.bot_account,
                websocket=True
            )
        )

    async def group_message_handler(self, message: MessageChain, group: Group, member: Member):
        message_text = message.asDisplay()
        parsed_command = self.parse_command(message_text)
        if not parsed_command:
            return
        command, args = parsed_command

        if member.permission == MemberPerm.Member:
            sender_role = 'member'
        elif member.permission == MemberPerm.Administrator:
            sender_role = 'admin'
        else:
            sender_role = 'owner'

        message = Message(
            bot=self,
            _type='group',
            message_text=message_text,
            command=command,
            args=args,
            sender_id=member.id,
            sender_role=sender_role,
            group_id=group.id
        )

        await self.command_handlers[command](message)

    async def private_message_handler(self, message: MessageChain, friend: Friend):
        message_text = message.asDisplay()
        parsed_command = self.parse_command(message_text)
        if not parsed_command:
            return
        command, args = parsed_command

        message = Message(
            bot=self,
            _type='private',
            message_text=message_text,
            command=command,
            args=args,
            sender_id=friend.id,
        )

        await self.command_handlers[command](message)

    async def send_group_message(self, group_id: int, message: str):
        await self.app.sendGroupMessage(group_id, MessageChain(__root__=[
            Plain(message)
        ]))

    async def send_private_message(self, friend_id: int, message: str):
        await self.app.sendFriendMessage(friend_id, MessageChain(__root__=[
            Plain(message)
        ]))

    def on_command(self, command_str: str):
        def wrapper(f):
            self.command_handlers[command_str] = f
        return wrapper

    def launch_blocking(self):
        self.bcc.receiver(GroupMessage)(self.group_message_handler)
        self.bcc.receiver(FriendMessage)(self.private_message_handler)
        self.scheduler.start()
        self.app.launch_blocking()

    def parse_command(self, message: str, ignore_missing_command=False):
        if not message.startswith('/'):
            return
        if message[1:] in self.command_handlers:
            return message[1:], ''
        command, args = message.split(' ', 1)
        command = command[1:]
        if command in self.command_handlers or ignore_missing_command:
            return command, args


bot = Bot()
