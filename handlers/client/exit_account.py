import typing

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from keyboards.default import confirm_exit_account_markup, back_markup
from database.models import Users

router = Router()


@router.message(Command(commands='exit'))
@router.callback_query(F.data == 'menu:exit')
async def exit_account_handler(message: typing.Union[types.Message, types.CallbackQuery], state: FSMContext):
	await state.clear()
	if isinstance(message, types.CallbackQuery):
		return await message.message.edit_text(
			'<b>Вы уверены, что хотите выйти из аккаунта <a href="https://school.mos.ru">МЭШ</a></b>',
			disable_web_page_preview=True,
			reply_markup=confirm_exit_account_markup())

	return await message.answer('<b>Вы уверены, что хотите выйти из аккаунта <a href="https://school.mos.ru">МЭШ</a></b>',
								disable_web_page_preview=True,
								reply_markup=confirm_exit_account_markup())


@router.callback_query(F.data == 'confirm_exit:accept')
async def confirm_exit_accept_callback(call: types.CallbackQuery, user: Users):
	user.token = None
	user.save()

	return await call.message.edit_text('Вы вышли из аккаунта',
										reply_markup=back_markup('Войти в аккаунт', 'back:auth_user'))