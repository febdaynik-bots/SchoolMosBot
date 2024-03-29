from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from school_mos import AUTH

# from config import aiohttp_session
from database.models import Users
from utils.dnevnik.async_ import Homework, Marks


class UsersMiddleware(BaseMiddleware):
	async def __call__(
			self,
			handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
			event: Union[Message, CallbackQuery],
			data: Dict[str, Any],
	) -> Any:

		user = Users.get_or_none(user_id=event.from_user.id)

		if user is None:
			user = Users.create(user_id=event.from_user.id, first_name=event.from_user.first_name,
								username=event.from_user.username)

		data['user'] = user
		if user.token is not None:
			try:
				student = AUTH(token=user.token)
				student.homework = Homework(student)
				student.marks = Marks(student)
			except Exception:
				student = None
		else:
			student = None

		data['student'] = student

		return await handler(event, data)
