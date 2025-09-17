import asyncio
import logging
from aiogram import Router, Bot, F
from aiogram.types import ChatJoinRequest, CallbackQuery

from bot.core.keyboard import UserFactory
from bot.core.database import DataBase
from bot.core.scheduler import Scheduler


channel_join_router = Router()


@channel_join_router.chat_join_request() #(F.chat.id==Config.get_channel_id())
async def channel_request(request: ChatJoinRequest, bot: Bot, _db: DataBase, _scheduler: Scheduler):
    source_link = request.invite_link.invite_link.removeprefix('https://t.me/').removesuffix('...')
    logging.debug(request.invite_link)

    logging.debug(f'channel id: {request.chat.id} from {source_link}')

    # sent message to confirm request    
    await bot.send_message(
        request.from_user.id,
        "<b>de Інструктор</b> 🚘\n\n"
        "Тести та правила дорожнього руху 2025 у спрощеній формі🚘\n"
        "Тренеруйтесь до іспитів разом із нами та керуйте авто впевнено🛞\n\n"
        
        "Які у вас ",
        reply_markup=UserFactory.join_button()
    )

    # save user
    await _db.users.create(request.from_user.id, request.from_user.username, request.from_user.full_name, source_link)

    # wait approve
    await _scheduler.schedule_approve(request.from_user.id, request.chat.id, seconds=55, job_id=f'r_{request.from_user.id}')
    await _scheduler.schedule_message_once(
        chat_id=request.from_user.id,
        text=f"Вітаю, <b>{request.from_user.first_name}</b>!\n"
        "Вашу заявку підтвердили ✅",
        seconds=60,
        job_id=f'm_{request.from_user.id}'
    )

@channel_join_router.callback_query(UserFactory.filter(F.action=='iam'))
async def iam(callback: CallbackQuery, callback_data: UserFactory, _db: DataBase):
    await _db.users.update(callback.from_user.id, {'iam': callback_data.value})
    await callback.answer()
    await callback.message.delete_reply_markup()
