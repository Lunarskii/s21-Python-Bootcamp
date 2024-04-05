from aiogram import (
    Router,
    F,
    types
)
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from .game_handler import handle_character_list, cmd_play_menu, data_print
from ..controller import Controller


router = Router()
controller = Controller()


class Talk(StatesGroup):
    character_list = State()
    npc_name = State()


@router.message(Command('talk'))
@router.message(F.text.lower() == 'talk')
async def handle_talk(message: Message, state: FSMContext):
    await handle_character_list(message, state, Talk.npc_name, character_list=controller.get_character_list())


@router.message(Talk.npc_name)
async def handle_talk2(message: Message, state: FSMContext):
    character_list = (await state.get_data())['character_list']
    character_name = message.text
    if character_name in character_list:
        character_id = character_list[character_name]
        await data_print(message, controller.talk(character_id))
        await cmd_play_menu(message, state)
    else:
        await message.answer('There is no such NPC. Try again or click on the button.')
