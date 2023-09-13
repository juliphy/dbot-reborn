from telebot import TeleBot, formatting

from values import *
from generate import process_name_step
from markup import Markup
from db import exist_user, find_user,delete_user, update_user


bot = TeleBot(token, parse_mode='HTML')

print('Бот стартував.')

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Start",reply_markup=Markup('start', exist_user(message.chat.id, bot)).markup)

@bot.message_handler(regexp='Зареєструватися')
def create_handler(message):
    msg = bot.send_message(message.chat.id, 'Введіть ваш ПІБ')
    bot.register_next_step_handler(msg,process_name_step, bot)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call): # <- passes a CallbackQuery type object to your function
    message = call.message.message_id
    id = call.from_user.id

    match (call.data):
        case "settings": 
            bot.edit_message_text('Settings', id, message_id=message)
            bot.edit_message_reply_markup(id, message, reply_markup=Markup('settings').markup)

        case "back_start":
            if exist_user(id,bot):

                bot.edit_message_text('Start',id, message_id=message)
                bot.edit_message_reply_markup(id, message, reply_markup=Markup('start',True).markup)
            
            else:
                bot.edit_message_text('Start',id, message_id=message)
                bot.send_message(id, 'Ви можете зареєструватися знову.', reply_markup=Markup('start', False).markup)
                

        case "info":
            user = find_user(id,bot)
            bot.edit_message_text("Ім'я: " + user["name"] + "\nДата народження: " + user["birthdate"] + "\nID для входу: " + formatting.hcode(user['id']), id,message_id=message)
            bot.edit_message_reply_markup(id, message, reply_markup=Markup('only_back').markup)
        
        case "delete":
            delete_user(id,bot)
            bot.edit_message_text('Профіль видалено. Щоб знову зробити профіль, натисніть кнопку Назад або пропишіть /start.',id, message)
            bot.edit_message_reply_markup(id, message,reply_markup=Markup('only_back', False).markup)

    if call.data.startswith('update'):
            bot.edit_message_text('Якщо ви вже не хочете змінювати, то натисніть кнопку снизу.', id,message)
            bot.edit_message_reply_markup(id, message, reply_markup=Markup('only_back').markup)

            if call.data.endswith('name'):
                msg = bot.send_message(id, 'Відправте бажаний ПІБ')

                bot.register_next_step_handler(msg, update_user, bot, 'name')
            elif call.data.endswith('date'):
                msg = bot.send_message(id, 'Відправте бажану дату народження')

                bot.register_next_step_handler(msg, update_user, bot, 'birthdate')

            elif call.data.endswith('photo'):
                msg = bot.send_message(id, 'Відправте бажене фото. Тільки 3x4 фото підтримуются.')

                bot.register_next_step_handler(msg, update_user, bot, 'photo')
            
            
bot.infinity_polling()