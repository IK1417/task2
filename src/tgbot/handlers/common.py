from aiogram import Dispatcher
from aiogram.types import Message


async def get_id(message: Message):
    await message.answer(message.from_user.id)


def register_common(dp: Dispatcher):
    dp.register_message_handler(
        get_id,
        commands=["get_my_id"],
        state="*",
    )
