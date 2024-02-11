import typing

from aiogram import types
from aiogram.filters import BaseFilter

from database.models import Users


class IsAccessUserFilter(BaseFilter):
    def __init__(self, is_access: bool = True):
        self.is_access = is_access

    async def __call__(self, message: typing.Union[types.Message, types.CallbackQuery], user: Users) -> bool:
        return self.is_access is bool(user.token)
