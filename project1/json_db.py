import asyncio
import os
import json
from aiogram.types import Message
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(os.environ['TOKEN'])
dp = Dispatcher(bot, storage=MemoryStorage())


def is_duplicate(userData, data):
    for user in data["users"]:
        if user["firstName"] == userData["firstName"] and user["secondName"] == userData["secondName"]:
            return True
    return False


class AddUserStates(StatesGroup):
    waiting_for_first_name = State()
    waiting_for_second_name = State()
    waiting_for_birthday = State()


class DeleteUserStates(StatesGroup):
    waiting_for_second_name = State()


class AddUser:
    @dp.message_handler(commands=["add_user"])
    async def add_user_start(self, msg: types.Message):
        await msg.answer('Введите имя нового сотрудника:')
        await AddUserStates.waiting_for_first_name.set()

    @dp.message_handler(state=AddUserStates.waiting_for_first_name)
    async def add_user_first_name(self, msg: types.Message, state: FSMContext):
        if msg.text.lower() == 'отмена':
            await state.finish()
            await msg.answer('Добавление нового сотрудника отменено.')
        else:
            async with state.proxy() as data:
                data['firstName'] = msg.text
            await msg.answer('Введите фамилию сотрудника:')
            await AddUserStates.waiting_for_second_name.set()
            await asyncio.sleep(5)

    @dp.message_handler(state=AddUserStates.waiting_for_second_name)
    async def add_user_second_name(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['secondName'] = msg.text
        await msg.answer('Введите дату рождения сотрудника в формате ДД.ММ:')
        await AddUserStates.waiting_for_birthday.set()

    @dp.message_handler(state=AddUserStates.waiting_for_birthday)
    async def add_user_birthday(self, msg: types.Message, state: FSMContext):
        try:
            birthday = datetime.strptime(msg.text, '%d.%m').date()
        except ValueError:
            await msg.answer('Неверный формат даты, попробуйте ещё раз:')
            return
        async with state.proxy() as data:
            data['birthday'] = birthday.strftime('%d.%m')
        user_data = {
            'userID': "000",
            'firstName': data['firstName'],
            'secondName': data['secondName'],
            'birthday': data['birthday']
        }
        with open("users.json", 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        if is_duplicate(user_data, existing_data):
            await msg.answer('Информация о пользователе уже существует!')
            return
        existing_data['users'].append(user_data)
        with open("users.json", 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        await msg.answer('Информация успешно добавлена!')
        await state.finish()


class DeleteUser:
    async def delete_user(self, msg: Message):
        await msg.answer('Введите фамилию пользователя, которого нужно удалить:')
        await DeleteUserStates.waiting_for_second_name.set()

    @dp.message_handler(state=DeleteUserStates.waiting_for_second_name)
    async def delete_users(self, msg: Message, state: FSMContext):
        if msg.text.lower() == 'отмена':
            await state.finish()
            await msg.answer('Удаление сотрудника отменено.')
        else:
            text = msg.text
            data = {}
            with open("users.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            list1 = data.get("users", [])
            for i, user in enumerate(list1):
                if user.get('secondName') == text:
                    del list1[i]
                    data['users'] = list1
                    with open("users.json", 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                    await msg.answer('Информация о пользователе удалена!')
                    await state.finish()
                    return
            await msg.answer('Пользователь с указанной фамилией не найден!')
            await state.finish()


async def show_data_json(msg: Message, user_id: str = None):
    data = {}
    with open("users.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    list1 = data.get("users", [])
    list1.sort(key=lambda x: x.get('secondName', ''))
    if user_id:
        for user in list1:
            if user.get('userID') == user_id:
                firstName = user.get('firstName')
                secondName = user.get('secondName')
                birthday = user.get('birthday')
                response = f"Имя: {firstName}\nФамилия: {secondName}\nДень рождения: {birthday}"
                await msg.answer(response)
                return
        await msg.answer('Пользователь с указанным ID не найден!')
    else:
        if list1:
            response = "Список пользователей:\n"
            for user in list1:
                firstName = user.get('firstName')
                secondName = user.get('secondName')
                birthday = user.get('birthday')
                response += f"- {secondName} {firstName} {birthday}\n"
            await msg.answer(response)
        else:
            await msg.answer('Пока нет зарегистрированных пользователей.')