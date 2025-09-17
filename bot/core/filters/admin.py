from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.core.config import Config


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message):
        return str(message.from_user.id) in Config.get_admins()
