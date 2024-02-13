import typing

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.dnevnik.types import SubjectRankType


def rating_markup(subject_ranks: typing.List[SubjectRankType]) -> InlineKeyboardBuilder.as_markup:
	markup = InlineKeyboardBuilder()

	DICT_RANK_STATUS = {
		'down': '⬇',
		'up': '⬆',
		'stable': '⏺'
	}

	for sr in subject_ranks:
		name = f'{DICT_RANK_STATUS[sr.rank.rankStatus]} {sr.rank.averageMarkFive} | {sr.name}'
		markup.button(text=name, callback_data='ignore')
	markup.adjust(1)

	markup.row(types.InlineKeyboardButton(text='« Назад', callback_data='back:start'))
	return markup.as_markup()
