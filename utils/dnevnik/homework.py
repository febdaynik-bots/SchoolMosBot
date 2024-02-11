import datetime
import re
import typing

import requests
import aiohttp
from school_mos.main import _Homework, AUTH, HW_ATTACHMENTS_URL
from school_mos.Types import HouseworkType
from school_mos import errors


async def get_week_boundaries(date: datetime.date):
	# Определяем первый день недели (понедельник)
	start_of_week = date - datetime.timedelta(days=date.weekday())

	# Определяем последний день недели (воскресенье)
	end_of_week = start_of_week + datetime.timedelta(days=6)

	return start_of_week.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d')


class CustomHomework(_Homework):
	def __init__(self, api_instance: AUTH, session_aiohttp: aiohttp.ClientSession = None):
		super().__init__(api_instance)
		self.aiohttp = session_aiohttp

	async def __get_homework(self, data):
		result = list()
		if data.status_code != 200:
			raise errors.RequestError(data.status_code)

		payload = data.json()['payload']

		if not payload:
			raise errors.NullFieldError

		for item in payload:
			material = item.get('additional_materials', [{}])
			result.append(
				HouseworkType(
					subject_name=item.get('subject_name', ''),
					description=re.sub(r'\n{2,}', '\n', item["description"]),
					attached_files=[HW_ATTACHMENTS_URL.format(item['link']) for shit in material
									if shit['type'] == 'attachments' for item in shit['items']],
					attached_tests=[HW_ATTACHMENTS_URL.format(item['urls'][0]['url']) for shit in material
									if shit['type'] == 'test_spec_binding' for item in shit['items']]
				)
			)
		return result

	async def get_by_week(self, current_date: typing.Optional[datetime.date] = None):
		if current_date is None:
			current_date = datetime.datetime.now()

		# В случае если это суббота или воскресенье, то домашнее задание будет смотреться с понедельника
		if current_date.weekday() == 5:
			current_date + datetime.timedelta(days=2)
		elif current_date.weekday() == 6:
			current_date + datetime.timedelta(days=1)

		start_of_week, end_of_week = await get_week_boundaries(current_date)
		data = requests.get(
			f"https://school.mos.ru/api/family/web/v1/homeworks?from={start_of_week}&"
			f"to={end_of_week}&"
			f"student_id={self.user.user_id}",
			headers={
				"Cookie": f"auth_token={self.user.token};student_id={self.user.user_id}",
				'Auth-Token': self.user.token,
				'x-mes-subsystem': "familyweb"
			}
		)
		return (
			await self.__get_homework(data=data),
			start_of_week,
			end_of_week
		)

	async def get_by_date(self, date_offset: int = 0):
		date_to_get = datetime.date.today() + datetime.timedelta(days=date_offset)

		data = requests.get(
			f"https://school.mos.ru/api/family/web/v1/homeworks?from={date_to_get}&to={date_to_get}&"
			f"student_id={self.user.user_id}",
			headers={
				"Cookie": f"auth_token={self.user.token};student_id={self.user.user_id}",
				'Auth-Token': self.user.token,
				'x-mes-subsystem': "familyweb"
			}
		)
		return await self.__get_homework(data=data)
