import telebot
import psycopg2
import telebot
from config import database, user, password, host, token



flag_for_add_note = False
bot = telebot.TeleBot(token)


def add_note_to_db(initial_text):
    day = determinate_day(initial_text)
    initial_text = initial_text.split()
    note, time = determinate_note_and_time(initial_text, day)
    print(day)
    print(note)
    print(time)


def determinate_day(text):
    days = ['понедельник', 'вторник', 'четверг', 'пятница', 'суббота', 'воскресенье']
    for day in days:
        if day in text.lower():
            return day


def determinate_note_and_time(initial_list, day):
    note = ''
    temp = []

    for part in initial_list:
        if part.lower() != day:
            note += part + ' '
        else:
            break

    temp.append(note)
    temp.append(initial_list[-1])
    return temp


'''
def connect_to_db():
    try:
        connection = psycopg2.connect(database=database,
                         user=user,
                         password=password,
                         host=host)

        with connection.cursor() as cursor:
            cursor.execute(
                'select * from infopersons;'
            )
            print(cursor.fetchone())

    except Exception as _ex:
        print(f'[INFO] При подключении к базе данных возникла ошибка >> {_ex}')

    finally:
        if connection:
            connection.close()
        print('[INFO] Подключение закрыто ')
'''


def back_to_main_manu(message):
    global flag_for_add_note

    flag_for_add_note = False

    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('Добавить запись')
    bot.send_message(message.chat.id, 'Что дальше?', reply_markup=keyboard)


def add_note(message):
    global flag_for_add_note

    if flag_for_add_note == True:
        add_note_to_db(message.text)
        bot.send_message(message.chat.id, '[DONE] Задача добавлена!')
        back_to_main_manu(message)

    else:
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Вернуться назад')
        bot.send_message(message.chat.id,
                         'Какую задачу хотите добавить?')
        bot.send_message(message.chat.id,
                         'Настоятельно рекомендую записывать в формате\n\n{ЗАДАЧА} {ДЕНЬ НЕДЕЛИ} {ВРЕМЯ}\n\n'
                         'В ином раскладе я вас просто не пойму\n\nПример: Покормить кота Воскресенье 16:34',
                         reply_markup=keyboard)

        flag_for_add_note = True



@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('Добавить запись')
    bot.send_message(message.chat.id, 'Привет-привет! Я To-Do бот.\n\nУмею запоминать предстоящие задачи.'
                                      '\n\nЧто вы хотите сделать?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def intent(message):
    if message.text.lower() == 'вернуться назад':
        back_to_main_manu(message)
    elif flag_for_add_note == True:
        add_note(message)
    elif message.text.lower() == 'добавить запись':
        add_note(message)
    else:
        bot.send_message(message.chat.id, 'Я вас не понимаю. Что вы имели ввиду?')




bot.polling(none_stop=True)


