import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.core.keyboard import AdminFactory
from bot.core.filters import IsAdmin


admin_router = Router()

@admin_router.message(Command('admin'), IsAdmin())
async def started(message: Message):
    await message.answer(
        'Ласкаво просимо !',
        reply_markup=AdminFactory.main_menu_keyboard()
    )
@admin_router.callback_query(AdminFactory.filter(F.action=='admin-panel'), IsAdmin())
async def started(callback: CallbackQuery):

    try:
        await callback.message.edit_text(
            'Адмін панель',
            reply_markup=AdminFactory.main_menu_keyboard()
        )
    except Exception:
        await callback.message.delete()
        await callback.message.answer(
            'Адмін панель',
            reply_markup=AdminFactory.main_menu_keyboard()
        )


@admin_router.message(Command('id'), IsAdmin())
async def started(message: Message):
    await message.answer(
        f'ID chat: {message.chat.id}'
    )