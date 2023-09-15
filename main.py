from telebot import TeleBot, formatting

from values import *
from generate import process_name_step
from markup import Markup
from db import exist_user
from callback import process_callback
from telebot.types import ReplyKeyboardRemove

bot = TeleBot(token, parse_mode='HTML')

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Start",reply_markup=Markup('start', exist_user(message.chat.id, bot)).markup)

@bot.message_handler(regexp='Зареєструватися')
def create_handler(message):
    msg = bot.send_message(message.chat.id, 'Введіть ваш ПІБ', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg,process_name_step, bot) # generate.py

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call): # <- passes a CallbackQuery type object to your function
    process_callback(call,bot) # callback.py
            
            
bot.infinity_polling()