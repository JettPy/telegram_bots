# 12 - выполняем проект
# 13 - выполняем проект
# 14 - начинаем делать презентацию, готов проект
# 15 - готова презентация, на уроке репетировать
# 16 - защита
import glob

import telebot
# from PIL.ImageFont import ImageFont
from telebot.types import Message
import dotenv
import os
from PIL import Image, ImageDraw, ImageFont
import io

dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(content_types=['photo'])
def get_photo(message: Message):
    photo_id = message.photo[-1].file_id
    photo_file = bot.get_file(photo_id)
    photo_path = photo_file.file_path
    downloaded_photo = bot.download_file(photo_path)
    photo = Image.open(io.BytesIO(downloaded_photo))
    bot.send_message(message.chat.id, "Введите текст")
    bot.register_next_step_handler(message, get_text, photo)


def get_text(message: Message, image: Image):
    text = message.text
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", size=44, encoding="utf-8")
    draw.text((100, 100), text, font=font)
    output = io.BytesIO()
    image.save(output, format="PNG")
    bot.send_photo(message.from_user.id, output.getvalue())


bot.infinity_polling()

