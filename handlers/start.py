from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from keyboards.default import start_markup

router = Router()


@router.message(CommandStart())
async def send_welcome(message: types.Message, state: FSMContext):
    await state.clear()

    return await message.answer('<b>Добро пожаловать в бота для взаимодействия с МЭШ\n(school.mos.ru)</b>',
                                reply_markup=start_markup())

