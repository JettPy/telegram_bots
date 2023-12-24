import telebot
from telebot.types import Message
import dotenv
import os

dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(content_types=['text'])
def echo(message: Message):
    bot.send_message(message.chat.id, message.text)


bot.infinity_polling()