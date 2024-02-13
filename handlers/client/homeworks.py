from aiogram import F, types, Router
from school_mos import AUTH

from database.models import Users
from utils.dnevnik import CustomHomework
from keyboards.list_homeworks import list_homeworks_markup
from keyboards.default import back_markup

router = Router()

# TODO: Доделать!!


@router.callback_query(F.data == 'menu:homeworks')
async def get_homeworks_callback(call: types.CallbackQuery, user: Users):
	student = AUTH(token=user.token)
	student.homework = CustomHomework(student)

	homeworks, start_of_week, end_of_week = await student.homework.get_by_week()

	return await call.message.edit_text(f'Домашнее задание на неделю ({start_of_week} - {end_of_week})',
										reply_markup=list_homeworks_markup(homeworks))


@router.callback_query(F.data.startswith('hw:info:'))
async def get_info_homework_callback(call: types.CallbackQuery, user: Users):
	offset, homework_id = call.data.removeprefix('hw:info:').split(':')

	student = AUTH(token=user.token)
	student.homework = CustomHomework(student)

	homework = await student.homework.get_by_id(homework_id=homework_id)

	return await call.message.edit_text(f'🏘 Домашнее задание на <b>{homework.date}</b> по предмету <b>{homework.name}</b>\n\n'
										f'👨‍🏫 Преподаватель: <b>{homework.teacher.last_name} {homework.teacher.first_name} {homework.teacher.middle_name}</b>\n\n'
										f'Задание: 	{homework.homework}',
										reply_markup=back_markup('« Назад', callback_data=f'hw:p:back:{offset}'))


@router.callback_query(F.data.startswith('hw:p:back:'))
@router.callback_query(F.data.startswith('hw:p:next:'))
async def pagination_homeworks_callback(call: types.CallbackQuery, user: Users):
	offset = call.data.removeprefix('hw:p:back:').removeprefix('hw:p:next:')

	student = AUTH(token=user.token)
	student.homework = CustomHomework(student)
	homeworks, start_of_week, end_of_week = await student.homework.get_by_week()

	return await call.message.edit_reply_markup(reply_markup=list_homeworks_markup(
		homeworks, offset=int(offset)
	))
