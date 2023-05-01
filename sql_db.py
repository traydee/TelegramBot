import os
import sqlite3
from aiogram import Bot, types, Dispatcher
from commands import Hellp_Com
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(os.environ['TOKEN'])
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    phone_number = State()

class StartState:
  async def chat_id(self, message: types.Message):
    connect = sqlite3.connect("users.db", check_same_thread=True)
    cursor = connect.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_id
        (id INTEGER, user_name VARCHAR, user_fname VARCHAR, user_lname VARCHAR, phone_number VARCHAR)
   """)
    connect.commit()
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        await bot.send_message(message.chat.id, "Пожалуйста, введите свой мобильный номер в формате 375ХХХХХХХХХ:")
        await UserState.phone_number.set()
        await message.delete()
    else:
        await bot.send_message(message.chat.id, f"Вот что я умею:{Hellp_Com}", parse_mode="HTML")
        await message.delete()
    cursor.close()
    connect.close()
  @dp.message_handler(state=UserState.phone_number)
  async def on_phone_number(self, message: types.Message, state: FSMContext):
    phone_number = message.text
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number
    if len(phone_number) < 12:
        await bot.send_message(message.chat.id, "Пожалуйста, введите корректный номер телефона.")
        return
    await state.update_data(phone_number=phone_number)
    user_name = message.from_user.username
    user_fname = message.from_user.first_name
    user_lname = message.from_user.last_name
    user_id = message.chat.id
    connect = sqlite3.connect("users.db", check_same_thread=True)
    cursor = connect.cursor()
    cursor.execute("INSERT INTO login_id (id, user_name, user_fname, user_lname, phone_number) VALUES (?, ?, ?, ?, ?)",
                 (user_id, user_name, user_fname, user_lname, phone_number))
    connect.commit()
    cursor.close()
    connect.close()
    await bot.send_message(message.chat.id, f"Вот что я умею:{Hellp_Com}", parse_mode="HTML")
    await state.finish()

async def show_data(message: types.Message):
    connect = sqlite3.connect("users.db", check_same_thread=True)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM login_id")
    data = cursor.fetchall()
    if data:
        response = "Список зарегистрированных пользователей:\n"
        for row in data:
            user_id = row[0]
            user_name = row[1]
            user_fname = row[2]
            user_lname = row[3]
            phone_number = row[4]
            response += f"- <b>{user_id}</b>: @{user_name} ({user_fname} {user_lname})\n{phone_number}\n"
        await bot.send_message(message.chat.id, response, parse_mode="HTML")
    else:
        await bot.send_message(message.chat.id, "Пока нет зарегистрированных пользователей.")
    cursor.close()
    connect.close()