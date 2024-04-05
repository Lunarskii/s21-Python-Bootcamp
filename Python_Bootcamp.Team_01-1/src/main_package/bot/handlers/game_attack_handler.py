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


class Attack(StatesGroup):
    enemy_list = State()
    enemy_name = State()


@router.message(Command('attack'))
@router.message(F.text.lower() == 'attack')
async def handle_attack(message: Message, state: FSMContext):
    await handle_character_list(message, state, Attack.enemy_name, enemy_list=controller.get_enemy_list())


@router.message(Attack.enemy_name)
async def handle_attack2(message: Message, state: FSMContext):
    enemy_list = (await state.get_data())['enemy_list']
    enemy_name = message.text
    if enemy_name in enemy_list:
        enemy_id = enemy_list[enemy_name]
        await data_print(message, controller.attack(enemy_id))
        await cmd_play_menu(message, state)
    else:
        await message.answer('There is no such enemy. Try again or click on the button.')
