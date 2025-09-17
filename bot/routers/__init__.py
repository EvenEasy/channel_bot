from aiogram import Dispatcher

from .user.main import main_router
from .user.channel_join import channel_join_router

from .admin.main import admin_router
from .admin.send_message import sendmessage_router


def setup_routers(dp: Dispatcher):
    dp.include_routers(
        main_router,
        channel_join_router,
        admin_router,
        sendmessage_router,
    )