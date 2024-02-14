from aiogram import F, types, Router
from school_mos import AUTH

from keyboards.list_marks import list_marks_markup, info_marks_markup

router = Router()


@router.callback_query(F.data == 'menu:scores')
async def get_marks_callback(call: types.CallbackQuery, student: AUTH):
	if student is None:
		return await call.answer('Ошибка авторизации. Попробуйте чуть позже')

	marks = await student.marks.get_by_lesson()

	return await call.message.edit_text('Ваши оценки', reply_markup=list_marks_markup(list(marks)))


@router.callback_query(F.data.startswith('mark:info:'))
async def get_info_mark_callback(call: types.CallbackQuery, student: AUTH):
	offset, mark_id = call.data.removeprefix('mark:info:').split(':')

	if student is None:
		return await call.answer('Ошибка авторизации. Попробуйте чуть позже')

	try:
		info_mark = await student.marks.get_by_id(int(mark_id))
	except Exception:
		return await call.answer('Возникла ошибка. Попробуйте ещё раз')

	period = len(info_mark.periods)

	return await call.message.edit_text(f'<b>{info_mark.name}</b>\n'
										f'<i>{info_mark.periods[period-1].title}</i>\n\n'
										f'Оценки:',
										reply_markup=info_marks_markup(info_mark.periods[period-1].marks, offset))


@router.callback_query(F.data.startswith('mark:p:back:'))
@router.callback_query(F.data.startswith('mark:p:next:'))
async def pagination_homeworks_callback(call: types.CallbackQuery, student: AUTH):
	offset = call.data.removeprefix('mark:p:back:').removeprefix('mark:p:next:')

	if student is None:
		return await call.answer('Ошибка авторизации. Попробуйте чуть позже')

	try:
		marks = await student.marks.get_by_lesson()
	except Exception:
		return await call.answer('Возникла ошибка. Попробуйте ещё раз')

	return await call.message.edit_reply_markup(reply_markup=list_marks_markup(
		list(marks), offset=int(offset)
	))

