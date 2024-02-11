from aiogram import types, exceptions, F, Router
from aiogram.fsm.context import FSMContext

from handlers import start, auth_user

router = Router(name='Router callback button')


async def delete_message(call: types.CallbackQuery):
    try:
        await call.message.delete()
    except exceptions.TelegramBadRequest:
        await call.message.edit_text('Сообщение удалено 🗑')


@router.callback_query(F.data.startswith('back:'))
async def back_callback(call: types.CallbackQuery, state: FSMContext):
    page = call.data.removeprefix('back:')
    await state.clear()
    if page == 'auth_user':
        await delete_message(call)
        return await auth_user.auth_user_handler(call.message, state)
    elif page == 'start':
        await delete_message(call)
        return await start.send_welcome(call.message, state)

    await call.answer('Что-то пошло не так')
