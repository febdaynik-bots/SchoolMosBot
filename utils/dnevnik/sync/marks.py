import typing

import requests
from school_mos.main import AUTH

from utils.dnevnik.sync.base import BaseClass
from utils.dnevnik.types import SubjectMarksType


class CustomMarks(BaseClass):
	def __init__(self, api_instance: AUTH, session: typing.Optional[requests.Session] = None):
		super().__init__(api_instance, session)

	def get_by_lesson(self) -> typing.Tuple[SubjectMarksType]:

		result = self._request(f'https://school.mos.ru/api/family/web/v1/subject_marks',
							method='get', params={'student_id': self.user.user_id},
							headers=self._get_headers())

		tuple_result = (SubjectMarksType(**res) for res in result['payload'])

		return tuple_result

	def get_by_id(self, subject_id: int) -> SubjectMarksType:
		result = self._request(f'https://school.mos.ru/api/family/web/v1/subject_marks/for_subject',
							method='get', params={'student_id': self.user.user_id, 'subject_id': subject_id},
							headers=self._get_headers())

		return SubjectMarksType(**result)
