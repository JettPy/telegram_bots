from PIL import Image, ImageFilter

panda = Image.open('panda.jpg')
# print(panda)
#
# print(panda.size)
# print(panda.filename)
# print(panda.format)
# print(panda.format_description)

# panda.show()

# cropped_panda = panda.crop((200, 100, 800, 600))
# cropped_panda.save('cropped_panda.jpg')
# cropped_panda.show()


# panda2 = panda.transpose(Image.TRANSPOSE)
# panda2.show()
#
# panda3 = panda.transpose(Image.TRANSVERSE)
# panda3.show()

# panda4 = panda.rotate(45)
# panda4.show()
#

from PIL import ImageDraw

# img_blank = Image.new('RGBA', (1200, 1200), color=(255, 255, 255))
#
# draw = ImageDraw.Draw(panda)
#
# draw.rectangle((200, 400, 700, 500), fill=(255, 0, 0), outline='yellow', width=5)
# draw.ellipse((200, 400, 700, 500), fill=(255, 0, 255), outline='purple', width=5)
# draw.polygon(((0, 0), (100, 0), (100, 100), (50, 200)), fill='blue', outline='pink')
# draw.line(((50, 700), (800, 600), (700, 500), (1000, 400)), fill='black', width=10, joint='curve')
#
# draw.arc((300, 100, 500, 300), start=10, end=270, width=10, fill='red')
# draw.chord((1000, 300, 1100, 500), start=10, end=180, width=10, fill='green')
# draw.pieslice(((800, 100), (1000, 300)), start=10, end=90, width=10, fill='blue')
# panda.show()

# image = panda.filter(ImageFilter.SMOOTH_MORE)
# image = image.filter(ImageFilter.EMBOSS)
# image.show()

import telebot
from telebot.types import Message
import dotenv
import os

dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(content_types=['photo'])
def handle_photo(message: Message):
    photo_id = message.photo[-1].file_id
    photo_file = bot.get_file(photo_id)
    photo_path = photo_file.file_path
    downloaded_photo = bot.download_file(photo_path)
    print(photo_id)
    print(photo_file)
    print(photo_path)
    print(downloaded_photo)
    bot.send_photo(message.from_user.id, downloaded_photo)


bot.infinity_polling()
