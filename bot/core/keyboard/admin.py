from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton


class AdminFactory(CallbackData, prefix='a'):
    action: str
    value: str = '0'
    
    @staticmethod
    def main_menu_keyboard():
        builder = InlineKeyboardBuilder()

        builder.button(text='📤 Розсилка', callback_data=AdminFactory(action='send-message-everyone'))
        builder.button(text='Редагувати ✏', callback_data=AdminFactory(action='edit-lables'))

        builder.adjust(2)

        return builder.as_markup()
    
    @staticmethod
    def cancel_button():
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Скасувати')]
            ],
            resize_keyboard=True
        )

    @staticmethod
    def cancel_and_clear_button():
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Скасувати'), KeyboardButton(text='Очистити')]
            ],
            resize_keyboard=True
        )

    @staticmethod
    def support_keyboard(chat_id: str):
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Відповісти", callback_data=f"answer_user_{chat_id}")]])

    @staticmethod
    def confirm_send():
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='📨 Розіслати', callback_data='confirm-mass-send-message')],
            [InlineKeyboardButton(text='Видалити ❌', callback_data='close-message')]
        ])

    @staticmethod
    def lables(ls: str):
        builder = InlineKeyboardBuilder()

        for lable in ls:
            builder.button(text=lable, callback_data=AdminFactory(action='edit-lable', value=lable))

        builder.button(text='Назад 🔙', callback_data=AdminFactory(action='admin-panel'))

        builder.adjust(1)

        return builder.as_markup()

