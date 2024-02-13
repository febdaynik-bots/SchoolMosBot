import datetime
import re
import typing

import requests
from school_mos.main import _Marks, AUTH, HW_ATTACHMENTS_URL
from school_mos import errors

from utils.get_week_days import get_week_boundaries
from .types import Marks


class CustomMarks(_Marks):
	def __init__(self, api_instance: AUTH):
		super().__init__(api_instance)

	async def __get_marks(self, data):
		...

	async def get_by_(self, current_date: typing.Optional[datetime.date] = None):
		...
