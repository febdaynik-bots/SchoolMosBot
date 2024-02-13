from aiogram import types, Router
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from filters.access_user import IsAccessUserFilter
from states import AuthUserState
from database.models import Users
from keyboards.default import back_markup
from utils.dnevnik import async_auth

import traceback

router = Router()
router.message.filter(IsAccessUserFilter(False))


@router.message(CommandStart())
async def auth_user_handler(message: types.Message, state: FSMContext):
	await state.clear()

	msg = await message.answer('Введите свой логин на school.mos.ru\n\n'
							   '<blockquote>Логин может представлять из себя: '
							   'номер телефона/СНИЛС/электронную почту</blockquote>',
							   reply_markup=back_markup('Начать заново', callback_data='back:auth_user'))
	await state.set_state(AuthUserState.login)
	return await state.update_data(msg=msg)


@router.message(AuthUserState.login)
async def AuthUserState_login_state(message: types.Message, state: FSMContext):
	data = await state.get_data()
	await data['msg'].edit_reply_markup()

	login = message.text

	msg = await message.answer(f'Вы ввели логин: {login}\n\n'
							   'Введите пароль от вашего аккаунта', reply_markup=data['msg'].reply_markup)
	await state.update_data(login=login, msg=msg)
	return await state.set_state(AuthUserState.password)


@router.message(AuthUserState.password)
async def AuthUserState_login_state(message: types.Message, state: FSMContext, user: Users):
	data = await state.get_data()
	await data['msg'].edit_reply_markup()

	msg = await message.answer('Ожидайте, идёт проверка данных...')
	try:
		auth_school_api = await async_auth.authStudent(data['login'], message.text)
	except Exception as e:
		traceback.print_exc()
		await msg.edit_text(str(e)+'\n\nПопробуйте ввести другой логин', reply_markup=data['msg'].reply_markup)
		await state.set_state(AuthUserState.login)
		return await state.update_data(msg=msg)

	await msg.edit_text('Аккаунт авторизован\nДанные сохраняются...', reply_markup=data['msg'].reply_markup)
	user.token = auth_school_api.token
	user.save()

	await msg.edit_text('Поздравляю. Вы авторизовались в системе',
						reply_markup=back_markup('В главное меню'))
	return await state.clear()
