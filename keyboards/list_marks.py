import typing

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.template_pagination import template_pagination_markup_by_list
from utils.dnevnik.types import SubjectMarksType, Marks
from utils.make_rank_place_emoji import make_rank_place_emoji


def list_marks_markup(subject_marks: typing.List[SubjectMarksType], offset: int = 0,
					  limit: int = 10) -> InlineKeyboardBuilder.as_markup:
	markup = InlineKeyboardBuilder()

	DICT_DYNAMIC = {
		'DOWN': '⬇',
		'UP': '⬆',
		'NONE': '⏺',
		'STABLE': '✅'
	}
	period = 0

	# Вычисление периода (не идеальное решение)
	for mark in subject_marks[offset:limit + offset]:
		if len(mark.periods) > period:
			period = len(mark.periods)

	for mark in subject_marks[offset:limit+offset]:
		if len(mark.periods) == 1 and period == 2:
			mark.dynamic = 'STABLE'
		name = f'{DICT_DYNAMIC[mark.dynamic]} {mark.average_by_all} | {mark.name}'
		markup.button(text=name, callback_data=f'mark:info:{offset}:{mark.id}')
	markup.adjust(2)

	template_pagination_markup_by_list(
		list_objects=subject_marks,
		callback_data='mark',
		back_callback_data='back:start',
		markup=markup,
		offset=offset,
		limit=limit
	)

	return markup.as_markup()


def info_marks_markup(marks: typing.List[Marks], offset: int) -> InlineKeyboardBuilder.as_markup:
	markup = InlineKeyboardBuilder()

	for mark in marks:
		markup.button(text=make_rank_place_emoji(mark.value), callback_data=f'ignore')
	markup.adjust(2)

	markup.row(types.InlineKeyboardButton(text='« Назад', callback_data=f'mark:p:back:{offset}'))

	return markup.as_markup()
