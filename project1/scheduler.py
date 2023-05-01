import datetime
import pytz
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
import json

bot = Bot(os.environ['TOKEN'])
storage = MemoryStorage()
dp = Dispatcher(bot)

async def birthday():
    now = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    now_date = now.strftime("%d.%m")
    with open("users.json") as file:
        text = json.load(file)
        for txt in text['users']:
            if txt['birthday'] == now_date:
                await bot.send_message(-1001670394888, f"С Днем Рождения 🎂\n{txt['firstName']} {txt['secondName']}!")


async def scan():
  now = datetime.datetime.now()
  photo = open('Scan/Сканирование.jpg', 'rb')
  if now.strftime("%w") == "2":
    await bot.send_message(-1001670394888, "Не забываем про сканирование!(всех категорий)")
  if now.strftime("%w") == "4":
    await bot.send_message(-1001670394888, "Не забываем про сканирование!(категорий из списка)")
    await bot.send_photo(-1001670394888, photo)
  print(now.strftime("%w"))


async def scheduler():
    while True:
        now = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
        if now.hour == 10 and now.minute == 0 and now.second == 0:
            asyncio.create_task(birthday())
        await asyncio.sleep(1)

async def scheduler2():
    while True:
        now = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
        if now.hour == 9 and now.minute == 30 and now.second == 0:
            asyncio.create_task(scan())
        await asyncio.sleep(1)