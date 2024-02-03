# В этом уроке мы познакомимся с кнопками inline меню и markup меню

# Подключаем необходимые библиотеки
import telebot
import os
import dotenv
from telebot.types import Message

# Загружаем токен из переменных окружения и создаем бота
dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

cities = [
    'Москва', 'Питер', 'Краснодар', 'Димитровград', 'Архангельск',
    'Курск', 'Волгоград', 'Реутов', 'Одинцово', 'Омск',
    'Новосибирск', 'Киров', 'Владимир', 'Тула', 'Калининград',
    'Ёшкар-ола', 'Казань', 'Новгород', 'Можайск', 'Химки',
    'Домодедово', 'Тверь', 'Подольск', 'Лобня', 'Дубна'
]

# Добавляем счетчик очков
score = 0

cities_used = set()

#  1. Inline меню

# Inline меню - это меню из кнопок, которые появляются под сообщениями отправляемые ботом.
# Создадим переменные которые создадут для нас меню:
# Первым делом создадим каркас для меню с помощью класса InlineKeyboardMarkup.
# Этот класс находится в telebot, модуле types.
# В конструктор передадим параметр row_width - он отвечает за количество кнопок в одной линии
inline_menu = telebot.types.InlineKeyboardMarkup(row_width=1)
# Далее создадим четыре кнопки. Для этого воспользуемся классом InlineKeyboardButton.
# Конструктор класса принимает текст, который будет отображаться на кнопке,
# а также передадим значение в callback_data, оно пригодиться нам далее:
lose_button = telebot.types.InlineKeyboardButton("Сдаться", callback_data='lose_button')
score_button = telebot.types.InlineKeyboardButton("Очки", callback_data='score_button')
restart_button = telebot.types.InlineKeyboardButton("Перезапустить", callback_data='restart_button')
help_button = telebot.types.InlineKeyboardButton("Подсказка", callback_data='help_button')
# После создания кнопок, их надо связать с нашим меню.
# Для этого используется метод add, в который через запятую передаем кнопки.
inline_menu.add(lose_button, score_button, restart_button, help_button)

# 2. Reply меню

# Reply меню - это меню из кнопок, которые появляются вместо клавиатуры.
# Создадим переменные которые создадут для нас меню:
# Первым делом создадим каркас для меню с помощью класса ReplyKeyboardMarkup.
# Этот класс находится в telebot, модуле types.
# В конструктор передадим параметр row_width - он отвечает за количество кнопок в одной линии
reply_menu = telebot.types.ReplyKeyboardMarkup(row_width=3)
# Далее создадим три кнопки. Для этого воспользуемся классом KeyboardButton.
# Конструктор класса принимает текст, который будет отображаться на кнопке:
clue1_button = telebot.types.KeyboardButton("Москва")
clue2_button = telebot.types.KeyboardButton("Одинцово")
clue3_button = telebot.types.KeyboardButton("Звенигород")
# После создания кнопок, их надо связать с нашим меню.
# Для этого используется метод add, в который через запятую передаем кнопки.
reply_menu.add(clue1_button, clue2_button, clue3_button)

# Отличие Reply меню от Inline меню помимо способа отображения кнопок в том, что Reply меню по нажатию на кнопку
# отправляет текст кнопки в чат.


def find_city(city: str):
    last_ch = city.lower()[-1]
    if last_ch == 'ь':
        last_ch = city.lower()[-2]
    for city_in_list in cities:
        if city_in_list.lower()[0] == last_ch and city_in_list not in cities_used:
            cities_used.add(city_in_list)
            return city_in_list
    return None


@bot.message_handler(commands=['start'])
def start(message):
    # Теперь к каждому нашему сообщению прикрепим меню.
    # Для этого используется параметр reply_markup. Он может принимать либо inline меню, либо reply меню.
    # Два меню сразу вывести нельзя.
    bot.send_message(message.chat.id, "Начинаем игру. Напишите город", reply_markup=inline_menu)


# Добавим команду для обнуления очков и перезапуска игры по команде /restart
@bot.message_handler(commands=['restart'])
def restart(message):
    global score
    cities_used.clear()
    score = 0
    bot.send_message(message.chat.id, 'Игра перезапущена, начинайте', reply_markup=inline_menu)


