from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from database.models import Users


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

		return await handler(event, data)
