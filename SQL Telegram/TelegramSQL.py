import telebot
from db import DBService
from db import test_table
# from db import test_table2
import sqlite3
with sqlite3.connect("database.db", check_same_thread=False) as db:
    cursor = db.cursor()

bot = telebot.TeleBot("5998745770:AAH0fylSrW26snjKBsd-ALZDY-0Il3P8H1Q")
types = telebot.types
test_t = test_table
db_service = DBService()


@bot.message_handler(commands=['start'])
def start_message(message):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Записаться", callback_data='writing')
    kb.add(btn1)
    bot.send_message(message.chat.id, 'Привет✌️, сейчас запишемся на тест', reply_markup=kb)


@bot.callback_query_handler(func=lambda callback: callback.data)
def writing(callback):
    if callback.data == "writing":
        bot.send_message(callback.message.chat.id, "Введите вашу фамилию")
        bot.register_next_step_handler(callback.message, get_name)


def get_name(message):
    us_id = message.text
    us_data = ""
    us_name = f'{message.from_user.first_name} {message.from_user.last_name}'
    test_table(user_id=us_id, user_name=us_name, user_data=us_data)
    bot.send_message(message.chat.id, "Введите дату тестирования")
    bot.register_next_step_handler(message, get_data)


def get_data(message):
    us_data = message.text
    cursor.execute(f"UPDATE test SET user_data = {us_data} WHERE ")
    db.commit()
    bot.send_message(message.chat.id, "Запись успешно произведенна😉")


@bot.message_handler(commands=['basa'])
def get_database(message):
    file = open("1.txt", "r")
    text = f'{file.readline()}{file.readline()}'
    text_f = f'Список участников:\n{text}'
    repl = text_f.replace('[', '').replace(']', '').replace("\\n", '').replace("'", '').replace(",", '-')
    bot.send_message(message.chat.id, repl)
    file.close()


bot.polling(none_stop=True)

# @bot.message_handler(commands=['basa'])
# def get_database(message):
# 	user = db_service.get_data()
# 	message_to_send = ""
# 	counter = 1
# 	for element in user:
# 		message_to_send += f'User {counter}: ' + str(element) + '\n'
# 		counter += 1
# 	repl = message_to_send.replace('(', '').replace(')', '').replace("'", '')
# 	bot.send_message(message.chat.id, repl)


# def get_name(message):
# 	with open("1.txt", "a") as file:
# 		file.write(f"{message.text} -")
# 		file.close()
# 		bot.send_message(message.chat.id, "Введите дату тестирования")
# 		bot.register_next_step_handler(message, get_data)
#
# def get_data(message):
# 	with open("1.txt", "a") as file:
# 		file.write(f" {message.text}\n")
# 		file.close()
# 		bot.send_message(message.chat.id, "Запись успешно произведенна😉")
