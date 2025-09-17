from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup


class UserFactory(CallbackData, prefix='u'):
    action: str
    value: str = '0'
    
    @staticmethod
    def join_button() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        builder.button(text="Планую почати навчання 🤔", callback_data=UserFactory(action='iam', value='0'))
        builder.button(text="Навчаюсь в автошколі (Теорія)🏫", callback_data=UserFactory(action='iam', value='1'))
        builder.button(text="Складаю теорію 💻", callback_data=UserFactory(action='iam', value='2'))
        builder.button(text="Складаю іспит з водіння 🚦", callback_data=UserFactory(action='iam', value='3'))
        builder.button(text="У мене є права !!! 🚘", callback_data=UserFactory(action='iam', value='4'))
        
        builder.adjust(1)
        
        return builder.as_markup()

