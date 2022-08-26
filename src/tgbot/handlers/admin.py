import sqlite3

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from tgbot.models.role import UserRole
from tgbot.states.add_admin import AddingAdmin


async def admin_start(message: Message):
    await message.reply("Привки-прививки, администраторы")


async def new_admin_id_request(message: Message):
    await message.reply("Хорошо, отправьте мне его айди")
    await AddingAdmin.GET_ID.set()


async def get_admin_id(message: Message, state: FSMContext):
    try:
        admin_id = int(message.text)
    except TypeError:
        await message.reply("Это не похоже на id, попробуйте снова...")
    else:
        conn = sqlite3.connect("database.db")
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO admins_id VALUES(?)", (admin_id,))
        conn.close()
        await state.finish()


async def send_parsable_pages(message: Message):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    all_links = cur.execute("SELECT * FROM parsable_pages").fetchall()
    links_str = '\n'.join([link[0] for link in all_links])
    await message.answer(
        "Все страницы, которые я могу распарсить:\n"+links_str+'\n'+'ДОБАВЬТЕ "/" ПЕРЕД ССЫЛКОЙ, чтобы получить данные за последние 7 дней'
    )


async def send_cnbc(message: Message):
    message.answer_document(open('out/cnbc.csv', 'rb'))


async def send_techstartups(message: Message):
    message.answer_document(open('out/techstartups.csv', 'rb'))
    

async def send_eu_startups(message: Message):
    message.answer_document(open('out/eu_startups.csv', 'rb'))
    

async def send_techstars(message: Message):
    message.answer_document(open('out/techstars.csv', 'rb'))
    

async def send_startupnews(message: Message):
    message.answer_document(open('out/startupnews.csv', 'rb'))
    

async def send_startupdaily(message: Message):
    message.answer_document(open('out/startupdaily.csv', 'rb'))


async def get_all(message: Message):
    message.answer_document(open('out/result.csv'))


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
    dp.register_message_handler(
        send_parsable_pages, state="*", role=UserRole.ADMIN, commands=["get_pages"]
    )

    #hardcoded commands - bad thing
    dp.register_message_handler(
        send_cnbc, role=UserRole.ADMIN, commands=["https://www.cnbc.com/startups/"],
    )

    dp.register_message_handler(
        send_techstartups, role=UserRole.ADMIN, commands=["https://techstartups.com/category/startups/"],
    )

    dp.register_message_handler(
        send_eu_startups, role=UserRole.ADMIN, commands=["https://www.eu-startups.com/"],
    )
    
    dp.register_message_handler(
        send_techstars, role=UserRole.ADMIN, commands=['https://www.techstars.com/newsroom']
    )

    dp.register_message_handler(
        send_techstars, role=UserRole.ADMIN, commands=['https://startupnews.com.au/category/news/']
    )

    dp.register_message_handler(
        send_techstars, role=UserRole.ADMIN, commands=['https://www.startupdaily.net/news/']
    )
