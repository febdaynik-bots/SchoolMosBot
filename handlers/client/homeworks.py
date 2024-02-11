from aiogram import F, types, Router
from school_mos import AUTH

from database.models import Users
from utils.dnevnik import CustomHomework
from keyboards.list_homeworks import list_homeworks_markup

router = Router()

# TODO: Доделать!!


@router.callback_query(F.data == 'menu:homeworks')
async def get_homeworks_callback(call: types.CallbackQuery, user: Users):
	student = AUTH(token=user.token)
	student.homework = CustomHomework(student)

	homeworks, start_of_week, end_of_week = await student.homework.get_by_week()
	print(homeworks)

	return await call.message.edit_text(f'Домашнее задание на неделю ({start_of_week} - {end_of_week})',
										reply_markup=list_homeworks_markup(homeworks))


@router.callback_query(F.data.startswith('hw:p:back:'))
@router.callback_query(F.data.startswith('hw:p:next:'))
async def pagination_homeworks_callback(call: types.CallbackQuery, user: Users):
	offset = call.data.removeprefix('hw:p:back:').removeprefix('hw:p:next:')
	print(offset)

	student = AUTH(token=user.token)
	student.homework = CustomHomework(student)
	homeworks, start_of_week, end_of_week = await student.homework.get_by_week()

	return await call.message.edit_reply_markup(reply_markup=list_homeworks_markup(
		homeworks, offset=int(offset)
	))
