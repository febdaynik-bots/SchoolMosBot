import datetime
import re
import typing

from school_mos.main import AUTH, HW_ATTACHMENTS_URL

from utils.get_week_days import async_get_week_boundaries
from utils.dnevnik.types import HouseworkType, InfoHouseworkType, Teacher
from utils.dnevnik.async_.base import AsyncBaseClass


def make_dates(start_of_week: str, end_of_week: str) -> str:
	start_of_week_date = datetime.datetime.strptime(start_of_week, '%Y-%m-%d')
	end_of_week_date = datetime.datetime.strptime(end_of_week, '%Y-%m-%d')

	difference = end_of_week_date - start_of_week_date

	list_dates = [(start_of_week_date + datetime.timedelta(days=i+1)).strftime('%Y-%m-%d')
				  for i in range(difference.days)]
	list_dates.extend([start_of_week, end_of_week])

	return ','.join(list_dates)


def get_schedule_id_by_lesson(shorts: list, date: str, subject_id: int, subject_name: str) -> int:
	for short in shorts:
		if short['date'] != date:
			continue

		for lesson in short['lessons']:
			if lesson['subject_id'] == subject_id and lesson['subject_name'] == subject_name:
				return int(lesson['schedule_item_id'])


class Homework(AsyncBaseClass):
	def __init__(self, api_instance: AUTH):
		super().__init__(api_instance)

	async def __get_homework(self, data, shorts: list) -> typing.List[HouseworkType]:
		result = list()

		for item in data:
			material = item.get('additional_materials', [{}])
			item_date = item.get('date')
			item_id = item.get('subject_id', 0)
			item_name = item.get('subject_name', '')
			schedule_item_id = get_schedule_id_by_lesson(shorts, item_date, item_id, item_name)
			result.append(
				HouseworkType(
					subject_id=item_id,
					subject_name=item_name,
					schedule_item_id=schedule_item_id,
					is_done=item.get('is_done'),
					date=item_date,
					description=re.sub(r'\n{2,}', '\n', item["description"]),
					attached_files=[HW_ATTACHMENTS_URL.format(item['link']) for shit in material
									if shit['type'] == 'attachments' for item in shit['items']],
					attached_tests=[HW_ATTACHMENTS_URL.format(item['urls'][0]['url']) for shit in material
									if shit['type'] == 'test_spec_binding' for item in shit['items']]
				)
			)
		return result

	async def get_by_week(self, current_date: typing.Optional[datetime.date] = None) -> typing.Tuple[
		typing.List[HouseworkType],
		str,
		str
	]:
		if current_date is None:
			current_date = datetime.datetime.now()

		# В случае если это суббота или воскресенье, то домашнее задание будет смотреться с понедельника
		if current_date.weekday() == 5:
			current_date += datetime.timedelta(days=2)
		elif current_date.weekday() == 6:
			current_date += datetime.timedelta(days=1)

		start_of_week, end_of_week = await async_get_week_boundaries(current_date)
		data = await self._request(
			method='get',
			url="https://school.mos.ru/api/family/web/v1/homeworks",
			params={
				'from': start_of_week,
				'to': end_of_week,
				'student_id': self.user.user_id
			},
			headers=self._get_headers())

		shorts = await self._request("https://school.mos.ru/api/family/web/v1/schedule/short", 'get',
			params={
				'student_id': self.user.user_id,
				'dates': make_dates(start_of_week, end_of_week),
			}, headers=self._get_headers())

		return (
			await self.__get_homework(data=data['payload'], shorts=shorts['payload']),
			start_of_week,
			end_of_week
		)

	async def get_by_id(self, homework_id: int) -> InfoHouseworkType:

		result = await self._request(f'https://school.mos.ru/api/family/web/v1/lesson_schedule_items/{homework_id}',
							method='get', params={'student_id': self.user.user_id, 'type': 'OO'},
							headers=self._get_headers())

		return InfoHouseworkType(
			subject_id=result.get('subject_id'),
			schedule_item_id=result.get('id'),
			subject_name=result.get('subject_name'),
			room_number=result.get('room_number'),
			homework=result['lesson_homeworks'][-1]['homework'],
			teacher=Teacher(**result['teacher']),
			date=result.get('date')
		)