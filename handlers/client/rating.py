from aiogram import F, types, Router
from school_mos import AUTH

from utils.dnevnik import Rating
from utils.make_rank_place_emoji import make_rank_place_emoji
from keyboards.rating import rating_markup

router = Router()


@router.callback_query(F.data == 'menu:rating')
async def get_rating_callback(call: types.CallbackQuery, student: AUTH):
	if student is None:
		return await call.answer('Ошибка авторизации. Попробуйте чуть позже')
	student.rating = Rating(student)

	try:
		rating = await student.rating.get()
		subject_rating = await student.rating.get_by_subject()
	except Exception:
		return await call.answer('Возникла ошибка. Попробуйте ещё раз')

	return await call.message.edit_text(f'{make_rank_place_emoji(rating[0].rankPlace)} — <b>Ваше место в рейтинге\n\n'
										'Рейтинг по предметам:</b>', reply_markup=rating_markup(subject_rating))
