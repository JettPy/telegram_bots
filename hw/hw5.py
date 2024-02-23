import telebot
from PIL import Image, ImageDraw
import io
import os
import dotenv

dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(content_types=['photo'])
def handle_image(message):
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    image_bytes = bot.download_file(file_info.file_path)
    image = Image.open(io.BytesIO(image_bytes))

    draw = ImageDraw.Draw(image)
    draw.ellipse((50, 50, 150, 150), outline="red", width=5)

    output_image = io.BytesIO()
    image.save(output_image, format="PNG")

    bot.send_photo(message.chat.id, output_image.getvalue())


bot.infinity_polling()