import typing

from school_mos.main import AUTH

from utils.dnevnik.async_.base import AsyncBaseClass
from utils.dnevnik.types import SubjectMarksType


class Marks(AsyncBaseClass):
	def __init__(self, api_instance: AUTH):
		super().__init__(api_instance)

	async def get_by_lesson(self) -> typing.List[SubjectMarksType]:

		result = await self._request(f'https://school.mos.ru/api/family/web/v1/subject_marks',
							method='get', params={'student_id': self.user.user_id},
							headers=self._get_headers())

		return [SubjectMarksType(**res) for res in result['payload']]

	async def get_by_id(self, subject_id: int) -> SubjectMarksType:
		result = await self._request(f'https://school.mos.ru/api/family/web/v1/subject_marks/for_subject',
							method='get', params={'student_id': self.user.user_id, 'subject_id': subject_id},
							headers=self._get_headers())

		return SubjectMarksType(**result)
