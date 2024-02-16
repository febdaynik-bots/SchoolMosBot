import datetime
import typing

from school_mos.main import AUTH

from utils.dnevnik.async_.base import AsyncBaseClass
from utils.dnevnik.types import RankShortType, SubjectRankType


class Rating(AsyncBaseClass):
	def __init__(self, api_instance: AUTH):
		super().__init__(api_instance)

	async def get(self) -> typing.List[RankShortType]:

		end_date = datetime.datetime.now()
		start_date_text = (end_date - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
		end_date_text = end_date.strftime('%Y-%m-%d')

		result = await self._request(f'https://school.mos.ru/api/ej/rating/v1/rank/rankShort',
							method='get',
							params={'personId': self.user.person_id, 'beginDate': start_date_text,
									'endDate': end_date_text},
							headers=self._get_headers())

		return [RankShortType(**i) for i in result]

	async def get_by_subject(self) -> typing.List[SubjectRankType]:

		date = datetime.datetime.now().strftime('%Y-%m-%d')

		result = await self._request(f'https://school.mos.ru/api/ej/rating/v1/rank/subjects',
						 method='get',
						 params={'personId': self.user.person_id, 'date': date},
						 headers=self._get_headers())

		return [SubjectRankType(**i) for i in result]
