import telebot
from telebot.types import Message
import dotenv
import os
import sqlite3

dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

connection = sqlite3.connect('notes.sqlite', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS notes
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    text TEXT)''')
connection.commit()


def add_note(user_id: int, text: str):
    cursor.execute('''INSERT INTO notes (user_id, text) VALUES (?, ?)''', (user_id, text))
    connection.commit()


@bot.message_handler(commands=['add'])
def add_note_handler(message: Message):
    bot.send_message(message.chat.id, "Введите ваш текст")
    bot.register_next_step_handler(message, add_note_step)


def add_note_step(message: Message):
    add_note(message.from_user.id, message.text)
    bot.send_message(message.chat.id, "Запись добавлена")


def get_notes(user_id: int):
    cursor.execute('''SELECT * FROM notes WHERE user_id = ?''', (user_id,))
    return cursor.fetchall()


@bot.message_handler(commands=['get'])
def get_notes_handler(message: Message):
    notes = get_notes(message.from_user.id)
    if notes:
        notes_text = '\n\n'.join([f'{note[0]}. {note[2]}' for note in notes])
        bot.send_message(message.chat.id, f'Вот твои записи:\n\n{notes_text}')
    else:
        bot.send_message(message.chat.id, 'У тебя пока нет записей.')


bot.infinity_polling()
