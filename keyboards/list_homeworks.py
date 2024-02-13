from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.template_pagination import template_pagination_markup_by_list


def list_homeworks_markup(homeworks: list, offset: int = 0, limit: int = 10) -> InlineKeyboardBuilder.as_markup:
	markup = InlineKeyboardBuilder()

	for homework in homeworks[offset:limit+offset]:
		markup.button(text=f'{homework.name}', callback_data=f'hw:info:{offset}:{homework.schedule_item_id}')
	markup.adjust(2)

	template_pagination_markup_by_list(
		list_objects=homeworks,
		callback_data='hw',
		back_callback_data='back:start',
		markup=markup,
		offset=offset,
		limit=limit
	)

	return markup.as_markup()
