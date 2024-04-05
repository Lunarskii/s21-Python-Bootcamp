from aiogram import (
    Router,
    F,
    types
)
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from .game_handler import handle_character_list, handle_items_list, cmd_play_menu, data_print
from ..controller import Controller


router = Router()
controller = Controller()


class TakeQuest(StatesGroup):
    npc_list = State()
    npc_name = State()


class CompleteQuest(StatesGroup):
    npc_list = State()
    npc_name = State()
    source_items_list = State()
    source_item_name = State()


@router.message(Command('take_quest'))
@router.message(F.text.lower() == 'take quest')
async def handle_take_quest(message: Message, state: FSMContext):
    await handle_character_list(message, state, TakeQuest.npc_name, npc_list=controller.get_npc_list())


@router.message(TakeQuest.npc_name)
async def handle_take_quest2(message: Message, state: FSMContext):
    npc_list = (await state.get_data())['npc_list']

    if message.text in npc_list:
        npc_name = message.text
        npc_id = npc_list[npc_name]
        await data_print(message, controller.take_quest(npc_id))
        await cmd_play_menu(message, state)
    else:
        await message.answer('There is no such NPC. Try again or click on the button.')


@router.message(Command('complete_quest'))
@router.message(F.text.lower() == 'complete quest')
async def handle_complete_quest(message: Message, state: FSMContext):
    await handle_character_list(message, state, CompleteQuest.npc_name, npc_list=controller.get_npc_list())


@router.message(CompleteQuest.npc_name)
async def handle_complete_quest2(message: Message, state: FSMContext):
    npc_list = (await state.get_data())['npc_list']

    if message.text in npc_list:
        npc_name = message.text
        await state.update_data(npc_name=npc_name)
        await handle_items_list(
            message,
            state,
            CompleteQuest.source_item_name,
            source_items_list=controller.get_inventory()
        )
    else:
        await message.answer('There is no such NPC. Try again or click on the button.')


@router.message(CompleteQuest.source_item_name)
async def handle_complete_quest3(message: Message, state: FSMContext):
    quest_data = await state.get_data()
    source_items_list = quest_data['source_items_list']

    if message.text in source_items_list:
        source_item_name = message.text
        npc_list = quest_data['npc_list']
        npc_name = quest_data['npc_name']
        npc_id = npc_list[npc_name]
        await data_print(message, controller.complete_quest(npc_id, source_item_name))
        await cmd_play_menu(message, state)
    else:
        await message.answer('There is no such item. Try again or click on the button.')
