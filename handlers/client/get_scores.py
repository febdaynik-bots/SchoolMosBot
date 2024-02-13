from aiogram import F, types, Router
from school_mos import AUTH

from database.models import Users
from utils.dnevnik import CustomHomework
from keyboards.list_homeworks import list_homeworks_markup

router = Router()


@router.callback_query(F.data == 'menu:scores')
async def get_marks_callback(call: types.CallbackQuery, user: Users):
	student = AUTH(token=user.token)
	student.marks = CustomHomework(student)

	# await

	# x = student.marks.get_marks(trimester=)
	# print(x)
	return await call.answer()
	# return await call.message.edit_text(f'Оценки за период (',
	# 									reply_markup=list_homeworks_markup(homeworks))

