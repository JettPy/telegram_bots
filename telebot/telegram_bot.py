import telebot
from telebot.types import Message
import dotenv
import os
import time

dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['count'])
def count(message: Message):
    bot.send_message(message.chat.id, '1')
    time.sleep(5)

    bot.send_message(message.chat.id, '2')
    time.sleep(5)

    bot.send_message(message.chat.id, '3')
    time.sleep(5)

    bot.send_message(message.chat.id, '4')
    time.sleep(5)

    bot.send_message(message.chat.id, '5')
    time.sleep(5)


@bot.message_handler(content_types=['text'])
def greetings(message):
    if message.text == 'привет' or message.text == 'Привет':
        bot.send_message(message.chat.id, f"Привет,  {str(message.from_user.username)}!")


bot.infinity_polling()