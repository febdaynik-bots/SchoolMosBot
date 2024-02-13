import typing

from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.template_pagination import template_pagination_markup_by_list
from utils.dnevnik.types import SubjectMarksType


def list_marks_markup(marks: typing.List[SubjectMarksType], offset: int = 0, limit: int = 10) -> InlineKeyboardBuilder.as_markup:
	markup = InlineKeyboardBuilder()

	DICT_DYNAMIC = {
		'DOWN': '⬇',
		'UP': '⬆',
		'NONE': '⏺',
		'STABLE': '✅'
	}

	for mark in marks[offset:limit+offset]:
		if len(mark.periods) == 1:
			mark.dynamic = 'STABLE'
		name = f'{DICT_DYNAMIC[mark.dynamic]} {mark.average_by_all} | {mark.name}'
		markup.button(text=name, callback_data=f'mark:info:{offset}:{mark.id}')
	markup.adjust(2)

	template_pagination_markup_by_list(
		list_objects=marks,
		callback_data='mark',
		back_callback_data='back:start',
		markup=markup,
		offset=offset,
		limit=limit
	)

	return markup.as_markup()
