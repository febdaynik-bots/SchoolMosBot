import datetime
import typing

from utils.dnevnik.types import Marks, HouseworkTypeByNotify
from utils.dnevnik.notify.base import BaseNotify
from utils.get_week_days import async_get_week_boundaries


class Notifications(BaseNotify):

	def __init__(self, token: str, user_id: int):
		super().__init__(token, user_id)

	async def _get_week(self):
		current_date = datetime.datetime.now()
		return await async_get_week_boundaries(current_date)

	async def get_homework(self, string_date: str) -> typing.List[HouseworkTypeByNotify]:
		start_of_week, end_of_week = await self._get_week()

		try:
			result = await self._request("https://school.mos.ru/api/family/web/v1/homeworks",
									   method='get',
									   params={'from': start_of_week, 'to': end_of_week, 'student_id': self.user_id},
									   headers=self._get_headers())
		except Exception:
			return []

		return [
			HouseworkTypeByNotify(**res) for res in result['payload']
			if datetime.datetime.strptime(
				# res['date_assigned_on'],
				res['date'],
				'%Y-%m-%d') >= datetime.datetime.strptime(string_date, '%Y-%m-%d')
		]

	async def get_marks(self, string_date: str) -> typing.List[Marks]:
		start_of_week, end_of_week = await self._get_week()

		try:
			result = await self._request(f'https://school.mos.ru/api/family/web/v1/marks',
										 method='get',
										 params={'student_id': self.user_id, 'from': start_of_week, 'to': end_of_week},
										 headers=self._get_headers())
		except Exception:
			return []

		return [
			Marks(**res) for res in result['payload']
			if datetime.datetime.strptime(datetime.datetime.strptime(
				res['created_at'],
				'%Y-%m-%dT%H:%M:%S'
			).strftime('%Y-%m-%d'), '%Y-%m-%d') >= datetime.datetime.strptime(string_date, '%Y-%m-%d')
		]

	def to_json(self, model):
		if isinstance(model, list):
			return [dict(m) for m in model]

		return model.model_dump_json()
