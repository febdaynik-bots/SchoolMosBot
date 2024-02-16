import datetime
import typing

from config import bot
from database.models import Users, Notify
from .dnevnik.notify.notifications import Notifications, Marks, HouseworkTypeByNotify


def getNoun(number, one, two, five):
	n = abs(number)
	n %= 100
	if (n >= 5) and (n <= 20):
		return '{} {}'.format(number, five)
	n %= 10
	if n == 1:
		return '{} {}'.format(number, one)
	elif (n >= 2) and (n <= 4):
		return '{} {}'.format(number, two)
	return '{} {}'.format(number, five)


async def make_text_homework_from_list(homeworks: typing.List[HouseworkTypeByNotify]) -> str:
	list_text_homeworks = list()

	for homework in homeworks:
		list_text_homeworks.append(f'<blockquote><b>{homework.name}</b>\n{homework.description}</blockquote>')

	return '\n'.join(list_text_homeworks)


async def make_text_marks_from_list(marks: typing.List[Marks]) -> str:
	list_text_marks = list()

	for mark in marks:
		mark_value = mark.value
		if not mark.is_point and mark.weight == 2:
			mark_value = f'{mark_value}/{mark.weight}'

		list_text_marks.append(f'<blockquote><b>{mark.name}</b>\n{mark.control_form_name}. '
							   f'Получена новая оценка — {mark_value}</blockquote>')

	return '\n'.join(list_text_marks)


async def student_notify():
	users = Users.select().where(Users.token.is_null(is_null=False))

	for user in users:
		student = Notifications(
			token=user.token,
			user_id=user.student_id
		)

		string_date = datetime.datetime.now().strftime('%Y-%m-%d')

		homeworks = await student.get_homework(string_date)
		marks = await student.get_marks(string_date)

		notify_db = Notify.get_or_none(user_id=user.user_id)
		if notify_db is None:
			notify_db = Notify.create(user=user)

		if homeworks:
			json_homeworks = student.to_json(homeworks)

			if notify_db.homeworks != json_homeworks:
				notify_db.homeworks = json_homeworks
			else:
				homeworks = list()

		if marks:
			json_marks = student.to_json(marks)

			if notify_db.marks != json_marks:
				notify_db.marks = json_marks
			else:
				marks = list()

		notify_db.save()

		text_homeworks = await make_text_homework_from_list(homeworks)
		text_marks = await make_text_marks_from_list(marks)

		count_notification = len(marks)+len(homeworks)
		if count_notification > 0:
			text = '<b>У вас {text_count_notifications}\n\n{texts}</b>'.format(
				text_count_notifications=getNoun(count_notification, 'новое уведомление', 'новых уведомления',
												 'новых уведомлений'),
				texts=f'{text_homeworks}\n\n{text_marks}'
			)

			await bot.send_message(chat_id=user.user_id, text=text)
