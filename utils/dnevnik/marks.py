import typing

from school_mos.main import AUTH

from utils.dnevnik.base import BaseClass
from .types import SubjectMarksType


class CustomMarks(BaseClass):
	def __init__(self, api_instance: AUTH):
		super().__init__(api_instance)

	async def get_by_lesson(self) -> typing.Tuple[SubjectMarksType]:

		result = await self._request(f'https://school.mos.ru/api/family/web/v1/subject_marks',
							method='get', params={'student_id': self.user.user_id},
							headers={
								"Cookie": f"auth_token={self.user.token};student_id={self.user.user_id}",
								'Auth-Token': self.user.token,
								'x-mes-subsystem': "familyweb"
							})

		tuple_result = (SubjectMarksType(**res) for res in result['payload'])

		return tuple_result

	async def get_by_id(self, subject_id: int):
		...
