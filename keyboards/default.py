from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_markup() -> InlineKeyboardBuilder.as_markup:
	markup = InlineKeyboardBuilder()
	markup.button(text='📚 Домашнее задание', callback_data='menu:homeworks')
	markup.button(text='5️⃣ Оценки', callback_data='menu:scores')
	markup.button(text='📊 Рейтинг', callback_data='menu:rating')
	markup.adjust(1, 2)
	return markup.as_markup()


def back_markup(btn_name: str = 'Отменить', callback_data: str = 'back:start') -> InlineKeyboardBuilder.as_markup:
	markup = InlineKeyboardBuilder()
	markup.button(text=btn_name, callback_data=callback_data)
	return markup.as_markup()
