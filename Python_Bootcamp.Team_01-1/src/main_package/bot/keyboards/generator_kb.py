from .kb_builder import get_inline_keyboard_markup


MAIN_MENU_BUTTONS = [
    'Characters',
    'Items'
]
CHARACTERS_MENU_BUTTONS = [
    'Name',
    'Last name',
    'Full name'
]
ITEMS_MENU_BUTTONS = [
    'Ammunition',
    'Armor',
    'Weapons',
    'Backpacks',
    'Food',
    'Soul Gems'
]


async def get_generate_menu_kb():
    return await get_inline_keyboard_markup(
        MAIN_MENU_BUTTONS,
        prefix='generate_',
        adjust=2
    )


async def get_characters_menu_kb():
    return await get_inline_keyboard_markup(
        CHARACTERS_MENU_BUTTONS,
        adjust=2,
        additional_buttons={'Back': 'back_to_generate_menu'}
    )


async def get_items_menu_kb():
    return await get_inline_keyboard_markup(
        ITEMS_MENU_BUTTONS,
        adjust=2,
        additional_buttons={'Back': 'back_to_generate_menu'}
    )
