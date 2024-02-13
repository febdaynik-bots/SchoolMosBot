from aiogram import F, types, Router
from school_mos import AUTH

from utils.dnevnik import CustomMarks
from keyboards.list_marks import list_marks_markup

router = Router()


@router.callback_query(F.data == 'menu:scores')
async def get_marks_callback(call: types.CallbackQuery, student: AUTH):
	if student is None:
		return await call.answer('Ошибка авторизации. Попробуйте чуть позже')
	student.marks = CustomMarks(student)

	marks = await student.marks.get_by_lesson()

	return await call.message.edit_text('Ваши оценки', reply_markup=list_marks_markup(list(marks)))


@router.callback_query(F.data.startswith('mark:p:back:'))
@router.callback_query(F.data.startswith('mark:p:next:'))
async def pagination_homeworks_callback(call: types.CallbackQuery, student: AUTH):
	offset = call.data.removeprefix('mark:p:back:').removeprefix('mark:p:next:')

	if student is None:
		return await call.answer('Ошибка авторизации. Попробуйте чуть позже')
	student.marks = CustomMarks(student)
	try:
		marks = await student.marks.get_by_lesson()
	except Exception:
		return await call.answer('Возникла ошибка. Попробуйте ещё раз')

	return await call.message.edit_reply_markup(reply_markup=list_marks_markup(
		list(marks), offset=int(offset)
	))

