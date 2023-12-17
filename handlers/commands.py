from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import reply

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer(f'{message.from_user.first_name}, выбери пункт для дальнейших дейтсвий', reply_markup=reply.start)