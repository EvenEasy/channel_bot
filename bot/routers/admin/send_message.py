import asyncio
from contextlib import suppress

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from bot.core.fsm import SendMessageEveryone
from bot.core.database import DataBase
from bot.core.keyboard import AdminFactory

sendmessage_router = Router()


@sendmessage_router.callback_query(AdminFactory.filter(F.action=='send-message-everyone'))
async def mass_send_message(callback: CallbackQuery, state: FSMContext):
    # set state
    await state.set_state(SendMessageEveryone.enter_message)

    # answer
    await callback.answer()
    await callback.message.answer(
        "Введіть своє оголошення на розсилку:",
        reply_markup=AdminFactory.cancel_button()
    )

@sendmessage_router.message(SendMessageEveryone.enter_message)
async def enter_message(message: Message, state: FSMContext):
    # finish state
    await state.clear()

    if message.text=='Скасувати':
        await message.answer("АДМІН ПАНЕЛЬ", reply_markup=AdminFactory.main_menu_keyboard())
        return

    # answer
    await message.answer("Все вірно?", reply_markup=ReplyKeyboardRemove())
    await message.copy_to(
        message.from_user.id,
        reply_markup=AdminFactory.confirm_send()
    )

@sendmessage_router.callback_query(F.data=='confirm-mass-send-message')
async def confirm_send(callback: CallbackQuery, _db: DataBase):

    # get list chats/users to send
    chats = await _db.users.get_all()

    await callback.message.answer("Починаю розсилку")
    await callback.answer()
    await callback.message.delete_reply_markup()

    # send message everyone
    count_sucess_sent = 0

    for chat in chats:
        with suppress(Exception):
            await callback.message.copy_to(
                chat.user_id,
                caption=callback.message.html_text.format(user=chat)
            )
            count_sucess_sent+=1
            await asyncio.sleep(0.12)

    # sucessful
    await callback.message.answer(
        "✔ Розсилку завершино !\n"
        "Результат:\n"
        f"відправлено: {count_sucess_sent}/{len(chats)}"
    )

@sendmessage_router.callback_query(F.data=='close-message')
async def close_message(callback: CallbackQuery):
    # delete message
    await callback.message.delete()

