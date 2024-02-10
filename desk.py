import telebot
from telebot.types import Message
import dotenv
import os
import sqlite3

dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

connection = sqlite3.connect('notes.txt', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS notes
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT)''')
connection.commit()


@bot.message_handler(commands=['add'])
def add_note_handler(message: Message):
    bot.send_message(message.chat.id, "Введи текст")
    bot.register_next_step_handler(message, add_note_step)


def add_note_step(message: Message):
    u_id = message.from_user.id
    u_text = message.text
    cursor.execute('''INSERT INTO notes (user_id, text) VALUES (?, ?)''', (u_id, u_text))
    connection.commit()
    bot.send_message(message.chat.id, "Готово")


@bot.message_handler(commands=['get'])
def add_note_handler(message: Message):
    cursor.execute('''SELECT * FROM notes WHERE user_id = ?''', (message.from_user.id,))
    data = cursor.fetchall()
    if data:
        notes_text = '\n\n'.join([f'{note[0]}. {note[2]}' for note in data])
        bot.send_message(message.chat.id, f'Вот твои записи:\n\n{notes_text}')
    else:
        bot.send_message(message.chat.id, 'У тебя пока нет записей.')


bot.infinity_polling()
