from aiogram import (
    Router,
    F,
    types
)
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from .game_handler import handle_locations_list, cmd_play_menu, data_print
from ..controller import Controller


router = Router()
controller = Controller()


class Location(StatesGroup):
    locations_list = State()
    location_name = State()


@router.message(Command('goto'))
@router.message(F.text.lower() == 'go to')
async def handle_goto(message: Message, state: FSMContext):
    await handle_locations_list(message, state, Location.location_name, locations_list=controller.get_locations_list())


@router.message(Location.location_name)
async def handle_goto2(message: Message, state: FSMContext):
    locations_list = (await state.get_data())['locations_list']

    if message.text in locations_list:
        location_name = message.text
        location_id = locations_list[location_name]
        await data_print(message, controller.goto(location_id))
        await cmd_play_menu(message, state)
    else:
        await message.answer('There is no such location. Try again or click on the button.')
