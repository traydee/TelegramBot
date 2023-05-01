import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram import Bot, Dispatcher
from commands import Contact
from json_db import AddUser, AddUserStates, DeleteUserStates, DeleteUser, show_data_json
from sql_db import show_data

bot = Bot(os.environ['TOKEN'])
dp = Dispatcher(bot)

add_user = AddUser()
delete_user = DeleteUser()

dp.register_message_handler(add_user.add_user_start)
dp.register_message_handler(add_user.add_user_first_name, state=AddUserStates.waiting_for_first_name)
dp.register_message_handler(add_user.add_user_second_name, state=AddUserStates.waiting_for_second_name)
dp.register_message_handler(add_user.add_user_birthday, state=AddUserStates.waiting_for_birthday)

dp.register_message_handler(delete_user.delete_user)
dp.register_message_handler(delete_user.delete_users, state=DeleteUserStates.waiting_for_second_name)

builder = InlineKeyboardMarkup(row_width=2).add(
InlineKeyboardButton(text="Администрация", callback_data="button1"),
InlineKeyboardButton(text="Прикассовая зона", callback_data="button2"),
InlineKeyboardButton(text="КБТ", callback_data="button3"),
InlineKeyboardButton(text="МБТ", callback_data="button4"),
InlineKeyboardButton(text="ТВ", callback_data="button5"),
InlineKeyboardButton(text="ИТ/Моб.Мир", callback_data="button6"))

admin_k = InlineKeyboardMarkup(row_width=2).add(
InlineKeyboardButton('Данные DB', callback_data='show_data'),
InlineKeyboardButton('Данные Json', callback_data='show_data_json'),
InlineKeyboardButton('Добавить пользователя', callback_data='add_user'),
InlineKeyboardButton('Удалить пользователя', callback_data='delete_user'))


builder2 = InlineKeyboardMarkup(row_width=2).add(
InlineKeyboardButton(text="Назад", callback_data="back"))


async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.data == 'button1':
        await bot.send_message(callback_query.from_user.id, text=f'Администрация:{Contact.admin}', parse_mode="HTML", reply_markup=builder2)
        await callback_query.message.delete()
    if callback_query.data == 'button2':
        await bot.send_message(callback_query.from_user.id, f'Прикассовая зона:{Contact.kassa}', parse_mode="HTML", reply_markup=builder2)
        await callback_query.message.delete()
    if callback_query.data == 'button3':
        await bot.send_message(callback_query.from_user.id, f'КБТ:{Contact.kbt}', parse_mode="HTML", reply_markup=builder2)
        await callback_query.message.delete()
    if callback_query.data == 'button4':
        await bot.send_message(callback_query.from_user.id, f'МБТ:{Contact.mbt}', parse_mode="HTML", reply_markup=builder2)
        await callback_query.message.delete()
    if callback_query.data == 'button5':
        await bot.send_message(callback_query.from_user.id, f'ТВ:{Contact.tv}', parse_mode="HTML", reply_markup=builder2)
        await callback_query.message.delete()
    if callback_query.data == 'button6':
        await bot.send_message(callback_query.from_user.id, f'ИТ/Моб.Мир:{Contact.it}', parse_mode="HTML", reply_markup=builder2)
        await callback_query.message.delete()
    if callback_query.data == 'back':
        await bot.send_message(callback_query.from_user.id, "Выбери группу контакта:", reply_markup=builder)
        await callback_query.message.delete()


async def process_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.data == 'show_data':
        await show_data(callback_query.message)
    if callback_query.data == 'add_user':
        await add_user.add_user_start(callback_query.message)
    if callback_query.data == 'delete_user':
        await delete_user.delete_user(callback_query.message)
    if callback_query.data == 'show_data_json':
        await show_data_json(callback_query.message)