import sqlite3

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from tgbot.models.role import UserRole
from tgbot.states.add_admin import AddingAdmin


async def admin_start(message: Message):
    await message.reply("Hello, Admin")


async def new_admin_id_request(message: Message):
    await message.reply("Ok, send me their id")
    await AddingAdmin.GET_ID.set()


async def get_admin_id(message: Message, state: FSMContext):
    try:
        admin_id = int(message.text)
    except TypeError:
        await message.reply("This does not look like an id. Come again...")
    else:
        conn = sqlite3.connect("non_root_admin.db")
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO admins_id VALUES(?)", (admin_id,))
        conn.close()
        await state.finish()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_start,
        commands=["start"],
        state="*",
        role=UserRole.ADMIN,
    )
    dp.register_message_handler(
        new_admin_id_request,
        commands=["add_admin"],
        state="*",
        role=UserRole.ADMIN,
    )

    dp.register_message_handler(
        get_admin_id,
        state=AddingAdmin.GET_ID,
        role=UserRole.ADMIN,
    )
