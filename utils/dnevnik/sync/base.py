import requests
import typing
import json

from school_mos import errors
from school_mos.main import AUTH


class BaseClass:

	def __init__(self, api_instance: AUTH, session: typing.Optional[requests.Session] = None):
		self.user = api_instance

		if session is None:
			session = requests.sessions.Session()
		self.session = session

	def _request(self, url: str, method: str = 'get', params: dict = None, data: dict = None,
					   headers: dict = None) -> typing.Union[dict, list]:
		result = self.session.request(method, url, params=params, json=data, headers=headers, timeout=(15, 30))
		return self._check_result(result)

	def _get_headers(self):
		return {
			"Cookie": f"auth_token={self.user.token};student_id={self.user.user_id}",
			'Auth-Token': self.user.token,
			'x-mes-subsystem': "familyweb"
		}

	def _check_result(self, result: requests.models.Response) -> requests.models.Response:
		try:
			result_json = result.json()
		except (json.JSONDecoder, json.JSONDecodeError) as e:
			raise 'Ошибка json: %s' % e

		if result.status_code != 200:
			raise errors.RequestError(result.status_code, result_json)

		if not result_json:
			raise errors.NullFieldError

		if isinstance(result_json, dict):
			if result_json.get('error'):
				raise 'Ошибка сервера: %s' % result_json.get('error')

		return result_json
