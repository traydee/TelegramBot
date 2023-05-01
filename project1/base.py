import os
import asyncio
import openai
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from background import keep_alive
from commands import Hellp_Com, Grafik, Grafik_promo, Inventa
from json_db import AddUser, AddUserStates, DeleteUserStates, DeleteUser, show_data_json
from sql_db import show_data, UserState, StartState
from keybords import builder, process_callback_button1, admin_k, process_callback
from scheduler import scheduler, scheduler2

openai.api_key = os.environ['gpt']
bot = Bot(os.environ['TOKEN'])
dp = Dispatcher(bot, storage=MemoryStorage())

add_user = AddUser()
delete_user = DeleteUser()
chat_id = StartState()

dp.register_message_handler(add_user.add_user_start, Command('add_user'))
dp.register_message_handler(add_user.add_user_first_name, state=AddUserStates.waiting_for_first_name)
dp.register_message_handler(add_user.add_user_second_name, state=AddUserStates.waiting_for_second_name)
dp.register_message_handler(add_user.add_user_birthday, state=AddUserStates.waiting_for_birthday)

dp.register_message_handler(delete_user.delete_user, Command('delete_user'))
dp.register_message_handler(delete_user.delete_users, state=DeleteUserStates.waiting_for_second_name)

dp.register_message_handler(chat_id.chat_id, Command('start'))
dp.register_message_handler(chat_id.on_phone_number, state=UserState.phone_number)

dp.register_message_handler(show_data_json, Command('show_data_json'))

dp.register_message_handler(show_data, Command('show_data'))


@dp.message_handler(content_types=["new_chat_members"])
async def new_member(message: types.Message):
    name = message.new_chat_members[0].first_name
    await bot.send_message(message.chat.id, f"Добро пожаловать, {name}!\nВот что я умею:{Hellp_Com}", parse_mode="HTML")


@dp.message_handler(commands=["grafic"])
async def send_graf(message: types.Message):
    graf = Grafik
    open_doc = open(f"{graf}", "rb")
    await bot.send_document(message.from_user.id, open_doc)
    await message.delete()


@dp.message_handler(commands=["grafic_promo"])
async def send_graf_promo(message: types.Message):
    graf = Grafik_promo
    open_doc = open(f"{graf}", "rb")
    await bot.send_document(message.from_user.id, open_doc)
    await message.delete()


@dp.message_handler(commands=["inventa"])
async def inventa(message: types.Message):
    await bot.send_message(message.from_user.id, f'<a href="{Inventa}">График инвентаризации</a>', parse_mode="HTML", disable_web_page_preview=True)
    await message.delete()


@dp.message_handler(commands=['contacts'])
async def process_command_1(message: types.Message):
    await bot.send_message(message.from_user.id, "Выбери группу контакта:", reply_markup=builder)
    await message.delete()


@dp.callback_query_handler(process_callback_button1, lambda c: c.data == 'button1' or 'button2' or 'button3' or 'button4')


@dp.message_handler(commands=['admin_p'])
async def process(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите функцию:", reply_markup=admin_k)
    await message.delete()


@dp.callback_query_handler(process_callback, lambda c: c.data in ['show_data', 'add_user', 'delete_user', 'show_data_json'])

@dp.message_handler(commands=['gpt'])
async def handle_message(message):
    sent_message = await bot.send_message(message.from_user.id, "Загружаем ответ⏳")
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=message.text,
      temperature=0.9,
      max_tokens=1000,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.6,
    )
    await bot.send_message(message.from_user.id, text=response['choices'][0]['text'])
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)

async def on_startup(dp):
    asyncio.create_task(scheduler())
    asyncio.create_task(scheduler2())


if __name__ == "__main__":
    keep_alive()
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
