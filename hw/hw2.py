# В этом уроке создадим игру в города

# Подключаем необходимые библиотеки
import telebot
import os
import dotenv

# Загружаем токен из переменных окружения и создаем бота
dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# Cоздаём список с именами городов
cities = [
    'Москва', 'Питер', 'Краснодар', 'Димитровград', 'Архангельск',
    'Курск', 'Волгоград', 'Реутов', 'Одинцово', 'Омск',
    'Новосибирск', 'Киров', 'Владимир', 'Тула', 'Калининград',
    'Йошкар-Ола', 'Казань', 'Новгород', 'Можайск', 'Химки',
    'Домодедово', 'Тверь', 'Подольск', 'Лобня', 'Дубна'
]

# Также пригодится запоминать названия городов, которые уже были что бы они не повторялись.
# Для этого идеально подойдет множество
cities_used = set()

score = 0
current_city = None


# Создадим функцию для определения следующего города
def find_city(city: str):
    # Приводим название к нижнему регистру и берем последний символ
    last_ch = city.lower()[-1]
    # Если город заканчивается на "ь", то берем предпоследний символ
    if last_ch == 'ь':
        last_ch = city.lower()[-2]
    # Далее перебираем все названия городов из списка
    for city_in_list in cities:
        # Если город из списка начинается на ту же букву, что мы определили раньше и он еще не использовался,
        # то помечаем город как использованный и возвращаем его
        if city_in_list.lower()[0] == last_ch and city_in_list not in cities_used:
            cities_used.add(city_in_list)
            return city_in_list
    # Если подходящего города не нашлось, то возвращаем None
    return None


# Выведем подсказку для пользователя по команде /start, что он начинает игру
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Начинаем игру. Напишите город")


# Далее будем обрабатывать каждое сообщение, считая что пользователь всегда будет вводить только названия городов
@bot.message_handler(content_types=['text'])
def text(message):
    # Получаем текс из сообщения
    word = message.text
    # Проверяем введенный пользователем город

    if word not in cities:
        bot.send_message(message.from_user.id, "По-моему, ты перепутал. Напиши ГОРОД.")
        return

    global current_city

    if word in cities_used:
        # Если такой город уже был, просим пользователя повторить попытку
        bot.send_message(message.from_user.id, "Так не честно! Город уже был. Напиши другой")
        # Выходит из функции
        return

    if current_city is not None and word.lower()[0] != current_city[-1]:
        bot.send_message(message.from_user.id, "Ты перепутал, твоя буква '{}'".format(current_city[-1]))
        return

    # Если такого города не было, сохраняем его
    cities_used.add(word)
    # Получаем следующий город из списка
    next_city = find_city(word)
    current_city = next_city
    global score
    score += 1
    # Если подходящего города нет, то пользователь побеждает
    if next_city is None:
        bot.send_message(message.from_user.id, f"У меня нет идей... Вы победили! Очки: {score}")
        cities_used.clear()
        score = 0
        current_city = None
        bot.send_message(message.from_user.id, "Чтобы снова начать игру, впишите город.")
    # Иначе выводим следующее название города
    else:
        bot.send_message(message.from_user.id, next_city)


# Постоянно слушаем сообщения от пользователя
bot.infinity_polling()