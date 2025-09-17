from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.core.database import DataBase


main_router = Router()


@main_router.message(Command('start'))
async def started(message: Message, state: FSMContext, _db: DataBase):

    # send welocme message
    await message.answer(
        "<b>de Інструктор</b> 🚘\n\n"
        "Тести та правила дорожнього руху 2025 у спрощеній формі🚘\n"
        "Тренеруйтесь до іспитів разом із нами та керуйте авто впевнено🛞"
    )

    # clear state if exists
    await state.clear()

    # save user
    await _db.users.create(message.from_user.id, message.from_user.username, message.from_user.full_name)

