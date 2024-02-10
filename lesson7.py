# 1) скобки [] обозначают набор символов:
# 1.1) [abcdef12345] - прямое перечисление всех символов
# 1.2) [a-f1-5] - перечисление интервалов символов
# 1.3) [^a-f1-5] и [^abcdef12345] - перечисление интервалов исключенных символов, т.е. все кроме них (инверсия)

# 2) Символы \w и \W - первый означает буквенный, цифровой символ или знак подчёркивания,
# второй НЕ буквенный, цифровой символ или знак
# \w аналогичен записи - [^a-zA-Z0-9-]

# 3) Символы \d и \D - цифровой символ и любой не цифровой аналогично

# 4) Символы \s и \S - пробельный (пробел, табуляция, перенос строки и т.д.) и не пробельный символ

# 5) Символ \ и т.п. записывается как \\ (перед ними ставится дополнительный обратный слэш), для экранирования

# 6) Символ ^ в начале и $ в конце означают начало и конец строки соответственно.

# 7) . (точка) - один любой символ

# Квантификация (количество повторений)

# 8) * - нуль или любое количество повторений

# 9) + - одно или любое количество повторений

# 10) ? - нуль или один символ (символ либо есть, либо его нет)

# 11.1) {n} - символ повторяется n раз
# 11.2) {m,n} - символ повторяется от m до n раз
# 11.3) {,n} - символ повторяется до n раз
# 11.4) {m,} - символ повторяется от m раз


# str1 = "Hello 123456\\, world12345!"
# match = re.search(r'\\', str1)
# print(match.span(), match.string, match.group(), sep='\n')
# # match = re.search(r'\W', str1)
# # # print(match)
#
# str2 = "Hello 123456, world12345!"
# match = re.findall(r"\d+", str2)
# print(match)  # Вывод: ['123456', '12345']
#
# str3 = "Hello 123456, world12345!"
# match = re.split(r"\d+", str3)
# print(match)  # Вывод: ['Hello ', ', world', '!']
#
# str4 = "Hello 123456, world12345!"
# match = re.sub(r"\d+", "00", str4)
# print(match)  # В
# ывод: Hello 00, world00!


import telebot
from telebot.types import Message
import dotenv
import os
import re
import urllib
import requests as req
# pip install requests


dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

url = 'https://www.youtube.com/results?'

regexp = '(?<=watch\?v=)[\w-]{11}'

pattern = re.compile(regexp)


@bot.message_handler(content_types=['text'])
def get_text_message(message: Message):
    query_string = urllib.parse.urlencode({"search_query": message.text})
    print(query_string)
    res = req.get(url + query_string)
    # bot.send_message(message.chat.id, query_string)
    print(res)
    if res.ok:
        video_ids = pattern.findall(res.text)
        print(video_ids)
        unic_ids = set()
        for video_id in video_ids:
            if len(unic_ids) == 10:
                break
            elif video_id not in unic_ids:
                unic_ids.add(video_id)
                answer = 'http://www.youtube.com/watch?v=' + video_id
                bot.send_message(message.chat.id, answer)


bot.infinity_polling()
