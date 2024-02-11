from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def template_pagination_markup(
        list_objects,
        callback_data: str,
        back_callback_data: str,
        markup: InlineKeyboardBuilder,
        offset: int = 0,
        limit: int = 24
) -> InlineKeyboardBuilder:

    total_page = (list_objects.count() + limit - 1) // limit
    page = int(offset / limit) + 1

    if total_page > 1:
        if page > 1:
            back_accounts_button = types.InlineKeyboardButton(text='« Назад',
                                                  callback_data=f'{callback_data}:p:back:{offset - limit}')
        else:
            back_accounts_button = types.InlineKeyboardButton(text=' ', callback_data='ignore')

        if page < total_page:
            next_accounts_button = types.InlineKeyboardButton(text='Далее »',
                                                  callback_data=f'{callback_data}:p:next:{offset + limit}')
        else:
            next_accounts_button = types.InlineKeyboardButton(text=' ', callback_data='ignore')

        markup.row(
            back_accounts_button,
            types.InlineKeyboardButton(text=f'{page}/{total_page}', callback_data=' '),
            next_accounts_button
        )
    markup.row(types.InlineKeyboardButton(text='« Назад', callback_data=back_callback_data))

    return markup


def template_pagination_markup_by_list(
        list_objects,
        callback_data: str,
        back_callback_data: str,
        markup: InlineKeyboardBuilder,
        offset: int = 0,
        limit: int = 24
) -> InlineKeyboardBuilder:

    total_page = (len(list_objects) + limit - 1) // limit
    page = int(offset / limit) + 1

    if total_page > 1:
        if page > 1:
            back_accounts_button = types.InlineKeyboardButton(text='« Назад',
                                                  callback_data=f'{callback_data}:p:back:{offset - limit}')
        else:
            back_accounts_button = types.InlineKeyboardButton(text=' ', callback_data='ignore')

        if page < total_page:
            next_accounts_button = types.InlineKeyboardButton(text='Далее »',
                                                  callback_data=f'{callback_data}:p:next:{offset + limit}')
        else:
            next_accounts_button = types.InlineKeyboardButton(text=' ', callback_data='ignore')

        markup.row(
            back_accounts_button,
            types.InlineKeyboardButton(text=f'{page}/{total_page}', callback_data=' '),
            next_accounts_button
        )
    markup.row(types.InlineKeyboardButton(text='« Назад', callback_data=back_callback_data))

    return markup
