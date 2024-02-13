from aiogram import F, types, Router
from school_mos import AUTH

from utils.dnevnik import Rating
from keyboards.rating import rating_markup

router = Router()


@router.callback_query(F.data == 'menu:rating')
async def get_rating_callback(call: types.CallbackQuery, student: AUTH):
	if student is None:
		return await call.answer('Ошибка авторизации. Попробуйте чуть позже')
	student.rating = Rating(student)

	try:
		rating = await student.rating.get_by_subject()
	except Exception:
		return await call.answer('Возникла ошибка. Попробуйте ещё раз')

	return await call.message.edit_text('Рейтинг по предметам', reply_markup=rating_markup(rating))
