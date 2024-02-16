import typing
import json

import asyncio
import aiohttp
from school_mos import errors


# Придётся сделать свой класс для авторизации юзера без запросов к сайту
class BaseNotify:
	def __init__(self, token: str, user_id: int):
		self.token = token
		self.user_id = user_id

	async def _request(self, url: str, method: str = 'get', params: dict = None, data: dict = None,
						   headers: dict = None) -> typing.Union[dict, list]:
		try:
			async with aiohttp.ClientSession() as session:
				async with session.request(url=url, method=method, params=params, json=data,
												 headers=headers) as resp:
					raw_result = await resp.text()
		except asyncio.TimeoutError:
			raise "Request timeout error"
		except aiohttp.ClientError as e:
			raise f"{type(e).__name__}: {e}"

		return await self._check_result(status_code=resp.status, result=raw_result)

	def _get_headers(self):
		return {
			"Cookie": f"auth_token={self.token};student_id={self.user_id}",
			'Auth-Token': self.token,
			'x-mes-subsystem': "familyweb"
		}

	async def _check_result(self, status_code, result: str) -> dict:
		try:
			result_json = json.loads(result)
		except (json.JSONDecoder, json.JSONDecodeError) as e:
			raise 'Ошибка json: %s' % e

		if status_code != 200:
			raise errors.RequestError(status_code, result_json)

		if not result_json:
			raise errors.NullFieldError

		if isinstance(result_json, dict):
			if result_json.get('error'):
				raise 'Ошибка сервера: %s' % result_json.get('error')

		return result_json