@bot.message_handler(content_types=['text'])
def text(message):
    word = message.text
    if word in cities_used:
        bot.send_message(message.chat.id, "Так не честно! Город уже был. Напиши другой", reply_markup=inline_menu)
    else:
        # Берем переменную из глобальной области видимости и увеличиваем ее
        global score
        score += 1
        cities_used.add(word)
        next_city = find_city(word)
        if next_city is None:
            bot.send_message(message.from_user.id, "Я не знаю. Вы побели")
        else:
            bot.send_message(message.from_user.id, next_city, reply_markup=inline_menu)


# Также теперь необходимо добавить функцию с декоратором callback_query_handler для inline меню.
# Это декоратор принимает в себя данные из нажатых кнопок в inline меню и помещает их в переменную call:
@bot.callback_query_handler(func=lambda call: call.data)
def button_handlers(call):
    global score
    # Ранее мы определили аргументы callback_data для кнопок inline меню, они нам сейчас пригодятся.
    # callback_data содержится в поле data объекта call.
    # Нам необходимо определить поведение для каждой кнопки. Для этого воспользуемся if - elif:
    if call.data == 'lose_button':
        # Если нажата кнопка "Сдаться". То выводим набранные очки и обнуляем счет
        # TODO
        pass
    elif call.data == 'score_button':
        # Если нажата кнопка "Сдаться". То выводим набранные очки и обнуляем счет
        # TODO
        pass
    elif call.data == 'restart_button':
        # Если нажата кнопка "Перезапустить". То перезапускаем игру
        # TODO
        pass
    elif call.data == 'help_button':
        # Если нажата кнопка "Подсказка". То выводим reply меню с подсказками
        # TODO
        pass


@bot.callback_query_handler(func=lambda call: call.data)
def button_handlers(call):
    global score
    # Ранее мы определили аргументы callback_data для кнопок inline меню, они нам сейчас пригодятся.
    # callback_data содержится в поле data объекта call.
    # Нам необходимо определить поведение для каждой кнопки. Для этого воспользуемся if - elif:
    if call.data == 'lose_button':
        # Если нажата кнопка "Сдаться". То выводим набранные очки и обнуляем счет
        bot.send_message(call.message.chat.id, f'Вы сдались. {score}', reply_markup=inline_menu)
        cities_used.clear()
        score = 0
    elif call.data == 'score_button':
        # Если нажата кнопка "Очки". То выводим набранные очки и обнуляем счет
        bot.send_message(call.message.chat.id, str(score))
    elif call.data == 'restart_button':
        # Если нажата кнопка "Перезапустить". То перезапускаем игру
        bot.send_message(call.message.chat.id, f'restart, score={score}')
        cities_used.clear()
        score = 0
    elif call.data == 'help_button':
        # Если нажата кнопка "Подсказка". То выводим reply меню с подсказками
        reply_menu = telebot.types.ReplyKeyboardMarkup(row_width=3)
        clue1_button = telebot.types.KeyboardButton("Москва")
        clue2_button = telebot.types.KeyboardButton("Одинцово")
        clue3_button = telebot.types.KeyboardButton("Звенигород")




# Удаление клавиатуры с кнопками
@bot.message_handler(commands=['/clear'])
def echo(message: Message):
    bot.reply_to(message, message.text, reply_markup=telebot.types.ReplyKeyboardRemove())


# Пример обработчиков разбитых на каждую кнопку по отдельности
@bot.callback_query_handler(func=lambda call: call.data == "lose_button")
def lose_button(call):
    bot.send_message(call.message.from_user.id, "lose_button")


@bot.callback_query_handler(func=lambda call: call.data == "score_button")
def score_button(call):
    bot.send_message(call.message.from_user.id, "score_button")


@bot.callback_query_handler(func=lambda call: call.data == "help_button")
def help_button(call):
    bot.send_message(call.message.from_user.id, "help_button")


@bot.callback_query_handler(func=lambda call: call.data == "restart_button")
def restart_button(call):
    bot.send_message(call.message.chat.id, "restart_button")


bot.infinity_polling()
