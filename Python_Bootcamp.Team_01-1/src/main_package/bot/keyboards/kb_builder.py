from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    ReplyKeyboardBuilder,
    KeyboardButton
)


async def get_inline_keyboard_markup(buttons: list[str] | dict[str, str],
                                     prefix: str | None = None,
                                     adjust: int | None = None,
                                     lower_case: bool = True,
                                     additional_buttons: dict[str, str] | None = None):
    builder = InlineKeyboardBuilder()

    if isinstance(buttons, dict):
        for btn_name, callback_data in buttons:
            builder.add(InlineKeyboardButton(
                text=btn_name,
                callback_data=callback_data.lower() if lower_case else callback_data
            ))
    elif isinstance(buttons, list):
        for btn_name in buttons:
            callback_data = btn_name.replace(' ', '_')
            if lower_case:
                callback_data = callback_data.lower()
            if prefix:
                callback_data = prefix + callback_data
            builder.add(InlineKeyboardButton(
                text=btn_name,
                callback_data=callback_data
            ))

    if adjust:
        builder.adjust(adjust)
    if additional_buttons:
        for text, callback_data in additional_buttons.items():
            builder.row(InlineKeyboardButton(text=text, callback_data=callback_data.lower().replace(' ', '_')))
    return builder.as_markup()


async def get_keyboard_markup(buttons: list[str],
                              adjust: int | None = None):
    builder = ReplyKeyboardBuilder()
    for btn_name in buttons:
        builder.add(KeyboardButton(text=btn_name))
    if adjust:
        builder.adjust(adjust)
    return builder.as_markup(resize_keyboard=True)
