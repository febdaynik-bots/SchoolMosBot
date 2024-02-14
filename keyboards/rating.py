import typing

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.dnevnik.types import SubjectRankType
from utils.make_rank_place_emoji import make_rank_place_emoji


def rating_markup(subject_ranks: typing.List[SubjectRankType]) -> InlineKeyboardBuilder.as_markup:
	markup = InlineKeyboardBuilder()

	DICT_RANK_STATUS = {
		'down': '⬇',
		'up': '⬆',
		'stable': '⏺'
	}

	DICT_RANK_PLACE = {
		1: '🥇',
		2: '🥈',
		3: '🥉',
	}

	for sr in subject_ranks:

		if sr.rank.rankPlace > 3:
			rank_place = make_rank_place_emoji(sr.rank.rankPlace)
		else:
			rank_place = DICT_RANK_PLACE[sr.rank.rankPlace]
		name = f'{rank_place} {sr.rank.averageMarkFive} | {sr.name}'

		markup.button(text=name, callback_data='ignore')
	markup.adjust(1)

	markup.row(types.InlineKeyboardButton(text='« Назад', callback_data='back:start'))
	return markup.as_markup()
