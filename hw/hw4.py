

# Подключаем необходимые библиотеки
import telebot
import os
import dotenv
from telebot.types import Message
import re

# Загружаем токен из переменных окружения и создаем бота
dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

global n1
global n2
@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(message.chat.id, "Отправьте сообщение.")


@bot.message_handler(content_types=['text'])
def math_search(message: Message):
    text = message.text
    pattern = r'(\d+)\s*([-+*/])\s*([\d+])'
    match = re.match(pattern, text)

    if match:
        n1 = int(match.group(1))
        operator = match.group(2)
        n2 = int(match.group(3))

        if operator == '+':
            res = n1 + n2
        elif operator == "-":
            res = n1 - n2
        elif operator == "*":
            res = n1 * n2
        elif operator == "/":
            res = n1 / n2

        bot.send_message(message.chat.id, f"{res}")
    else:
        bot.send_message(message.chat.id, "Неверный формат, попробуйте еще раз")

bot.infinity_polling()