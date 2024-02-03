import random

import telebot
from telebot.types import Message
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

bot = telebot.TeleBot(config.get('TOKENS','API_TOKEN'))


words = ['лиса', 'зима', 'лето']
used = set()

word = ''
answer = ''
hp = 0


@bot.message_handler(commands=['start'])
def start(message: Message):
    global word, hp, answer
    word = random.choice(words)
    hp = 5
    answer = "-" * len(word)
    bot.send_message(message.chat.id, "Это виселица! Начинаем!")
    bot.send_message(message.chat.id, answer)


@bot.message_handler(content_types=['text'])
def get_text(message: Message):
    global hp, answer
    data = message.text.lower()
    if len(data) != 1 or not ('а' <= data <= 'я'):
        bot.send_message(message.chat.id, "Введите одну русскую букву")
        return
    if data in used:
        bot.send_message(message.chat.id, "Уже было")
        bot.send_message(message.chat.id, """
 O
/|\\
 |
 /\\
 =======
""")
        return
    if data not in word:
        used.add(data)
        hp -= 1
        if hp == 0:
            bot.send_message(message.chat.id, "Вы проиграли!")
        else:
            bot.send_message(message.chat.id, "Попробуйте еще раз")
            bot.send_message(message.chat.id, "0\n|\n|\\\n=========")
    else:
        used.add(data)
        tmp_answer = ''
        for i, letter in enumerate(word):
            if letter == data:
                tmp_answer += data
            else:
                tmp_answer += answer[i]
        answer = tmp_answer
        bot.send_message(message.chat.id, answer)
        if word == answer:
            bot.send_message(message.chat.id, "Вы победили!")

bot.infinity_polling()