from aiogram import (
    Router,
    F,
    types
)
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from .main_handler import cmd_start
from ..keyboards.game_kb import (
    get_main_game_menu_kb,
    get_choosing_an_action_kb,
    get_inline_keyboard_markup,
    get_keyboard_markup
)
from ..controller import Controller


router = Router()
controller = Controller()


@router.message(Command('play'))
@router.message(F.text.lower() == 'play')
async def cmd_play(message: Message, state: FSMContext):
    await message.answer(f'<b>The history of the world</b>\n\n {controller.get_history()}')
    await cmd_play_menu(message, state)


@router.message(Command('stop'))
@router.message(F.text.lower() == 'stop')
async def cmd_stop(message: Message):
    await message.answer(
        text='Game stopped.',
        reply_markup=ReplyKeyboardRemove()
    )
    await cmd_start(message)


@router.message(Command('play_menu'))
@router.message(F.text.lower() == 'play_menu')
async def cmd_play_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Choose an action.',
        reply_markup=await get_choosing_an_action_kb()
    )


async def handle_character_list(message: Message, state: FSMContext, next_state: State, **kwargs):
    character_list: dict | int = kwargs.get('character_list', 0)
    npc_list: dict | int = kwargs.get('npc_list', 0)
    enemy_list: dict | int = kwargs.get('enemy_list', 0)

    if character_list or npc_list or enemy_list:
        await state.update_data(**kwargs)
        await state.set_state(next_state)
        if character_list:
            text = 'Choose a Character.'
            iterable_list = character_list
        elif npc_list:
            text = 'Choose a NPC.'
            iterable_list = npc_list
        else:
            text = 'Choose an Enemy.'
            iterable_list = enemy_list
        await message.answer(
            text=text,
            reply_markup=await get_keyboard_markup([key for key in iterable_list], 4)
        )
    else:
        await message.answer('There are no characters available.')


async def handle_items_list(message: Message, state: FSMContext, next_state: State, **kwargs):
    source_items_list: dict | int = kwargs.get('source_items_list', 0)
    destination_items_list: dict | int = kwargs.get('destination_items_list', 0)

    if (source_items_list and len(source_items_list)) or (destination_items_list and len(destination_items_list)):
        await state.update_data(**kwargs)
        await state.set_state(next_state)
        if source_items_list:
            iterable_list = source_items_list
        else:
            iterable_list = destination_items_list
        await message.answer(
            text='Select the item.',
            reply_markup=await get_keyboard_markup([item.name for item in iterable_list], 4)
        )
    else:
        await message.answer('The character\'s inventory is empty.')


async def handle_locations_list(message: Message, state: FSMContext, next_state: State, **kwargs):
    locations_list: dict | int = kwargs.get('locations_list', 0)

    if locations_list and len(locations_list):
        await state.update_data(**kwargs)
        await state.set_state(next_state)
        await message.answer(
            text='Select a location to move to.',
            reply_markup=await get_keyboard_markup([key for key in locations_list], 4)
        )
    else:
        await message.answer('There are no available locations to move to.')


async def data_print(message: Message, data):
    if isinstance(data, list):
        for msg in data:
            await message.answer(msg)
    elif isinstance(data, str):
        await message.answer(data)
