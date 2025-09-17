from aiogram.fsm.state import State, StatesGroup


class SendMessageEveryone(StatesGroup):
    enter_message = State()
    confirm = State()
