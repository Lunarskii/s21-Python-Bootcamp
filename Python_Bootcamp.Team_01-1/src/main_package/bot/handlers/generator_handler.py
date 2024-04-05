from aiogram import (
    Router,
    F,
    types
)
from aiogram.filters import Command
from random import choice


from ..keyboards.generator_kb import get_generate_menu_kb, get_characters_menu_kb, get_items_menu_kb
from ..db_dict.ammunition import AMMUNITION, AMMUNITION_TYPES
from ..db_dict.armor import ARMOR, ARMOR_TYPES
from ..db_dict.backpacks import BACKPACKS, BACKPACKS_TYPES
from ..db_dict.food import FOOD, FOOD_TYPES
from ..db_dict.soul_gems import SOUL_GEMS, SOUL_GEMS_TYPES
from ..db_dict.weapons import WEAPONS, WEAPONS_TYPES
from ..db_dict.character_names import NAMES, LAST_NAMES


router = Router()


@router.message(Command('generate'))
@router.message(F.text.lower() == 'generate')
async def cmd_generate(message: types.Message):
    await message.answer(
        text='What do you want to generate?',
        reply_markup=await get_generate_menu_kb()
    )


@router.callback_query(F.data == 'generate_characters')
async def handle_characters(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text='CHARACTERS',
        reply_markup=await get_characters_menu_kb()
    )
    await callback.answer()


@router.callback_query(F.data.in_({'name', 'last_name', 'full_name'}))
async def handle_name(callback: types.CallbackQuery):
    data = callback.data
    if data == 'name':
        await callback.message.answer(choice(NAMES))
    elif data == 'last_name':
        await callback.message.answer(choice(LAST_NAMES))
    elif data == 'full_name':
        await callback.message.answer(f'{choice(NAMES)} {choice(LAST_NAMES)}')
    await callback.answer()


@router.callback_query(F.data == 'generate_items')
async def handle_items(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text='ITEMS',
        reply_markup=(await get_items_menu_kb())
    )
    await callback.answer()


@router.callback_query(F.data.in_({'ammunition', 'armor', 'backpacks', 'food', 'soul_gems', 'weapons'}))
async def handle_name(callback: types.CallbackQuery):
    data = callback.data
    if data == 'ammunition':
        await callback.message.answer(f'{choice(AMMUNITION_TYPES)} {choice(AMMUNITION)}')
    elif data == 'armor':
        await callback.message.answer(f'{choice(ARMOR)} {choice(ARMOR_TYPES)}')
    elif data == 'backpacks':
        await callback.message.answer(f'{choice(BACKPACKS_TYPES)} {choice(BACKPACKS)}')
    elif data == 'food':
        await callback.message.answer(f'{choice(FOOD_TYPES)} {choice(FOOD)}')
    elif data == 'soul_gems':
        await callback.message.answer(f'{choice(SOUL_GEMS_TYPES)} {choice(SOUL_GEMS)}')
    elif data == 'weapons':
        await callback.message.answer(f'{choice(WEAPONS_TYPES)} {choice(WEAPONS)}')
    await callback.answer()


@router.callback_query(F.data == 'back_to_generate_menu')
async def back_to_generate_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    await cmd_generate(callback.message)
    await callback.answer()
