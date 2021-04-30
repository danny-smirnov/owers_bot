import telebot
from telebot import types
import database_queries as dq
import STATES as st

token = '1795920252:AAFtZkAe89kYjz9KbYCRX4RPqX5950LEpRA'

bot = telebot.TeleBot(token)



def menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    keyboard_buttons = []
    keyboard_buttons.append(types.KeyboardButton(text='Добавить долг'))
    keyboard_buttons.append(types.KeyboardButton(text='История долгов'))
    keyboard.add(*keyboard_buttons)
    return keyboard

@bot.message_handler(commands = ['start'])
def welcome(message):
    try:
        bot.send_message(message.chat.id, 'Ну привет, должники. Давайте считать, кто сколько кому торчит\n', reply_markup = menu_keyboard())
        if dq.check_user_in_db(message.chat.id) == False:
            dq.add_client(message.chat.id)
            dq.set_state(message.chat.id, st.MAIN)
        else:
            dq.set_state(message.chat.id, st.MAIN)
    except Exception as error:
        bot.send_message(message.chat.id, 'Произошла ошибка. Отправьте команду /start чтобы продолжить работу с ботом')



@bot.message_handler(func = lambda message: message.text == 'Добавить долг' and dq.get_state(message.chat.id) == st.MAIN)
def add_debt(message):
    try:
        bot.send_message(message.chat.id, 'Опишите долг в следующем формате:\n'
                                        '[Имя Должника] [Имя Платившего] [Сумма] [Комментарий]', reply_markup=telebot.types.ReplyKeyboardRemove())
        dq.set_state(message.chat.id, st.ADD_DEBT)
    except:
        bot.send_message(message.chat.id, 'Произошла ошибка. Отправьте команду /start чтобы продолжить работу с ботом')

def check_isdigit(message):
    if type(message) == str:
        if str.isdigit(message) == True:
            return True
    return False

@bot.message_handler(func = lambda message: dq.get_state(message.chat.id) == st.ADD_DEBT)
def insert_debt_in_db(message):
    try:
        if len(message.text.split()) != 4 or check_isdigit(message.text.split()[2]) == False:
            bot.send_message(message.chat.id, 'Неверно заполненная форма')
        else:
            ower = message.text.split()[0]
            owe_to = message.text.split()[1]
            amount = message.text.split()[2]
            comment = message.text.replace('{} {} {}'.format(ower, owe_to, amount), '')
            dq.add_debt(ower, owe_to, amount, comment)
            bot.send_message(message.chat.id, 'Долг успешно добавлен', reply_markup = menu_keyboard())
            dq.set_state(message.chat.id, st.MAIN)
    except Exception as error:
        bot.send_message(message.chat.id, 'Произошла ошибка. Отправьте команду /start чтобы продолжить работу с ботом')


@bot.message_handler(func = lambda message: dq.get_state(message.chat.id) == st.MAIN and message.text == 'История долгов')
def show_all_history(message):
    try:
        all = dq.show_all_debts()
        text = ''
        for i in all:
            text += 'Должник: {}\nПлативший: {}\nСумма: {}\nКомментарий: {}'.format(*i)+'\n\n'
        bot.send_message(message.chat.id, 'История долгов:\n\n'+text, reply_markup = menu_keyboard())
    except:
        bot.send_message(message.chat.id, 'Произошла ошибка. Отправьте команду /start чтобы продолжить работу с ботом')


bot.infinity_polling()


