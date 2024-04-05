from aiogram import (
    Router,
    F,
    types
)
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from ..keyboards.kb_builder import get_keyboard_markup

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text='Че хотим?', reply_markup=await get_keyboard_markup(['Generate', 'Play']))
    await cmd_help(message)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('/play - Start the game.\n'
                         '/stop - Stop the game.\n'
                         '/play_menu - Open the game menu separately from the in-game story.\n'
                         '/talk - Open the NPC communication menu.\n'
                         '/attack - Open the attack menu on opponents.\n'
                         '/trade - Open the trade menu with the NPC.\n'
                         '/goto - Open the location navigation menu.\n'
                         '\n'
                         '/generate - Open the generation menu.\n')
