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


class Trade(StatesGroup):
    npc_list = State()
    npc_name = State()
    source_items_list = State()
    source_item_name = State()
    source_item_quantity = State()
    destination_items_list = State()
    destination_item_name = State()
    destination_item_quantity = State()


@router.message(Command('trade'))
@router.message(F.text.lower() == 'trade')
async def handle_trade(message: Message, state: FSMContext):
    await handle_character_list(message, state, Trade.npc_name, npc_list=controller.get_npc_list())


@router.message(Trade.npc_name)
async def handle_trade2(message: Message, state: FSMContext):
    npc_list = (await state.get_data())['npc_list']

    if message.text in npc_list:
        npc_name = message.text
        await state.update_data(npc_name=npc_name)
        await handle_items_list(
            message,
            state,
            Trade.source_item_name,
            source_items_list=controller.get_inventory()
        )
    else:
        await message.answer('There is no such NPC. Try again or click on the button.')


@router.message(Trade.source_item_name)
async def handle_trade3(message: Message, state: FSMContext):
    source_items_list = (await state.get_data())['source_items_list']

    if message.text in source_items_list:
        source_item_name = message.text
        await state.update_data(source_item_name=source_item_name)
        await state.set_state(Trade.source_item_quantity)
        max_quantity = len(source_items_list[source_item_name])
        range_quantity = f'[1-{max_quantity}]' if max_quantity != 1 else f'[{max_quantity}]'
        await message.answer(text=f'Enter the number of items. {range_quantity}', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('There is no such item. Try again or click on the button.')


@router.message(Trade.source_item_quantity)
async def handle_trade4(message: Message, state: FSMContext):
    if message.text.isdigit():
        source_item_quantity = int(message.text)
        trade_data = await state.get_data()
        source_items_list = trade_data['source_items_list']
        source_item_name = trade_data['source_item_name']
        if source_item_quantity <= len(source_items_list[source_item_name]):
            npc_list = trade_data['npc_list']
            npc_name = trade_data['npc_name']
            npc_id = npc_list[npc_name]
            await state.update_data(source_item_quantity=source_item_quantity)
            await handle_items_list(
                message,
                state,
                Trade.destination_item_name,
                destination_items_list=controller.get_inventory(npc_id)
            )
        else:
            await message.answer(f'There are not enough \'{source_item_name}\' in the character inventory.')
    else:
        await message.answer('It\'s not a number. Try again.')


@router.message(Trade.destination_item_name)
async def handle_trade5(message: Message, state: FSMContext):
    destination_items_list = (await state.get_data())['destination_items_list']

    if message.text in destination_items_list:
        destination_item_name = message.text
        await state.update_data(destination_item_name=destination_item_name)
        await state.set_state(Trade.destination_item_quantity)
        max_quantity = len(destination_items_list[destination_item_name])
        range_quantity = f'[1-{max_quantity}]' if max_quantity != 1 else f'[{max_quantity}]'
        await message.answer(text=f'Enter the number of items. {range_quantity}', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('There is no such item. Try again or click on the button.')


@router.message(Trade.destination_item_quantity)
async def handle_trade6(message: Message, state: FSMContext):
    if message.text.isdigit():
        destination_item_quantity = int(message.text)
        trade_data = await state.get_data()
        destination_items_list = trade_data['destination_items_list']
        destination_item_name = trade_data['destination_item_name']
        if destination_item_quantity <= len(destination_items_list[destination_item_name]):
            source_item_name = trade_data['source_item_name']
            source_item_quantity = trade_data['source_item_quantity']
            npc_list = trade_data['npc_list']
            npc_name = trade_data['npc_name']
            npc_id = npc_list[npc_name]
            await data_print(
                message,
                controller.trade(
                    npc_id,
                    source_item_name,
                    source_item_quantity,
                    destination_item_name,
                    destination_item_quantity
                )
            )
            await cmd_play_menu(message, state)
        else:
            await message.answer(f'There are not enough \'{destination_item_name}\' in the character inventory.')
    else:
        await message.answer('It\'s not a number. Try again.')
