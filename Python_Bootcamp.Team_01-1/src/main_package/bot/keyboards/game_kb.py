from .kb_builder import get_inline_keyboard_markup, get_keyboard_markup


async def get_main_game_menu_kb():
    return await get_inline_keyboard_markup(
        ['Play'],
        prefix='game_',
        adjust=2
    )


async def get_choosing_an_action_kb():
    return await get_keyboard_markup(
        ['Talk', 'Attack', 'Trade', 'Take quest', 'Complete quest', 'Go to', 'Stop'],
        adjust=3
    )
