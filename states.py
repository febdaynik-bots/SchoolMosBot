from aiogram.fsm.state import State, StatesGroup


class AuthUserState(StatesGroup):
	login = State()
	password = State()

